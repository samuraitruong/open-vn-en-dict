import requests
from pyquery import PyQuery as pq
import os.path
import json
import concurrent.futures
import os.path
import pprint
import sys
import argparse
import store
from laban import labalvn


parser = argparse.ArgumentParser(description='Input argruments.')
parser.add_argument('--debug', dest='debug',
                    help='debug 1 single word ex:  Chicken')
parser.add_argument('--log-file', dest='logFile', default="logs.json",
                    help='The logs file  to keep track proceeded words')

parser.add_argument('--input-file', dest='inputFile', default="words.json",
                    help='List of words to process, defautl will fetch from github')

args = parser.parse_args()


def getWordList():
    URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"
    r = requests.get(url=URL)
    data = r.json()
    with open('words.json', 'w') as outfile:
        json.dump(data, outfile)
    return data


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


if args.debug:
    debug = labalvn.fetchWord(args.debug)
    pprint.pprint(debug)
    store.writeJson(debug, args.debug, True)
    exit()


logs = {}
if os.path.isfile(args.logFile):
    with open(args.logFile) as json_file:
        logs = json.load(json_file)
        print("Proceeded : %d" % (len(logs)))

print("Retrive list of all english words")
if(os.path.isfile(args.inputFile)):
    with open(args.inputFile, "r") as inputFile:
        words = json.load(inputFile)
else:
    words = getWordList()
print("Total english words %d" % (len(words)))
# for key in words:
#     if key < "hype":
#         logs[key] = 1
# with open("logs.json", 'w+') as outfile:
#     outfile.seek(0)
#     outfile.truncate()
#     json.dump(logs, outfile, indent=4, sort_keys=True)
delta = 0
with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
    future_to_url = {executor.submit(
        labalvn.fetchWord, key): key for key in words if logs.get(key) == None}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            fileName = "html/" + url.lower()+".json"
            html = future.result()
            if html != None:

                with open(fileName.lower(), 'w+') as outfile:
                    outfile.seek(0)
                    outfile.truncate()
                    json.dump(html, outfile, indent=4, sort_keys=True)
                logs[url] = 1
                delta = delta + 1
                if delta > 1000:
                    delta = 0
                    print("Update logs files")
                    with open(args.logFile, 'w+') as logFile:
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
