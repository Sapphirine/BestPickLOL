const moduleItems = document.getElementsByClassName("module");
const form = document.forms["paras"];
const r = document.getElementById("r");
const rs = document.getElementsByClassName("rs");
const btn = document.getElementById("btn");
for (moduleItem of moduleItems) {
    moduleItem.innerHTML = getModule(moduleItem.id);
    moduleItem.id = "";
}
var btnChangeTiming;

function btnChange() {
    btn.className = "btn btn-primary btn-lg btn-block";
    btn.innerHTML = "Resubmit";
}

function selectChange(self) {
    self.style.color = (self.value == 0) ? "rgba(0,0,0,.3)" : "black";
}

function formSubmit() {
    clearTimeout(btnChangeTiming);
    btn.className = "btn btn-warning btn-lg btn-block";
    btn.innerHTML = "Calculating...";
    btn.onclick = null;
    let bans, pick0, pick1, need;
    list = [];
    for(i = 1; i <= 5; i++) {
        domNode = form["p"+i+"m"];
        v = parseInt(domNode.value);
        list.push(v);
    }
    pick0 = list.join(',');
    list = [];
    for(i = 6; i <= 10; i++) {
        domNode = form["p"+i+"m"];
        v = parseInt(domNode.value);
        list.push(v);
    }
    pick1 = list.join(',');
    list = [];
    for(i = 1; i <= 10; i++) {
        domNode = form["b"+i+"m"];
        v = parseInt(domNode.value);
        list.push(v);
    }
    bans = list.join(',');
    need = form["rn"].value;
    let message = {
        bans: bans,
        pick0: pick0,
        pick1: pick1,
        need: need
    }
    //ajaxTo("GET", "http://127.0.0.1:5002/url/data", message, showReturn, true);
    ajaxTo("GET", "server/noserver.php", message, showReturn, true);
    return false;
}
function showReturn(json) {
    window.scrollTo(0,document.body.scrollHeight);
    btn.className = "btn btn-success btn-lg btn-block";
    btn.innerHTML = "Success";
    btn.onclick = formSubmit;
    btnChangeTiming = setTimeout(btnChange, 3000);
    r.id = "";
    if(form["rn"].value == 1) {
        rn = json.recommend.split(",");
        for(index = 0; index < 10; index++)
            rs[index].innerHTML = getName(parseInt(rn[index]));
    } else {
        rna = json.recommend1.split(",");
        rnb = json.recommend2.split(",");
        for(index = 0; index < 10; index++)
            rs[index].innerHTML = getName(parseInt(rna[index]))+" & "+getName(parseInt(rnb[index]));
    }
    window.scrollTo(0,document.body.scrollHeight);
}

function obj2str(obj) {
    let key, str = "", notFirst = false;
    for(key in obj) {
        if(notFirst) str += "&";
        str += key + "=" + obj[key];
        notFirst = true;
    }
    return str;
}
function ajaxTo(method = "POST", url, para, callback, jsonFormat = true) {
    let xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function() {
        if(xmlhttp.readyState == 4 && xmlhttp.status == 200) {
            if(jsonFormat) {
                console.log("Response: "+xmlhttp.responseText);
                callback(JSON.parse(xmlhttp.responseText));
            } else {
                callback({
                    state: "success",
                    text: xmlhttp.responseText
                });
            }
        } else if(xmlhttp.status >= 400) {
            callback({
                state: "fail",
                code: xmlhttp.status,
                text: xmlhttp.responseText
            });
        }
    }
    console.log("Require: "+url+"?"+obj2str(para));
    xmlhttp.open(method, method=="GET" ? url+"?"+obj2str(para) : url, true);
    xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xmlhttp.send(method=="POST" ? obj2str(para) : "");
}

