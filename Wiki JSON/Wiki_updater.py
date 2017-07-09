# Storm Wolf (Jeff Falberg)
# Wiki card scrapper for card inserts

import urllib.request as urr
import urllib.error
from urllib.parse import quote
import sys
import re
import json
from datetime import datetime

sys.argv = ["Wiki_updater.py", "input.txt", "failed.txt"]
input_file = sys.argv[1]
failed_file = sys.argv[2]

database = open(input_file, "r")
fail = open(failed_file, "w", encoding='utf-8')
listoflines = database.readlines()
database.close()
listofdata = []

print('--Starting Wiki picture inserts.py--')
for line in listoflines:
    json_filename = 'C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGO_DB\\http\\json\\' + str(int(line)) + '.json'
    json_filename = re.sub('\n', '', json_filename)
    with open(json_filename, encoding='utf8') as data_file:
        card_json = json.load(data_file)
    card_name = card_json["name"].replace(' ', '_').replace('#', '')
    wiki_url = "http://yugioh.wikia.com/wiki/" + quote(card_name)
    print('Processing: '+wiki_url)
    try:
        page = urr.urlopen(wiki_url)
        if page.getcode() == 200:
            sourcepage = page.read()
            source = sourcepage.decode("utf-8")
            ## CARD NAME
            try:
                regexName = re.compile(r"data\">\n(.*)</td>")
                patternName = re.compile(regexName)
                card_name = re.findall(patternName, source)[0]
            except IndexError:
                wiki_url = "http://yugioh.wikia.com/wiki/" + quote(card_name) + '_(card)'
                page = urr.urlopen(wiki_url)
                if page.getcode() == 200:
                    sourcepage = page.read()
                    source = sourcepage.decode("utf-8")
                    regexName = re.compile(r"data\">\n(.*)</td>")
                    patternName = re.compile(regexName)
                    card_name = re.findall(patternName, source)[0]                
            card_name = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', card_name)
            card_name = re.sub('&amp;', '&', card_name)
            card_name = re.sub('&#160;', ' ', card_name)
            card_json["name"] = card_name
            ## CARD DESC
            regexText = re.compile(r";;\">\n(.*?)<\/td>", re.DOTALL)
            patternText = re.compile(regexText)
            try:
                card_text = re.findall(patternText, source)[0]
                card_text = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', card_text)
                card_text = re.sub('<dd>', '\n', card_text)
                card_text = re.sub('</dd>', '\n', card_text)
                card_text = re.sub('<dl>', '\n', card_text)
                card_text = re.sub('</dl>', '\n', card_text)
                card_text = re.sub('<br />', '\n', card_text)
                card_text = re.sub('&amp;', '&', card_text)
                card_text = re.sub('&#160;', ' ', card_text)
                card_text = re.sub('\n Pendulum Effect\n\n ', 'Pendulum Effect\n', card_text)
                card_text = re.sub('\n\n\n Monster Effect\n\n ', 'Monster Effect\n', card_text)
                card_json["desc"] = card_text
                try:
                    regexLink = re.compile(r"Link Arrows(.*?)<tr", re.DOTALL)
                    patternLink = re.compile(regexLink)
                    links = re.findall(patternLink, source)[0]
                    links = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', links)
                    links = re.sub('\n', '', links)
                    link_marker = re.sub(' , ', ' ', links)
                    link_marker = re.sub('Top-Left', '[🡴]', link_marker)
                    link_marker = re.sub('Top-Right', '[🡵]', link_marker)
                    link_marker = re.sub('Bottom-Left', '[🡷]', link_marker)
                    link_marker = re.sub('Bottom-Right', '[🡶]', link_marker)
                    link_marker = re.sub('Top', '[🡱]', link_marker)
                    link_marker = re.sub('Bottom', '[🡳]', link_marker)
                    link_marker = re.sub('Left', '[🡰]', link_marker)
                    link_marker = re.sub('Right', '[🡲]', link_marker)
                    link_marker = re.sub(r'\s$', '', link_marker)
                    if '[' in link_marker:
                        card_json["desc"] = 'Link Arrows: ' + link_marker + '\n\n' + card_text
                        links = []
                        if '[🡴]' in link_marker:
                            links.append(0)
                        if '[🡱]' in link_marker:
                            links.append(1)
                        if '[🡵]' in link_marker:
                            links.append(2)
                        if '[🡰]' in link_marker:
                            links.append(3)
                        if '[🡲]' in link_marker:
                            links.append(4)
                        if '[🡷]' in link_marker:
                            links.append(5)
                        if '[🡳]' in link_marker:
                            links.append(6)
                        if '[🡶]' in link_marker:
                            links.append(7)
                        card_json["links"] = links
                except IndexError:
                    pass
            except IndexError:
                pass
            # OCG PACK NAME
            try:
                regexOCGpackid = re.compile(r"Japanese</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                patternOCGpackid = re.compile(regexOCGpackid)
                OCG_pack_id = re.findall(patternOCGpackid, source)[0]
                OCG_pack = OCG_pack_id.split('-')[0]
                card_json["ocg"]["pack"] = OCG_pack
                card_json["ocg"]["pack_id"] = OCG_pack_id
            except IndexError:
                try:
                    regexOCGpackid = re.compile(r"Japanese</caption>.*?\)\">(.*?)</a>", re.DOTALL)
                    patternOCGpackid = re.compile(regexOCGpackid)
                    OCG_pack_id = re.findall(patternOCGpackid, source)[0]
                    OCG_pack = OCG_pack_id.split('-')[0]
                    card_json["ocg"]["pack"] = OCG_pack
                    card_json["ocg"]["pack_id"] = OCG_pack_id
                except IndexError:
                    pass
            # OCG PACK DATE
            try:
                regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
                patternOCG = re.compile(regexOCG)
                OCG_date = re.findall(patternOCG, source)[0]
                card_json["ocg"]["date"] = OCG_date
                card_json["ocg"]["pack"] = OCG_pack_id.split('-')[0]
            except IndexError:
                pass
            # TCG PACK
            try:
                try:
                    regexTCG = re.compile(r"North American English</caption>.*?\d\">(.*?) </td", re.DOTALL)
                    patternTCG = re.compile(regexTCG)
                    TCG_date_na = re.findall(patternTCG, source)[0]
                    try:
                        datetime_TCG_na = datetime.strptime(TCG_date_na, '%Y-%m-%d')
                    except ValueError:
                        datetime_TCG_na = datetime.strptime('3000-12-12', '%Y-%m-%d')
                    regexTCGpackid = re.compile(r"North American English</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                    patternTCGpackid = re.compile(regexTCGpackid)
                    tcg_pack_id_na = re.findall(patternTCGpackid, source)[0]
                except IndexError:
                    datetime_TCG_na = datetime.strptime('3000-12-12', '%Y-%m-%d')
                    TCG_date_na = ''
                    tcg_pack_id_na = ''
                regexTCG = re.compile(r">English</caption>.*?\d\">(.*?) </td", re.DOTALL)
                patternTCG = re.compile(regexTCG)
                TCG_date_w = re.findall(patternTCG, source)[0]
                try:
                    datetime_TCG_w = datetime.strptime(TCG_date_w, '%Y-%m-%d')
                except ValueError:
                    datetime_TCG_w = datetime.strptime('3000-12-12', '%Y-%m-%d')
                try:
                    regexTCGpackid = re.compile(r"English</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                    patternTCGpackid = re.compile(regexTCGpackid)
                    tcg_pack_id_w = re.findall(patternTCGpackid, source)[0]
                except IndexError:
                    regexTCGpackid = re.compile(r"English</caption>.*?\)\">(.*?)</a>", re.DOTALL)
                    patternTCG = re.compile(regexTCGpackid)
                    TCG_date_w = re.findall(patternTCG, source)[0]
                if datetime_TCG_na > datetime_TCG_w :
                    TCG_date = TCG_date_w
                    tcg_pack_id = tcg_pack_id_w
                else :
                    TCG_date = TCG_date_na
                    tcg_pack_id = tcg_pack_id_na
                tcg_pack_name = tcg_pack_id.split('-')[0]
                if len(TCG_date) > 15 or len(TCG_date)<1 :
                    fail.write(card_json["name"]+" failed due to an issue with Wiki page")
                else :
                    card_json["tcg"]["date"] = TCG_date
                    card_json["tcg"]["pack"] = tcg_pack_name
                    card_json["tcg"]["pack_id"] = tcg_pack_id
            except IndexError:
                pass
            # CARD PICTURE
            try:
                regexPicture = re.compile(r"cardtable-cardimage\".*?<a href=\"(.*?)cb=", re.DOTALL)
                patternPicture = re.compile(regexPicture)
                card_picture = re.findall(patternPicture, source)[0]
                card_json["picture"] = card_picture
            except IndexError:
                fail.write('Picture not found for: '+card_json["name"]+'\n')
            with open(json_filename, 'w', encoding='utf8') as outfile:
                json.dump(card_json, outfile,ensure_ascii=False, indent=4, separators=(',', ': '))
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print(card_json["name"]+" failed due to HTTPError")
            fail.write(card_json["name"]+" failed due to HTTPError\n")
            continue
        else:
            raise

fail.close()
