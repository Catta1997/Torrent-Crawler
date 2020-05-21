# importing the requests library 
import requests,os,subprocess
import sys
from bs4 import BeautifulSoup

#config
torrent_pages = 3
add_torrent_command = '/share/CACHEDEV1_DATA/.qpkg/QTransmission/bin/transmission-remote -n qnap:qnap -a'
#aria2c -d ~/Downloads --seed-time=0 "magnet:?xt=urn:btih:248D0A1CD08284299DE78D5C1ED359BB46717D8C"
autoadd = True
#end config


resulst = list()
GB = list()
result = ['']
torrent = 1
GB_ord_ext = list()
GB_ord = list()
MB_ord_ext = list()
MB_ord = list()
name_torrent = list()
def bubbleSort(arr,arr2,arr3,arr4):
    n = len(arr)
def bubbleSort2(arr,arr2):
    n = len(arr)
def split_and_keep(s, sep):
    if not s: return ['']
    p=chr(ord(max(s))+1)
    return s.replace(sep, sep+p).split(p)
def search1337x(r,name_s):
    global torrent
    global GB_ord_ext
    global GB_ord
    global MB_ord_ext
    global MB_ord
    global name_torrent
    # extracting data in json format 
    pastebin_url = r.text 
    #print("The pastebin URL is:%s"%pastebin_url) 
    html = pastebin_url
    parsed_html = BeautifulSoup(html,"html.parser")
    title_box = parsed_html.findAll('td', attrs={'class':'coll-1 name'})
    #page_link = parsed_html.findAll('div', attrs={'class':'pagination'})
    x = 0
    if len(title_box)== 0:
        print("No torrent founded for \"" + name_s+"\"")
        print("")
        exit(1)
    #Get Torrent Size
    for dim in parsed_html.findAll('td', attrs={'class':'coll-4'}):
        GB.append(dim.text)
        x+=1
    x = 0
    #Get torrent name
    for parsed in title_box:
        for a in parsed.find_all('a', href=True):
            string_res = (a.text)
            if(string_res != ""):
                line = GB[x]
                dim = line
            if('torrent' in a['href']):
                result.append('https://www.1377x.to' + a['href'])
        x += 1
    x = 0
    #Dim
    for parsed in title_box:
        for a in parsed.find_all('a', href=True):
            string_res = (a.text)
            if(string_res != ""):
                line = GB[x]
                dim = line
                dims = split_and_keep(dim, 'B')[0]
                name_torrent.append(string_res)
                if "GB" in dims:
                    dims = dims[: -3]
                    GB_ord.append(dims)
                    GB_ord_ext.append(split_and_keep(dim, 'B')[0])
                if "MB" in dims:
                    dims = dims[: -3]
                    MB_ord.append(dims)
                    MB_ord_ext.append(split_and_keep(dim, 'B')[0])
        x += 1
def search1377x_request(name_s):
    global torrent_pages
    # sending get request and saving the response as response object 
    max = torrent_pages
    for c in range(1,max + 1):
        URL = "https://www.1377x.to/search/" + name_s + "/" + "%d"%c + "/"
        r = requests.get(url = URL, params = {}) 
        search1337x(r,name_s)
def sort():
    global torrent
    global GB_ord_ext
    global GB_ord
    global MB_ord_ext
    global MB_ord
    global name_torrent
    bubbleSort(GB_ord,name_torrent,result,GB_ord_ext)
    bubbleSort2(MB_ord,MB_ord_ext)
    x = 0
    dim_tot = MB_ord_ext + GB_ord_ext
    for elem in dim_tot:
        print('---------')
        print('Torrent %d' %(torrent) + ":")
        print("\x1b[36mTITLE: " + name_torrent[x] + "\x1b[0m")
        print("\x1b[32mDIM: " + dim_tot[x]+ "\x1b[0m" )
        torrent+=1
        x+=1
def select():
    print('---------')
    print("")
    found = 0
    while(found == 0):
        print("")
        print("")
        number = int(input('Choose torrent:'))
        if(number < len(result)):
            URL = result[number]
            r = requests.get(url = URL, params = {}) 
            # extracting data in json format
            pastebin_url = r.text
            html = pastebin_url
            parsed_html = BeautifulSoup(html,"html.parser")
            #print("The pastebin URL is:%s"%pastebin_url) 
            magnet_link = ''
            dim_tot = MB_ord_ext + GB_ord_ext
            #title_box = parsed_html.findAll('li')
            for parsed in parsed_html.findAll('li'):
                for a in parsed.find_all('a', href=True):
                    if('magnet' in a['href']):
                        magnet_link = a['href']
            print("")
            found = 1
            print("\x1b[36mTITLE: " + name_torrent[number-1] + "\x1b[0m")
            print("\x1b[32mDIM: " + dim_tot[number-1]+ "\x1b[0m" )
            print('Magnet:\x1b[31;1m ' + magnet_link + "\x1b[0m")
            conf = input("y to confirm, n to repeat: ")
            print("")
            if(conf == 'n' or conf == 'N'):
                found = 0
            elif(autoadd and (conf == 'y' or conf == 'Y')):
                command = add_torrent_command + ' \"' + magnet_link + '\" >&- 2> add_torrent_output.txt'
                os.system(command)
                with open('add_torrent_output.txt', 'r') as f:
                    if 'command not found' not in f.read():
                        print('\x1b[32mSuccess\x1b[0m' + '\x1b[0m')
                    else:
                        print("\x1b[31;1mError, command not found\x1b[0m")
                        print("")
                        print('Magnet:\x1b[31;1m ' + magnet_link + "\x1b[0m")
            else :
                print("Magnet: \x1b[31;1m" + magnet_link + "\x1b[0m")
                print("")
                print("")
            print("")
        else :
            print("")
            print("\x1b[31;1mOut of range\x1b[0m")
def main():
    if len (sys.argv) == 1 :
        name_input = input('Nome Film da cercare:').strip()
    else :
        name_input = sys.argv[1]
        for x in sys.argv[2:]:
            name_input += ' ' + x
    name = str(name_input).replace(' ' , '%20')
    search1377x_request(name)
    sort()
    select()
if __name__ == "__main__":
    main()