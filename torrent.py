'''Simple parsing  script to obtain magnet link of a torrent'''

from bs4 import BeautifulSoup
import json
# import os
import signal
import subprocess
import sys
import re
import requests

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

    '''Common functions'''

    def __init__(self, gui: bool) -> None:
        self.gui = gui
        self.json_torrent = '''
            {
                "Torrent": [
                    ]
            }
            '''
        self.read_config()
        signal.signal(signal.SIGTERM, TorrentDownloader.sig_handler)
        signal.signal(signal.SIGINT, TorrentDownloader.sig_handler)
        if(self.gui):
            self.ricerca_gui()
        else:
            self.ricerca_cli()

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
        self.torrent_list = json.loads(self.json_torrent)
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
        self.json_torrent = json.dumps(self.torrent_list)
        self.torrent_list['Torrent'] = sorted(
            self.torrent_list['Torrent'], key=lambda pos: pos[self.sort_by], reverse=True)  # sort list with given key selected in config.json
        # update json with sorted json
        self.json_torrent = json.dumps(self.torrent_list)

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
            self.search1337x(req)

    '''GUI Functions'''

    def ricerca_gui(self) -> None:
        '''GUI search function'''
        # GUI import
        selfw = self
        from PySide2.QtWidgets import QCheckBox, QPushButton, QLineEdit
        from PySide2.QtCore import QObject
        from PySide2.QtGui import QKeyEvent

        class KeyPressEater(QObject):
            '''event filter '''

            def eventFilter(self, widget, event: QKeyEvent) -> bool:
                from PySide2.QtCore import QEvent, Qt
                if (event.type() == QEvent.KeyPress):
                    key = event.key()
                    if key == Qt.Key_Return:
                        TorrentDownloader.avvia_ricerca(selfw)
                        return True
                return False
        self.filtro = KeyPressEater()
        TorrentDownloader.titolo: QLineEdit = TorrentDownloader.window.findChild(
            QLineEdit, "titolo")
        TorrentDownloader.cerca: QPushButton = TorrentDownloader.window.findChild(
            QPushButton, "cerca")
        TorrentDownloader.add: QCheckBox = TorrentDownloader.window.findChild(
            QCheckBox, "add")
        TorrentDownloader.cerca.clicked.connect(
            lambda: TorrentDownloader.avvia_ricerca(self))
        TorrentDownloader.titolo.installEventFilter(self.filtro)

    def start(self, magnet_link: str) -> bool:
        '''start gui search'''
        if (self.autoadd):
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
        if (self.gui):
            from PySide2.QtWidgets import QTextEdit
            text: QTextEdit = TorrentDownloader.magnet_window.findChild(
                QTextEdit, "magnet_link")
            text.insertPlainText(magnet_link)
            TorrentDownloader.magnet_window.show()
        else:
            print(
                f"\nMagnet:{red}{magnet_link}{reset_clr}\n")
        return True

    @staticmethod
    def print_elem_gui(elem: dict, torrent: int) -> None:
        '''insert torrent element in table'''
        from PySide2.QtWidgets import QTableWidgetItem
        title_t = elem['name']
        min_pos = 0
        max_pos = 70
        if max_pos < len(title_t):
            TorrentDownloader.tabella.setItem(torrent, 0, QTableWidgetItem(
                (title_t[min_pos:max_pos] + "\n" + title_t[max_pos:140])))
        else:
            TorrentDownloader.tabella.setItem(
                torrent, 0, QTableWidgetItem((title_t)))
        TorrentDownloader.tabella.setItem(
            torrent, 1, QTableWidgetItem(f"{str(elem['size'])} {elem['type']}"))
        TorrentDownloader.tabella.setItem(
            torrent, 2, QTableWidgetItem(elem['seed']))
        TorrentDownloader.tabella.setItem(
            torrent, 3, QTableWidgetItem(elem['leech']))
        TorrentDownloader.tabella.setItem(
            torrent, 4, QTableWidgetItem(elem['movie_type']))
        TorrentDownloader.tabella.setItem(
            torrent, 5, QTableWidgetItem(elem['date']))
        TorrentDownloader.tabella.resizeColumnsToContents()
        TorrentDownloader.tabella.resizeRowsToContents()

    def avvia_ricerca(self) -> None:
        '''avvio ricerca GUI'''
        from PySide2.QtWidgets import QTableWidget, QPushButton, QApplication
        # reset to allow multiple search
        self.json_torrent = '''
        {
            "Torrent": [
                ]
        }
        '''
        name_input = TorrentDownloader.titolo.text()
        self.search1377x_request(str(name_input))
        # populate tabel
        torrent = 1
        TorrentDownloader.tabella: QTableWidget = TorrentDownloader.window.findChild(
            QTableWidget, "tableWidget")
        TorrentDownloader.seleziona: QPushButton = TorrentDownloader.window.findChild(
            QPushButton, "select")
        TorrentDownloader.seleziona.clicked.connect(
            lambda: TorrentDownloader.get_selected_element(self))
        TorrentDownloader.tabella.clearContents()
        TorrentDownloader.tabella.setRowCount(0)
        QApplication.processEvents()
        for elem in self.torrent_list['Torrent']:
            pos = torrent - 1
            TorrentDownloader.tabella.insertRow(pos)
            TorrentDownloader.print_elem_gui(elem, pos)
            torrent += 1

    def get_selected_element(self) -> None:
        '''get list of selected row in GUI'''
        # GUI (first time only)
        self.autoadd = TorrentDownloader.add.isChecked()
        # get multiple selection
        items = TorrentDownloader.tabella.selectedItems()
        for item in items:
            # only 1 item in a row
            if item.column() == 1:
                # start download with each selected row
                self.selected_elem = self.torrent_list[
                    'Torrent'][item.row()]
                self.get_magnet()

    '''CLI Functions'''

    def ricerca_cli(self) -> None:
        if len(sys.argv) == 1:
            name_input = input('Nome Film da cercare: ').strip()
        else:
            name_input = sys.argv[1]
            for elem in sys.argv[2:]:
                name_input += '%20' + elem
        self.search1377x_request(str(name_input))
        # print list
        torrent = 1
        self.torrent_list = json.loads(self.json_torrent)
        for elem in self.torrent_list['Torrent']:
            # write _____________
            print(underscore + ' ' * 120 + reset_clr+'\n')
            print(
                f" {bold_text}Torrent {torrent} :{reset_clr}")
            TorrentDownloader.print_elem(elem)
            torrent += 1
        self.choose()

    @staticmethod
    def print_elem(elem: dict) -> None:
        '''Print torrent element'''
        title_t = elem['name']
        min_pos = 0
        max_pos = 95
        print(
            f" {cyan}TITLE: {title_t[min_pos:max_pos]}{reset_clr}")
        while max_pos < len(title_t):
            min_pos += 95
            max_pos += 95
            print(f" {cyan}       {title_t[min_pos:max_pos]}{reset_clr}")
        print(
            f" {red}DATE: {elem['date']}{reset_clr}")
        print(
            f" {green}DIM: {str(elem['size'])} {elem['type']}{reset_clr}")
        print(
            f" {yellow}SEED: {elem['seed']}{reset_clr}")
        print(
            f" {white}LEECH: {elem['leech']}{reset_clr}")
        print(
            f" {magenta}TYPE: {elem['movie_type']}{reset_clr}")

    def choose(self) -> None:
        '''Select torrent'''
        # write _____________
        print(underscore+' ' * 120+reset_clr+'\n')
        found = 0
        while found == 0:
            try:
                number = int(input('Choose torrent: '))
            except ValueError:
                print(
                    f"\n{red}Not Valid!!{reset_clr}\n")
                TorrentDownloader.choose(self)
            found = 1
            number -= 1  # indice di un array
            self.selected_elem = self.torrent_list['Torrent'][number]
            TorrentDownloader.print_elem(self.selected_elem)
            conf = ""
            while conf.lower() not in ['y', 'n']:
                conf = input("\ny to confirm, n to repeat: ")
            if conf.lower() == 'n':
                found = 0
            elif (conf.lower() == 'y'):
                # controllo che number sia una scelta valida:
                if number < len(self.torrent_list['Torrent']) and number >= 0:
                    self.get_magnet()
                else:
                    print(
                        f"{red}Not Valid{reset_clr}")

    def get_magnet(self) -> None:
        '''function to get magnet link'''
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        req = requests.get(self.selected_elem['link'], headers=headers)
        # extracting data in json format
        parsed_html = BeautifulSoup(req.text, "html.parser")
        magnet_link = ''
        for parsed in parsed_html.findAll('li'):
            for x in parsed.find_all(href=re.compile("^magnet:\?xt=urn:btih:[0-9a-fA-F]{40,}.*$")): # search magnet link using regex
                magnet_link = x['href']
        if magnet_link != '':
            if not self.start(magnet_link):
                if (self.gui):
                    from PySide2.QtWidgets import QTextEdit
                    text: QTextEdit = TorrentDownloader.magnet_window.findChild(
                        QTextEdit, "magnet_link")
                    text.insertPlainText(magnet_link)
                    TorrentDownloader.magnet_window.show()
                else:  # error in starting magnet link
                    print(
                        f"{red}An Error Occured while executing command{reset_clr}\n")
                    print(
                        f"\nMagnet:{red}{magnet_link}{reset_clr}\n")
        else:
            print(
                f"{red}No Magnet Link Found{reset_clr}\n")


if __name__ == "__main__":
    print(f"{red} Please run terminal.py or gui.py{reset_clr}")
