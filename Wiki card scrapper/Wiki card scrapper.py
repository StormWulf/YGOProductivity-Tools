# Storm Wolf (Jeff Falberg)
# Wiki card scrapper for card names and descriptions

import urllib.request as urr
import urllib.error
from urllib.error import HTTPError
import sys
import re

sys.argv = ["Wiki card scrapper.py", "input.txt", "output.sql"]
input_file = sys.argv[1]
output_file = sys.argv[2]


database = open(input_file, "r")
query = open(output_file, "w", encoding='utf-8')
listoflines = database.readlines()
database.close()
listofdata = []
prescript = {'VJMP-JP': 200,
             'WJMP-JP': 203,
             'SJMP-JP': 204,
             '20AP-JP': 213,
             'PP19-JP': 214,
             'VB19-JP': 215,
             'RATE-EN': 911,
             'MACR-JP': 912,
             'SR04-JP': 304
             }

for line in listoflines :
    old_line = line
    while(len(line)<9) :
        line = '0' + line
    if len(line)>9 :
        pack = int(line[3:6])
        number = line[6:9]
        pack = list(prescript.keys())[list(prescript.values()).index(pack)]
        line = str(pack) + number
    wiki_url = "http://yugioh.wikia.com/wiki/" + line
    try:
        page = urr.urlopen(wiki_url)
        if page.getcode() == 200 :
            sourcepage = page.read()
            source = sourcepage.decode("utf-8")
            regexName = re.compile(r"data\">\n(.*)</td>")
            patternName = re.compile(regexName)
            try :
                card_name = re.findall(patternName, source)[0]
                card_name = re.sub('"', '""', card_name)
                card_name = re.sub('&amp;', '&', card_name)
                #regexText = re.compile(r";;\">\n(.*[^<\/td>]*\.)*<\/td>", re.S)
                regexText = re.compile(r";;\">\n(.*)")
                patternText = re.compile(regexText)
                card_text = re.findall(patternText, source)[0]
                card_text = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', card_text)
                card_text = re.sub('"', '""', card_text)
                card_text = re.sub('<dd>', '\n', card_text)
                card_text = re.sub('</dd>', '\n', card_text)
                card_text = re.sub('<dl>', '\n', card_text)
                card_text = re.sub('</dl>', '\n', card_text)
                card_text = re.sub('<br />', '\n', card_text)
                card_text = re.sub('&amp;', '&', card_text)
                print('Processing: '+line)
                #print('update texts set name="'+card_name+'", desc="'+card_text+'" where id='+line+';')
                query.write('update texts set name="'+card_name+'", desc="'+card_text+'" where id='+old_line+';')
            except IndexError :
                pass
            continue
    except urllib.error.HTTPError as err :
        if err.code == 404 :
            continue
        else :
            raise
query.close()
