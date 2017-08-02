# Storm Wolf (Jeff Falberg)
# Wiki card scrapper for card inserts

import urllib.request as urr
import urllib.error
from urllib.parse import quote
import sys
import re
import json

sys.argv = ["Wiki_scrapper.py", "input.txt", "failed.txt"]
input_file = sys.argv[1]
failed_file = sys.argv[2]

database = open(input_file, "r")
fail = open(failed_file, "w", encoding='utf-8')
listoflines = database.readlines()
database.close()
listofdata = []
setcode_math = []
prescript = {
		  'VJMP': 100200,
		  'WJMP': 100203,
		  'SJMP': 100204,
          'VF17': 100230,
		  'YA03': 100218,
          'COTD': 101001,
		  'CIBR': 101002,
		  'DBSW': 100419,
          'VP17': 100209,
          'SR05': 100305,
          'EP17': 100420
		  }
SETCODES = {}
with open('setcodes.txt','r', encoding='utf-8') as inf:
    SETCODES = eval(inf.read())
inf.close()
CARD_TYPES = {
		  'Normal Spell Card': 2,
		  'Normal Trap Card': 4,
		  'Normal_Monster': 17,
		  'Effect_Monster': 33,
		  'Ritual Spell Card': 130,
          'Ritual_Monster': 129,
          'Spirit_monster': 545,
		  'Union_monster': 1025,
          'Gemini_monster': 2081,
		  'Tuner_monster': 4129,
		  'Quick-Play Spell Card': 65538,
		  'Continuous Spell Card': 131074,
		  'Equip Spell Card': 262146,
		  'Field Spell Card': 524290,
		  'Continuous Trap Card': 131076,
		  'Counter Trap Card': 1048580,
		  'Flip_monster': 2097185,
		  'Fusion_Monster': 65,
		  'Synchro_Monster': 8193,
		  'Xyz_Monster': 8388609,
		  'Pendulum_Monster': 16777217,
		  'Link_Monster': 33554433,
		  }
RACE = {
		  'Warrior': 1,
		  'Spellcaster': 2,
		  'Fairy': 4,
		  'Fiend': 8,
		  'Zombie': 16,
		  'Machine': 32,
		  'Aqua': 64,
		  'Pyro': 128,
		  'Rock': 256,
		  'Winged_Beast': 512,
		  'Plant': 1024,
		  'Insect': 2048,
		  'Thunder': 4096,
		  'Dragon': 8192,
		  'Beast': 16384,
		  'Beast-Warrior': 32768,
		  'Dinosaur': 65536,
		  'Fish': 131072,
		  'Sea_Serpent': 262144,
		  'Reptile': 524288,
		  'Psychic': 1048576,
		  'Divine-Beast': 2097152,
		  'Creator God': 4194304,
		  'Wyrm': 8388608,
		  'Cyberse': 16777216
		  }
ATTRIBUTE = {
		  'EARTH': 1,
		  'WATER': 2,
		  'FIRE': 4,
		  'WIND': 8,
		  'LIGHT': 16,
		  'DARK': 32,
		  'DIVINE': 64
		  }
