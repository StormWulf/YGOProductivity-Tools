# Storm Wolf (Jeff Falberg)
# Wiki card scrapper for card names and descriptions
import urllib.request as urr
import urllib.error
from urllib.parse import quote
from urllib.error import HTTPError
import sys
import re
import sqlite3

sys.argv = ["Wiki pack scrapper.py", "input.txt", "output.sql", "failed.txt"]
input_file = sys.argv[1]
output_file = sys.argv[2]
failed_file = sys.argv[3]
#Edit this path if used by a different machine
conn = sqlite3.connect( "C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGOPro-Salvation-Server\\http\\ygopro\\databases\\0-en-OCGTCG.cdb" )
curs = conn.cursor()

database = open(input_file, "r")
query = open(output_file, "w", encoding='utf-8')
fail = open(failed_file, "w", encoding='utf-8')
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
        print('Processing: '+name)
        page = urr.urlopen(wiki_url)
        if page.getcode() == 200 :
            sourcepage = page.read()
            source = sourcepage.decode("utf-8")
            try:
                #TCG date
                regexTCG = re.compile(r"North American English</caption>.*?\d\">(.*?) </td", re.DOTALL)
                patternTCG = re.compile(regexTCG)
                TCG_date = re.findall(patternTCG, source)[0]
                regexTCGpackid = re.compile(r"North American English</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                patternTCGpackid = re.compile(regexTCGpackid)
                tcg_pack_id = re.findall(patternTCGpackid, source)[0]
                query.write('INSERT OR REPLACE INTO "tcg" VALUES ("'+line+'","'+tcg_pack_id+'","","","'+TCG_date+'");')
                #OCG date
                regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
                patternOCG = re.compile(regexOCG)
                OCG_date = re.findall(patternOCG, source)[0]
                regexOCGpackid = re.compile(r"Japanese</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                patternOCGpackid = re.compile(regexOCGpackid)
                OCG_pack_id = re.findall(patternOCGpackid, source)[0]
                query.write('INSERT OR REPLACE INTO "ocg" VALUES ("'+line+'","'+OCG_pack_id+'","","","'+OCG_date+'");')
            except IndexError :
                wiki_url = "http://yugioh.wikia.com/wiki/" + quote(name) + "_(card)"
                page = urr.urlopen(wiki_url)
                if page.getcode() == 200 :
                    sourcepage = page.read()
                    source = sourcepage.decode("utf-8")
                    try :
                        #TCG date
                        regexTCG = re.compile(r"North American English</caption>.*?\d\">(.*?) </td", re.DOTALL)
                        patternTCG = re.compile(regexTCG)
                        TCG_date = re.findall(patternTCG, source)[0]                        
                        regexTCGpackid = re.compile(r"North American English</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                        patternTCGpackid = re.compile(regexTCGpackid)
                        tcg_pack_id = re.findall(patternTCGpackid, source)[0]
                        query.write('INSERT OR REPLACE INTO "tcg" VALUES ("'+line+'","'+tcg_pack_id+'","","","'+TCG_date+'");')
                        #OCG date
                        regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
                        patternOCG = re.compile(regexOCG)
                        OCG_date = re.findall(patternOCG, source)[0]
                        regexOCGpackid = re.compile(r"Japanese</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                        patternOCGpackid = re.compile(regexOCGpackid)
                        OCG_pack_id = re.findall(patternOCGpackid, source)[0]
                        query.write('INSERT OR REPLACE INTO "ocg" VALUES ("'+line+'","'+OCG_pack_id+'","","","'+OCG_date+'");')
                    except IndexError :
                        print(name+" failed due to IndexError")
                        fail.write(name+" failed due to IndexError\n")
                        pass
                    continue
    except urllib.error.HTTPError as err :
        if err.code == 404 :
           # try:
               # wiki_url = "http://yugioh.wikia.com/wiki/" + line
               # page = urr.urlopen(wiki_url)
##            print(name+" failed due to HTTPError")
##            fail.write(name+" failed due to HTTPError\n")
            try:
                regexTCG = re.compile(r"English</caption>.*?\d\">(.*?) </td", re.DOTALL)
                patternTCG = re.compile(regexTCG)
                TCG_date = re.findall(patternTCG, source)[0]
                regexTCGpackid = re.compile(r"English</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                patternTCGpackid = re.compile(regexTCGpackid)
                tcg_pack_id = re.findall(patternTCGpackid, source)[0]
                query.write('INSERT OR REPLACE INTO "tcg" VALUES ("'+line+'","'+tcg_pack_id+'","","","'+TCG_date+'");')
            except IndexError :
                pass
            try: 
                #OCG date
                regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
                patternOCG = re.compile(regexOCG)
                OCG_date = re.findall(patternOCG, source)[0]
                regexOCGpackid = re.compile(r"Japanese</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                patternOCGpackid = re.compile(regexOCGpackid)
                OCG_pack_id = re.findall(patternOCGpackid, source)[0]
                query.write('INSERT OR REPLACE INTO "ocg" VALUES ("'+line+'","'+OCG_pack_id+'","","","'+OCG_date+'");')
            except IndexError :
                pass
        else :
            raise
query.close()
fail.close()
