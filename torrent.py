'''Simple parsing  script to obtain magnet link of a torrent'''
import json
import os
import signal
import subprocess
import sys
import requests
from bs4 import BeautifulSoup


class TorrentDownloader():
    '''Torrent magnet link'''
    # config
    torrent_pages = 3
    QNAP = 0
    add_torrent_command = ['transmission-remote -n transmission:transmission -a',
                           '/share/CACHEDEV1_DATA/.qpkg/QTransmission/bin/transmission-remote -n qnap:qnap -a'][QNAP]
    autoadd = True
    # end config

    json_torrent = '''
    {
        "Torrent": [
            ]
    }
    '''

    def search1337x(self, req, name_s):
        '''Parsing function'''
        # extracting data in json format
        parsed_html = BeautifulSoup(req.text, "html.parser")
        if len(parsed_html.findAll('td', attrs={'class': 'coll-1 name'})) == 0:
            print("No torrent founded for \"" + name_s+"\"")
            print("")
            sys.exit(1)
        # Get Torrent Size
        for parsed in parsed_html.findAll('tr'):
            size = "0 "
            seed = ""
            leech = ""
            for elem in parsed.findAll('td', attrs={'class': 'coll-2'}):
                seed = (elem.text)
            for elem in parsed.findAll('td', attrs={'class': 'coll-3'}):
                leech = (elem.text)
            for elem in parsed.findAll('td', attrs={'class': 'coll-4'}):
                size = (elem.text)
            title = ""
            link = ""
            for elem in parsed.findAll('td', attrs={'class': 'coll-1'}):
                for tit in elem.find_all('a', href=True):
                    link = tit['href']
                    title = tit.text
            if len(title) > 1:
                temp = {
                    'name': title,
                    'size': float(size.split(" ")[0]),
                    'seed': seed,
                    'leech': leech,
                    'type': size.split(" ")[1],
                    'link': 'https://www.1377x.to' + link
                }

                data = json.loads(self.json_torrent)
                t_list = data['Torrent']
                t_list.append(temp)
                self.json_torrent = json.dumps(data, indent=4)
                sorted_obj = dict(data)
                sorted_obj['Torrent'] = sorted(
                    data['Torrent'], key=lambda pos: pos['size'], reverse=True)
                self.json_torrent = json.dumps(sorted_obj, indent=4)

    def search1377x_request(self, name_s):
        '''Request to site'''
        # sending get request and saving the response as response object
        max_elem = self.torrent_pages
        for elem in range(1, max_elem + 1):
            url = "https://www.1377x.to/search/" + name_s + "/" + "%d" % elem + "/"
            req = requests.get(url=url, params={})
            self.search1337x(req, name_s)

    def print_list(self):
        '''Print function'''
        torrent = 1
        data = json.loads(self.json_torrent)
        for elem in data['Torrent']:
            print('---------')
            print('Torrent %d' % (torrent) + ":")
            print("\x1b[36mTITLE: " + elem['name'] + "\x1b[0m")
            print("\x1b[32mDIM: " + str(elem['size']) +
                  " " + elem['type'] + "\x1b[0m")
            print("\x1b[33mSEED: " + elem['seed'] + "\x1b[0m")
            print("\x1b[37mLEECH: " + elem['leech'] + "\x1b[0m")
            torrent += 1

    def select(self):
        '''Select torrent'''
        print('---------')
        found = 0
        while found == 0:
            item_dict = json.loads(self.json_torrent)
            try:
                number = int(input('Choose torrent:'))
            except ValueError:
                print("")
                print("\x1b[31;1mNot Valid!!\x1b[0m")
                self.select()
            number -= 1  # indice di un array
            if number < len(item_dict['Torrent']):
                item_dict = json.loads(self.json_torrent)[
                    'Torrent'][number]
                url = item_dict['link']
                req = requests.get(url=url, params={})
                # extracting data in json format
                pastebin_url = req.text
                html = pastebin_url
                parsed_html = BeautifulSoup(html, "html.parser")
                magnet_link = ''
                for parsed in parsed_html.findAll('li'):
                    for elem in parsed.find_all('a', href=True):
                        if 'magnet' in elem['href']:
                            magnet_link = elem['href']
                print("----------------------------------")
                found = 1
                print("\x1b[36mTITLE: " + item_dict['name'] + "\x1b[0m")
                print("\x1b[32mDIM: " + str(item_dict['size']) +
                      " " + item_dict['type'] + "\x1b[0m")
                print("\x1b[33mSEED: " + item_dict['seed'] + "\x1b[0m")
                print("\x1b[37mLEECH: " + item_dict['leech'] + "\x1b[0m")
                conf = input("y to confirm, n to repeat: ")
                print("----------------------------------")
                if conf in ('n', 'N'):
                    found = 0
                elif(self.autoadd and (conf in ('y', 'Y'))):
                    command = self.add_torrent_command + ' \'' + \
                        magnet_link + '\' >&- 2> add_torrent_output.txt'
                    subprocess.call(command)
                    with open('add_torrent_output.txt', 'r') as file:
                        if 'command not found' not in file.read():
                            print('\x1b[32mSuccess\x1b[0m' + '\x1b[0m')
                        else:
                            print("\x1b[31;1mError, command not found\x1b[0m")
                            print("----------------------------------")
                            print('Magnet:\x1b[31;1m ' +
                                  magnet_link + "\x1b[0m")
                else:
                    print("Magnet: \x1b[31;1m" + magnet_link + "\x1b[0m")
            else:
                print("")
                print("\x1b[31;1mOut of range\x1b[0m")

    def __init__(self):
        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)
        if len(sys.argv) == 1:
            name_input = input('Nome Film da cercare:').strip()
        else:
            name_input = sys.argv[1]
            for elem in sys.argv[2:]:
                name_input += ' ' + elem
        name = str(name_input).replace(' ', '%20')
        self.search1377x_request(name)
        self.print_list()
        self.select()

    @classmethod
    def sig_handler(cls, _signo, _stack_frame):
        '''Get ctr+c signal'''
        print("\n")
        sys.exit(0)


if __name__ == "__main__":
    x = TorrentDownloader()
