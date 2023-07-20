'''Common functions'''
import signal
import subprocess
import sys
import re
import json
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


class TorrentDownloader():
    '''Add magnet link to transmission or other torrent client'''

    def __init__(self) -> None:
        self.torrent_pages = None
        self.autoadd = None
        self.custom_cmd = None
        self.sort_by = None
        self.gui = None

    json_torrent = '''
            {
                "Torrent": [
                    ]
            }
            '''

    def setup(self) -> None:
        '''inizitialize variables'''
        self.json_torrent = '''
            {
                "Torrent": [
                    ]
            }
            '''
        self.read_config(self)
        signal.signal(signal.SIGTERM, TorrentDownloader.sig_handler)
        signal.signal(signal.SIGINT, TorrentDownloader.sig_handler)

    @classmethod
    def sig_handler(cls, _signo, _stack_frame) -> None:
        '''Catch ctr+c signal'''
        print("\n")
        sys.exit(0)

    def read_config(self) -> None:
        '''read config.json'''
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
            print(
                f"{ red  }config.json not found, using default value{reset_clr}")

    def search1337x(self, req: requests.models.Response) -> None:
        '''Parsing function'''
        # extracting data in json format
        self.torrent_list = json.loads(TorrentDownloader.json_torrent)
        for parsed in BeautifulSoup(req.text, "html.parser").findAll('tr'):
            try:
                size = (parsed.find('td', attrs={
                        'class': 'coll-4'}).get_text())
                leech = (parsed.find('td', attrs={
                         'class': 'coll-3'}).get_text())
                date_t = (parsed.find(
                    'td', attrs={'class': 'coll-date'}).get_text())
                seed = (parsed.find('td', attrs={
                        'class': 'coll-2'}).get_text())
                elem = parsed.find('td', attrs={'class': 'coll-1'})
                for tit in elem.find_all('a', href=True):
                    link = tit['href']
                    title = tit.text
                    if "/sub/" in link:
                        type_torr = link.split("/")[3]
                if len(title) > 1:
                    temp = {
                        'name': title,
                        'size': float(size.split(" ")[0]),
                        'seed': seed,
                        'leech': leech,
                        'movie_type': type_torr,
                        'type': size.split(" ")[1],
                        'date': date_t,
                        'link': 'https://www.1337xx.to' + link
                    }
                    self.torrent_list['Torrent'].append(temp)
            except AttributeError:
                continue

            # create a json with torrent info
        TorrentDownloader.json_torrent = json.dumps(self.torrent_list)
        self.torrent_list['Torrent'] = sorted(
            self.torrent_list['Torrent'], key=lambda pos: pos[self.sort_by], reverse=True)  # sort list with given key selected in config.json
        # update json with sorted json
        TorrentDownloader.json_torrent = json.dumps(self.torrent_list)

    def search1377x_request(self, name_s: str) -> None:
        '''Request to the torrent site'''
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
            self.search1337x(self,req)

    def start(self, magnet_link: str) -> bool:
        '''start magnet'''
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
        print("else")
        if self.gui:
            print("if")
            TorrentDownloader.show_magnet(magnet_link)
        else:
            print(
                f"\nMagnet:{red}{magnet_link}{reset_clr}\n")
        return True

    def get_magnet(self, link: str, gui: bool) -> None:
        '''function to get magnet link'''
        self.gui = gui
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        req = requests.get(link, headers=headers)
        # extracting data in json format
        print("req")
        parsed_html = BeautifulSoup(req.text, "html.parser")
        magnet_link = ''
        for parsed in parsed_html.findAll('li'):
            # search magnet link using regex
            for x in parsed.find_all(href=re.compile("^magnet:\?xt=urn:btih:[0-9a-fA-F]{40,}.*$")):
                magnet_link = x['href']
        if magnet_link != '':
            if not TorrentDownloader.start(TorrentDownloader, magnet_link):
                if self.gui:
                    from gui import TorrentDownloaderGUI
                    TorrentDownloader.show_magnet(magnet_link)
                else:  # error in starting magnet link
                    print(
                        f"{red}An Error Occured while executing command{reset_clr}\n")
                    print(
                        f"\nMagnet:{red}{magnet_link}{reset_clr}\n")
        else:
            print(
                f"{red}No Magnet Link Found{reset_clr}\n")
    
    def show_magnet(str_magnet: str) -> None:
        '''show magnet link on window'''
        from PySide2.QtCore import QFile
        from PySide2.QtUiTools import QUiLoader
        from PySide2.QtWidgets import QTextEdit
        loader = QUiLoader()
        magnet_ui = 'Resources/show.ui'
        ui_magnet = QFile(magnet_ui)
        TorrentDownloader.magnet_window = loader.load(magnet_ui)
        ui_magnet.close()
        print("textedit 2")
        text: QTextEdit = TorrentDownloader.magnet_window.findChild(
            QTextEdit, "magnet_link")
        text.insertPlainText(str_magnet)
        print("open 2")
        TorrentDownloader.magnet_window.show()


if __name__ == "__main__":
    print(f"{red} Please run terminal.py or gui.py{reset_clr}")
