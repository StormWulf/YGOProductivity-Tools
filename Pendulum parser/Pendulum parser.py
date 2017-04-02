# Storm Wolf (Jeff Falberg)
# Pendulum Monster parser

import sys
import re
import sqlite3

sys.argv = ["Pendulum parser.py", "input.txt", "output.sql"]
input_file = sys.argv[1]
output_file = sys.argv[2]
#Edit this path if used by a different machine
conn = sqlite3.connect( "C:\\Users\\Jeff\\Documents\\GitHub\\YGOPro Salvation Server\\YGOPro-Support-System\\http\\ygopro\\databases\\0-en-OCGTCG.cdb" )
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
    level = curs.execute("SELECT level FROM datas WHERE ID=?", (line ,))
    level = level.fetchone()
    level = int(re.sub("[^0-9]","",str(level)))
    level = hex(level)
    if len(level) < 4 :
        scale = 0
        level = int(level,16)
    else :
        try :
            scale = int(level[3:5])
        except ValueError :
            scale = int(str(level[3:5]),16)
        try :
            level = int(level[7:9])
        except ValueError :
            level = int(str(level[7:9]),16)
    line = line.rstrip()
    print(line, name, 'Level', level, 'Pendulum Scale', scale)
    query.write(line + ' ' + name + ' Level ' + str(level) + ' Pendulum Scale ' + str(scale) + '\n')
    
query.close()
