# Storm Wolf (Jeff Falberg)
# ID compiler for packs

import urllib.request as urr
import urllib.error
from urllib.error import HTTPError
import sys
import re

sys.argv = ["ID compiler.py", "input.txt"]
input_file = sys.argv[1]

database = open(input_file, "r")
listoflines = database.readlines()
database.close()
listofdata = []

for line in listoflines :
    line = line.replace(' ','_').replace('#','')
    line = line.rstrip()
    wiki_url = "http://yugioh.wikia.com/wiki/" + line
    page = urr.urlopen(wiki_url)
    if page.getcode() == 200 :
        sourcepage = page.read()
        source = sourcepage.decode("utf-8")    
        regexName = re.compile(r"data\">\n(.*)</td>")
        patternName = re.compile(regexName)
        card_name = re.findall(patternName, source)[0]
        card_name = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', card_name)
        card_name = re.sub('&amp;', '&', card_name)
        card_name = re.sub('&#160;', ' ', card_name)
        regexID = re.compile(r"(\d\d\d\d\d\d\d\d)<\/a><\/td><\/tr>")
        patternID = re.compile(regexID)
        change_id = str(int(re.findall(patternID, source)[0]))
        line = line.rstrip()
        print(change_id+': 2, //'+card_name)
