# importing the requests library 
import requests 
from bs4 import BeautifulSoup


name = raw_input('Nome Film da cercare:').strip()
name = str(name).replace(' ' , '+')
print (name)
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
parsed_html = BeautifulSoup(html)

title_box = parsed_html.findAll('td', attrs={'class':'coll-1 name'})
x = 0

for dim in parsed_html.findAll('td', attrs={'class':'coll-4'}):
    GB.append(dim.text)
    x+=1
x = 0
print("")
print("")
print("")
for parsed in parsed_html.findAll('td', attrs={'class':'coll-1 name'}):
    print(x)
    for a in parsed.find_all('a', href=True):
        string_res = (a.text)
        if(string_res != ""):
            line = GB[x]
            dim = line
            print(string_res)
            print("DIM: " + split_and_keep(dim, 'B')[0])
        if('torrent' in a['href']):
            result.append('https://www.1377x.to' + a['href'])
    x += 1
print('---------')
print('---------')
print('---------')
print('---------')
print('---------')
print('---------')
number = input('Ins number result:')
print(result[number])