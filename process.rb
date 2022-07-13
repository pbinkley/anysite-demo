#!/usr/bin/env ruby

require 'anystyle'
require 'fileutils'
require 'json'
require 'byebug'

filename = ARGV.first # e.g. source/test-full.txt
citations = []

fileext = File.extname(filename) # .txt
filebase = File.basename(filename, fileext) # test-full
FileUtils.mkdir_p('output')
outputfile = "output/#{filebase}.json"

headings = [] # will have two elements: main section and (optionally) subsection

File.readlines(filename).each_with_index do |line, index|
  puts "**** Line #{index + 1}"
  line.strip!
  next if line == ''

  # this picks up Markdown-style headers, which will be converted to 
  # collections in Zotero
  if line.start_with?('#') # this is a section heading
    cleanline = line.sub(/^\#*/, '').strip
    if line.start_with?('##') # subsection
      headings[1] = cleanline
    else # main section
      headings = [cleanline, '']
    end
    puts "Headings: #{headings}"
    next
  end

  original = line.dup # save the original so we can add it to the record

  # here is where you can add code to modify the input citation

  # e.g.: if the citations are numbered, you can discard the numbers:
  #   line = line.gsub(/^\d+\.?\)?/, '').strip

  # e.g. if bibliographic abbreviations like "vol." are in a language AnyStyle doesn't
  # understand you can change them to English to improve citation parsing
  #   line.gsub!(/ Вып\./, ' vol.')

  # e.g. other idiosyncrasies can be fixed, e.g. abbreviated placenames
  #   line.gsub!(' М.:', ' Москва:')

  # parse the citation
  parsedline = AnyStyle.parse(line) # default format: CSL
  citation = parsedline.first

  # now you can fix specific fields in the output record:
  # I found these to be necessary to produce valid records for Zotero import

  # type field is required
  citation[:type] = 'book' if citation[:type].nil?

  # rename pages field
  if citation[:pages]
    citation[:page] = citation[:pages]
    citation.delete(:pages)
  end

  # format the date
  if citation[:date]
    citation[:issued] = { :"date-parts" => [citation[:date]] } 
    citation.delete(:date)
  end

  # save source line as note - this ends up in the Extra field in the 
  # Zotero record, and is convenient for correcting the record in Zotero
  citation[:note] = original

  # if you want to convert headings into collections, this is necessary to save
  # the headings into the Extra field
  if headings.count > 0
    path = "#{headings[0]}"
    path += "|#{headings[1]}" if headings[1] != ''
    citation[:subject] = [path]
    citation[:note] += " | ZoteroFolder: #{path}"
  end

  citations << citation
end

# save the citations in a file suitable for Zotero import
File.write(outputfile, JSON.pretty_generate(citations))

puts 'done'