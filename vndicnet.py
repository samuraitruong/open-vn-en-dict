# http://1.vndic.net/
# http://1.vndic.net/index.php?word=malchus&dict=en_en
# http://1.vndic.net/index.php?word=malchus&dict=en_vn
import re
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


class vndicnet:
    @staticmethod
    def getWord(word, dict="en_vn"):
        # api-endpoint
        URL = "http://1.vndic.net/fast_dict.php"
        # http://1.vndic.net/fast_dict.php?word=secondary&dict=en_vi&m=1
        # defining a params dict for the parameters to be sent to the API
        PARAMS = {
            "word": word,
            "dict": dict,
            "m": 1
        }

        # sending get request and saving the response as response object
        r = requests.get(url=URL, params=PARAMS)

        # extracting data in json format
        data = r.text
        html = pq(data)
        return html(".maincontent").html()

    @staticmethod
    def transform(raw):
        pronounce = ""
        m = re.search(r'>/(.*)/<', raw)

        if m:
            pronounce = m.group(1)

        raw = re.sub(r'\?word=([^&]*)&amp;dict=([^"]*)', r"\1", raw)
        raw = raw.replace("\t", "")
        html = pq(raw)

        mappings = {
            "images/hoa.png": "bullet-1",
            "images/green.png": "bullet-2",
            "images/dot.png": "bullet-3",
            "images/ticx.png": "bullet-4"
        }
        for el in html("img"):
            href = pq(el).attr("src")
            print(href)
            pq(el).after(pq("<span class='%s'></span>" % (mappings.get(href))))
        html("img").remove()
        return {
                "data": {
                    "content": html.html(),
                    "pronounce": pronounce


            }
        }
    
    @staticmethod
    def fetchWord(word):
        return {

        }


if __name__ == "__main__":
    html = vndicnet.getWord("chicken", "en_vn")
    item = vndicnet.transform(html)
    store.writeJson(item, "data1/chicken.json", True)
    pprint.pprint(item)
