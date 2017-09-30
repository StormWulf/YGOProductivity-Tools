var scraperjs = require('scraperjs');
scraperjs.StaticScraper.create()
    .request({ url:'http://yugioh.wikia.com/wiki/Stardust_Dragon', encoding: "utf8"})
    .scrape(function($) {
        setcode = []; 
        $('dt').filter(function() {
            return $(this).text().match(/Archetypes and series(.*)/);
        }).nextUntil('dt').each(function(){
                setcode.push($(this).text().trim());
            });
        card = {};
        $(".cardtablerowheader").each(function() {
            return $(this).each( function(index) {
                card[$(this).text()] = $(this).next().text(); 
            });
        });
        desc = $(".navbox-list").eq(0).html().replace('<br>','\n').replace(/<.*?>/g,'').replace(/&apos;/g, "'").replace(/&quot;/g, '"').replace(/&gt;/g, '>').replace(/&lt;/g, '<').replace(/&amp;/g, '&').trim();
        picture = $(".cardtable-cardimage").eq(0).html().match(/<a href=\"(.*?)\"/)[1];
        card_json = {"ocg":{}, "tcg":{}};
        /*card_json.ocg.pack = 
        card_json.ocg.pack_id = 
        card_json.ocg.date =
        card_json.tcg.pack =
        card_json.tcg.pack_id =
        card_json.tcg.date =*/
        card_json.id = parseInt(card.Passcode);
        card_json.setcode = setcode;
        card_json.type = (card.Types.split(' / ')[1] + ' / ' + card.Types.split(' / ')[2] + ' / ' + card.Types.split(' / ')[3]).replace('/ undefined','').replace('  / undefined','').trim();
        card_json.atk = parseInt(card['ATK / DEF'].split(' / ')[0]);
        card_json.def = parseInt(card['ATK / DEF'].split(' / ')[1]);
        card_json.level = parseInt(card.Level);
        card_json.race = card.Types.split(' / ')[0].trim();
        card_json.attribute = card.Attribute.trim();
        card_json.name = card.English.trim().replace('Check translation','');
        card_json.desc = desc;
        card_json.picture = picture;
        console.log(card_json);
    });