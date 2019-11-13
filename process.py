import requests
from pyquery import PyQuery as pq
import os.path
import json
import concurrent.futures
import os.path
import pprint
import sys

entries = os.listdir('html/')
print("Total find found: %d" % (len(entries)))

related = {}
for file in entries:
    try:
        print(file)
        with open("html/" + file) as f:
            data = json.load(f)
            for key in data:
                item = data[key]
                suggests = item.get("suggests")
                if suggests and len(suggests) > 0:
                    for s in suggests:
                        related[s["word"]] = 1
    except:
        print("ERROR : " + file)
print(related)
with open("suggests.json", "w+") as outFile:
    json.dump(related, outFile, indent=4)
