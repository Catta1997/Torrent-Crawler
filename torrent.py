'''Simple parsing  script to obtain magnet link of a torrent'''
import json
import signal
import subprocess
import sys
import requests
from PySide2 import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *
from bs4 import BeautifulSoup


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
    GUI = True
    torrent_pages = 3
    QNAP = 0
    cmd = '/share/CACHEDEV1_DATA/.qpkg/QTransmission/bin/transmission-remote' if QNAP else 'transmission-remote'
    user = 'qnap:qnap' if QNAP else 'transmission:transmission'

    cmd_command = [f"{cmd}", '-n', f"{user}", '-a']
    autoadd = True
    # end config

    json_torrent = '''
    {
        "Torrent": [
            ]
    }
    '''

    def search1337x(self, req):
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
                TorrentDownloader.json_torrent = json.dumps(sorted_obj, indent=4)

    def search1377x_request(self, name_s):
        '''Request to site'''
        # sending get request and saving the response as response object
        max_elem = TorrentDownloader.torrent_pages
        for elem in range(1, max_elem + 1):
            url = f"https://www.1377x.to/search/{name_s}/{elem}/"
            req = requests.get(url=url, params={})
            if elem == 1:
                parsed_html = BeautifulSoup(req.text, "html.parser")
                if len(parsed_html.findAll('tr')) == 1:
                    print(f"{TorrentDownloader.red}No torrent founded for \"{name_s}\"{TorrentDownloader.TorrentDownloader.reset_clr}")
                    print("")
                    sys.exit(0)
            TorrentDownloader.search1337x(self,req)

    def print_elem_gui(self, elem):
        '''Print torrent element'''
        title_t = elem['name']
        min_pos = 0
        max_pos = 95
        TorrentDownloader.tabella.setItem(0,0,QTableWidgetItem(title_t[min_pos:max_pos]))
        TorrentDownloader.tabella.setItem(0,1,QTableWidgetItem(f"{str(elem['size'])} {elem['type']}"))
        TorrentDownloader.tabella.setItem(0,2,QTableWidgetItem(f"{elem['seed']}"))
        TorrentDownloader.tabella.setItem(0,3,QTableWidgetItem(f"{elem['leech']}"))
        TorrentDownloader.tabella.setItem(0,4,QTableWidgetItem(f"{elem['movie_type']}"))
        TorrentDownloader.tabella.setItem(0,5,QTableWidgetItem(f"{elem['date']}"))
        TorrentDownloader.tabella.resizeColumnsToContents()

    def print_elem(self, elem):
        '''Print torrent element'''
        title_t = elem['name']
        min_pos = 0
        max_pos = 95
        print(f" {TorrentDownloader.cyan}TITLE: {title_t[min_pos:max_pos]} {TorrentDownloader.reset_clr}")
        while max_pos < len(title_t):
            min_pos += 95
            max_pos += 95
            print(f" {TorrentDownloader.cyan}       {title_t[min_pos:max_pos]} {TorrentDownloader.reset_clr}")
        print(f" {TorrentDownloader.red}DATE: {elem['date']} {TorrentDownloader.reset_clr}")
        print(f" {TorrentDownloader.green}DIM: {str(elem['size'])} {elem['type']} {TorrentDownloader.reset_clr}")
        print(f" {TorrentDownloader.yellow}SEED: {elem['seed']} {TorrentDownloader.reset_clr}")
        print(f" {TorrentDownloader.white}LEECH: {elem['leech']} {TorrentDownloader.reset_clr}")
        print(f" {TorrentDownloader.magenta}RESOLUTION: {elem['movie_type']} {TorrentDownloader.reset_clr}")

    def select_gui(self):
        torr = TorrentDownloader.tabella.currentRow()
        item_dict = json.loads(TorrentDownloader.json_torrent)[
                    'Torrent'][torr-1]
        req = requests.get(url=item_dict['link'], params={})
        # extracting data in json format
        parsed_html = BeautifulSoup(req.text, "html.parser")
        magnet_link = ''
        for parsed in parsed_html.findAll('li'):
            for elem in parsed.find_all('a', href=True):
                if 'magnet' in elem['href']:
                    magnet_link = elem['href']
        print(magnet_link)

    def avvia_ricerca(self):
        TorrentDownloader.json_torrent = '''
    {
        "Torrent": [
            ]
    }
    '''
        name_input = TorrentDownloader.titolo.text()
        TorrentDownloader.search1377x_request(self, str(name_input))
        # print list
        torrent = 1
        data = json.loads(TorrentDownloader.json_torrent)
        TorrentDownloader.tabella = TorrentDownloader.window.findChild(QTableWidget,"tableWidget")
        TorrentDownloader.seleziona = TorrentDownloader.window.findChild(QPushButton, "select")
        TorrentDownloader.seleziona.clicked.connect(TorrentDownloader.select_gui)
        #table_view->horizontalHeader()->setStretchLastSection(true);
        TorrentDownloader.tabella.clearContents()
        TorrentDownloader.tabella.setRowCount(0)
        QApplication.processEvents()
        for elem in data['Torrent']:
            TorrentDownloader.tabella.insertRow(0)
            TorrentDownloader.print_elem_gui(self, elem)
            torrent += 1

    def select(self):
        '''Select torrent'''
        # write _____________
        print(f'{TorrentDownloader.underscore}'+' '*120+f'{TorrentDownloader.reset_clr}\n')
        found = 0
        while found == 0:
            item_dict = json.loads(TorrentDownloader.json_torrent)
            try:
                number = int(input('Choose torrent: '))
            except ValueError:
                print(f"\n{TorrentDownloader.red}Not Valid!!{TorrentDownloader.reset_clr}\n")
                TorrentDownloader.select()
            number -= 1  # indice di un array
            if number < len(item_dict['Torrent']) and number >= 0:
                item_dict = json.loads(TorrentDownloader.json_torrent)[
                    'Torrent'][number]
                req = requests.get(url=item_dict['link'], params={})
                # extracting data in json format
                parsed_html = BeautifulSoup(req.text, "html.parser")
                magnet_link = ''
                for parsed in parsed_html.findAll('li'):
                    for elem in parsed.find_all('a', href=True):
                        if 'magnet' in elem['href']:
                            magnet_link = elem['href']
                found = 1
                TorrentDownloader.print_elem(item_dict)
                conf = ""
                while conf.lower() not in ['y', 'n']:
                    conf = input("\ny to confirm, n to repeat: ")
                if conf.lower() == 'n':
                    found = 0
                elif (TorrentDownloader.autoadd and conf.lower() == 'y'):
                    TorrentDownloader.cmd_command.append(f"\"{magnet_link}\"")
                    try:
                        subprocess.check_call(TorrentDownloader.cmd_command)
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        print(f"\n{TorrentDownloader.red}Error, command not found{TorrentDownloader.reset_clr}")
                        print(f"\nMagnet:{TorrentDownloader.red} {magnet_link} {TorrentDownloader.reset_clr}\n")
                        sys.exit(0)
                    print(f'\n{TorrentDownloader.green}Success{TorrentDownloader.reset_clr}')
                else:
                    print(f"\nMagnet:{TorrentDownloader.red} {magnet_link} {TorrentDownloader.reset_clr}\n")
            else:
                print(f"{TorrentDownloader.red}Not Valid{TorrentDownloader.reset_clr}")

    def __init__(self):
        signal.signal(signal.SIGTERM, TorrentDownloader.sig_handler)
        signal.signal(signal.SIGINT, TorrentDownloader.sig_handler)
        if(TorrentDownloader.GUI):
            TorrentDownloader.titolo = TorrentDownloader.window.findChild(QLineEdit,"titolo")
            TorrentDownloader.cerca = TorrentDownloader.window.findChild(QPushButton,"cerca")
            TorrentDownloader.cerca.clicked.connect(TorrentDownloader.avvia_ricerca)
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
                print(f'{TorrentDownloader.underscore}' + ' '*120 + f'{TorrentDownloader.reset_clr}\n')
                print(f" {TorrentDownloader.bold_text}Torrent {torrent} :{TorrentDownloader.reset_clr}")
                TorrentDownloader.print_elem(elem)
                torrent += 1
            TorrentDownloader.select()

    @classmethod
    def sig_handler(cls, _signo, _stack_frame):
        '''Get ctr+c signal'''
        print("\n")
        sys.exit(0)

if __name__ == "__main__":
    x = TorrentDownloader()
