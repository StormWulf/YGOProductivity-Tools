# Storm Wolf (Jeff Falberg)
# Detection for cards without pictures

import sys
import re
import sqlite3
import os.path

sys.argv = ["missing_pics_finder.py", "input.txt", "output.txt"]
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
	type = curs.execute("SELECT type FROM datas where ID in (SELECT ID FROM texts where ID=?)", (line ,))
	type = type.fetchone()
	line = line.rstrip()
	if type == (524290,) :
		if os.path.exists('C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGOPro-Salvation-Server\\http\\ygopro\\pics\\field\\'+line+'.png') :
			pass
		else :
			print(line,name,"needs a Field picture")
			query.write(line + ' ' + name + ' ' + " needs a Field picture\n")
	if os.path.exists('C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGOPro-Salvation-Server\\http\\ygopro\\pics\\'+line+'.jpg') :
		pass
	else :
		print(line,name,"needs a card picture")
		query.write(line + ' ' + ' ' + name + " needs a card picture\n")
query.close()
