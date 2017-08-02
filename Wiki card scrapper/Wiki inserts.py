# Storm Wolf (Jeff Falberg)
# Wiki card scrapper for card inserts

import urllib.request as urr
import urllib.error
import sys
import re
import os
from PIL import Image
from resizeimage import resizeimage

sys.argv = ["Wiki inserts.py", "input.txt", "output.sql", "pack_output.sql", "failed.txt"]
input_file = sys.argv[1]
output_file = sys.argv[2]
pack_output_file = sys.argv[3]
failed_file = sys.argv[4]

database = open(input_file, "r")
query = open(output_file, "w", encoding='utf-8')
pack_query = open(pack_output_file, "w", encoding='utf-8')
fail = open(failed_file, "w", encoding='utf-8')
listoflines = database.readlines()
database.close()
listofdata = []
setcode_math = []
prescript = {
		  'VJMP': 100200,
		  'WJMP': 100203,
		  'SJMP': 100204,
		  'YA03': 100218,
		  'COTD': 101001,
		  'MACR': 100912,
		  'CP17': 100217,
		  'DP18': 100418,
		  'SD32': 100332,
		  'CIBR': 101002,
		  'DBSW': 100419
		  }
SETCODES = {
		  'Amazoness': 4,
		  'HERO': 8,
		  'Destiny HERO': 49160,
		  'roid': 16,
		  'Gladiator Beast': 25,
		  'Ninja': 43,
          'Six Samurai': 61,
		  'Timelord': 74,
		  'Gadget': 81,
		  'Mermail': 116,
		  'Cyber': 147,
		  'Cyberdark': 16531,
		  'Magician': 152,
		  'Odd-Eyes': 153,
		  'Superheavy Samurai': 154,
		  'Performapal': 159,
		  'D/D': 175,
		  'Ritual Beast': 181,
		  'Raidraptor': 186,
		  'Zefra': 196,
		  'D/D/D': 4271,
          'Mecha Phantom Beast': 4123,
		  'Ritual Beast Tamer': 4277,
		  'Abyss Actor': 4332,
		  'Stargrail': 253,
		  'Starrelic': 254,
		  'Clear Wing': 255,
		  'Synchron': 4119,
		  'Vehicroid': 4118,
		  'Synchro Dragon': 8215,
		  'Supreme King Dragon': 8440,
		  'Gouki': 252,
		  'Bonding': 512,
		  'Vullet': 513,
		  'Metaphys': 514,
		  'Crawler': 516,
		  'Altergeist': 517,
          'Magibullet': 518,
          'Weathery': 519
		  }
