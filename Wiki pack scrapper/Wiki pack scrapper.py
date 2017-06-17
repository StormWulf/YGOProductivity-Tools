# Storm Wolf (Jeff Falberg)
# Wiki card scrapper for card names and descriptions
import urllib.request as urr
import urllib.error
from urllib.parse import quote
from urllib.error import HTTPError
import sys
import re
import sqlite3
from datetime import datetime

sys.argv = ["Wiki pack scrapper.py", "input.txt", "tcg_output.sql", "ocg_output.sql", "failed.txt"]
input_file = sys.argv[1]
tcg_output_file = sys.argv[2]
ocg_output_file = sys.argv[3]
failed_file = sys.argv[4]
#Edit this path if used by a different machine
conn = sqlite3.connect( "C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGOPro-Salvation-Server\\http\\ygopro\\databases\\0-en-OCGTCG.cdb" )
curs = conn.cursor()

database = open(input_file, "r")
tcg_query = open(tcg_output_file, "w", encoding='utf-8')
ocg_query = open(ocg_output_file, "w", encoding='utf-8')
fail = open(failed_file, "w", encoding='utf-8')
listoflines = database.readlines()
database.close()
listofdata = []

for line in listoflines :
	name = curs.execute("SELECT name FROM texts WHERE ID=?", (line ,))
	name = name.fetchone()
	name = str(name)
	name = name[2:-3]
	lname = name.replace(' ','_').replace('#','').replace('-','-')
	line = line.rstrip()
	#print(name)
	wiki_url = "http://yugioh.wikia.com/wiki/" + quote(lname)
	try:
##		try:
		page = urr.urlopen(wiki_url)
		if page.getcode() == 200 :
			sourcepage = page.read()
			source = sourcepage.decode("utf-8")
			regexCardType = re.compile(r"Card type,(.*?),")
			patternCardType = re.compile(regexCardType)
			#CardType = re.findall(patternCardType, source)[0]
			print('Processing: '+wiki_url)
##		except IndexError:
##			wiki_url = "http://yugioh.wikia.com/wiki/" + quote(lname) + "_(card)"
##			page = urr.urlopen(wiki_url)
##			if page.getcode() == 200 :
##				sourcepage = page.read()
##				source = sourcepage.decode("utf-8")
##				print('Processing: '+wiki_url)
		#TCG date
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
			regexTCG = re.compile(r"English</caption>.*?\d\">(.*?) </td", re.DOTALL)
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
				fail.write(name+" failed due to an issue with Wiki page")
			else :
				tcg_query.write('INSERT OR REPLACE INTO "pack" VALUES ("'+line+'","'+tcg_pack_id+'","'+tcg_pack_name+'","'+name+'","'+TCG_date+'");\n')
		except IndexError:
			pass
		#OCG date
		try:
			regexOCG = re.compile(r"Japanese name</th>.*?\d\">(.*?) </td", re.DOTALL)
			patternOCG = re.compile(regexOCG)
			OCG_date = re.findall(patternOCG, source)[0]
			regexOCGpackid = re.compile(r"Japanese</caption>.*?\"mw-redirect\">(.*?)</a>", re.DOTALL)
			patternOCGpackid = re.compile(regexOCGpackid)
			OCG_pack_id = re.findall(patternOCGpackid, source)[0]
			if len(OCG_pack_id) > 10 :
				OCG_pack_id = ''
			ocg_pack_name = OCG_pack_id.split('-')[0]
			if len(OCG_date) > 15 :
				fail.write(name+" failed due to an issue with Wiki page\n")
			else :
				ocg_query.write('INSERT OR REPLACE INTO "pack" VALUES ("'+line+'","'+OCG_pack_id+'","'+ocg_pack_name+'","'+name+'","'+OCG_date+'");\n')
		except IndexError:
			pass
	except urllib.error.HTTPError as err :
		if err.code == 404 :
			print(wiki_url+" failed due to HTTPError")
			fail.write(name+" failed due to HTTPError\n")
			continue
		else :
			raise
tcg_query.close()
ocg_query.close()
fail.close()
