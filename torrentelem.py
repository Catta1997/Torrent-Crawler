import datetime


class TorrentElem:
    name: str = ""
    size: float = 0.0
    date: datetime = datetime.datetime.now()
    seeders: str = ""
    leecher: str = ""
    file_type: str = ""
    magnet: str = ""

    def __init__(self, name: str, size: float, date: datetime, seeders: str, leecher: str, file_type: str, magnet: str):
        self.name = name
        self.size = int(size)
        self.date = date
        self.seeders = seeders
        self.leecher = leecher
        self.file_type = file_type
        self.magnet = magnet

