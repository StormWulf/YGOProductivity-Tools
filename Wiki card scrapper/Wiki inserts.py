# Storm Wolf (Jeff Falberg)
# Wiki card scrapper for card inserts

import urllib.request as urr
import urllib.error
from urllib.parse import quote
from urllib.error import HTTPError
import sys
import re
import sqlite3

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
prescript = {'VJMP': 100200,
             'WJMP': 100203,
             'SJMP': 100204,
             'YA03': 100218,
             'COTD': 101001,
             'MACR': 100912,
             'CP17': 100217,
             'DP18': 100418,
             'SD32': 100332
             }
SETCODES = {'Amazoness': 4,
            'HERO': 8,
            }
CARD_TYPES = {'Normal Spell Card': 2,
              'Normal Trap Card': 4,
              'Level': 17,
              'Effect Monster': 33,
              'Ritual Spell Card': 130,
              'Quick-Play Spell Card': 65538,
              'Continuous Spell Card': 131074,
              'Equip Spell Card': 262146,
              'Field Spell Card': 524290,
              'Continuous Trap Card': 131076,
              'Counter Trap Card': 1048580,
              'Flip monster,Effect Monster': 2097185,
              'Xyz Monster': 8388641,
              'Pendulum Monster': 16777249,
              'Link Monster': 33554465
              }
