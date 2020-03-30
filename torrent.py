# importing the requests library 
import requests
from bs4 import BeautifulSoup


name = raw_input('Nome Film da cercare:').strip()
name = str(name).replace(' ' , '%20')
resulst = list()
GB = list()
result = ['']
URL = "https://www.1377x.to/category-search/" + name + "/Movies/1/"
PARAMS = {}


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
print("")
print("Torrnets:")
print("")
for dim in parsed_html.findAll('td', attrs={'class':'coll-4'}):
    GB.append(dim.text)
    x+=1
x = 0
for parsed in parsed_html.findAll('td', attrs={'class':'coll-1 name'}):
    print('---------')
    print('Torrent %d' %x + ":")
    for a in parsed.find_all('a', href=True):
        string_res = (a.text)
        if(string_res != ""):
            line = GB[x]
            dim = line

#        echo -e "\t\x1b[32mAttempt $i: Success\x1b[0m"
 #       Success=$((Success + 1))
#    else
#        echo -e "\t\x1b[31mAttempt $i: Fail\x1b[0m"#
#


            print("\x1b[36m" + string_res + "\x1b[0m")
            print("\x1b[32mDIM: " + split_and_keep(dim, 'B')[0]+ "\x1b[0m" )
        if('torrent' in a['href']):
            result.append('https://www.1377x.to' + a['href'])
    x += 1
print('---------')
print("")
number = input('Ins number result:')
print("")
print("Magnet: \x1b[31;1m" + result[number]+ "\x1b[0m")
print("")