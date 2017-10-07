var scraperjs = require('scraperjs'),
    fs = require("fs"),
    SETCODES = require('./setcode.json'),
    ATTRIBUTES = require('./attributes.json'),
    RACE = require('./race.json'),
    MONSTER_TYPE = require('./monster_type.json'),
    ST_TYPE = require('./st_type.json'),
    PRERELEASE = require('./prerelease.json'),
    markers,
    lineReader = require('readline').createInterface({
        input: require('fs').createReadStream('./input.txt')
      });
lineReader.on('line', function (line) {
    line = line.replace('_',' ').trim();
    console.log('Reading: '+line);
    scraperjs.StaticScraper.create()
        .request({ url:'http://yugioh.wikia.com/wiki/'+line })
        .scrape(function($) {
            // Setcode operation
            setcode = []; 
            $('dt').filter(function() {
                return $(this).text().match(/Archetypes and series(.*)/);
            }).nextUntil('dt').each(function(){
                    setcode.push($(this).text().trim());
                });
            setcode_math = [];
            for (var i = 0; i < setcode.length; i++) {
                setcode_math.push(SETCODES[setcode[i]]);
            }
            setcode_math = setcode_math.filter(function(n){ 
                return n != undefined; 
            });
            setcode = '';
            for (var j = 0; j < setcode_math.length; j++) {
                bit = setcode_math[j];
                if (bit.length < 5) {
                    bit = bit.replace('0x', '00');
                }
                else {
                    bit = bit.replace('0x', '');
                }
                setcode += bit;
            }
            setcode = parseInt(setcode.toString(16),16);
            if(isNaN(setcode)) {
                setcode = 0;
            }
            // Scrape most of the other card information
            card = {};
            $(".cardtablerowheader").each(function() {
                return $(this).each( function(index) {
                    card[$(this).text()] = $(this).next().text(); 
                });
            });
            // Initiate json
            card_json = {"ocg":{}, "tcg":{}};

            //TCG Pack Info
            tcg_list = $('.navbox-list caption').next().next().text().trim().split('\n \n');
            tcg_list = tcg_list.filter(function(n){ 
                return n.includes('-EN'); 
            }).sort()[0];
            if(tcg_list != undefined){
                tcg_list = tcg_list.trim().split('\n');
                card_json.tcg.pack = tcg_list[2].trim();
                card_json.tcg.pack_id = tcg_list[1].trim();
                card_json.tcg.date = tcg_list[0].trim();
            }

            //OCG Pack Info
            ocg_list = $('.navbox-list caption').next().next().text().trim().split('\n \n');
            ocg_list = ocg_list.filter(function(n){ 
                return n.includes('-JP'); 
            }).sort()[0];
            if(ocg_list != undefined){
                ocg_list = ocg_list.trim().split('\n');
                card_json.ocg.pack = ocg_list[2].trim();
                card_json.ocg.pack_id = ocg_list[1].trim();
                card_json.ocg.date = ocg_list[0].trim();
            }

            if(!isNaN(card.Passcode)){
            card_json.id = parseInt(card.Passcode);
            }
            else{
                if(ocg_list != undefined){
                    card_json.id = parseInt(PRERELEASE[card_json.ocg.pack_id.split('-JP')[0]] + card_json.ocg.pack_id.split('-JP')[1]);
                }
                else{
                    card_json.id = parseInt(PRERELEASE[card_json.ocg.pack_id.split('-EN')[0]] + card_json.ocg.pack_id.split('-EN')[1]);
                }
            }
            card_json.setcode = setcode;
            if(card['Card type'] == '\nMonster ') {
                card_json.type = MONSTER_TYPE[(card.Types.split(' / ')[1] + ' / ' + card.Types.split(' / ')[2] + ' / ' + card.Types.split(' / ')[3]).replace('/ undefined','').replace('  / undefined','').trim()];
                if (card.Types.split(' / ')[1] == 'Xyz') {
                    card_json.level = parseInt(card.Rank);
                }
                if (card.Types.split(' / ')[1] == 'Pendulum' || card.Types.split(' / ')[2] == 'Pendulum'){
                    if (card.Types.split(' / ')[1] == 'Xyz') {
                        card_json.level = parseInt('0x' + parseInt(card['Pendulum Scale']).toString(16) + '0' + parseInt(card['Pendulum Scale']).toString(16) + '000' + parseInt(card.Rank).toString(16),16);                   
                    }
                    else {
                        card_json.level = parseInt('0x' + parseInt(card['Pendulum Scale']).toString(16) + '0' + parseInt(card['Pendulum Scale']).toString(16) + '000' + parseInt(card.Level).toString(16),16);
                    }
                }
                else {
                    if(card.Types.split(' / ')[1] != 'Link') {
                        if(card['ATK / DEF'].split(' / ')[0].trim() == '?'){
                            card_json.atk = -2;
                        }
                        else{
                            card_json.atk = parseInt(card['ATK / DEF'].split(' / ')[0]);
                        }
                        if(card['ATK / DEF'].split(' / ')[1].trim() == '?'){
                            card_json.def = -2;
                        }
                        else{
                            card_json.def = parseInt(card['ATK / DEF'].split(' / ')[1]);
                        }
                    }
                    else{
                        if(card['ATK / LINK'].split(' / ')[0].trim() == '?'){
                            card_json.atk = -2;
                        }
                        else{
                            card_json.atk = parseInt(card['ATK / LINK'].split(' / ')[0]); 
                        }                       
                        card_json.def = '-';
                        card_json.level = parseInt(card['ATK / LINK'].split(' / ')[1]);
                        markers = card['Link Arrows'].replace('Top-Left', '[🡴]').replace('Top-Right', '[🡵]').replace('Bottom-Left', '[🡷]').replace('Bottom-Right', '[🡶]').replace('Top', '[🡱]').replace('Bottom', '[🡳]').replace('Left', '[🡰]').replace('Right', '[🡲]').replace(/\s,\s/g, '').trim();
                        links = [];
                        if(markers.includes('[🡴]')){
                            links.push(0);
                        }
                        if(markers.includes('[🡱]')){
                            links.push(1);
                        }
                        if(markers.includes('[🡵]')){
                            links.push(2);
                        }
                        if(markers.includes('[🡰]')){
                            links.push(3);
                        }
                        if(markers.includes('[🡲]')){
                            links.push(4);
                        }
                        if(markers.includes('[🡷]')){
                            links.push(5);
                        }
                        if(markers.includes('[🡳]')){
                            links.push(6);
                        }
                        if(markers.includes('[🡶]')){
                            links.push(7);
                        }
                        card_json.links = links;
                    }
                }
                card_json.race = RACE[card.Types.split(' / ')[0].trim()];
                card_json.attribute = ATTRIBUTES[card.Attribute.trim()];
            }
            else {
                card_json.type = ST_TYPE[card['Card type'].trim() + ' / ' + card.Property.trim()];
                card_json.atk = 0;
                card_json.def = 0;
                card_json.level = 0;
                card_json.race = 0;
                card_json.attribute = 0;
            }
            card_json.name = card.English.trim().replace('Check translation','');
            card_json.desc = $(".navbox-list").eq(0).html().replace('<br>','\n').replace(/<.*?>/g,'').replace(/&apos;/g, "'").replace(/&quot;/g, '"').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&').replace(/&#x2019;/g, "'").replace(/&#x25CF;/g, "●").replace(/\n /g, "\n").trim();
            if(markers !== undefined) {
                card_json.desc = 'Link Arrows: ' + markers + '\n\n' + card_json.desc;
            }
            card_json.picture = $(".cardtable-cardimage").eq(0).html().match(/<a href=\"(.*?)\"/)[1];
            //console.log(card);
            //console.log(card_json);
            var wstream = fs.createWriteStream('C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGO_DB\\http\\json\\'+card_json.id+'.json');
            wstream.write(JSON.stringify(card_json, null, 2));
            wstream.end();
            markers = undefined;
        });
    });