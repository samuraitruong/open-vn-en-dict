import requests
import pprint


class cambridge:
    @staticmethod
    def getWord(word):
        URL = f'https://dictionary.cambridge.org/vi/spellcheck/english-vietnamese/?q={word}'
        print(URL)
        response = requests.get(URL)
        html = response.text
        return html


if __name__ == "__main__":
    pprint.pprint(cambridge.getWord("hello"))
