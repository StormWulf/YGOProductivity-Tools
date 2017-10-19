var scraperjs = require('scraperjs'),
    input_file = require('./updater_input.json'),
    jsonfile = require('jsonfile'),
    fs = require("fs"),
    async = require("async"),
    SETCODES = require('./setcode.json'),
    sleep = require('sleep'),
    markers,
    id_update = {},
    concerned_cards = [];

async.eachLimit(input_file, 100, function (line, next){
    var filename = 'C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGO_DB\\http\\json\\' + String(line) + '.json';
    var card_json = jsonfile.readFileSync(filename);
    if(card_json.type !== 16401){
        if(card_json.tcg.pack_id !== undefined){
            wiki_url = card_json.tcg.pack_id;
        }
        else{
            wiki_url = card_json.ocg.pack_id;
        }
        if(!wiki_url.match(/\-/)){
            wiki_url = card_json.name.replace('#','');
        }
    }
    else{
        wiki_url = card_json.name.replace('#','');
    }
    //console.log(wiki_url);
    scraperjs.StaticScraper.create()
        .request({ url:'http://yugioh.wikia.com/wiki/'+wiki_url, encoding: 'utf8' })
        .scrape(function($) {
            console.log('Reading: '+card_json.id + ' ' + card_json.name);
            // Scrape most of the other card information
            card = {};
            $(".cardtablerowheader").each(function() {
                return $(this).each( function(index) {
                    card[$(this).text()] = $(this).next().text(); 
                });
            });

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

            //TCG Pack Info
            tcg_list = $('.navbox-list caption').next().next().text().trim().split('\n \n');
            tcg_list = tcg_list.filter(function(n){ 
                return n.match(/\d\d\d\d\-\d\d\-\d\d/); 
            });
            tcg_list = tcg_list.filter(function(n){ 
                return !n.match(/[\u3000-\u303F]|[\u3040-\u309F]|[\u30A0-\u30FF]|[\uFF00-\uFFEF]|[\u4E00-\u9FAF]|[\u2605-\u2606]|[\u2190-\u2195]|\u203B/g); 
            });
            tcg_list = tcg_list.filter(function(n){ 
                return !n.match(/\-[A-Z][0-9]|\-KR|\-JP|\-TC|\-SP/); 
            }).map(function(s) {
                return s.trim();
            }).sort()[0];
            if(tcg_list != undefined){
                old_date = card_json.tcg.date;
                tcg_list = tcg_list.trim().split('\n');
                card_json.tcg.pack = tcg_list[2].trim();
                card_json.tcg.pack_id = tcg_list[1].trim();
                card_json.tcg.date = tcg_list[0].trim();
                if (card_json.ocg.date > old_date){
                    concerned_cards.push(card_json.id);
                    fs.writeFileSync('./concerned_cards.json', JSON.stringify(concerned_cards, null, 4));
                }
            }

            //OCG Pack Info
            ocg_list = $('.navbox-list caption').next().next().text().trim().split('\n \n');
            ocg_list = ocg_list.filter(function(n){ 
                return n.match(/\d\d\d\d\-\d\d\-\d\d/); 
            });
            ocg_list = ocg_list.filter(function(n){ 
                return n.match(/[\u3000-\u303F]|[\u3040-\u309F]|[\u30A0-\u30FF]|[\uFF00-\uFFEF]|[\u4E00-\u9FAF]|[\u2605-\u2606]|[\u2190-\u2195]|\u203B|\-JP/g); 
            }).map(function(s) {
                return s.trim();
            }).sort()[0];
            if(ocg_list != undefined){
                old_date = card_json.ocg.date;
                ocg_list = ocg_list.trim().split('\n');
                card_json.ocg.pack = ocg_list[2].trim();
                card_json.ocg.pack_id = ocg_list[1].trim();
                card_json.ocg.date = ocg_list[0].trim();
                if (card_json.ocg.date > old_date){
                    concerned_cards.push(card_json.id);
                    fs.writeFileSync('./concerned_cards.json', JSON.stringify(concerned_cards, null, 4));
                }
            }
            if(!isNaN(card.Passcode) && card_json.id > 100200000){
                old_id = card_json.id;
                card_json.id = parseInt(card.Passcode);
                fs.rename(filename, 'C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGO_DB\\http\\json\\' + String(card_json.id) + '.json', function(err) {
                    if ( err ) console.log('ERROR: ' + err);
                });
                filename = 'C:\\Users\\auron\\OneDrive\\Documents\\GitHub\\YGO_DB\\http\\json\\' + String(card_json.id) + '.json';
                id_update[String(old_id)] = card_json.id;
                fs.writeFileSync('./id_update.json', JSON.stringify(id_update, null, 4));
            }
            card_json.setcode = setcode;
            if(card.English == undefined){
                console.log("ERROR WITH: "+card_json.id+" "+card_json.name);
            }
            else{
                card_json.name = card.English.trim().replace('Check translation','');
            }
            card_json.desc = $(".navbox-list").eq(0).html().replace(/\<br\>/g,'\n').replace(/<.*?>/g,'').replace(/&apos;/g, "'").replace(/&quot;/g, '"').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&').replace(/&#x2019;/g, "'").replace(/&#x25CF;/g, "●").replace(/\n /g, "\n").trim();
            if(card.Types && card.Types.split(' / ')[1] == 'Link'){
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
            if(markers !== undefined) {
                card_json.desc = 'Link Arrows: ' + markers + '\n\n' + card_json.desc;
            }
            card_json.picture = $(".cardtable-cardimage").eq(0).html().match(/<a href=\"(.*?)\"/)[1];
            //console.log(card);
            //console.log(card_json);
            fs.writeFileSync(filename, JSON.stringify(card_json, null, 4));
            markers = undefined;
            sleep.sleep(3);
            next();
        });
});