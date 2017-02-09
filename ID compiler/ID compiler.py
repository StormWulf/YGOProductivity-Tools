# Storm Wolf (Jeff Falberg)
# ID compiler for packs

import urllib.request as urr
import urllib.error
from urllib.error import HTTPError
import sys
import re
import sqlite3

sys.argv = ["ID compiler.py", "input.txt"]
input_file = sys.argv[1]

database = open(input_file, "r")
listoflines = database.readlines()
database.close()
listofdata = []

for line in listoflines :
    wiki_url = "http://yugioh.wikia.com/wiki/" + line
    try:
        page = urr.urlopen(wiki_url)
        if page.getcode() == 200 :
            sourcepage = page.read()
            source = sourcepage.decode("utf-8")    
            regexID = re.compile(r"(\d\d\d\d\d\d\d\d)<\/a><\/td><\/tr>")
            patternID = re.compile(regexID)
            try :
                change_id = re.findall(patternID, source)[0]
                line = line.rstrip()
                print(change_id)
            except IndexError :
                pass
                continue
    except urllib.error.HTTPError as err :
        if err.code == 404 :
            continue
        else :
            raise 
