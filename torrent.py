# importing the requests library 
import requests 
from bs4 import BeautifulSoup
# api-endpoint 

name = raw_input('Nome Film da cercare:').strip()
name = str(name).replace(' ' , '+')
print (name)
resulst = list()
GB = list()
result = ['']
URL = "https://www.1377x.to/category-search/" + name + "/Movies/1/"


# location given here 
# defining a params dict for the parameters to be sent to the API 
PARAMS = {}


def split_and_keep(s, sep):
    if not s: return [''] # consistent with string.split()
    # Find replacement character that is not used in string
    # i.e. just use the highest available character plus one
    # Note: This fails if ord(max(s)) = 0x10FFFF (ValueError)
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



# extracting latitude, longitude and formatted address 
# of the first matching location 


# printing the output 

