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

logs = {}
error = {}
for file in entries[:1000]:
    try:
        print(file)
        with open("html/" + file) as f:
            data = json.load(f)
            en_vn = data.get("en_vn")
            if en_vn:
                logs[en_vn["data"]["word"]] = 1
            else:
                error[file.replace(".json", "")] = 1
    except Exception as e:
        print(e)
        print("ERROR : " + file)
print(logs)
with open("goodWords1.json", "w+") as outFile:
    json.dump(logs, outFile, indent=4)
with open("errors.json", "w+") as outFile:
    json.dump(error, outFile, indent=4)

1
