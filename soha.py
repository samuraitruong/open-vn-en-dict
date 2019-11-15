import requests
from pyquery import PyQuery as pq


class soha:
    @staticmethod
    def getWord(word, dict="en_vn"):

        URL = f'http://tratu.soha.vn/index.php'
        res = requests.get(URL, params={"search": word, "dict": dict})
        html = pq(res.text)
        links = html("#bodyContent fieldset  span a")
        suggests = []
        suggests = [{"word": link.text} for link in links]
        body = html("#bodyContent")

        # suggests.append(pq(link).html())
        result = {
            dict: {
                "data": {
                    "pronounce": html(".mw-headline>font").text().strip(),
                },

                "suggests": suggests
            }
        }
        return result


if __name__ == "__main__":
    print(soha.getWord("home"))
