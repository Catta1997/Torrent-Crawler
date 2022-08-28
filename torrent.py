'''Simple parsing  script to obtain magnet link of a torrent'''
import json
import signal
import subprocess
import sys
import requests
from bs4 import BeautifulSoup


class TorrentDownloader():
    '''Torrent magnet link'''
    #text format
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
            #create a json with torrent info
            if len(title) > 1:
                temp = {
                    'name': title,
                    'size': float(size.split(" ")[0]),
                    'seed': seed,
                    'leech': leech,
                    'movie_type': type_torr,
                    'type': size.split(" ")[1],
                    'date' : date_t,
                    'link': 'https://www.1377x.to' + link
                }
                data = json.loads(self.json_torrent)
                data['Torrent'].append(temp)
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
            url = f"https://www.1377x.to/search/{name_s}/{elem}/"
            req = requests.get(url=url, params={})
            if elem == 1:
                parsed_html = BeautifulSoup(req.text, "html.parser")
                if len(parsed_html.findAll('tr')) == 1:
                    print(f"{self.red}No torrent founded for \"{name_s}\"{self.reset_clr}")
                    print("")
                    sys.exit(0)
            self.search1337x(req)

    def print_list(self):
        '''Print function'''
        torrent = 1
        data = json.loads(self.json_torrent)
        for elem in data['Torrent']:
            # write _____________
            print(f'{self.underscore}' + ' '*120 + f'{self.reset_clr}\n')
            print(f" {self.bold_text}Torrent {torrent} :{self.reset_clr}")
            self.print_elem(elem)
            torrent += 1

    def print_elem(self,elem):
        '''Print torrent element'''
        title_t = elem['name']
        min_pos= 0
        max_pos= 95
        print(f" {self.cyan}TITLE: {title_t[min_pos:max_pos]} {self.reset_clr}")
        while max_pos< len(title_t):
            min_pos+= 95
            max_pos+= 95
            print(f" {self.cyan}       {title_t[min_pos:max_pos]} {self.reset_clr}")
        print(f" {self.red}DATE: {elem['date']} {self.reset_clr}")
        print(f" {self.green}DIM: {str(elem['size'])} {elem['type']} {self.reset_clr}")
        print(f" {self.yellow}SEED: {elem['seed']} {self.reset_clr}")
        print(f" {self.white}LEECH: {elem['leech']} {self.reset_clr}")
        print(f" {self.magenta}RESOLUTION: {elem['movie_type']} {self.reset_clr}")

    def select(self):
        '''Select torrent'''
        # write _____________
        print(f'{self.underscore}'+' '*120+f'{self.reset_clr}\n')
        found = 0
        while found == 0:
            item_dict = json.loads(self.json_torrent)
            try:
                number = int(input('Choose torrent: '))
            except ValueError:
                print(f"\n{self.red}Not Valid!!{self.reset_clr}\n")
                self.select()
            number -= 1  # indice di un array
            if number < len(item_dict['Torrent']):
                item_dict = json.loads(self.json_torrent)[
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
                self.print_elem(item_dict)
                conf = ""
                while conf.lower() not in ['y','n']:
                    conf = input("\ny to confirm, n to repeat: ")
                if conf.lower() == 'n':
                    found = 0
                elif(self.autoadd and conf.lower() == 'y'):
                    self.cmd_command.append(f"\"{magnet_link}\"")
                    try:
                        subprocess.check_call(self.cmd_command)
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        print(f"\n{self.red}Error, command not found{self.reset_clr}")
                        print(f"\nMagnet:{self.red} {magnet_link} {self.reset_clr}\n")
                        sys.exit(0)
                    print(f'\n{self.green}Success{self.reset_clr}')
                else:
                    print(f"\nMagnet:{self.red} {magnet_link} {self.reset_clr}\n")
            else:
                print(f"\n{self.red}Out of range{self.reset_clr}")

    def __init__(self):
        signal.signal(signal.SIGTERM, self.sig_handler)
        signal.signal(signal.SIGINT, self.sig_handler)
        if len(sys.argv) == 1:
            name_input = input('Nome Film da cercare: ').strip()
        else:
            name_input = sys.argv[1]
            for elem in sys.argv[2:]:
                name_input += '%20' + elem
        self.search1377x_request(str(name_input))
        self.print_list()
        self.select()

    @classmethod
    def sig_handler(cls, _signo, _stack_frame):
        '''Get ctr+c signal'''
        print("\n")
        sys.exit(0)

if __name__ == "__main__":
    x = TorrentDownloader()