print('--Starting Wiki inserts.py--')
print('This does not generate alias values, assign it manually if a card needs it.\n\n')
for line in listoflines:
    name = line.replace(' ','_').replace('#','').replace('–','-')
    name = name.rstrip()
    wiki_url = "http://yugioh.wikia.com/wiki/" + quote(name)
    print('Processing: '+wiki_url)
    try:
        page = urr.urlopen(wiki_url)
        if page.getcode() == 200:
            sourcepage = page.read()
            source = sourcepage.decode("utf-8")
            card_json = {"ocg":{}, "tcg":{}}
            # OCG PACK INFO
            try:
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
                # TCG PACK INFO
                try:
                    regexOCGpackid = re.compile(r"English</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                    patternOCGpackid = re.compile(regexOCGpackid)
                    OCG_pack_id = re.findall(patternOCGpackid, source)[0]
                    OCG_pack = OCG_pack_id.split('-')[0]
                    card_json["tcg"]["pack"] = OCG_pack
                    card_json["tcg"]["pack_id"] = OCG_pack_id
                except IndexError:
                    try:
                        regexOCGpackid = re.compile(r"English</caption>.*?\)\">(.*?)</a>", re.DOTALL)
                        patternOCGpackid = re.compile(regexOCGpackid)
                        OCG_pack_id = re.findall(patternOCGpackid, source)[0]
                        OCG_pack = OCG_pack_id.split('-')[0]
                        card_json["tcg"]["pack"] = OCG_pack
                        card_json["tcg"]["pack_id"] = OCG_pack_id
                    except IndexError:
                        pass
            except IndexError:
                print(name+" failed because the card page doesn't exist yet")
                fail.write(name+" failed because the card page doesn't exist yet\n")
            # CARD ID
            try:
                OCG_pack = prescript[OCG_pack]
                OCG_ext = OCG_pack_id.split('-JP')[1]
                if OCG_ext == 'SP1':
                    OCG_ext = '000'
                card_id = str(OCG_pack) + str(OCG_ext)
                card_id = str(int(card_id))
            except KeyError:
                card_id = 'MISSING'
            try:
                regexID = re.compile(r"(\d\d\d\d\d\d\d\d)<\/a><\/td><\/tr>")
                patternID = re.compile(regexID)
                card_id = re.findall(patternID, source)[0]
                card_id = str(int(card_id))
            except IndexError:
                pass
            try:
                card_json["id"] = int(card_id)
            except ValueError:
                card_json["id"] = card_id
            ## SETCODE
            try:
                setcode_math = []
                regexSetcode = re.compile(r"Archetypes</a> and <a href=\"/wiki/Series\" title=\"Series\">series</a> \n</dt><dd> (.*?)</dl>", re.DOTALL)
                patternSetcode = re.compile(regexSetcode)
                setcode = re.findall(patternSetcode, source)[0]
                setcode = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', setcode)
                setcode = re.sub('"', '""', setcode)
                setcode = re.sub('<dd>', '', setcode)
                setcode = re.sub('</dd>', '', setcode)
                setcode = re.sub('<dl>', '', setcode)
                setcode = re.sub('</dl>', '', setcode)
                setcode = re.sub('<br />', '', setcode)
                setcode = re.sub('&amp;', '&', setcode)
                setcode = re.sub('&#160;', ' ', setcode)
                setcode = re.sub("\n", "', '", setcode)
                setcode = re.sub(" '", "", setcode)
                setcode = re.sub(" ' ", "", setcode)
                setcode = re.sub("'", "", setcode)
                setcode = re.sub(", ", ",", setcode)
                setcode = setcode.split(',')
                for i in range(0, len(setcode)):
                    try:
                        setcode_math.append(SETCODES[setcode[i]])
                    except KeyError:
                        pass
                setcode = ''
                for j in range(0, len(setcode_math)):
                    bit = setcode_math[j]
                    if len(bit) < 5:
                        bit = re.sub('0x', '00', bit)
                    else:
                        bit = re.sub('0x', '', bit)
                    setcode = setcode + bit
                try:
                    setcode = str(int(setcode, 16))
                except ValueError:
                    setcode = '0'
            except IndexError:
                setcode = '0'
            card_json["setcode"] = int(setcode)
            ## TYPE
            regexCardType0 = re.compile(r"Card type\">Card type</a></th><td class=\"cardtablerowdata\">.*?\">(.*?)</a>", re.DOTALL)
            patternCardType0 = re.compile(regexCardType0)
            card_type0 = re.findall(patternCardType0, source)[0]
            if card_type0 == 'Monster':
                regexCardType = re.compile(r"<\/a> \/ <a href=\"\/wiki\/(.*?)\"")
                patternCardType = re.compile(regexCardType)                
                card_type = re.findall(patternCardType, source)[0]
                try:
                    card_type = int(str(CARD_TYPES[card_type]))
                except KeyError:
                    card_type = int(str(CARD_TYPES['Normal_Monster']))
                try:
                    card_type2 = re.findall(patternCardType, source)[1]
                    if card_type2 == 'Effect_Monster' and card_type != 4129:
                        card_type += 32
                except IndexError:
                    pass
                try:
                    regexFlip = re.compile(r"/wiki/Flip_effect")
                    patternFlip = re.compile(regexFlip)
                    flip_check = re.findall(patternFlip, source)[0]
                    card_type += 2097152
                except IndexError:
                    pass
            else:
                regexCardType = re.compile(r"Property</a></th><td class=\"cardtablerowdata\">.*?title=\"(.*?)\">", re.DOTALL)
                patternCardType = re.compile(regexCardType)
                card_type = re.findall(patternCardType, source)[0]
                card_type = str(CARD_TYPES[card_type])               
            card_json["type"] = int(card_type)
            ## ATK
            try:
                regexATK = re.compile(r"ATK Monster Cards\">(.*?)</a>")
                patternATK = re.compile(regexATK)
                ATK = re.findall(patternATK, source)[0]
            except IndexError:
                ATK = 0
            if ATK == "?":
                ATK = -2
            card_json["atk"] = int(ATK)
            ## DEF
            try:
                try:
                    regexDEF = re.compile(r"DEF Monster Cards\">(.*?)</a>")
                    patternDEF = re.compile(regexDEF)
                    DEF = re.findall(patternDEF, source)[0]
                except IndexError:
                    regexLink = re.compile(r">Link Arrows.*?</td>", re.DOTALL)
                    patternLink = re.compile(regexLink)
                    link_marker = re.findall(patternLink, source)[0]
                    DEF = '-'
            except IndexError:
                DEF = 0
            if DEF == "?":
                DEF = -2
            if DEF != '-' : 
                card_json["def"] = int(DEF)
            else:
                card_json["def"] = DEF
            ## LEVEL
            if card_type0 == 'Monster':
                try:
                    try:
                        regexLevel = re.compile(r"Level \d{1,2} Monster Cards\">(.*?)</a>")
                        patternLevel = re.compile(regexLevel)
                        level = re.findall(patternLevel, source)[0]
                    except IndexError:
                        regexLevel = re.compile(r"Rank \d{1,2} Monster Cards\">(.*?)</a>")
                        patternLevel = re.compile(regexLevel)
                        level = re.findall(patternLevel, source)[0]
                except IndexError:
                    regexLevel = re.compile(r"Link \d{1,2} Monster Cards\">(.*?)</a>")
                    patternLevel = re.compile(regexLevel)
                    level = re.findall(patternLevel, source)[0]
            else:
                level = 0
            card_json["level"] = int(level)
            try:
                regexScale = re.compile(r"Pendulum Scale \d{1,2} Monster Cards\">(.*?)</a>")
                patternScale = re.compile(regexScale)
                pscale = re.findall(patternScale, source)[0]
                if pscale == '10':
                    pscale = 'A'
                if pscale == '11':
                    pscale = 'B'
                if pscale == '12':
                    pscale = 'C'
                if pscale == '13':
                    pscale = 'D'
                if level == '10':
                    level = 'A'
                if level == '11':
                    level = 'B'
                if level == '12':
                    level = 'C'
                level = '0x' + pscale + '0' + pscale + '000' + level
                level = str(int(level, 16))
                card_json["level"] = int(level)
            except IndexError:
                pass
            ## RACE
            if card_json["level"] > 0:
                regexRace = re.compile(r"Type\">.*?/wiki/(.*?)\"", re.DOTALL)
                patternRace = re.compile(regexRace)
                race = re.findall(patternRace, source)[0]
                race = str(RACE[race])
                card_json["race"] = int(race)
            else:
                card_json["race"] = 0
            ## ATTRIBUTE
            try:
                regexAttribute = re.compile(r"Attribute</a></th><td class=\"cardtablerowdata\">\n<a href=\"/wiki/(.*?)\"", re.DOTALL)
                patternAttribute = re.compile(regexAttribute)
                attribute = re.findall(patternAttribute, source)[0]
                attribute = str(ATTRIBUTE[attribute])
            except IndexError:
                attribute = 0
            card_json["attribute"] = int(attribute)
            ## CARD NAME
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
                    regexLink = re.compile(r">Link Arrows(.*?)</td>", re.DOTALL)
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
            OCG_pack = OCG_pack_id.split('-')[0]
            # ALIAS
            try:
                regexAlias = re.compile(r"This card's name is always treated as \"(.*?)\"", re.DOTALL)
                patternAlias = re.compile(regexAlias)
                card_json["alias"] = re.findall(patternAlias, card_json["desc"])[0]
            except IndexError:
                pass
            # PACK INFO
            regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
            patternOCG = re.compile(regexOCG)
            try:
                OCG_date = re.findall(patternOCG, source)[0]
                card_json["ocg"]["date"] = OCG_date
            except IndexError:
                pass
            regexOCG = re.compile(r"English</caption>.*?\d\">(.*?) </td", re.DOTALL)
            patternOCG = re.compile(regexOCG)
            try:
                TCG_date = re.findall(patternOCG, source)[0]
                card_json["tcg"]["date"] = TCG_date
            except IndexError:
                pass
            # CARD PICTURE
            try:
                regexPicture = re.compile(r"cardtable-cardimage\".*?<a href=\"(.*?)cb=", re.DOTALL)
                patternPicture = re.compile(regexPicture)
                card_picture = re.findall(patternPicture, source)[0]
                card_json["picture"] = card_picture
            except IndexError:
                fail.write('Picture not found for: '+card_name+'\n')
            json_filename = 'C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGO_DB\\http\\json\\' + card_id + '.json'
            with open(json_filename, 'w', encoding='utf8') as outfile:
                json.dump(card_json, outfile, indent = 4, ensure_ascii=False, separators=(',', ': '))
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print(name+" failed due to HTTPError")
            fail.write(name+" failed due to HTTPError\n")
            continue
        else:
            raise

fail.close()
