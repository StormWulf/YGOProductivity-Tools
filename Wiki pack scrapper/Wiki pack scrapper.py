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
                #regexTCG = re.compile(r"French name</th>.*?\d\">(.*?) </td", re.DOTALL)
                patternTCG = re.compile(regexTCG)
                TCG_date = re.findall(patternTCG, source)[0]
                query.write('update dates set tcg_date="'+TCG_date+'" where id='+line+';')
                #OCG date
                regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
                patternOCG = re.compile(regexOCG)
                OCG_date = re.findall(patternOCG, source)[0]
                query.write('update dates set ocg_date="'+OCG_date+'" where id='+line+';')
            except IndexError :
                wiki_url = "http://yugioh.wikia.com/wiki/" + quote(name) + "_(card)"
                page = urr.urlopen(wiki_url)
                if page.getcode() == 200 :
                    sourcepage = page.read()
                    source = sourcepage.decode("utf-8")
                    regexName = re.compile(r"data\">\n(.*)</td>")
                    patternName = re.compile(regexName)
                    try :
                        #TCG date
                        regexTCG = re.compile(r"North American English</caption>.*?\d\">(.*?) </td", re.DOTALL)
                        patternTCG = re.compile(regexTCG)
                        TCG_date = re.findall(patternTCG, source)[0]
                        query.write('update dates set tcg_date="'+TCG_date+'" where id='+line+';')
                        #OCG date
                        regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
                        patternOCG = re.compile(regexOCG)
                        OCG_date = re.findall(patternOCG, source)[0]
                        query.write('update dates set ocg_date="'+OCG_date+'" where id='+line+';')
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
            regexTCG = re.compile(r"English</caption>.*?\d\">(.*?) </td", re.DOTALL)
            patternTCG = re.compile(regexTCG)
            TCG_date = re.findall(patternTCG, source)[0]
            query.write('update dates set tcg_date="'+TCG_date+'" where id='+line+';')
            #OCG date
            regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
            patternOCG = re.compile(regexOCG)
            OCG_date = re.findall(patternOCG, source)[0]
            query.write('update dates set ocg_date="'+OCG_date+'" where id='+line+';')
            #continue
            #except urllib.error.HTTPError as err :
                #pass
            #continue
        else :
            raise
query.close()
fail.close()
