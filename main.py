import requests
from pyquery import PyQuery as pq
import os.path
import json
import concurrent.futures
import os.path
import pprint
import sys


def getWordList():
    URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"
    r = requests.get(url=URL)
    data = r.json()
    with open('words.json', 'w') as outfile:
        json.dump(data, outfile)
    return data


def downloadVoice(json, type):
    word = json["word"]
    response = requests.get(
        "https://dict.laban.vn/ajax/getsound?accent="+type+"&word=" + word)
    rawJson = response.json()
    if response.status_code == 200 and rawJson["error"] == 0 and rawJson["data"] != "":
        response = requests.get(rawJson["data"])
        json["speak"][type] = rawJson["data"]
        if response.status_code == 200:
            with open('voice/' + word + "_" + type + ".mp3", 'wb') as f:
                f.write(response.content)


def parseHtml(input, fetchVoice=False):
    json = {}
    if "best" not in input:
        return json
    best = input["best"]

    json["word"] = best["word"]
    html = pq(best["details"])
    json["id"] = best["id"]
    json["pronounce"] = html("span.color-black").text()
    json["type"] = html("div.bg-grey.bold.font-large.m-top20").text()
    json["mean"] = html(".green.bold.margin25.m-top15")
    json["content"] = html("#content_selectable").html().replace(
        "https://dict.laban.vn", "").strip()
    if fetchVoice:
        json["speak"] = {}
        downloadVoice(json, "us")
        downloadVoice(json, "uk")
    return json


def transformLaban(json):
    output = {}
    if "enViData" in json:
        output["en_vn"] = {
            "suggests": json["enViData"]["suggests"],
            "data": parseHtml(json["enViData"], True)
        }
    if "enEnData" in json:
        output["en_en"] = {
            "suggests": json["enEnData"]["suggests"],
            "data": parseHtml(json["enEnData"], False)
        }
    if "synData" in json:
        output["synonyms"] = {
            "suggests": json["synData"]["suggests"],
            "data": parseHtml(json["synData"], False)
        }
    return output


def getWordFromLaban(word):
    fileName = "html/" + word+".json"
    # if os.path.isfile(fileName):
    #     print("Ignore ", url)
    #     return None

    URL = "https://dict.laban.vn/find"
    URL = "https://dict.laban.vn/ajax/find"  # ?type=1&query=history
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {"type": 1, "query": word}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)
    json = r.json()

    return transformLaban(json)
    # extracting data in json format
    # data = r.text

    # html = pq(data)
    # # print(html("#column-content").html())
    # return html("#slide_show").html()


def getWord(word):
    # print("Going to get word %s", word)

    # api-endpoint
    URL = "http://tratu.soha.vn/dict/en_vn/"+word

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    data = r.text
    html = pq(data)
    # print(html("#column-content").html())
    return html("#column-content").html()


logs = {}
with open('logs.json') as json_file:
    logs = json.load(json_file)
    print("Proceeded : %d" % (len(logs)))

if len(sys.argv) > 1:
    pprint.pprint(getWordFromLaban(sys.argv[1]))
    exit()
print("Retrive list of all english words")
words = getWordList()
print("Total english words %d" % (len(words)))
# for key in words:
#     if key < "hype":
#         logs[key] = 1
# with open("logs.json", 'w+') as outfile:
#     outfile.seek(0)
#     outfile.truncate()
#     json.dump(logs, outfile, indent=4, sort_keys=True)
#  exit()
delta = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
    future_to_url = {executor.submit(
        getWordFromLaban, key): key for key in words if logs.get(key) == None}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            fileName = "html/" + url+".json"
            html = future.result()
            if html != None:

                with open(fileName, 'w+') as outfile:
                    outfile.seek(0)
                    outfile.truncate()
                    json.dump(html, outfile, indent=4, sort_keys=True)
                logs[url] = 1
                delta = delta + 1
                if delta > 1000:
                    delta = 0
                    print("Update logs files")
                    with open("logs.json", 'w+') as logFile:
                        logFile.seek(0)
                        logFile.truncate()
                        json.dump(logs, logFile, indent=4, sort_keys=True)
        # except requests..exceptions.ConnectionError:
        #    print('%r generated an exception: %s' % (url, exc))
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
            # exit()
        else:
            print('%r page is %d bytes' % (url, len(html)))
