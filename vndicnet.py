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
        pronounce = "";
        m = re.search(r'>/(.*)/<', raw)
        if m:
            pronounce = m.group(1)

        raw = re.sub(r'\?word=([^&]*)&amp;dict=([^"]*)', r"\1", raw)
        raw = raw.replace("\t", "");
        html = pq(raw)
        html("img").remove()
        return {
            "en_vn": {
                "data": {
                    "content": html.html(),
                    "pronounce": pronounce


                }
            }
        }


if __name__ == "__main__":
    html = vndicnet.getWord("expensive", "en_vn")
    pprint.pprint(vndicnet.transform(html))
