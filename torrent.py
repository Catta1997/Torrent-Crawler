# importing the requests library 
import requests,os,subprocess
import sys
from bs4 import BeautifulSoup

if len (sys.argv) ==1 :
    name_input = raw_input('Nome Film da cercare:').strip()
else :
    name_input = sys.argv[1]
    for x in sys.argv[2:]:
        name_input += ' ' + x
name = str(name_input).replace(' ' , '%20')
resulst = list()
GB = list()
result = ['']
URL = "https://www.1377x.to/category-search/" + name + "/Movies/1/"
PARAMS = {}

add_torrent_command = 'addtorr'
autoadd = True

def bubbleSort(arr,arr2,arr3,arr4):
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                arr2[j], arr2[j+1] = arr2[j+1], arr2[j]
                arr3[j], arr3[j+1] = arr3[j+1], arr3[j]
                arr4[j], arr4[j+1] = arr4[j+1], arr4[j]


def bubbleSort2(arr,arr2):
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j+1] :
                arr[j], arr[j+1] = arr[j+1], arr[j]
                arr2[j], arr2[j+1] = arr2[j+1], arr2[j]
def split_and_keep(s, sep):
    if not s: return ['']
    p=chr(ord(max(s))+1)
    return s.replace(sep, sep+p).split(p)


# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
# extracting data in json format 
pastebin_url = r.text 
#print("The pastebin URL is:%s"%pastebin_url) 
html = pastebin_url
parsed_html = BeautifulSoup(html,"html.parser")

title_box = parsed_html.findAll('td', attrs={'class':'coll-1 name'})
x = 0
print("")
if len(title_box)== 0: 
    print("No torrent founded for \"" + name_input+"\"")
    print("")
    exit(1)
print("%d" %len(title_box) + " torrents founded for \"" + name_input +"\"")
print("")

GB_ord_ext = list()
GB_ord = list()
MB_ord_ext = list()
MB_ord = list()
name_torrent = list()

for dim in parsed_html.findAll('td', attrs={'class':'coll-4'}):
    GB.append(dim.text)
    x+=1

x = 0

for parsed in parsed_html.findAll('td', attrs={'class':'coll-1 name'}):
    #print('---------')
    #print('Torrent %d' %(x+1) + ":")
    for a in parsed.find_all('a', href=True):
        string_res = (a.text)
        if(string_res != ""):
            line = GB[x]
            dim = line
            #print("\x1b[36m" + string_res + "\x1b[0m")
            #print("\x1b[32mDIM: " + split_and_keep(dim, 'B')[0]+ "\x1b[0m" )
            #print(a['href'])
        if('torrent' in a['href']):
            result.append('https://www.1377x.to' + a['href'])
    x += 1
x = 0
for parsed in parsed_html.findAll('td', attrs={'class':'coll-1 name'}):
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
            bubbleSort(GB_ord,name_torrent,result,GB_ord_ext)
            bubbleSort2(MB_ord,MB_ord_ext)
    x += 1

x = 0
torrent = 1
for elem in MB_ord:
    print('---------')
    print('Torrent %d' %(torrent) + ":")
    print("\x1b[36m" + name_torrent[x] + "\x1b[0m")
    print("\x1b[32mDIM: " + MB_ord_ext[x]+ "\x1b[0m" )
    torrent+=1
    x+=1
x = 0
for elem in GB_ord:
    print('---------')
    print('Torrent %d' %(torrent) + ":")
    print("\x1b[36m" + name_torrent[x] + "\x1b[0m")
    print("\x1b[32mDIM: " + GB_ord_ext[x]+ "\x1b[0m" )
    torrent+=1
    x+=1

print('---------')
print("")
found = 0
while(found == 0):
    print("")
    print("")
    number = input('Choose torrent:')
    if(number < len(result)):

        URL = result[number]
        r = requests.get(url = URL, params = PARAMS) 
        # extracting data in json format 
        pastebin_url = r.text 
        #print("The pastebin URL is:%s"%pastebin_url) 
        html = pastebin_url
        parsed_html = BeautifulSoup(html,"html.parser")
        magnet_link = ''
        #title_box = parsed_html.findAll('li')
        for parsed in parsed_html.findAll('li'):
            for a in parsed.find_all('a', href=True):
                if('magnet' in a['href']):
                    magnet_link = a['href']


        print("")
        if(autoadd):
            command = add_torrent_command + ' \'' + magnet_link + '\' >&- 2> add_torrent_output.txt'
            os.system(command)
            with open('add_torrent_output.txt', 'r') as f:
                if 'command not found' not in f.read():
                    print('\x1b[32mSuccess\x1b[0m')
                else:
                    print("\x1b[31;1mError, command not found\x1b[0m")
        else :
            print("Magnet: \x1b[31;1m" + magnet_link + "\x1b[0m")
            print("")
            print("")
        found = 1
        print("")
    else : 
        print("")
        print("\x1b[31;1mOut of range\x1b[0m")