import requests
from pyquery import PyQuery as pq
import os.path
import json


class labalvn:

    @staticmethod
    def parseHtml(input, fetchVoice=False):
        json = {}
        if "best" not in input:
            return json
        best = input["best"]

        json["word"] = best["word"]
        html = pq(best["details"])
        #json["id"] = best["id"]
        json["pronounce"] = html("span.color-black").text()
        json["type"] = html("div.bg-grey.bold.font-large.m-top20").text()
        json["mean"] = html(".green.bold.margin25.m-top15")
        json["content"] = html("#content_selectable").html().replace(
            "https://dict.laban.vn", "").strip()
        if fetchVoice:
            json["speak"] = {}
            labalvn.downloadVoice(json, "us")
            labalvn.downloadVoice(json, "uk")
        return json

    @staticmethod
    def downloadVoice(json, type):
        try:
            word = json["word"]

            filename = 'voice/' + word.lower() + "_" + type + ".mp3"
            response = requests.get(
                "https://dict.laban.vn/ajax/getsound?accent="+type+"&word=" + word)
            rawJson = response.json()
            if response.status_code == 200 and rawJson["error"] == 0 and rawJson["data"] != "":
                json["speak"][type] = rawJson["data"]
                if os.path.isfile(filename):
                    return None

                response = requests.get(rawJson["data"])
                if response.status_code == 200:
                    with open(filename, 'wb') as f:
                        f.write(response.content)
        except Exception as ex:
            print(ex)

    @staticmethod
    def transform(json):
        output = {}
        if "enViData" in json:
            output["en_vn"] = {
                "suggests": json["enViData"]["suggests"],
                "data": labalvn.parseHtml(json["enViData"], True)
            }
        if "enEnData" in json:
            output["en_en"] = {
                "suggests": json["enEnData"]["suggests"],
                "data": labalvn.parseHtml(json["enEnData"], False)
            }
        if "synData" in json:
            output["synonyms"] = {
                "suggests": json["synData"]["suggests"],
                "data": labalvn.parseHtml(json["synData"], False)
            }
        return output

    @staticmethod
    def fetchWord(word, type=1):
        # fileName = "html/" + word+".json"

        # URL = "https://dict.laban.vn/find"
        URL = "https://dict.laban.vn/ajax/find"  # ?type=1&query=history
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {"type": type, "query": word}

        # sending get request and saving the response as response object
        r = requests.get(url=URL, params=PARAMS)
        json = r.json()

        return labalvn.transform(json)
