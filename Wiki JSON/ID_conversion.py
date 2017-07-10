# Storm Wolf (Jeff Falberg)
# ID conversion for prerelease -> official cards

import urllib.request as urr
import urllib.error
from urllib.parse import quote
from urllib.error import HTTPError
import sys
import re
import json
import os

sys.argv = ["ID_conversion.py", "input.txt"]
input_file = sys.argv[1]

database = open(input_file, "r")
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
    try:
        page = urr.urlopen(wiki_url)
        if page.getcode() == 200 :
            sourcepage = page.read()
            source = sourcepage.decode("utf-8")   
            regexID = re.compile(r"(\d\d\d\d\d\d\d\d)<\/a><\/td><\/tr>")
            patternID = re.compile(regexID)
            try :
                change_id = re.findall(patternID, source)[0]
                line = line.rstrip()
                print(line+': '+str(int(change_id))+',')
                card_json["id"] = int(change_id)
                with open(json_filename, 'w', encoding='utf8') as outfile:
                    json.dump(card_json, outfile,ensure_ascii=False, indent=4, separators=(',', ': '))
                os.rename(json_filename, 'C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGO_DB\\http\\json\\' + str(int(change_id)) + '.json')
            except IndexError :
                wiki_url = "http://yugioh.wikia.com/wiki/" + quote(card_name) + "_(card)"
                page = urr.urlopen(wiki_url)
                if page.getcode() == 200 :
                    sourcepage = page.read()
                    source = sourcepage.decode("utf-8")   
                    regexID = re.compile(r"(\d\d\d\d\d\d\d\d)<\/a><\/td><\/tr>")
                    patternID = re.compile(regexID)
                    try :
                        change_id = re.findall(patternID, source)[0]
                        line = line.rstrip()
                        print(line+': '+str(int(change_id))+',')
                        card_json["id"] = int(change_id)
                        with open(json_filename, 'w', encoding='utf8') as outfile:
                            json.dump(card_json, outfile,ensure_ascii=False, indent=4, separators=(',', ': '))
                        os.rename(json_filename, 'C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGO_DB\\http\\json\\' + str(int(change_id)) + '.json')
                    except IndexError :
                        print(wiki_url+" failed due to IndexError")
                        pass
                    continue
    except urllib.error.HTTPError as err :
        if err.code == 404 :
            print(wiki_url+" failed due to HTTPError")
            continue
        else :
            raise