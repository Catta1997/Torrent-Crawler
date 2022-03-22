# importing the requests library
import requests
import os
import sys
from bs4 import BeautifulSoup
import json
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


def split_and_keep(s, sep):
    if not s:
        return ['']
    p = chr(ord(max(s))+1)
    return s.replace(sep, sep+p).split(p)


def search1337x(r, name_s):
    global torrent
    global name_torrent
    global json_torrent
    # extracting data in json format
    pastebin_url = r.text
    #print("The pastebin URL is:%s"%pastebin_url)
    html = pastebin_url
    parsed_html = BeautifulSoup(html, "html.parser")
    title_box = parsed_html.findAll('td', attrs={'class': 'coll-1 name'})
    #page_link = parsed_html.findAll('div', attrs={'class':'pagination'})
    x = 0
    if len(title_box) == 0:
        print("No torrent founded for \"" + name_s+"\"")
        print("")
        exit(1)
    # Get Torrent Size
    for dim in parsed_html.findAll('td', attrs={'class': 'coll-4'}):
        GB.append(dim.text)
        x += 1
    x = 0
    # Get torrent info
    for parsed in title_box:
        for a in parsed.find_all('a', href=True):
            string_res = (a.text)
            if(len(string_res) > 1):
                line = GB[x]
                dim = line
                name_torrent.append(string_res)
                temp = {
                    'name': string_res,
                    # split_and_keep(dim, ' ')[0],
                    'size': float(dim.split(" ")[0]),
                    'type': split_and_keep(dim, ' ')[-1],
                    'link': 'https://www.1377x.to' + a['href']
                }
                data = json.loads(json_torrent)
                t_list = data['Torrent']
                # print(t_list)
                t_list.append(temp)
                json_torrent = json.dumps(data, indent=4)
                sorted_obj = dict(data)
                sorted_obj['Torrent'] = sorted(
                    data['Torrent'], key=lambda x: x['size'], reverse=True)
                json_torrent = json.dumps(sorted_obj, indent=4)
        x += 1
    x = 0
    item_dict = json.loads(json_torrent)
    print(len(item_dict['Torrent']))


def search1377x_request(name_s):
    global torrent_pages
    # sending get request and saving the response as response object
    max = torrent_pages
    for c in range(1, max + 1):
        URL = "https://www.1377x.to/search/" + name_s + "/" + "%d" % c + "/"
        r = requests.get(url=URL, params={})
        search1337x(r, name_s)


def sort():
    global torrent

    global name_torrent
    global json_torrent
   # bubbleSort(GB_ord,name_torrent,result,GB_ord_ext)
    # bubbleSort2(MB_ord,MB_ord_ext)
    x = 0

    data = json.loads(json_torrent)
    for elem in data['Torrent']:
        print('---------')
        print('Torrent %d' % (torrent) + ":")
        print("\x1b[36mTITLE: " + elem['name'] + "\x1b[0m")
        print("\x1b[32mDIM: " + str(elem['size']) +
              " " + elem['type'] + "\x1b[0m")
        torrent += 1
        x += 1


def select():
    print('---------')
    print("")
    found = 0
    while(found == 0):
        print("")
        print("")
        item_dict = json.loads(json_torrent)
        number = int(input('Choose torrent:'))
        number -= 1  # indice di un array
        if(number < len(item_dict['Torrent'])):
            item_dict = json.loads(json_torrent)['Torrent'][number]
            URL = item_dict['link']
            r = requests.get(url=URL, params={})
            # extracting data in json format
            pastebin_url = r.text
            html = pastebin_url
            parsed_html = BeautifulSoup(html, "html.parser")
            #print("The pastebin URL is:%s"%pastebin_url)
            magnet_link = ''
            #title_box = parsed_html.findAll('li')
            for parsed in parsed_html.findAll('li'):
                for a in parsed.find_all('a', href=True):
                    if('magnet' in a['href']):
                        magnet_link = a['href']
            print("")
            found = 1
            print("\x1b[36mTITLE: " + item_dict['name'] + "\x1b[0m")
            print("\x1b[32mDIM: " + str(item_dict['size']) +
                  " " + item_dict['type'] + "\x1b[0m")
            conf = input("y to confirm, n to repeat: ")
            print("")
            if(conf == 'n' or conf == 'N'):
                found = 0
            elif(autoadd and (conf == 'y' or conf == 'Y')):
                command = add_torrent_command + ' \'' + \
                    magnet_link + '\' >&- 2> add_torrent_output.txt'
                os.system(command)
                with open('add_torrent_output.txt', 'r') as f:
                    if 'command not found' not in f.read():
                        print('\x1b[32mSuccess\x1b[0m' + '\x1b[0m')
                    else:
                        print("\x1b[31;1mError, command not found\x1b[0m")
                        print("")
                        print('Magnet:\x1b[31;1m ' + magnet_link + "\x1b[0m")
            else:
                print("Magnet: \x1b[31;1m" + magnet_link + "\x1b[0m")
                print("")
                print("")
            print("")
        else:
            print("")
            print("\x1b[31;1mOut of range\x1b[0m")


def main():
    if len(sys.argv) == 1:
        name_input = input('Nome Film da cercare:').strip()
    else:
        name_input = sys.argv[1]
        for x in sys.argv[2:]:
            name_input += ' ' + x
    name = str(name_input).replace(' ', '%20')
    search1377x_request(name)
    sort()
    select()


if __name__ == "__main__":
    main()