CARD_TYPES = {
		  'Normal Spell Card': 2,
		  'Normal Trap Card': 4,
		  'Level': 17,
		  'Effect Monster': 33,
		  'Ritual Spell Card': 130,
          'Spirit monster': 545,
		  'Union monster': 1057,
          'Gemini monster': 2081,
		  'Tuner monster': 4129,
		  'Quick-Play Spell Card': 65538,
		  'Continuous Spell Card': 131074,
		  'Equip Spell Card': 262146,
		  'Field Spell Card': 524290,
		  'Continuous Trap Card': 131076,
		  'Counter Trap Card': 1048580,
		  'Flip monster': 2097185,
		  'Flip monster,Effect Monster': 2097185,
		  'Fusion Monster': 97,
		  'Fusion Monster,Effect Monster': 97,
		  'Synchro Monster': 8225,
		  'Xyz Monster': 8388641,
		  'Pendulum Monster': 16777249,
		  'Pendulum Monster,Effect Monster': 16777249,
		  'Link Monster': 33554465
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
		  'Winged-Beast': 512,
		  'Plant': 1024,
		  'Insect': 2048,
		  'Thunder': 4096,
		  'Dragon': 8192,
		  'Beast': 16384,
		  'Beast-Warrior': 32768,
		  'Dinosaur': 65536,
		  'Fish': 131072,
		  'Sea Serpent': 262144,
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
    name = line.replace(' ','_').replace('#','')
    name = name.rstrip()
    wiki_url = "http://yugioh.wikia.com/wiki/" + name
    print('Processing: '+wiki_url)
    try:
        page = urr.urlopen(wiki_url)
        if page.getcode() == 200:
            sourcepage = page.read()
            source = sourcepage.decode("utf-8")
            try:
                try:
                    regexOCGpackid = re.compile(r"Japanese</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                    patternOCGpackid = re.compile(regexOCGpackid)
                    OCG_pack_id = re.findall(patternOCGpackid, source)[0]
                except IndexError:
                    try:
                        regexOCGpackid = re.compile(r"Japanese</caption>.*?\)\">(.*?)</a>", re.DOTALL)
                        patternOCGpackid = re.compile(regexOCGpackid)
                        OCG_pack_id = re.findall(patternOCGpackid, source)[0]
                    except IndexError:
                        try:
                            regexOCGpackid = re.compile(r"English</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
                            patternOCGpackid = re.compile(regexOCGpackid)
                            OCG_pack_id = re.findall(patternOCGpackid, source)[0]
                        except IndexError:
                            regexOCGpackid = re.compile(r"English</caption>.*?\)\">(.*?)</a>", re.DOTALL)
                            patternOCGpackid = re.compile(regexOCGpackid)
                            OCG_pack_id = re.findall(patternOCGpackid, source)[0]
            except IndexError:
                print(name+" failed because the card page doesn't exist yet")
                fail.write(name+" failed because the card page doesn't exist yet\n")
            OCG_pack = OCG_pack_id[0:4]
            try:
                OCG_pack = prescript[OCG_pack]
                OCG_ext = OCG_pack_id[7:10]
                # if int(OCG_ext) < 100:
                    # OCG_ext = '0' + str(OCG_ext)
                card_id = str(OCG_pack) + str(OCG_ext)
            except KeyError:
                card_id = 'MISSING'
            try:
                regexID = re.compile(r"(\d\d\d\d\d\d\d\d)<\/a><\/td><\/tr>")
                patternID = re.compile(regexID)
                card_id = re.findall(patternID, source)[0]
            except IndexError:
                pass
            ## OT (not important anymore)
            ot = '3'
            ## ALIAS (has to be updated manually if apply)
            alias = '0'
            ## SETCODE (parsed output has to be fixed)
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
                    bit = hex(int(setcode_math[j]))
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
            ## TYPE
            regexCardType0 = re.compile(r"Card type,(.*?),")
            patternCardType0 = re.compile(regexCardType0)
            card_type0 = re.findall(patternCardType0, source)[0]
            if card_type0 == 'Monster Card':
                regexCardType = re.compile(r"Type,.*?,(.*?)\"")
                patternCardType = re.compile(regexCardType)
                try: 
                    card_type = re.findall(patternCardType, source)[0]
                    card_type = re.sub(',Level', '', card_type)
                except IndexError:
                    card_type = 'Link Monster'
                card_type = str(CARD_TYPES[card_type])
            else:
                regexCardType = re.compile(r"Property,(.*?),")
                patternCardType = re.compile(regexCardType)
                card_type = re.findall(patternCardType, source)[0]
                card_type = re.sub(',Level', '', card_type)
                card_type = str(CARD_TYPES[card_type])
            ## ATK
            try:
                regexATK = re.compile(r"ATK Monster Cards\">(.*?)</a>")
                patternATK = re.compile(regexATK)
                ATK = re.findall(patternATK, source)[0]
            except IndexError:
                ATK = '0'
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
                DEF = '0'
            ## LEVEL
            try:
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
            except IndexError:
                level = '0'
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
            except IndexError:
                pass
            ## RACE
            try:
                regexRace = re.compile(r"Type\">.*?/wiki/(.*?)\"", re.DOTALL)
                patternRace = re.compile(regexRace)
                race = re.findall(patternRace, source)[0]
                race = str(RACE[race])
            except IndexError:
                race = '0'
            except KeyError:
                race = '0'
            ## ATTRIBUTE
            try:
                regexAttribute = re.compile(r"Attribute</a></th><td class=\"cardtablerowdata\">\n<a href=\"/wiki/(.*?)\"", re.DOTALL)
                patternAttribute = re.compile(regexAttribute)
                attribute = re.findall(patternAttribute, source)[0]
                attribute = str(ATTRIBUTE[attribute])
            except IndexError:
                    attribute = '0'
            ## CARD NAME
            regexName = re.compile(r"data\">\n(.*)</td>")
            patternName = re.compile(regexName)
            card_name = re.findall(patternName, source)[0]
            card_name = re.sub('"', '""', card_name)
            card_name = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', card_name)
            card_name = re.sub('&amp;', '&', card_name)
            card_name = re.sub('&#160;', ' ', card_name)
            ## CARD DESC
            regexText = re.compile(r";;\">\n(.*?)<\/td>", re.DOTALL)
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
            try:
                regexLink = re.compile(r">Link Arrows.*?</td>", re.DOTALL)
                patternLink = re.compile(regexLink)
                link_marker = re.findall(patternLink, source)[0]
                link_marker = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', link_marker)
                link_marker = re.sub('"', '""', link_marker)
                link_marker = re.sub('<dd>', '\n', link_marker)
                link_marker = re.sub('</dd>', '\n', link_marker)
                link_marker = re.sub('<dl>', '\n', link_marker)
                link_marker = re.sub('</dl>', '\n', link_marker)
                link_marker = re.sub('<br />', '\n', link_marker)
                link_marker = re.sub('>Link Arrows\n', 'Link Arrows: ', link_marker)
                link_marker = re.sub('Top-Left', '[🡴]', link_marker)
                link_marker = re.sub('Top-Right', '[🡵]', link_marker)
                link_marker = re.sub('Bottom-Left', '[🡷]', link_marker)
                link_marker = re.sub('Bottom-Right', '[🡶]', link_marker)
                link_marker = re.sub('Top', '[🡱]', link_marker)
                link_marker = re.sub('Bottom', '[🡳]', link_marker)
                link_marker = re.sub('Left', '[🡰]', link_marker)
                link_marker = re.sub('Right', '[🡲]', link_marker)
                link_marker = re.sub('&amp;', '&', link_marker)
                link_marker = re.sub('&#160;', ' ', link_marker)
                card_text = link_marker + '\n\n' + card_text
            except IndexError:
                pass
            OCG_pack = OCG_pack_id.split('-')[0]
            # PACK INFO
            try:
                regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
                patternOCG = re.compile(regexOCG)
                try:
                    OCG_date = re.findall(patternOCG, source)[0]
                except IndexError:
                    OCG_date = ''
            except IndexError:
                regexOCG = re.compile(r"English</caption>.*?\d\">(.*?) </td", re.DOTALL)
                patternOCG = re.compile(regexOCG)
                try:
                    OCG_date = re.findall(patternOCG, source)[0]
                except IndexError:
                    OCG_date = ''
            query.write('INSERT OR REPLACE INTO "datas" VALUES ("'+card_id+'","'+ot+'","'+alias+'","'+setcode+'","'+card_type+'","'+ATK+'","'+DEF+'","'+level+'","'+race+'","'+attribute+'","0");\n')
            query.write('INSERT OR REPLACE INTO "texts" VALUES ("'+card_id+'","'+card_name+'","'+card_text+'","","","","","","","","","","","","","","","","");\n')
            line = re.sub('"', '""', line)
            line = line.rstrip()
            pack_query.write('INSERT OR REPLACE INTO "pack" VALUES ("'+card_id+'","'+OCG_pack_id+'","'+OCG_pack+'","'+line+'","'+OCG_date+'");\n')
            try:
                regexPicture = re.compile(r"cardtable-cardimage\".*?<a href=\"(.*?)\"", re.DOTALL)
                patternPicture = re.compile(regexPicture)
                card_picture = re.findall(patternPicture, source)[0]
                fullfilename = os.path.join('C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGOPro-Salvation-Server\\http\\ygopro\\pics', card_id+".jpg")
                urr.urlretrieve(card_picture, fullfilename)
                with open(fullfilename, 'r+b') as f:
                    with Image.open(f) as image:
                        cover = resizeimage.resize_cover(image, [177, 254])
                        cover.save(fullfilename, image.format)
            except IndexError:
                fail.write('Picture not found for: '+card_name+'\n')
    except urllib.error.HTTPError as err:
        if err.code == 404:
            print(name+" failed due to HTTPError")
            fail.write(name+" failed due to HTTPError\n")
            continue
        else:
            raise
query.close()
pack_query.close()
fail.close()
