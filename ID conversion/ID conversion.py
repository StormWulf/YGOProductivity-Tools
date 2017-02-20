# Storm Wolf (Jeff Falberg)
# ID conversion for prerelease -> official cards
import urllib.request as urr
import urllib.error
from urllib.parse import quote
from urllib.error import HTTPError
import sys
import re
import sqlite3

sys.argv = ["ID conversion.py", "input.txt", "output.sql"]
input_file = sys.argv[1]
output_file = sys.argv[2]

#Edit this path if used by a different machine
conn = sqlite3.connect( "C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGOPro-Salvation-Server\\http\\ygopro\\databases\\0-en-OCGTCG.cdb" )
curs = conn.cursor()

database = open(input_file, "r")
query = open(output_file, "w", encoding='utf-8')
listoflines = database.readlines()
database.close()
listofdata = []

for line in listoflines :
    name = curs.execute("SELECT name FROM texts WHERE ID=?", (line ,))
    name = name.fetchone()
    name = str(name)
    name = name[2:-3]
    name = name.replace(' ','_').replace('#','').replace('-','-')
    #print(name)
    wiki_url = "http://yugioh.wikia.com/wiki/" + quote(name)
    try:
        page = urr.urlopen(wiki_url)
        if page.getcode() == 200 :
            sourcepage = page.read()
            source = sourcepage.decode("utf-8")   
            regexID = re.compile(r"(\d\d\d\d\d\d\d\d)<\/a><\/td><\/tr>")
            patternID = re.compile(regexID)
            try :
                change_id = re.findall(patternID, source)[0]
                #print(line,end="")
                line = line.rstrip()
                print(line+': '+change_id)
                query.write('update datas set id='+change_id+' where id='+line+';\n')
                query.write('update texts set id='+change_id+' where id='+line+';\n')
            except IndexError :
                wiki_url = "http://yugioh.wikia.com/wiki/" + quote(name) + "_(card)"
                page = urr.urlopen(wiki_url)
                if page.getcode() == 200 :
                    sourcepage = page.read()
                    source = sourcepage.decode("utf-8")   
                    regexID = re.compile(r"(\d\d\d\d\d\d\d\d)<\/a><\/td><\/tr>")
                    patternID = re.compile(regexID)
                    try :
                        change_id = re.findall(patternID, source)[0]
                        #print(line,end="")
                        line = line.rstrip()
                        print(line+': '+change_id)
                        query.write('update datas set id='+change_id+' where id='+line+';\n')
                        query.write('update texts set id='+change_id+' where id='+line+';\n')
                    except IndexError :
                        print(name+" failed due to IndexError")
                        pass
                    continue
    except urllib.error.HTTPError as err :
        if err.code == 404 :
           # try:
               # wiki_url = "http://yugioh.wikia.com/wiki/" + line
               # page = urr.urlopen(wiki_url)
            print(name+" failed due to HTTPError")
            #fail.write(name+" failed due to HTTPError\n")
            continue
            #except urllib.error.HTTPError as err :
                #pass
            #continue
        else :
            raise                    
query.close()
