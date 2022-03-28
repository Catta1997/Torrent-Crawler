'''Simple parsing  script to obtain magnet link of a torrent'''
import json
import os
import signal
import sys
import requests
from bs4 import BeautifulSoup


class TorrentDownloader():
    '''Torrent magnet link'''
    # config
    torrent_pages = 3
    add_torrent_command = 'transmission-remote -n transmission:transmission -a'
    autoadd = True
    # end config

    resulst = list()
    GB = list()
    result = ['']
    torrent = 1
    name_torrent = list()
    json_torrent = '''
    {
        "Torrent": [
            ]
    }
    '''

    @classmethod
    def split_and_keep(cls, name, sep):
        '''Renove GB/MB from string'''
        if not name:
            return ['']
        pos = chr(ord(max(name))+1)
        return name.replace(sep, sep+pos).split(pos)

    def search1337x(self, req, name_s):
        '''Parsing function'''
        # extracting data in json format
        parsed_html = BeautifulSoup(req.text, "html.parser")
        title_box = parsed_html.findAll('td', attrs={'class': 'coll-1 name'})
        if len(title_box) == 0:
            print("No torrent founded for \"" + name_s+"\"")
            print("")
            sys.exit(1)
        # Get Torrent Size
        for dim in parsed_html.findAll('td', attrs={'class': 'coll-4'}):
            self.GB.append(dim.text)
        # Get torrent info
        pos = 0
        for parsed in title_box:
            for elem in parsed.find_all('a', href=True):
                string_res = (elem.text)
                if len(string_res) > 1:
                    line = self.GB[pos]
                    dim = line
                    self.name_torrent.append(string_res)
                    temp = {
                        'name': string_res,
                        # split_and_keep(dim, ' ')[0],
                        'size': float(dim.split(" ")[0]),
                        'type': self.split_and_keep(dim, ' ')[-1],
                        'link': 'https://www.1377x.to' + elem['href']
                    }
                    data = json.loads(self.json_torrent)
                    t_list = data['Torrent']
                    # print(t_list)
                    t_list.append(temp)
                    self.json_torrent = json.dumps(data, indent=4)
                    sorted_obj = dict(data)
                    sorted_obj['Torrent'] = sorted(
                        data['Torrent'], key=lambda pos: pos['size'], reverse=True)
                    self.json_torrent = json.dumps(sorted_obj, indent=4)
            pos += 1
        pos = 0
        #item_dict = json.loads(TorrentDownloader.json_torrent)

    def search1377x_request(self, name_s):
        '''Request to site'''
        # sending get request and saving the response as response object
        max_elem = self.torrent_pages
        for elem in range(1, max_elem + 1):
            url = "https://www.1377x.to/search/" + name_s + "/" + "%d" % elem + "/"
            req = requests.get(url=url, params={})
            self.search1337x(req, name_s)

    def sort(self):
        '''Print function'''
        #x = 0
        torrent = 1
        data = json.loads(self.json_torrent)
        for elem in data['Torrent']:
            print('---------')
            print('Torrent %d' % (torrent) + ":")
            print("\x1b[36mTITLE: " + elem['name'] + "\x1b[0m")
            print("\x1b[32mDIM: " + str(elem['size']) +
                  " " + elem['type'] + "\x1b[0m")
            torrent += 1
           # x += 1

    def select(self):
        '''Select torrent'''
        print('---------')
        print("")
        found = 0
        while found == 0:
            print("")
            print("")
            item_dict = json.loads(self.json_torrent)
            number = int(input('Choose torrent:'))
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
                #print("The pastebin URL is:%s"%pastebin_url)
                magnet_link = ''
                #title_box = parsed_html.findAll('li')
                for parsed in parsed_html.findAll('li'):
                    for elem in parsed.find_all('a', href=True):
                        if 'magnet' in elem['href']:
                            magnet_link = elem['href']
                print("")
                found = 1
                print("\x1b[36mTITLE: " + item_dict['name'] + "\x1b[0m")
                print("\x1b[32mDIM: " + str(item_dict['size']) +
                      " " + item_dict['type'] + "\x1b[0m")
                conf = input("y to confirm, n to repeat: ")
                print("")
                if conf in ('n', 'N'):
                    found = 0
                elif(self.autoadd and (conf in ('n', 'N'))):
                    command = self.add_torrent_command + ' \'' + \
                        magnet_link + '\' >&- 2> add_torrent_output.txt'
                    os.system(command)
                    with open('add_torrent_output.txt', 'r') as file:
                        if 'command not found' not in file.read():
                            print('\x1b[32mSuccess\x1b[0m' + '\x1b[0m')
                        else:
                            print("\x1b[31;1mError, command not found\x1b[0m")
                            print("")
                            print('Magnet:\x1b[31;1m ' +
                                  magnet_link + "\x1b[0m")
                else:
                    print("Magnet: \x1b[31;1m" + magnet_link + "\x1b[0m")
                    print("")
                    print("")
                print("")
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
        self.sort()
        self.select()

    @classmethod
    def sig_handler(cls, _signo, _stack_frame):
        '''Get ctr+c signal'''
        print("\n")
        sys.exit(0)


if __name__ == "__main__":
    x = TorrentDownloader()
