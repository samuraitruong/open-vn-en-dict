import requests
from pyquery import PyQuery as pq
import json
import concurrent.futures


def getWordList():
    URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words_dictionary.json"
    r = requests.get(url=URL)
    data = r.json()
    with open('words.json', 'w') as outfile:
        json.dump(data, outfile)
    return data


def getWordFromLaban(word):
    URL = "https://dict.laban.vn/find"

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {"type": 1, "query": word}

    # sending get request and saving the response as response object
    r = requests.get(url=URL, params=PARAMS)

    # extracting data in json format
    data = r.text
    html = pq(data)
    # print(html("#column-content").html())
    return html("#slide_show").html()


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


words = getWordList()
print(getWordFromLaban("School"))
# with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
#     future_to_url = {executor.submit(
#         getWordFromLaban, key): key for key in words}
#     for future in concurrent.futures.as_completed(future_to_url):
#         url = future_to_url[future]
#         try:
#             html = future.result()
#             with open("html/" + url+'.html', 'w+') as outfile:
#                 outfile.write(html)
#         except Exception as exc:
#             print('%r generated an exception: %s' % (url, exc))
#         else:
#             print('%r page is %d bytes' % (url, len(html)))
