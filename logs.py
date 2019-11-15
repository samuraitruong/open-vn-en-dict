import requests
from pyquery import PyQuery as pq
import os.path
import json
import concurrent.futures
import os.path
import pprint
import sys
import store

entries = os.listdir('html/')
print("Total find found: %d" % (len(entries)))

logs = {}
error = {}
for file in entries:
    try:
        print(file)
        data = store.readJson("html/" + file)
        en_vn = data.get("en_vn")
        if en_vn:
            logs[en_vn["data"]["word"]] = 1
        else:
            error[file.replace(".json", "")] = 1
    except Exception as e:
        print(e)
        print("ERROR : " + file)
print(logs)
store.writeJson(logs, "goodWords.json")
store.writeJson(error, "errors.json")

1
