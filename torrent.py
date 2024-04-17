"""Common functions"""
import signal
import subprocess
import sys
import re
import json
import torrentelem

try:
    import requests
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    print('Install requirments.txt')
    sys.exit(1)

# text format
bold_text = "\033[1m"
underscore = "\x1b[4m"
reset_clr = "\x1b[0m"
red = "\x1b[31m"
green = "\x1b[32m"
yellow = "\x1b[33m"
blue = "\x1b[34m"
magenta = "\x1b[35m"
cyan = "\x1b[36m"
white = "\x1b[37m"


class TorrentDownloader:
    """Add magnet link to transmission or other torrent client"""

    def __init__(self) -> None:
        # a rigor non la chiamo mai
        self.torrent_pages = None
        self.autoadd = None
        self.custom_cmd = None
        self.sort_by = None
        self.gui = None

    torren_fields = []

    def setup(self, gui:bool) -> None:
        """inizitialize variables"""
        self.read_config()
        self.gui = gui
        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)

    @classmethod
    def sig_handler(cls, _signo, _stack_frame) -> None:
        """Catch ctr+c signal"""
        print("\n")
        sys.exit(0)

    def read_config(self) -> None:
        """read config.json"""
        # inizialize with default value
        self.torrent_pages: int = 3
        self.autoadd: bool = True
        self.custom_cmd: str = ""
        self.sort_by: str = "size"
        try:
            tmp: dict = json.load(open('config.json'))
            self.torrent_pages: int = tmp['torrent_pages']
            self.autoadd: bool = tmp['autoadd']
            self.custom_cmd: str = tmp['custom_command']
            self.sort_by: str = tmp['sort_by']
        except FileNotFoundError:
            print(f"{red}config.json not found, using default value{reset_clr}")

    def solidtorrents_request(self, name_s: str) -> None:
        """Request to the torrent site"""
        # sending get request and saving the response as response object
        max_elem = self.torrent_pages
        for elem in range(1, max_elem + 1):
            url = f"https://solidtorrents.to/search?q={name_s}&page={elem}/"
            req = requests.get(url=url, params={})
            self.searchSolidtorrents(req)

    def searchSolidtorrents(self, req: requests.models.Response) -> None:
        for parsed in BeautifulSoup(req.text, "html.parser").find_all(
                "li", {"class": "card search-result my-2"}
        ):
            stats_div = parsed.find("div", {"class": "stats"})
            x = stats_div.find_all("div")
            name = parsed.find("a").text
            size = float(re.sub(r"^\W*|\W*$", "", (x[1].text))[0])
            seed = re.sub(r"^\W*|\W*$", "", x[2].text)
            leech = re.sub(r"^\W*|\W*$", "", x[3].text)
            movie_type: ""
            type_t = re.sub(r"^\W*|\W*$", "", x[1].text).split(" ", 1)
            date = re.sub(r"^\W*|\W*$", "", x[4].text)
            link = parsed.find("a", {"class": "dl-magnet"})["href"]
            temp = torrentelem.TorrentElem(name=name, size=size, seeders=seed, leecher=leech, date=date,
                                           file_type=type_t[0], magnet="", link=link)
            self.torren_fields.append(temp)
        self.torren_fields.sort(key=lambda x: x.size, reverse=True)

    def search1337x(self, req: requests.models.Response) -> None:
        """Parsing function"""
        # extracting data in json format
        for parsed in BeautifulSoup(req.text, "html.parser").findAll("tr"):
            try:
                type_torr = ""
                title = ""
                link = ""
                size = parsed.find("td", attrs={"class": "coll-4"}).get_text()
                leech = parsed.find("td", attrs={"class": "coll-3"}).get_text()
                date_t = parsed.find("td", attrs={"class": "coll-date"}).get_text()
                seed = parsed.find("td", attrs={"class": "coll-2"}).get_text()
                elem = parsed.find("td", attrs={"class": "coll-1"})
                for tit in elem.find_all("a", href=True):
                    link = tit["href"]
                    title = tit.text
                    if "/sub/" in link:
                        type_torr = link.split("/")[3]
                if len(title) > 1:
                    temp = torrentelem.TorrentElem(name=title, size=float(size.split(" ")[0]), seeders=seed,
                                                   leecher=leech,
                                                   date=date_t, file_type=type_torr, magnet="",
                                                   link=("https://www.1337xx.to" + link))
                    self.torren_fields.append(temp)
            except AttributeError:
                continue

            # create a json with torrent info
            self.torren_fields.sort(key=lambda x: x.size, reverse=True)

    #   self.json_torrent = json.dumps(self.torrent_list)

    def search1377x_request(self, name_s: str) -> None:
        """Request to the torrent site"""
        # sending get request and saving the response as response object
        max_elem = self.torrent_pages
        for elem in range(1, max_elem + 1):
            url = f"https://www.1377x.to/search/{name_s}/{elem}/"
            req = requests.get(url=url, params={})
            if elem == 1:
                parsed_html = BeautifulSoup(req.text, "html.parser")
                if len(parsed_html.findAll('tr')) == 1:
                    print(
                        f"{red}No torrent founded for \"{name_s}\"{reset_clr}")
                    print("")
                    sys.exit(0)
            self.search1337x(req=req)

    def start(self, magnet_link: str) -> bool:
        """start magnet"""
        if self.autoadd:
            # avvio il magnet
            if self.custom_cmd:
                try:
                    cmd = self.custom_cmd.split()
                    cmd.append(magnet_link)
                    # subprocess.Popen(cmd)
                except subprocess.CalledProcessError:
                    return False
            elif sys.platform.startswith('linux'):
                try:
                    subprocess.Popen(['/usr/bin/xdg-open', magnet_link])
                except subprocess.CalledProcessError:
                    return False
            # TODO add and check windows support
            # elif sys.platform.startswith('win32'):
            #   done = os.startfile(magnet_link)
            # elif sys.platform.startswith('cygwin'):
            #    done = os.startfile(magnet_link)
            elif sys.platform.startswith('darwin'):
                try:
                    subprocess.Popen(['/usr/bin/open', magnet_link])
                except subprocess.CalledProcessError:
                    return False
            else:
                try:
                    subprocess.Popen(['/usr/bin/xdg-open', magnet_link])
                except subprocess.CalledProcessError:
                    return False
            print(
                f'\n{green}Success{reset_clr}')
            return True
        # no autoadd
        if not self.gui:
            print(
                f"\nMagnet:{red}{magnet_link}{reset_clr}\n")
        return True





if __name__ == "__main__":
    print(f"{red} Please run terminal.py or gui.py{reset_clr}")