function getName(id) {
    switch(id) {
        case 266: return "Aatrox";
        case 103: return "Ahri";
        case 84: return "Akali";
        case 12: return "Alistar";
        case 32: return "Amumu";
        case 34: return "Anivia";
        case 1: return "Annie";
        case 22: return "Ashe";
        case 136: return "Aurelion Sol";
        case 268: return "Azir";
        case 432: return "Bard";
        case 53: return "Blitzcrank";
        case 63: return "Brand";
        case 201: return "Braum";
        case 51: return "Caitlyn";
        case 164: return "Camille";
        case 69: return "Cassiopeia";
        case 31: return "Cho'Gath";
        case 42: return "Corki";
        case 122: return "Darius";
        case 131: return "Diana";
        case 119: return "Draven";
        case 36: return "Dr. Mundo";
        case 245: return "Ekko";
        case 60: return "Elise";
        case 28: return "Evelynn";
        case 81: return "Ezreal";
        case 9: return "Fiddlesticks";
        case 114: return "Fiora";
        case 105: return "Fizz";
        case 3: return "Galio";
        case 41: return "Gangplank";
        case 86: return "Garen";
        case 150: return "Gnar";
        case 79: return "Gragas";
        case 104: return "Graves";
        case 120: return "Hecarim";
        case 74: return "Heimerdinger";
        case 420: return "Illaoi";
        case 39: return "Irelia";
        case 427: return "Ivern";
        case 40: return "Janna";
        case 59: return "Jarvan IV";
        case 24: return "Jax";
        case 126: return "Jayce";
        case 202: return "Jhin";
        case 222: return "Jinx";
        case 145: return "Kai'Sa";
        case 429: return "Kalista";
        case 43: return "Karma";
        case 30: return "Karthus";
        case 38: return "Kassadin";
        case 55: return "Katarina";
        case 10: return "Kayle";
        case 141: return "Kayn";
        case 85: return "Kennen";
        case 121: return "Kha'Zix";
        case 203: return "Kindred";
        case 240: return "Kled";
        case 96: return "Kog'Maw";
        case 7: return "LeBlanc";
        case 64: return "Lee Sin";
        case 89: return "Leona";
        case 127: return "Lissandra";
        case 236: return "Lucian";
        case 117: return "Lulu";
        case 99: return "Lux";
        case 54: return "Malphite";
        case 90: return "Malzahar";
        case 57: return "Maokai";
        case 11: return "Master Yi";
        case 21: return "Miss Fortune";
        case 62: return "Wukong";
        case 82: return "Mordekaiser";
        case 25: return "Morgana";
        case 267: return "Nami";
        case 75: return "Nasus";
        case 111: return "Nautilus";
        case 518: return "Neeko";
        case 76: return "Nidalee";
        case 56: return "Nocturne";
        case 20: return "Nunu & Willump";
        case 2: return "Olaf";
        case 61: return "Orianna";
        case 516: return "Ornn";
        case 80: return "Pantheon";
        case 78: return "Poppy";
        case 555: return "Pyke";
        case 246: return "Qiyana";
        case 133: return "Quinn";
        case 497: return "Rakan";
        case 33: return "Rammus";
        case 421: return "Rek'Sai";
        case 58: return "Renekton";
        case 107: return "Rengar";
        case 92: return "Riven";
        case 68: return "Rumble";
        case 13: return "Ryze";
        case 113: return "Sejuani";
        case 235: return "Senna";
        case 35: return "Shaco";
        case 98: return "Shen";
        case 102: return "Shyvana";
        case 27: return "Singed";
        case 14: return "Sion";
        case 15: return "Sivir";
        case 72: return "Skarner";
        case 37: return "Sona";
        case 16: return "Soraka";
        case 50: return "Swain";
        case 517: return "Sylas";
        case 134: return "Syndra";
        case 223: return "Tahm Kench";
        case 163: return "Taliyah";
        case 91: return "Talon";
        case 44: return "Taric";
        case 17: return "Teemo";
        case 412: return "Thresh";
        case 18: return "Tristana";
        case 48: return "Trundle";
        case 23: return "Tryndamere";
        case 4: return "Twisted Fate";
        case 29: return "Twitch";
        case 77: return "Udyr";
        case 6: return "Urgot";
        case 110: return "Varus";
        case 67: return "Vayne";
        case 45: return "Veigar";
        case 161: return "Vel'Koz";
        case 254: return "Vi";
        case 112: return "Viktor";
        case 8: return "Vladimir";
        case 106: return "Volibear";
        case 19: return "Warwick";
        case 498: return "Xayah";
        case 101: return "Xerath";
        case 5: return "Xin Zhao";
        case 157: return "Yasuo";
        case 83: return "Yorick";
        case 350: return "Yuumi";
        case 154: return "Zac";
        case 238: return "Zed";
        case 115: return "Ziggs";
        case 26: return "Zilean";
        case 142: return "Zoe";
        case 143: return "Zyra";
        default: return "No Result";
    }
}

