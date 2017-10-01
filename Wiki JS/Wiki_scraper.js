var scraperjs = require('scraperjs'),
    fs = require("fs"),
    SETCODES = require('./setcode.json'),
    ATTRIBUTES = require('./attributes.json'),
    RACE = require('./race.json'),
    MONSTER_TYPE = require('./monster_type.json'),
    ST_TYPE = require('./st_type.json');
scraperjs.StaticScraper.create()
    .request({ url:'http://yugioh.wikia.com/wiki/Odd-Eyes_Pendulum_Dragon', encoding: "utf8"})
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
        // Scrape most of the other card information
        card = {};
        $(".cardtablerowheader").each(function() {
            return $(this).each( function(index) {
                card[$(this).text()] = $(this).next().text(); 
            });
        });
        // Initiate json
        card_json = {"ocg":{}, "tcg":{}};
/*         card_json.ocg.pack = 
        card_json.ocg.pack_id = 
        card_json.ocg.date =
        card_json.tcg.pack =
        card_json.tcg.pack_id = 
        card_json.tcg.date = */
        card_json.id = parseInt(card.Passcode);
        card_json.setcode = setcode;
        if(card['Card type'] == '\nMonster ') {
            card_json.type = MONSTER_TYPE[(card.Types.split(' / ')[1] + ' / ' + card.Types.split(' / ')[2] + ' / ' + card.Types.split(' / ')[3]).replace('/ undefined','').replace('  / undefined','').trim()];
            card_json.atk = parseInt(card['ATK / DEF'].split(' / ')[0]);
            card_json.def = parseInt(card['ATK / DEF'].split(' / ')[1]);
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
                card_json.level = parseInt(card.Level);
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
        card_json.picture = $(".cardtable-cardimage").eq(0).html().match(/<a href=\"(.*?)\"/)[1];
        //console.log(card);
        console.log(card_json);
    });