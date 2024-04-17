import datetime
import re
from bs4 import BeautifulSoup
import requests


class TorrentElem:
    name: str = ""
    size: float = 0.0
    date: datetime = datetime.datetime.now()
    seeders: str = ""
    leecher: str = ""
    file_type: str = ""
    link: str = ""
    magnet: str = ""

    def __init__(self, name: str, size: float, date: datetime, seeders: str, leecher: str, file_type: str, link: str,
                 magnet: str = ""):
        self.name = name
        self.size = int(size)
        self.date = date
        self.seeders = seeders
        self.leecher = leecher
        self.file_type = file_type
        self.link = link
        self.magnet = magnet

    def get_magnet(self) -> None:
        """function to get magnet link"""
        pattern = "^magnet:\?xt=urn:btih:[0-9a-fA-F]{40,}.*$"
        if not re.match(pattern=pattern, string=self.link):
            """function to get magnet link"""
            headers = {"User-Agent": "Mozilla/5.0"}
            req = requests.get(self.link, headers=headers)
            # extracting data in json format
            parsed_html = BeautifulSoup(req.text, "html.parser")
            self.magnet = ""
            for parsed in parsed_html.findAll("li"):
                # search magnet link using regex
                for x in parsed.find_all(
                        href=re.compile(pattern)
                ):
                    self.magnet = x["href"]
        else:
            self.magnet = self.link
