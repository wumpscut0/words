import http.client as http
from logging import getLogger
from string import ascii_letters
from json import loads
from os import getenv
from re import fullmatch, I
from typing import Dict, List
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
logger = getLogger("stdout")

class DictionaryYandexNetApi:
    _host = "dictionary.yandex.net"
    _url = f"/api/v1/dicservice.json/lookup?key={getenv('YANDEX_DICT')}&lang=en-ru&text="

    def __init__(self, word=None):
        self.data = None
        if word is None:
            return
        self.word = word


        if not fullmatch(r"[a-z-]+", self.word, flags=I):
            logger.error(f"Incorrect word {self.word} for extract data")
            return

        connection = http.HTTPSConnection(self._host)
        connection.request(method="GET", url=self._url + self.word)
        response = connection.getresponse()
        if response.status == 200:
            self.data = loads(response.read())
            logger.info(f"Data resaved for word {word}")
        else:
            logger.critical(f"{self._host} returned unexpected code {response.status} {response.reason} for word {word} {response.read().decode()}")
        connection.close()

    def parse_translates(self, data_: Dict | None = None) -> List[str] | None:
        data = data_ or self.data
        if data is None:
            # logger.error(f"Data for parse translates not found for word {self.word}")
            return

        translates = []

        try:
            for pos in data["def"]:
                for tr in pos.get("tr", ()):
                    t = tr.get("text")
                    if t and all(True if sym not in ascii_letters else False for sym in t):
                        translates.append(t)
        except KeyError as e:
            e.add_note(f"{self._host} returned unexpected data {data}")
            logger.error(e)
        return translates

    def parse_transcription(self, data_=None) -> str | None:
        data = data_ or self.data
        if data is None:
            # logger.error(f"Data for parse transcription not found for word {self.word}")
            return

        for pos in data["def"]:
            ts = pos.get("ts")
            if ts:
                return ts

        logger.warning(f"Transcription not found for word")


if __name__ == '__main__':
    print(DictionaryYandexNetApi("time").data)