function getModule(name) {
    return "\
    <select name='"+name+"' id='"+name+"' style='color:rgba(0,0,0,.3)' class='form-control' onchange='selectChange(this)'>\
        <option value='0' style='color:rgba(0,0,0,.3)'>-[ Not specify ]-</option>\
        <option value='266' style='color:black'>Aatrox</option>\
        <option value='103' style='color:black'>Ahri</option>\
        <option value='84' style='color:black'>Akali</option>\
        <option value='12' style='color:black'>Alistar</option>\
        <option value='32' style='color:black'>Amumu</option>\
        <option value='34' style='color:black'>Anivia</option>\
        <option value='1' style='color:black'>Annie</option>\
        <option value='22' style='color:black'>Ashe</option>\
        <option value='136' style='color:black'>Aurelion Sol</option>\
        <option value='268' style='color:black'>Azir</option>\
        <option value='432' style='color:black'>Bard</option>\
        <option value='53' style='color:black'>Blitzcrank</option>\
        <option value='63' style='color:black'>Brand</option>\
        <option value='201' style='color:black'>Braum</option>\
        <option value='51' style='color:black'>Caitlyn</option>\
        <option value='164' style='color:black'>Camille</option>\
        <option value='69' style='color:black'>Cassiopeia</option>\
        <option value='31' style='color:black'>Cho'Gath</option>\
        <option value='42' style='color:black'>Corki</option>\
        <option value='122' style='color:black'>Darius</option>\
        <option value='131' style='color:black'>Diana</option>\
        <option value='119' style='color:black'>Draven</option>\
        <option value='36' style='color:black'>Dr. Mundo</option>\
        <option value='245' style='color:black'>Ekko</option>\
        <option value='60' style='color:black'>Elise</option>\
        <option value='28' style='color:black'>Evelynn</option>\
        <option value='81' style='color:black'>Ezreal</option>\
        <option value='9' style='color:black'>Fiddlesticks</option>\
        <option value='114' style='color:black'>Fiora</option>\
        <option value='105' style='color:black'>Fizz</option>\
        <option value='3' style='color:black'>Galio</option>\
        <option value='41' style='color:black'>Gangplank</option>\
        <option value='86' style='color:black'>Garen</option>\
        <option value='150' style='color:black'>Gnar</option>\
        <option value='79' style='color:black'>Gragas</option>\
        <option value='104' style='color:black'>Graves</option>\
        <option value='120' style='color:black'>Hecarim</option>\
        <option value='74' style='color:black'>Heimerdinger</option>\
        <option value='420' style='color:black'>Illaoi</option>\
        <option value='39' style='color:black'>Irelia</option>\
        <option value='427' style='color:black'>Ivern</option>\
        <option value='40' style='color:black'>Janna</option>\
        <option value='59' style='color:black'>Jarvan IV</option>\
        <option value='24' style='color:black'>Jax</option>\
        <option value='126' style='color:black'>Jayce</option>\
        <option value='202' style='color:black'>Jhin</option>\
        <option value='222' style='color:black'>Jinx</option>\
        <option value='145' style='color:black'>Kai'Sa</option>\
        <option value='429' style='color:black'>Kalista</option>\
        <option value='43' style='color:black'>Karma</option>\
        <option value='30' style='color:black'>Karthus</option>\
        <option value='38' style='color:black'>Kassadin</option>\
        <option value='55' style='color:black'>Katarina</option>\
        <option value='10' style='color:black'>Kayle</option>\
        <option value='141' style='color:black'>Kayn</option>\
        <option value='85' style='color:black'>Kennen</option>\
        <option value='121' style='color:black'>Kha'Zix</option>\
        <option value='203' style='color:black'>Kindred</option>\
        <option value='240' style='color:black'>Kled</option>\
        <option value='96' style='color:black'>Kog'Maw</option>\
        <option value='7' style='color:black'>LeBlanc</option>\
        <option value='64' style='color:black'>Lee Sin</option>\
        <option value='89' style='color:black'>Leona</option>\
        <option value='127' style='color:black'>Lissandra</option>\
        <option value='236' style='color:black'>Lucian</option>\
        <option value='117' style='color:black'>Lulu</option>\
        <option value='99' style='color:black'>Lux</option>\
        <option value='54' style='color:black'>Malphite</option>\
        <option value='90' style='color:black'>Malzahar</option>\
        <option value='57' style='color:black'>Maokai</option>\
        <option value='11' style='color:black'>Master Yi</option>\
        <option value='21' style='color:black'>Miss Fortune</option>\
        <option value='62' style='color:black'>Wukong</option>\
        <option value='82' style='color:black'>Mordekaiser</option>\
        <option value='25' style='color:black'>Morgana</option>\
        <option value='267' style='color:black'>Nami</option>\
        <option value='75' style='color:black'>Nasus</option>\
        <option value='111' style='color:black'>Nautilus</option>\
        <option value='518' style='color:black'>Neeko</option>\
        <option value='76' style='color:black'>Nidalee</option>\
        <option value='56' style='color:black'>Nocturne</option>\
        <option value='20' style='color:black'>Nunu & Willump</option>\
        <option value='2' style='color:black'>Olaf</option>\
        <option value='61' style='color:black'>Orianna</option>\
        <option value='516' style='color:black'>Ornn</option>\
        <option value='80' style='color:black'>Pantheon</option>\
        <option value='78' style='color:black'>Poppy</option>\
        <option value='555' style='color:black'>Pyke</option>\
        <option value='246' style='color:black'>Qiyana</option>\
        <option value='133' style='color:black'>Quinn</option>\
        <option value='497' style='color:black'>Rakan</option>\
        <option value='33' style='color:black'>Rammus</option>\
        <option value='421' style='color:black'>Rek'Sai</option>\
        <option value='58' style='color:black'>Renekton</option>\
        <option value='107' style='color:black'>Rengar</option>\
        <option value='92' style='color:black'>Riven</option>\
        <option value='68' style='color:black'>Rumble</option>\
        <option value='13' style='color:black'>Ryze</option>\
        <option value='113' style='color:black'>Sejuani</option>\
        <option value='235' style='color:black'>Senna</option>\
        <option value='35' style='color:black'>Shaco</option>\
        <option value='98' style='color:black'>Shen</option>\
        <option value='102' style='color:black'>Shyvana</option>\
        <option value='27' style='color:black'>Singed</option>\
        <option value='14' style='color:black'>Sion</option>\
        <option value='15' style='color:black'>Sivir</option>\
        <option value='72' style='color:black'>Skarner</option>\
        <option value='37' style='color:black'>Sona</option>\
        <option value='16' style='color:black'>Soraka</option>\
        <option value='50' style='color:black'>Swain</option>\
        <option value='517' style='color:black'>Sylas</option>\
        <option value='134' style='color:black'>Syndra</option>\
        <option value='223' style='color:black'>Tahm Kench</option>\
        <option value='163' style='color:black'>Taliyah</option>\
        <option value='91' style='color:black'>Talon</option>\
        <option value='44' style='color:black'>Taric</option>\
        <option value='17' style='color:black'>Teemo</option>\
        <option value='412' style='color:black'>Thresh</option>\
        <option value='18' style='color:black'>Tristana</option>\
        <option value='48' style='color:black'>Trundle</option>\
        <option value='23' style='color:black'>Tryndamere</option>\
        <option value='4' style='color:black'>Twisted Fate</option>\
        <option value='29' style='color:black'>Twitch</option>\
        <option value='77' style='color:black'>Udyr</option>\
        <option value='6' style='color:black'>Urgot</option>\
        <option value='110' style='color:black'>Varus</option>\
        <option value='67' style='color:black'>Vayne</option>\
        <option value='45' style='color:black'>Veigar</option>\
        <option value='161' style='color:black'>Vel'Koz</option>\
        <option value='254' style='color:black'>Vi</option>\
        <option value='112' style='color:black'>Viktor</option>\
        <option value='8' style='color:black'>Vladimir</option>\
        <option value='106' style='color:black'>Volibear</option>\
        <option value='19' style='color:black'>Warwick</option>\
        <option value='498' style='color:black'>Xayah</option>\
        <option value='101' style='color:black'>Xerath</option>\
        <option value='5' style='color:black'>Xin Zhao</option>\
        <option value='157' style='color:black'>Yasuo</option>\
        <option value='83' style='color:black'>Yorick</option>\
        <option value='350' style='color:black'>Yuumi</option>\
        <option value='154' style='color:black'>Zac</option>\
        <option value='238' style='color:black'>Zed</option>\
        <option value='115' style='color:black'>Ziggs</option>\
        <option value='26' style='color:black'>Zilean</option>\
        <option value='142' style='color:black'>Zoe</option>\
        <option value='143' style='color:black'>Zyra</option>\
    </select>\
    "
}