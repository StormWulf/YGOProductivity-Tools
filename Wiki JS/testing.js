var scraperjs = require('scraperjs');
scraperjs.StaticScraper.create()
    .request({ url:'http://yugioh.wikia.com/wiki/Stardust_Dragon', encoding: "utf8"})
    .scrape(function($) {
        card = {};
        $(".cardtablerowheader").map(function() {
            return $(this).each( function(index) {
                card[$(this).text()] = $(this).next().text(); 
            });
        });
        $(".cardtablespanrow").each( function(index) {
            var boxes = $(this).find('table');
            var title= $(this).children().eq(0).text().trim();
            card[title]={};
            return boxes.each (function() {
                var rows =  $(this).children().eq(0).children();
                var sub_title = rows.eq(0).children().eq(0).children().eq(1).text().trim();
                var card_text = rows.eq(2).text().trim();
                card[title][sub_title] = card_text;
            });
        });
/*         $(".cardtable-cardimage").each( function(index) {
            return card.picture = $(this);
            }); */
        card_json = {"ocg":{}, "tcg":{}};
        /*card_json.ocg.pack = 
        card_json.ocg.pack_id = 
        card_json.ocg.date =
        card_json.tcg.pack =
        card_json.tcg.pack_id =
        card_json.tcg.date =*/
        card_json.id = parseInt(card.Passcode);
        //card_json.setcode =
        card_json.type = (card.Types.split(' / ')[1] + ' / ' + card.Types.split(' / ')[2] + ' / ' + card.Types.split(' / ')[3]).replace('/ undefined','').replace('  / undefined','').trim();
        card_json.atk = parseInt(card['ATK / DEF'].split(' / ')[0]);
        card_json.def = parseInt(card['ATK / DEF'].split(' / ')[1]);
        card_json.level = parseInt(card.Level);
        card_json.race = card.Types.split(' / ')[0].trim();
        card_json.attribute = card.Attribute.trim();
        card_json.name = card.English.trim().replace('Check translation','');
        card_json.desc = card['Card descriptions'].English;
        //card_json.picture = card.picture;
        console.log(card);
        //console.log(card_json);
    });