RACE = {'Warrior': 1,
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
ATTRIBUTE = {'EARTH': 1,
             'WATER': 2,
             'FIRE': 4,
             'WIND': 8,
             'LIGHT': 16,
             'DARK': 32,
             'DIVINE': 64
             }
print('--Starting Wiki inserts.py--')
print('If you see "MISSING" values for card ID, assign it manually. You should check the pre-script repository for which ID to use.')
print('This does not generate alias values, assign it manually if a card needs it.\n\n')
for line in listoflines :
	name = line.replace(' ','_').replace('#','')
	wiki_url = "http://yugioh.wikia.com/wiki/" + name
	print('Processing: '+wiki_url)
	page = urr.urlopen(wiki_url)
	if page.getcode() == 200 :
		sourcepage = page.read()
		source = sourcepage.decode("utf-8")
		## CARD ID
		try :
			regexOCGpackid = re.compile(r"Japanese</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
			patternOCGpackid = re.compile(regexOCGpackid)
			OCG_pack_id = re.findall(patternOCGpackid, source)[0]
		except IndexError :
			try :
				regexOCGpackid = re.compile(r"English</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
				patternOCGpackid = re.compile(regexOCGpackid)
				OCG_pack_id = re.findall(patternOCGpackid, source)[0]
			except IndexError :
				regexOCGpackid = re.compile(r"English</caption>.*?\)\">(.*?)</a>", re.DOTALL)
				patternOCGpackid = re.compile(regexOCGpackid)
				OCG_pack_id = re.findall(patternOCGpackid, source)[0]
		OCG_pack = OCG_pack_id[0:4]
		try :
			OCG_pack = prescript[OCG_pack]
			OCG_ext = OCG_pack_id[8:10]
			if int(OCG_ext) < 100 :
				OCG_ext = '0' + str(OCG_ext)
			card_id = str(OCG_pack) + str(OCG_ext)
		except KeyError :
			card_id = 'MISSING'
		## OT (not important anymore)
		ot = '3'
		## ALIAS (has to be updated manually if apply)
		alias = '0'
		## SETCODE (parsed output has to be fixed)
		try:
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
			setcode = "['" + setcode + "]"
			setcode = re.sub(" ',", "',", setcode)
			setcode = re.sub(" ' ", " '", setcode)
			setcode = re.sub(" ']", "]", setcode)
##			for i in range(0, len(setcode)) :
##				try :
##					setcode_math = []
##					setcode_math.append(SETCODES[setcode[i]])
##				except KeyError:
##					pass
##			str(setcode_math)
		except IndexError:
			#setcode_math = '0'
			setcode = '0'
		## TYPE
		regexCardType0 = re.compile(r"Card type,(.*?),")
		patternCardType0 = re.compile(regexCardType0)
		card_type0 = re.findall(patternCardType0, source)[0]
		if card_type0 == 'Monster Card' :
			regexCardType = re.compile(r"Type,.*?,(.*?)\"")
			patternCardType = re.compile(regexCardType)
			card_type = re.findall(patternCardType, source)[0]
			card_type = re.sub(',Level', '', card_type)
			card_type = str(CARD_TYPES[card_type])
		else :
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
			regexDEF = re.compile(r"DEF Monster Cards\">(.*?)</a>")
			patternDEF = re.compile(regexDEF)
			DEF = re.findall(patternDEF, source)[0]
		except IndexError:
			DEF = '0'
		## LEVEL
		try:
			regexLevel = re.compile(r"Level \d{1,2} Monster Cards\">(.*?)</a>")
			patternLevel = re.compile(regexLevel)
			level = re.findall(patternLevel, source)[0]
		except IndexError:
			regexLevel = re.compile(r"Rank \d{1,2} Monster Cards\">(.*?)</a>")
			patternLevel = re.compile(regexLevel)
			level = re.findall(patternLevel, source)[0]
		except IndexError:
			level = '0'
		try:
			regexScale = re.compile(r"Pendulum Scale \d{1,2} Monster Cards\">(.*?)</a>")
			patternScale = re.compile(regexScale)
			pscale = re.findall(patternScale, source)[0]
			if pscale == '10' :
				pscale = 'A'
			if pscale == '11' :
				pscale = 'B'
			if pscale == '12' :
				pscale = 'C'
			if pscale == '13' :
				pscale = 'D'
			if level == '10' :
				level = 'A'
			if level == '11' :
				level = 'B'
			if level == '12' :
				level = 'C'
			level = '0x' + pscale + '0' + pscale + '000' + level
		except IndexError:
			pass
		## RACE
		try :
			regexRace = re.compile(r"Type\">.*?/wiki/(.*?)\"", re.DOTALL)
			patternRace = re.compile(regexRace)
			race = re.findall(patternRace, source)[0]
			race = str(RACE[race])
		except IndexError :
			race = '0'
		except KeyError :
			race = '0'
		## ATTRIBUTE
		try :
			regexAttribute = re.compile(r"Attribute</a></th><td class=\"cardtablerowdata\">\n<a href=\"/wiki/(.*?)\"", re.DOTALL)
			patternAttribute = re.compile(regexAttribute)
			attribute = re.findall(patternAttribute, source)[0]
			attribute = str(ATTRIBUTE[attribute])
		except IndexError :
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
		if "Link \d" in card_text :
			regexLink = re.compile(r">Link Markers.*?</td>", re.DOTALL)
			patternLink = re.compile(regexLink)
			link_marker = re.findall(patternLink, source)[0]
			link_marker = re.sub('(?!<dd>|</dd>|<dl>|</dl>|<br>|<br />)(<.*?>)','', link_marker)
			link_marker = re.sub('"', '""', link_marker)
			link_marker = re.sub('<dd>', '\n', link_marker)
			link_marker = re.sub('</dd>', '\n', link_marker)
			link_marker = re.sub('<dl>', '\n', link_marker)
			link_marker = re.sub('</dl>', '\n', link_marker)
			link_marker = re.sub('<br />', '\n', link_marker)
			link_marker = re.sub('>Link Markers\n', 'Link Markers: ', link_marker)
			link_marker = re.sub('&amp;', '&', link_marker)
			link_marker = re.sub('&#160;', ' ', link_marker)
			card_text = link_marker + card_text
		# PACK INFO
		try :
			regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
			patternOCG = re.compile(regexOCG)
			OCG_date = re.findall(patternOCG, source)[0]
		except IndexError :
			regexOCG = re.compile(r"English</caption>.*?\d\">(.*?) </td", re.DOTALL)
			patternOCG = re.compile(regexOCG)
			OCG_date = re.findall(patternOCG, source)[0]
		query.write('INSERT OR REPLACE INTO "datas" VALUES ("'+card_id+'","'+ot+'","'+alias+'","'+setcode+'","'+card_type+'","'+ATK+'","'+DEF+'","'+level+'","'+race+'","'+attribute+'","0");\n')
		query.write('INSERT OR REPLACE INTO "texts" VALUES ("'+card_id+'","'+card_name+'","'+card_text+'","","","","","","","","","","","","","","","","");\n')
		pack_query.write('INSERT OR REPLACE INTO "pack" VALUES ("'+card_id+'","'+OCG_pack_id+'","","","'+OCG_date+'");\n')
query.close()
pack_query.close()
