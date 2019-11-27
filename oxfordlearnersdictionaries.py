import requests
from pyquery import PyQuery as pq
import store
import pprint
import http.client
import re


class oxfordlearnersdictionaries:
    @staticmethod
    def transform(data):
        return data

    @staticmethod
    def request(word, type="english"):
        URL = f'https://www.oxfordlearnersdictionaries.com/definition/{type}/{word}_1'
        # print("URL:  " + URL)
        # conn = http.client.HTTPSConnection(
        #     "www.oxfordlearnersdictionaries.com", 443)
        # conn.request("GET", f'/definition/{type}/{word}_1')
        # response = conn.getresponse()
        # print(response.status, response.reason)
        # data = response.read()
        # print(data)
        print("URL: " + URL)
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate"

        }
        res = requests.get(URL, verify=True, headers=headers)
        data = res.text
        return data

    @staticmethod
    def parseHtml(htmlText):
        # regex replace
        htmlText = re.sub(r'dpsid="([^"]*)"', r'', htmlText)
        htmlText = re.sub(r'dpsref="([^"]*)"', r'', htmlText)
        htmlText = re.sub(r'dupedid="([^"]*)"', r'', htmlText)
        htmlText = re.sub(
            r"https:\/\/www.oxfordlearnersdictionaries.com\/([^\/]*)\/(english|collocations)", "", htmlText)
        html = pq(htmlText)
        html(".oxford3000, #ad_contentslot_2, .dictlinks").remove()
        html(".phon").remove(".bre").remove('.wrap').remove(".name")
        return {"data": {
            "content": html(".entry").html(),
            "word": html(".webtop-g h2").text(),
            "pronounce": html(".phon").text(),
            "type":   html(".webtop-g .pos").text(),
            "speak": {
                "uk": html(".pron-uk").attr("data-src-mp3"),
                "us": html(".pron-us").attr("data-src-mp3")
            }
        }}

    @staticmethod
    def fetchWord(word, dict="english"):

        data = oxfordlearnersdictionaries.request(word)

        return data


if __name__ == "__main__":
    html = oxfordlearnersdictionaries.fetchWord("home")
    item = oxfordlearnersdictionaries.parseHtml(html)
    pprint.pprint(item)
