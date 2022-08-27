'''Simple parsing  script to obtain magnet link of a torrent'''
import json
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
                    print(f"\x1b[31;1mNo torrent founded for \"{name_s}\"\x1b[0m")
                    print("")
                    sys.exit(0)
            self.search1337x(req)

    def print_list(self):
        '''Print function'''
        torrent = 1
        data = json.loads(self.json_torrent)
        for elem in data['Torrent']:
            print('\033[4m')
            print(' '*120)
            print('\x1b[0m')
            print(f" \033[1mTorrent {torrent} :\x1b[0m")
            self.print_elem(elem)
            torrent += 1

    def print_elem(self,elem):
        '''Print torrent element'''
        title_t = elem['name']
        min = 0
        max = 95
        print(f" \x1b[36mTITLE: {title_t[min:max]} \x1b[0m")
        while max < len(title_t):
            min += 95
            max += 95
            print(f" \x1b[36m       {title_t[min:max]} \x1b[0m")
        print(f" \033[91mDATE: {elem['date']} \x1b[0m")
        print(f" \x1b[32mDIM: {str(elem['size'])} {elem['type']} \x1b[0m")
        print(f" \x1b[33mSEED: {elem['seed']} \x1b[0m")
        print(f" \x1b[37mLEECH: {elem['leech']} \x1b[0m")
        print(f" \x1b[35mRESOLUTION: {elem['movie_type']} \x1b[0m")

    def select(self):
        '''Select torrent'''
        print('\033[4m')
        print(' '*120)
        print('\x1b[0m')
        found = 0
        while found == 0:
            item_dict = json.loads(self.json_torrent)
            try:
                number = int(input('Choose torrent: '))
            except ValueError:
                print("")
                print("\x1b[31;1mNot Valid!!\x1b[0m")
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
                print('\033[4m')
                print(' '*120)
                print('\x1b[0m')
                found = 1
                self.print_elem(item_dict)
                conf = input("y to confirm, n to repeat: ")
                print('\033[4m')
                print(' '*120)
                print('\x1b[0m')
                if conf in ('n', 'N'):
                    found = 0
                elif(self.autoadd and (conf in ('y', 'Y'))):
                    self.cmd_command.append(f"\"{magnet_link}\"")
                    try:
                        subprocess.check_call(self.cmd_command)
                    except (subprocess.CalledProcessError, FileNotFoundError):
                        print("\x1b[31;1mError, command not found\x1b[0m")
                        print('\033[4m')
                        print(' '*120)
                        print('\x1b[0m')
                        print(f"Magnet:\x1b[31;1m {magnet_link} \x1b[0m")
                        sys.exit(0)
                    print('\x1b[32mSuccess\x1b[0m')
                else:
                    print(f"Magnet:\x1b[31;1m {magnet_link} \x1b[0m")
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
