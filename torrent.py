'''Simple parsing  script to obtain magnet link of a torrent'''

from bs4 import BeautifulSoup
import json
import os
import signal
import subprocess
import sys
import re
import requests



class TorrentDownloader():
    '''Torrent magnet link'''
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
    # config
    torrent_pages = 3
    autoadd = False
    # end config

    json_torrent = '''
    {
        "Torrent": [
            ]
    }
    '''

    @staticmethod
    def verify_magnet_link(magnet_link):
        '''verify a magnet link using regex'''
        result = re.fullmatch(
            "^magnet:\?xt=urn:btih:[0-9a-fA-F]{40,}.*$", magnet_link)
        if result is not None:
            return True
        else:
            return False

    @staticmethod
    def search1337x(req):
        '''Parsing function'''
        # extracting data in json format
        for parsed in BeautifulSoup(req.text, "html.parser").findAll('tr'):
            size = "0 "
            seed = ""
            leech = ""
            date_t = ""
            for elem in parsed.findAll('td', attrs={'class': 'coll-2'}):
                seed = (elem.text)
            for elem in parsed.findAll('td', attrs={'class': 'coll-3'}):
                leech = (elem.text)
            for elem in parsed.findAll('td', attrs={'class': 'coll-4'}):
                size = (elem.text)
            for elem in parsed.findAll('td', attrs={'class': 'coll-date'}):
                date_t = (elem.text)
            title = ""
            link = ""
            type_torr = ""
            for elem in parsed.findAll('td', attrs={'class': 'coll-1'}):
                for tit in elem.find_all('a', href=True):
                    link = tit['href']
                    title = tit.text
                    if "/sub/" in link:
                        type_torr = link.split("/")[3]
            # create a json with torrent info
            if len(title) > 1:
                temp = {
                    'name': title,
                    'size': float(size.split(" ")[0]),
                    'seed': seed,
                    'leech': leech,
                    'movie_type': type_torr,
                    'type': size.split(" ")[1],
                    'date': date_t,
                    'link': 'https://www.1377x.to' + link
                }
                data = json.loads(TorrentDownloader.json_torrent)
                data['Torrent'].append(temp)
                TorrentDownloader.json_torrent = json.dumps(data, indent=4)
                sorted_obj = dict(data)
                sorted_obj['Torrent'] = sorted(
                    data['Torrent'], key=lambda pos: pos['size'], reverse=True)
                TorrentDownloader.json_torrent = json.dumps(
                    sorted_obj, indent=4)

    @staticmethod
    def print_elem_gui(elem, torrent):
        '''Print torrent element'''
        from PySide2.QtWidgets import QTableWidgetItem
        title_t = elem['name']
        min_pos = 0
        max_pos = 95
        TorrentDownloader.tabella.setItem(
            torrent, 0, QTableWidgetItem(title_t[min_pos:max_pos]))
        TorrentDownloader.tabella.setItem(
            torrent, 1, QTableWidgetItem(f"{str(elem['size'])} {elem['type']}"))
        TorrentDownloader.tabella.setItem(
            torrent, 2, QTableWidgetItem(f"{elem['seed']}"))
        TorrentDownloader.tabella.setItem(
            torrent, 3, QTableWidgetItem(f"{elem['leech']}"))
        TorrentDownloader.tabella.setItem(
            torrent, 4, QTableWidgetItem(f"{elem['movie_type']}"))
        TorrentDownloader.tabella.setItem(
            torrent, 5, QTableWidgetItem(f"{elem['date']}"))
        TorrentDownloader.tabella.resizeColumnsToContents()

    @staticmethod
    def print_elem(elem):
        '''Print torrent element'''
        title_t = elem['name']
        min_pos = 0
        max_pos = 95
        print(
            f" {TorrentDownloader.cyan}TITLE: {title_t[min_pos:max_pos]}{TorrentDownloader.reset_clr}")
        while max_pos < len(title_t):
            min_pos += 95
            max_pos += 95
            print(
                f" {TorrentDownloader.cyan}       {title_t[min_pos:max_pos]}{TorrentDownloader.reset_clr}")
        print(
            f" {TorrentDownloader.red}DATE: {elem['date']}{TorrentDownloader.reset_clr}")
        print(
            f" {TorrentDownloader.green}DIM: {str(elem['size'])} {elem['type']}{TorrentDownloader.reset_clr}")
        print(
            f" {TorrentDownloader.yellow}SEED: {elem['seed']}{TorrentDownloader.reset_clr}")
        print(
            f" {TorrentDownloader.white}LEECH: {elem['leech']}{TorrentDownloader.reset_clr}")
        print(
            f" {TorrentDownloader.magenta}RESOLUTION: {elem['movie_type']}{TorrentDownloader.reset_clr}")

    @staticmethod
    def search1377x_request(name_s):
        '''Request to the torrent site'''
        # sending get request and saving the response as response object
        max_elem = TorrentDownloader.torrent_pages
        for elem in range(1, max_elem + 1):
            url = f"https://www.1377x.to/search/{name_s}/{elem}/"
            req = requests.get(url=url, params={})
            if elem == 1:
                parsed_html = BeautifulSoup(req.text, "html.parser")
                if len(parsed_html.findAll('tr')) == 1:
                    print(
                        f"{TorrentDownloader.red}No torrent founded for \"{name_s}\"{TorrentDownloader.reset_clr}")
                    print("")
                    sys.exit(0)
            TorrentDownloader.search1337x(req)

    def avvia_ricerca(self):
        '''avvio ricerca GUI'''
        from PySide2.QtWidgets import QTableWidget, QPushButton, QApplication
        # reset to allow multiple search
        TorrentDownloader.json_torrent = '''
    {
        "Torrent": [
            ]
    }
    '''
        name_input = TorrentDownloader.titolo.text()
        TorrentDownloader.search1377x_request(str(name_input))
        # populate tabel
        torrent = 1
        data = json.loads(TorrentDownloader.json_torrent)
        TorrentDownloader.tabella = TorrentDownloader.window.findChild(
            QTableWidget, "tableWidget")
        TorrentDownloader.seleziona = TorrentDownloader.window.findChild(
            QPushButton, "select")
        TorrentDownloader.seleziona.clicked.connect(
            lambda: TorrentDownloader.get_selected_element(self))
        TorrentDownloader.tabella.clearContents()
        TorrentDownloader.tabella.setRowCount(0)
        QApplication.processEvents()
        for elem in data['Torrent']:
            pos = torrent - 1
            TorrentDownloader.tabella.insertRow(pos)
            TorrentDownloader.print_elem_gui(elem, pos)
            torrent += 1

    def get_selected_element(self):
        # GUI (first time only)
        TorrentDownloader.autoadd = TorrentDownloader.add.isChecked()
        # get multiple selection
        items = TorrentDownloader.tabella.selectedItems()
        for item in items:
            # only 1 item in a row
            if item.column() == 1:
                # start download with each selected row
                TorrentDownloader.get_magnet(self, item.row())
        return

    def choose(self):
        '''Select torrent'''
        # write _____________
        print(f'{TorrentDownloader.underscore}'+' ' *
              120+f'{TorrentDownloader.reset_clr}\n')
        found = 0
        while found == 0:
            item_dict = json.loads(TorrentDownloader.json_torrent)
            try:
                number = int(input('Choose torrent: '))
            except ValueError:
                print(
                    f"\n{TorrentDownloader.red}Not Valid!!{TorrentDownloader.reset_clr}\n")
                TorrentDownloader.choose(self)
            found = 1
            item_dict = json.loads(TorrentDownloader.json_torrent)[
                'Torrent'][number-1]
            TorrentDownloader.print_elem(item_dict)
            conf = ""
            while conf.lower() not in ['y', 'n']:
                conf = input("\ny to confirm, n to repeat: ")
            if conf.lower() == 'n':
                found = 0
            elif (conf.lower() == 'y'):
                number -= 1  # indice di un array
                # controllo che number sia una scelta valida:
                item_dict = json.loads(TorrentDownloader.json_torrent)
                if number < len(item_dict['Torrent']) and number >= 0:
                    TorrentDownloader.get_magnet(self, number)
                else:
                    print(
                        f"{TorrentDownloader.red}Not Valid{TorrentDownloader.reset_clr}")

    def get_magnet(self, position):
        '''function to get magnet link'''
        item_dict = json.loads(TorrentDownloader.json_torrent)[
            'Torrent'][position]
        req = requests.get(url=item_dict['link'], params={})
        # extracting data in json format
        parsed_html = BeautifulSoup(req.text, "html.parser")
        magnet_link = ''
        for parsed in parsed_html.findAll('li'):
            for elem in parsed.find_all('a', href=True):
                # not put verify here 'cause href can be magnet or other things
                if ('magnet' in elem['href']):
                    magnet_link = elem['href']
                    break  # stop se trovo un "magnet"
        # check if it's a fake magnet link
        if (not TorrentDownloader.verify_magnet_link(magnet_link)):
            print(
                f"{TorrentDownloader.red}Not a valid Magnet{TorrentDownloader.reset_clr}")
            sys.exit(0)
        else:
            TorrentDownloader.start(self, magnet_link)

    def start(self, magnet_link):
        '''start gui search'''
        if (TorrentDownloader.autoadd):
            done = True
            # avvio il magnet
            if sys.platform.startswith('linux'):
                try:
                    subprocess.Popen(['xdg-open', magnet_link])
                except subprocess.CalledProcessError:
                    done = False
            elif sys.platform.startswith('win32'):
                done = os.startfile(magnet_link)  # check false
            elif sys.platform.startswith('cygwin'):
                done = os.startfile(magnet_link)  # check false
            elif sys.platform.startswith('darwin'):
                try:
                    subprocess.Popen(['open', magnet_link])
                except subprocess.CalledProcessError:
                    done = False
            else:
                try:
                    subprocess.Popen(['xdg-open', magnet_link])
                except subprocess.CalledProcessError:
                    done = False
            if done:
                print(
                    f'\n{TorrentDownloader.green}Success{TorrentDownloader.reset_clr}')
            else:  # ho incontrato un errore
                if (self.gui):
                    from PySide2.QtWidgets import QTextEdit
                    text = TorrentDownloader.magnet_window.findChild(
                        QTextEdit, "magnet_link")
                    text.insertPlainText(magnet_link)
                    TorrentDownloader.magnet_window.show()
                else:
                    print(
                        f"\nMagnet:{TorrentDownloader.red}{magnet_link}{TorrentDownloader.reset_clr}\n")
        else:
            if (self.gui):
                from PySide2.QtWidgets import QTextEdit
                text = TorrentDownloader.magnet_window.findChild(
                    QTextEdit, "magnet_link")
                text.insertPlainText(magnet_link)
                TorrentDownloader.magnet_window.show()
            else:
                print(
                    f"\nMagnet:{TorrentDownloader.red}{magnet_link}{TorrentDownloader.reset_clr}\n")

    def __init__(self, gui):
        self.gui = gui
        self_wrapp = self
        signal.signal(signal.SIGTERM, TorrentDownloader.sig_handler)
        signal.signal(signal.SIGINT, TorrentDownloader.sig_handler)
        if(self.gui):
            # GUI import
            from PySide2.QtWidgets import QCheckBox, QPushButton, QLineEdit
            from PySide2.QtCore import QObject

            class KeyPressEater(QObject):
                '''event filter '''

                def eventFilter(self, widget, event):
                    from PySide2.QtCore import QEvent, Qt
                    if (event.type() == QEvent.KeyPress):
                        key = event.key()
                        if key == Qt.Key_Return:
                            TorrentDownloader.avvia_ricerca(self_wrapp)
                    return False
            TorrentDownloader.filtro = KeyPressEater()
            TorrentDownloader.titolo = TorrentDownloader.window.findChild(
                QLineEdit, "titolo")
            TorrentDownloader.cerca = TorrentDownloader.window.findChild(
                QPushButton, "cerca")
            TorrentDownloader.add = TorrentDownloader.window.findChild(
                QCheckBox, "add")
            TorrentDownloader.cerca.clicked.connect(
                lambda: TorrentDownloader.avvia_ricerca(self_wrapp))
            TorrentDownloader.titolo.installEventFilter(
                TorrentDownloader.filtro)
        else:
            if len(sys.argv) == 1:
                name_input = input('Nome Film da cercare: ').strip()
            else:
                name_input = sys.argv[1]
                for elem in sys.argv[2:]:
                    name_input += '%20' + elem
            TorrentDownloader.search1377x_request(str(name_input))
            # print list
            torrent = 1
            data = json.loads(TorrentDownloader.json_torrent)
            for elem in data['Torrent']:
                # write _____________
                print(f'{TorrentDownloader.underscore}' + ' ' *
                      120 + f'{TorrentDownloader.reset_clr}\n')
                print(
                    f" {TorrentDownloader.bold_text}Torrent {torrent} :{TorrentDownloader.reset_clr}")
                TorrentDownloader.print_elem(elem)
                torrent += 1
            TorrentDownloader.choose(self)

    @classmethod
    def sig_handler(cls, _signo, _stack_frame):
        '''Catch ctr+c signal'''
        print("\n")
        sys.exit(0)
