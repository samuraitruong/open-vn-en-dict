import requests
from pyquery import PyQuery as pq
import store
import pprint


class tracau:
    @staticmethod
    def transform(data):
        return data

    @staticmethod
    def request(word, type="en"):
        URL = f'https://api.tracau.vn/WBBcwnwQpV89/s/{word}/{type}'
        res = requests.get(URL)
        data = res.json()

        return data

    @staticmethod
    def parseHtml(htmlText, word, id):
        html = pq(htmlText)
        pronounce = html("#pa #C_C").text();
        return {"data": {
            "content": html(id).html(),
            "word": word,
            "pronounce": pronounce
        }}

    @staticmethod
    def fetchWord(word, dict="en_vn"):

        data = tracau.request(word)
        item = data.get("tratu")
        if(item is None or len(item) == 0):
            return {}

        htmlText = item[0]["fields"]["fulltext"]
        word1 = item[0]["fields"]["word"]
        sentences = [f["fields"] for f in data.get("sentences", [])]

        return {
            "en_vn": tracau.parseHtml(htmlText, word1, "#ev"),
            "en_en": tracau.parseHtml(htmlText, word1, "#ox"),
            "synonyms": tracau.parseHtml(htmlText, word1, "#th"),
            "grammar": tracau.parseHtml(htmlText, word1, "#bb"),
            "specialist": tracau.parseHtml(htmlText, word1, "#et"),
            "sentences": sentences,
            "suggestions": data.get("suggestions")
        }
        # return result


if __name__ == "__main__":
    item = tracau.fetchWord("homesick")
    pprint.pprint(item)
