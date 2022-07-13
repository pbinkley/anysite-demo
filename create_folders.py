#!/usr/bin/env python

from pyzotero import zotero
import configparser

import pdb

config = configparser.ConfigParser()
config.read('config.ini') # read config: config['Zotero']['library_id']

project = config['Zotero']
zot = zotero.Zotero(project['library_id'], project['library_type'], project['api_key'])

# make list of existing collections: returns flat list
coll_list = {}
collections = zot.everything(zot.collections()) # this includes subcollections: have coll['data']['parentCollection']
for coll in collections:
  if 'parentCollection' in coll['data']:
    parent = coll['data']['parentCollection']
  else:
    parent = ''
  print(f"{coll['data']['name']}: {coll['key']} | {parent}")
  coll_list[coll['key']] = {"name": coll["data"]["name"], "parent": parent}
  # name = coll['data']['name']

# make list of combined collections: key is concatenated list of parent|child names
# e.g. "Soil|Books"
combined_coll_list = {}
for key in coll_list:
  coll = coll_list[key]
  if coll['parent']:
    combined_coll_list[f"{coll_list[coll['parent']]['name']}|{coll['name']}"] = key
  else:
    combined_coll_list[coll['name']] = key

# now work through items in "uncorrected" collection, into which items
# have been imported
items = zot.everything(zot.collection_items(combined_coll_list['uncorrected']))
for item in items:
  print(f"Item: {item['data']['extra']}")
  collection_split = item['data']['extra'].split('| ZoteroFolder: ')
  if len(collection_split) > 1:
     collection_name = collection_split[1]
     print(collection_name)
     if not(collection_name in combined_coll_list):
       # create directory, and add to combined_coll_list
       # create parent, if it has one
       parent_key = ''
       parts = collection_name.split('|')
       if len(parts) == 2:
         # there's a parent collection
         parent_name = parts.pop(0) # leaves just the child name in the parts list
         print(f"  Parent: {parent_name}")
         if parent_name in combined_coll_list: # parent collection exists
           parent_key = combined_coll_list[parent_name]
         else: # must create parent collection
           parent = zot.create_collections([{ "name": parent_name }])
           parent_key = parent['successful']['0']['data']['key']
           combined_coll_list[parent_name] = parent_key
       # now create main collection as child of parent
       if parent_key != '':
         print(f"  Create top: {parent_name}, child: {parts[0]}")
         coll = zot.create_collections([{"name": parts[0], "parentCollection": parent_key}])
       else:
         print(f"  Create top: {parts[0]}")
         coll = zot.create_collections([{"name": parts[0]}])
       key = coll['successful']['0']['data']['key']
       combined_coll_list[collection_name] = key

  # now add item to its collection
  zot.addto_collection(combined_coll_list[collection_name], item)
