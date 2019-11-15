import json
import os


def writeJson(obj, filePath, verbose=False):
    if verbose:
        print("writing json file to", filePath)
    with open(filePath, "w+") as file:
        file.seek(0)
        file.truncate()
        json.dump(obj, file, indent=4)


def readJson(file, default={}):
    if os.path.isfile(file):
        with open(file) as json_file:
            data = json.load(json_file)
            return data
