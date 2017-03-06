# Storm Wolf (Jeff Falberg)
# Wiki card scrapper for card names and descriptions

import urllib.request as urr
import urllib.error
from urllib.parse import quote
from urllib.error import HTTPError
import sys
import re
import sqlite3

sys.argv = ["Wiki card scrapper.py", "input.txt", "output.sql", "failed.txt"]
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
            regexName = re.compile(r"data\">\n(.*)</td>")
            patternName = re.compile(regexName)
            try :
                card_name = re.findall(patternName, source)[0]
                card_name = re.sub('"', '""', card_name)
                card_name = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', card_name)
                card_name = re.sub('&amp;', '&', card_name)
                card_name = re.sub('&#160;', ' ', card_name)
##                Uncomment for Link Monsters
##                regexLink = re.compile(r">Link Markers.*?</td>", re.DOTALL)
##                patternLink = re.compile(regexLink)
##                link_marker = re.findall(patternLink, source)[0]
##                link_marker = re.findall(patternLink, source)[0]
##                link_marker = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', link_marker)
##                link_marker = re.sub('"', '""', link_marker)
##                link_marker = re.sub('<dd>', '\n', link_marker)
##                link_marker = re.sub('</dd>', '\n', link_marker)
##                link_marker = re.sub('<dl>', '\n', link_marker)
##                link_marker = re.sub('</dl>', '\n', link_marker)
##                link_marker = re.sub('<br />', '\n', link_marker)
##                link_marker = re.sub('>Link Markers\n', 'Link Markers: ', link_marker)
##                link_marker = re.sub('&amp;', '&', link_marker)
##                link_marker = re.sub('&#160;', ' ', link_marker)
                regexText = re.compile(r";;\">\n(.*?)<\/td>", re.DOTALL)                
                #regexText = re.compile(r";;\">\n(.*)")
##                regexText = re.compile(r"<span lang=\"fr\".*?</table>", re.DOTALL)
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
                card_text = re.sub('&#160;', ' ', card_text)
                card_text = re.sub('\n Pendulum Effect\n\n ', 'Pendulum Effect\n', card_text)
                card_text = re.sub('\n\n\n Monster Effect\n\n ', 'Monster Effect\n', card_text)
                #print('Processing: '+line)
                #print('update texts set name="'+card_name+'", desc="'+card_text+'" where id='+line+';')
##                This this for Link Monsters
##                query.write('update texts set name="'+card_name+'", desc="'+link_marker+"\n\n"+card_text+'" where id='+line+';')
                query.write('update texts set name="'+card_name+'", desc="'+card_text+'" where id='+line+';')
            except IndexError :
                wiki_url = "http://yugioh.wikia.com/wiki/" + quote(name) + "_(card)"
                page = urr.urlopen(wiki_url)
                if page.getcode() == 200 :
                    sourcepage = page.read()
                    source = sourcepage.decode("utf-8")
                    regexName = re.compile(r"data\">\n(.*)</td>")
                    patternName = re.compile(regexName)
                    try :
                        card_name = re.findall(patternName, source)[0]
                        card_name = re.sub('"', '""', card_name)
                        card_name = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', card_name)
                        card_name = re.sub('&amp;', '&', card_name)
                        card_name = re.sub('&#160;', ' ', card_name)
                        #regexText = re.compile(r";;\">\n(.*[^<\/td>]*\.)*<\/td>", re.DOTALL)    
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
                        card_text = re.sub('&#160;', ' ', card_text)
                        query.write('update texts set name="'+card_name+'", desc="'+card_text+'" where id='+line+';')
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
            print(name+" failed due to HTTPError")
            fail.write(name+" failed due to HTTPError\n")
            continue
            #except urllib.error.HTTPError as err :
                #pass
            #continue
        else :
            raise
query.close()
fail.close()
