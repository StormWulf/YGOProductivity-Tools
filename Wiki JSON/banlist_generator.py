# Storm Wolf (Jeff Falberg)
# JS Banlist Generator

import urllib.request as urr
import urllib.error
from urllib.parse import quote
import sys
import re

sys.argv = ["banlist_generator.py", "banlist_input.txt", "banlist.txt"]
input_file = sys.argv[1]
banlist_file = sys.argv[2]

database = open(input_file, "r", encoding='utf-8')
ban_list = open(banlist_file, "w", encoding='utf-8')
listoflines = database.readlines()
database.close()
listofdata = []

for line in listoflines:
    name = line.split(';')[0]
    limit = line.split(';')[1]
    new_name = name.replace(' ', '_').title().replace('_A_','_a_').replace('_An_','_an_').replace('_Of_','_of_').replace('_The_','_the_').replace('_Is_','_is_').replace('_From_','_from_')
    wiki_url = "http://yugioh.wikia.com/wiki/" + quote(new_name).replace('%27S','%27s').replace('%E2%80%90','-')
    print('Processing: '+wiki_url)
    page = urr.urlopen(wiki_url)
    if page.getcode() == 200:
        sourcepage = page.read()
        source = sourcepage.decode("utf-8")
        regexID = re.compile(r"(\d\d\d\d\d\d\d\d)<\/a><\/td><\/tr>")
        patternID = re.compile(regexID)
        card_ID = int(re.findall(patternID, source)[0])
        ban_list.write(str(card_ID).rstrip()+': '+limit.rstrip()+', // '+name.rstrip()+'\n')
ban_list.close()
