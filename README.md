# anystyle-demo
Demo scripts for importing unformatted citations into Zotero using AnySite and PyZotero

These two scripts can be used:

1. to transform a human-readable list of bibliographic
  citations into json, which can be imported into [Zotero](https://zotero.org)
2. optionally, to organize the imported items into folders or make 
  other automated changes to the imported items in Zotero

The first is a Ruby script ```process.rb```, which uses the gem
```[anystyle]``` (as used by the site [AnyStyle.io](https://anystyle.io)). The second 
(which is optional) is a Python script which uses the library [```pyzotero```](https://github.com/urschrei/pyzotero) 
to alter the imported items using the [Zotero Web API](https://www.zotero.org/support/dev/web_api/v3/start). The case that
prompted this project was the need to import a few hundred unformatted
citations, typed in a Word document, into Zotero. 

## Sample import

A sample import of twelve records organized under headers can be seen in
the [anystyle-demo library](https://www.zotero.org/groups/4734751/anystyle-demo/library). The source file is included in [```sample/sample.txt```](https://raw.githubusercontent.com/pbinkley/anystyle-demo/main/sample/sample.txt),
and the JSON output file is in [```output/sample.json```](https://raw.githubusercontent.com/pbinkley/anystyle-demo/main/output/sample.json).

Within a [sample record](https://www.zotero.org/groups/4734751/anystyle-demo/collections/GAC5PBHA/items/PTGEXRXF/collection), the 
```Extra``` field (scroll to the bottom of the Zotero record) contains the source
citation, for consultation during correction. The field also contains
the heading(s) under which the item will be moved.

## Set Up

- run ```bundle install``` to install the Ruby dependencies (i.e. 
  the ```anystyle``` gem)
- run ```pip install -m requirements.txt``` to install the Python dependencies 
  (i.e the ```pyzotero``` library)
- put your citations in a plain text file. Every line will be treated as a citation,
  so don't break citations over multiple lines. Empty lines will be ignored.
- Markdown-style headings may be added to group items into collections (see below)
- ```pyzotero``` requires a [Zotero API key](https://www.zotero.org/settings/keys/new) with appropriate permissions: 
  ```Library access``` and ```Write access``` to your personal library or to a 
  group library if you are using one. See the [pyzotero docs](https://github.com/urschrei/pyzotero#quickstart) for details of the 
  necessary fields. The credentials should be put in a file
  named ```config.ini``` in the same directory as the scripts, in this format:

```
[Zotero]
library_id = [id]
library_type = [type]
api_key = [key]
```

- ```[id]```: an integer
- ```[type]```: either ```personal``` or ```group```
- ```[key]```: 24-character alphanumeric key

## Running process.rb

This script reads the source citation file and outputs a CSL JSON file. It can be
adapted to do other pre- and post-conversion changes to the items (see the comments 
in the script for examples).

- run ```./process.rb <path to citation file>.txt```. A directory named ```output``` 
  will be created, and a file ```<citation file name>.json``` will be written in it.
  The format is [CSL JSON](https://citeproc-js.readthedocs.io/en/latest/csl-json/markup.html).
- import the JSON file into Zotero using the desktop client: ```File | Import...```. 
  (For this project we used an empty new private [group library](https://www.zotero.org/support/groups), and I would be 
  cautious about importing directly into a large existing library, since cleaning up 
  a mistaken import without disturbing the previous items might take a lot of work.)
- if you will be using the Python script to organize the items into collections, you
  should first add all the items to a collection called "uncorrected"
- note that the original citation is stored in the ```Extra``` field in the Zotero 
  item, where it can be consulted during the correction process.
- if the source file contains [Markdown-style headings](https://www.markdownguide.org/basic-syntax/#headings) (level 1 or 2), these will 
  be converted into folder paths and added to the ```Extra``` field. The included 
  Python script can be run to create these folders and add items to them.

## Importing the items

- in the Zotero desktop app, choose the target library (using an empty group library is 
  recommended) and use the ```File | Import...``` command to import the JSON file. Sync your 
  desktop app to see the results.

## Running create_folders.py

This script uses the Zotero Web API to assign imported items to collections based on the headers
in the source file. It can be adapted to do other post-processing tasks.

- run ```./create_folders.py```. It expects to find the credentials it needs in ```config.ini```
  in the same directory. The script will examine each item in the ```uncorrected``` collection
  (imported or pre-existing), determine what collection it belongs in by examining the 
  ```Extra``` field, create that collection if necessary, and add the item into it. The script can
  handle two levels of collections (e.g. "Countries/India"). 
- when the script is done, sync the library to your Zotero desktop client to see the results.
  The items are not removed from the ```uncorrected``` collection, so this collection can be used in 
  the correction process: as each item is corrected, it is removed from this collection (but still 
  exists in the other collection it was added to).

## Manual Correction

- after the items are imported and organized, you will want to check them for accuracy. To 
  manage the workflow, you can work through the ```uncorrected``` collection, and remove 
  each item from that collection after it has been checked. When the ```uncorrected``` 
  collection is empty, you're done. The items will still belong to the collections they
  were placed in, based on the headings.