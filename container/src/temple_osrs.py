import requests
import json
import logging
import time
import datetime
import asyncio
from functools import partial
from requests.exceptions import HTTPError

FILE_LOCATION = "src/conf/time.output"
resp_test = b'{"data":[{"Username":"Saltysyra1","Date":"2022-12-16 09:29:13","Skill":"Smithing1","Type":"Skill","Xp":5000001},{"Username":"Ivan Btw","Date":"2023-04-12 04:49:31","Skill":"Alchemical Hydra","Milestone":"XP","Type":"Pvm","Xp":700},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Prayer","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Magic","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Cooking","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Attack","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Fletching","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Defence","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Crafting","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Strength","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Herblore","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Hitpoints","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Slayer","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Ranged","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Cute Jesus","Date":"2023-04-12 00:28:00","Skill":"Farming","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Diablolatino","Date":"2023-04-12 00:17:30","Skill":"Nex","Milestone":"XP","Type":"Pvm","Xp":200},{"Username":"Kaanploxrun","Date":"2023-04-11 23:42:14","Skill":"Zulrah","Milestone":"XP","Type":"Pvm","Xp":400},{"Username":"Hitpointler","Date":"2023-04-11 21:54:02","Skill":"Cooking","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Hitpointler","Date":"2023-04-11 21:54:02","Skill":"Firemaking","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Hitpointler","Date":"2023-04-11 21:54:02","Skill":"Farming","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Hitpointler","Date":"2023-04-11 21:54:02","Skill":"Attack","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Hitpointler","Date":"2023-04-11 21:54:02","Skill":"Defence","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Hitpointler","Date":"2023-04-11 21:54:02","Skill":"Strength","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Hitpointler","Date":"2023-04-11 21:54:02","Skill":"Hitpoints","Milestone":"Level","Type":"Skill","Xp":99},{"Username":"Hitpointler","Date":"2023-04-11 21:54:02","Skill":"Ranged","Milestone":"Level","Type":"Skill","Xp":99}]}'
resp_test2 = b'{"data":[{"Username":"Saltysyra1","Date":"2022-12-16 09:29:13","Skill":"Smithing1","Type":"Skill","Xp":5000001},{"Username":"Consumption","Date":"2022-12-16 08:49:25","Skill":"General Graardor","Type":"Pvm","Xp":300},{"Username":"Lukezz","Date":"2022-12-15 23:17:05","Skill":"Hitpoints","Type":"Skill","Xp":90000000},{"Username":"Cookiehcake","Date":"2022-12-15 22:59:40","Skill":"Dagannoth Rex","Type":"Pvm","Xp":1300},{"Username":"Cookiehcake","Date":"2022-12-15 22:59:40","Skill":"Dagannoth Supreme","Type":"Pvm","Xp":1300},{"Username":"Cookiehcake","Date":"2022-12-15 22:59:40","Skill":"KreeArra","Type":"Pvm","Xp":1000},{"Username":"Syraspecial","Date":"2022-12-15 22:33:08","Skill":"Alchemical Hydra","Type":"Pvm","Xp":100},{"Username":"Top V1","Date":"2022-12-15 20:53:37","Skill":"Dagannoth Rex","Type":"Pvm","Xp":1900},{"Username":"Top V1","Date":"2022-12-15 20:53:37","Skill":"Dagannoth Supreme","Type":"Pvm","Xp":1800},{"Username":"Cinderal","Date":"2022-12-15 19:13:43","Skill":"Zulrah","Type":"Pvm","Xp":100},{"Username":"Vlk1ng","Date":"2022-12-15 17:43:22","Skill":"King Black Dragon","Type":"Pvm","Xp":1300},{"Username":"Top V1","Date":"2022-12-15 17:41:29","Skill":"Alchemical Hydra","Type":"Pvm","Xp":1600},{"Username":"Consumption","Date":"2022-12-15 17:33:24","Skill":"General Graardor","Type":"Pvm","Xp":200},{"Username":"Lukezz","Date":"2022-12-15 13:23:33","Skill":"Nex","Type":"Pvm","Xp":900},{"Username":"Confusedgali","Date":"2022-12-15 10:00:49","Skill":"Ehp","Type":"Skill","Xp":300},{"Username":"Confusedgali","Date":"2022-12-15 10:00:49","Skill":"Clue_medium","Type":"Pvm","Xp":200},{"Username":"Confusedgali","Date":"2022-12-15 10:00:49","Skill":"Wintertodt","Type":"Pvm","Xp":100},{"Username":"Waldroni","Date":"2022-12-15 06:56:00","Skill":"Attack","Type":"Skill","Xp":5000000},{"Username":"Cinderal","Date":"2022-12-15 06:31:50","Skill":"Mining","Type":"Skill","Xp":15000000},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Dagannoth Supreme","Type":"Pvm","Xp":1700},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Thermonuclear Smoke Devil","Type":"Pvm","Xp":3400},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Ranged","Type":"Skill","Xp":45000000},{"Username":"Top V1","Date":"2022-12-15 00:31:23","Skill":"Dagannoth Prime","Type":"Pvm","Xp":1700},{"Username":"Top V1","Date":"2022-12-14 13:02:43","Skill":"KreeArra","Type":"Pvm","Xp":100},{"Username":"The Nevster","Date":"2022-12-14 12:40:09","Skill":"Strength","Type":"Skill","Xp":25000000}]}'
members_resp = b'["Weapons","Lukezz","Iamxerxes","Saltysyra","Spectralclan","L Z","Killer9823","The Nevster","Strobax","Antipatchy","Synizta","Swiftee Only","Hic Dwayne","Sp1nk","T O Dd","Stinkyfishy","Sperg","Twincyclone","Syravard","Consumption","Devau","Calleigh","Icalleigh","Knd Xp","Masuasukki","Confusedgali","Positive Doc","Diablolatino","Stroplanklot","Stroplank","Syraoverstro","Onmytoddish","Babymetal72","Strobim","Iamstroplank","Dim Xp","Ok A Y","Masuman","Doo M","Syraspecial","Iv An","Rosaa","Amourosaa","Maryhindge","Telex","Pokimanex","Bakedup","Synizta Btw","Crys","Sir Frosties","Jappie009","Sakurosaa","Waldroni","Jkqp","Kaylynne","Wowarchie","Cinderal","Zaprowsdower","Coldstrider","Hxc Kaylynne","Malle Balle","Rimmernathan","Grif Ball","Hc Crys","Cbacher","Doofe","Tuttifruttii","Bentz","Alqon","Kushpappi","Aleavvy","Sirr Blood","Goblin Cook","Guccirune","Osrslilkid","Da Wolfy","No4skin4me","Cookiehcake","Westv Jr","Rohhan","Licharus","Osf Vegeta","Cettoh","Mseppe","Gordfather","Tiggga","Unclegord","Chugcowwalk","East Varrock","Mr Afker99","Bahshiestyy","Gg Joe","Cooke Guy","Caruerosaa","Jaxom333","Tomauh","Rednation M8","Gumii Chan","Drakulz","Ironmisko","H Nevs","Suedonyx","Sardukai33","West Varrock","Titanstrike","Winny Wins","Truck4","Meloo","Savage Syn","Iyiagix","Fuwi","Xjohnn","Sgt Snorkels","Iron Skebber","Seppe M","Big Brane","Cutty Flam 8","Tynan","Axeforrest","Milfponyy","Khronos127","Odd Plopz","Maximumpanda","Kluns","Del Houm","Hi 44hi44","Dakinedank","Masu Alt","Stinky Chair","Mr Cookie 03","Bl00dd00m","Xatalus","Wildbenjiyt","Valdzx","Torilla","Akanshindoi","Mdor3051","Callmedeath","Explosher","Luckystronk","Strider3141","Slightly Sas","D Limbs","Top V1","Crushable","Lyfe Problem","Camarao","Vlk1ng","Big Pegasus","Henk Speklap","Ovilander","Dogi555","Azarathos","Bitglitched","Pinkiejam","Krispy Crys","Wisdom Lily","Mr Danyal","Mustafa Omar","Ancientrevan","Need R1zla","Wh1sp3r3r","Hadrielll","Oviz","Need Plums","17cloak1851","Bellaraina","Owo Kitty","Amby Fenix","Crazyannah","Xpr0 Sniper","Domkaz8","St Georges B","Dan Xvii","Tealeuf","Jk Y","Dolorosaa","W O O D","Beefletics","Blindsagex","Golden Kiwii"]'
new_player_resp = b'\r\n{"data":{"info":{"Username":"Weapons","Country":"-","Game mode":0,"Cb-3":0,"F2p":0,"Banned":0,"Disqualified":0,"Clan preference":null,"Last checked":"2022-12-05 20:32:52","Last checked unix":1670272372},"Date":"2022-12-05 20:32:52","Overall":331726573,"Overall_rank":130420,"Overall_level":2082,"Overall_ehp":550.985844749104,"Attack":27687801,"Attack_rank":24188,"Attack_level":99,"Attack_ehp":0,"Defence":18006003,"Defence_rank":50649,"Defence_level":99,"Defence_ehp":43.40950110678449,"Strength":36322233,"Strength_rank":28120,"Strength_level":99,"Strength_ehp":0,"Hitpoints":59345751,"Hitpoints_rank":17582,"Hitpoints_level":99,"Hitpoints_ehp":0.296728755,"Ranged":67123470,"Ranged_rank":14131,"Ranged_level":99,"Ranged_ehp":23.16263943703979,"Prayer":5520808,"Prayer_rank":148200,"Prayer_level":90,"Prayer_ehp":3.0671155555555556,"Magic":20905070,"Magic_rank":47045,"Magic_level":99,"Magic_ehp":0.10452535,"Cooking":6756549,"Cooking_rank":354245,"Cooking_level":92,"Cooking_ehp":8.8946806969334,"Woodcutting":7957698,"Woodcutting_rank":152613,"Woodcutting_level":94,"Woodcutting_ehp":45.282487104757436,"Fletching":7582622,"Fletching_rank":220396,"Fletching_level":93,"Fletching_ehp":0.03791311,"Fishing":3317716,"Fishing_rank":317216,"Fishing_level":85,"Fishing_ehp":28.44227240697709,"Firemaking":5221171,"Firemaking_rank":365643,"Firemaking_level":89,"Firemaking_ehp":9.750471620080592,"Crafting":10168270,"Crafting_rank":128414,"Crafting_level":96,"Crafting_ehp":29.787925398059542,"Smithing":3725422,"Smithing_rank":177076,"Smithing_level":86,"Smithing_ehp":10.636384210526316,"Mining":3423670,"Mining_rank":196488,"Mining_level":85,"Mining_ehp":36.283123588269035,"Herblore":5632383,"Herblore_rank":123078,"Herblore_level":90,"Herblore_ehp":14.223367681232068,"Agility":2030998,"Agility_rank":247103,"Agility_level":80,"Agility_ehp":37.371456670756906,"Thieving":2210821,"Thieving_rank":273086,"Thieving_level":81,"Thieving_ehp":16.687118484848483,"Slayer":20659214,"Slayer_rank":18791,"Slayer_level":99,"Slayer_ehp":220.07734373015072,"Farming":13072124,"Farming_rank":161567,"Farming_level":99,"Farming_ehp":11.396096459899749,"Runecraft":1183279,"Runecraft_rank":262027,"Runecraft_level":74,"Runecraft_ehp":5.376616666666667,"Hunter":870990,"Hunter_rank":506045,"Hunter_level":71,"Hunter_ehp":3.395873390827088,"Construction":3002510,"Construction_rank":192679,"Construction_level":84,"Construction_ehp":3.302203324738987,"Ehp":550.9858,"Ehp_rank":79026,"Im_ehp":0,"Lvl3_ehp":0,"F2p_ehp":0,"Uim_ehp":0,"Clue_all":243,"Clue_beginner":0,"Clue_easy":2,"Clue_medium":6,"Clue_hard":153,"Clue_elite":71,"Clue_master":11,"LMS":0,"Abyssal Sire":685,"Abyssal Sire_ehb":15.222222222222221,"Alchemical Hydra":2219,"Alchemical Hydra_ehb":67.24242424242425,"Barrows Chests":277,"Bryophyta":0,"Callisto":0,"Callisto_ehb":0,"Cerberus":1503,"Cerberus_ehb":24.639344262295083,"Chambers of Xeric":732,"Chambers of Xeric_ehb":244,"Chambers of Xeric Challenge Mode":74,"Chambers of Xeric Challenge Mode_ehb":30.833333333333336,"Chaos Elemental":0,"Chaos Elemental_ehb":0,"Chaos Fanatic":0,"Chaos Fanatic_ehb":0,"Commander Zilyana":95,"Commander Zilyana_ehb":1.7272727272727273,"Corporeal Beast":105,"Corporeal Beast_ehb":1.75,"Crazy Archaeologist":0,"Dagannoth Prime":253,"Dagannoth Prime_ehb":2.53,"Dagannoth Rex":314,"Dagannoth Rex_ehb":3.14,"Dagannoth Supreme":319,"Dagannoth Supreme_ehb":3.19,"Deranged Archaeologist":0,"General Graardor":821,"General Graardor_ehb":14.927272727272728,"Giant Mole":126,"Giant Mole_ehb":1.26,"Grotesque Guardians":232,"Grotesque Guardians_ehb":6.444444444444445,"Hespori":0,"Kalphite Queen":67,"Kalphite Queen_ehb":1.34,"King Black Dragon":0,"King Black Dragon_ehb":0,"Kraken":3194,"Kraken_ehb":31.94,"KreeArra":673,"KreeArra_ehb":16.825,"Kril Tsutsaroth":664,"Kril Tsutsaroth_ehb":10.215384615384615,"Mimic":1,"Obor":0,"Sarachnis":0,"Sarachnis_ehb":0,"Scorpia":0,"Scorpia_ehb":0,"Skotizo":51,"Skotizo_ehb":1.1333333333333333,"The Gauntlet":0,"The Gauntlet_ehb":0,"The Corrupted Gauntlet":107,"The Corrupted Gauntlet_ehb":15.285714285714286,"Theatre of Blood":0,"Theatre of Blood_ehb":0,"Thermonuclear Smoke Devil":1042,"Thermonuclear Smoke Devil_ehb":8.336,"TzKal-Zuk":0,"TzKal-Zuk_ehb":0,"TzTok-Jad":11,"TzTok-Jad_ehb":5.5,"Venenatis":92,"Venenatis_ehb":1.84,"Vetion":0,"Vetion_ehb":0,"Vorkath":1882,"Vorkath_ehb":55.35294117647059,"Wintertodt":196,"Zalcano":0,"Zulrah":1973,"Zulrah_ehb":49.325,"The Nightmare":0,"The Nightmare_ehb":0,"Soul Wars Zeal":0,"Tempoross":0,"Theatre of Blood Challenge Mode":0,"Theatre of Blood Challenge Mode_ehb":0,"Bounty Hunter Hunter":0,"Bounty Hunter Rogue":0,"Phosanis Nightmare":0,"Phosanis Nightmare_ehb":0,"Nex":1041,"Nex_ehb":80.07692307692308,"Rift":58,"PvP Arena":0,"Tombs of Amascut":134,"Tombs of Amascut_ehb":38.285714285714285,"Tombs of Amascut Expert":357,"Tombs of Amascut Expert_ehb":119,"Ehb":851.3623,"Im_ehb":0}}'
old_player_resp = b'\r\n{"data":{"info":{"Username":"Weapons","Country":"-","Game mode":0,"Cb-3":0,"F2p":0,"Banned":0,"Disqualified":0,"Clan preference":null,"Last checked":"2022-12-05 20:32:52","Last checked unix":1670272372},"Date":"2022-11-14 09:50:40","Overall":308376211,"Overall_rank":141172,"Overall_level":2066,"Overall_ehp":518.1998371928617,"Attack":27641618,"Attack_rank":23992,"Attack_level":99,"Attack_ehp":0,"Defence":17618410,"Defence_rank":54273,"Defence_level":99,"Defence_ehp":42.47507836107675,"Strength":33603881,"Strength_rank":32338,"Strength_level":99,"Strength_ehp":0,"Hitpoints":56518945,"Hitpoints_rank":19572,"Hitpoints_level":99,"Hitpoints_ehp":0.282594725,"Ranged":62977153,"Ranged_rank":16130,"Ranged_level":99,"Ranged_ehp":23.16263943703979,"Prayer":5519613,"Prayer_rank":146580,"Prayer_level":90,"Prayer_ehp":3.0664516666666666,"Magic":20253442,"Magic_rank":50916,"Magic_level":99,"Magic_ehp":0.10126721,"Cooking":5463394,"Cooking_rank":391905,"Cooking_level":90,"Cooking_ehp":7.430515606914457,"Woodcutting":6239478,"Woodcutting_rank":175725,"Woodcutting_level":91,"Woodcutting_ehp":36.57806247608179,"Fletching":7206815,"Fletching_rank":225423,"Fletching_level":93,"Fletching_ehp":0.036034075,"Fishing":3270716,"Fishing_rank":318246,"Fishing_level":85,"Fishing_ehp":28.08621180091648,"Firemaking":4924605,"Firemaking_rank":370864,"Firemaking_level":89,"Firemaking_ehp":9.306722078504851,"Crafting":5371583,"Crafting_rank":186704,"Crafting_level":90,"Crafting_ehp":18.88636403442318,"Smithing":3649162,"Smithing_rank":179488,"Smithing_level":86,"Smithing_ehp":10.4357,"Mining":3302885,"Mining_rank":203562,"Mining_level":85,"Mining_ehp":33.70916451142666,"Herblore":5587170,"Herblore_rank":123335,"Herblore_level":90,"Herblore_ehp":14.122894347898734,"Agility":1806889,"Agility_rank":268873,"Agility_level":79,"Agility_ehp":34.063574751937715,"Thieving":2032279,"Thieving_rank":284985,"Thieving_level":80,"Thieving_ehp":15.875563939393938,"Slayer":20569214,"Slayer_rank":18699,"Slayer_level":99,"Slayer_ehp":219.2718836228897,"Farming":9927420,"Farming_rank":189841,"Farming_level":96,"Farming_ehp":9.740989091478696,"Runecraft":1104359,"Runecraft_rank":264083,"Runecraft_level":74,"Runecraft_ehp":5.047783333333333,"Hunter":815990,"Hunter_rank":524979,"Hunter_level":71,"Hunter_ehp":3.2479673695685145,"Construction":2971190,"Construction_rank":203423,"Construction_level":84,"Construction_ehp":3.2723747533104155,"Ehp":518.1998,"Ehp_rank":84498,"Im_ehp":0,"Lvl3_ehp":0,"F2p_ehp":0,"Uim_ehp":0,"Clue_all":243,"Clue_beginner":0,"Clue_easy":2,"Clue_medium":6,"Clue_hard":153,"Clue_elite":71,"Clue_master":11,"LMS":0,"Abyssal Sire":685,"Abyssal Sire_ehb":15.222222222222221,"Alchemical Hydra":2219,"Alchemical Hydra_ehb":67.24242424242425,"Barrows Chests":277,"Bryophyta":0,"Callisto":0,"Callisto_ehb":0,"Cerberus":1503,"Cerberus_ehb":24.639344262295083,"Chambers of Xeric":724,"Chambers of Xeric_ehb":241.33333333333334,"Chambers of Xeric Challenge Mode":62,"Chambers of Xeric Challenge Mode_ehb":25.833333333333336,"Chaos Elemental":0,"Chaos Elemental_ehb":0,"Chaos Fanatic":0,"Chaos Fanatic_ehb":0,"Commander Zilyana":95,"Commander Zilyana_ehb":1.7272727272727273,"Corporeal Beast":105,"Corporeal Beast_ehb":1.75,"Crazy Archaeologist":0,"Dagannoth Prime":253,"Dagannoth Prime_ehb":2.53,"Dagannoth Rex":314,"Dagannoth Rex_ehb":3.14,"Dagannoth Supreme":319,"Dagannoth Supreme_ehb":3.19,"Deranged Archaeologist":0,"General Graardor":821,"General Graardor_ehb":14.927272727272728,"Giant Mole":126,"Giant Mole_ehb":1.26,"Grotesque Guardians":232,"Grotesque Guardians_ehb":6.444444444444445,"Hespori":0,"Kalphite Queen":67,"Kalphite Queen_ehb":1.34,"King Black Dragon":0,"King Black Dragon_ehb":0,"Kraken":3194,"Kraken_ehb":31.94,"KreeArra":673,"KreeArra_ehb":16.825,"Kril Tsutsaroth":658,"Kril Tsutsaroth_ehb":10.123076923076923,"Mimic":1,"Obor":0,"Sarachnis":0,"Sarachnis_ehb":0,"Scorpia":0,"Scorpia_ehb":0,"Skotizo":46,"Skotizo_ehb":1.0222222222222221,"The Gauntlet":0,"The Gauntlet_ehb":0,"The Corrupted Gauntlet":106,"The Corrupted Gauntlet_ehb":15.142857142857142,"Theatre of Blood":0,"Theatre of Blood_ehb":0,"Thermonuclear Smoke Devil":1042,"Thermonuclear Smoke Devil_ehb":8.336,"TzKal-Zuk":0,"TzKal-Zuk_ehb":0,"TzTok-Jad":11,"TzTok-Jad_ehb":5.5,"Venenatis":92,"Venenatis_ehb":1.84,"Vetion":0,"Vetion_ehb":0,"Vorkath":1882,"Vorkath_ehb":55.35294117647059,"Wintertodt":196,"Zalcano":0,"Zulrah":1973,"Zulrah_ehb":49.325,"The Nightmare":0,"The Nightmare_ehb":0,"Soul Wars Zeal":0,"Tempoross":0,"Theatre of Blood Challenge Mode":0,"Theatre of Blood Challenge Mode_ehb":0,"Bounty Hunter Hunter":0,"Bounty Hunter Rogue":0,"Phosanis Nightmare":0,"Phosanis Nightmare_ehb":0,"Nex":965,"Nex_ehb":74.23076923076923,"Rift":58,"PvP Arena":0,"Tombs of Amascut":132,"Tombs of Amascut_ehb":37.714285714285715,"Tombs of Amascut Expert":300,"Tombs of Amascut Expert_ehb":100,"Ehb":817.9317,"Im_ehb":0}}'

skills = ["Ranged","Magic","Hitpoints","Slayer","Defence","Attack","Strength","Construction","Prayer","Hunter","Firemaking","Herblore","Fletching","Cooking","Thieving","Smithing","Farming","Crafting","Fishing","Woodcutting","Agility","Mining","Runecraft"]
bosses = ["Abyssal Sire","Alchemical Hydra","Barrows Chests","Bryophyta","Callisto","Cerberus","Chambers of Xeric","Chambers of Xeric Challenge Mode","Chaos Elemental","Chaos Fanatic","Commander Zilyana","Corporeal Beast","Crazy Archaeologist","Dagannoth Prime","Dagannoth Rex","Dagannoth Supreme","Deranged Archaeologist","General Graardor","Giant Mole","Grotesque Guardians","Hespori","Kalphite Queen","King Black Dragon","Kraken","KreeArra","Kril Tsutsaroth","Mimic", "Obor","Sarachnis","Scorpia","Skotizo","The Gauntlet","The Corrupted Gauntlet","Theatre of Blood","Thermonuclear Smoke Devil","TzKal-Zuk","TzTok-Jad","Venenatis","Vetion","Vorkath","Wintertodt","Zalcano","Zulrah","The Nightmare","Tempoross","Theatre of Blood Challenge Mode","Phosanis Nightmare","Nex","Rift","Tombs of Amascut","Tombs of Amascut Expert","Phantom Muspah", "Artio", "Calvarion", "Spindel", "Duke Sucellus", "The Whisperer", "Vardorvis", "The Leviathan", "Scurrius", "Colosseum Glory", "Lunar Chests", "Sol Heredit"]

class Achievement():
    def __init__(self, entry: dict):
        self.username = entry["Username"]
        self.date = entry["Date"]
        self.skill = entry["Skill"]
        self.type = entry["Type"]
        self.xp = f'{entry["Xp"]:,}'

    def __eq__(self, other):
        return self.username == other.username and self.date == other.date and self.skill == other.skill and self.type == other.type and self.xp == other.xp

    def __repr__(self) -> str:
        rtn_str = f"{self.username}" 
        if self.type == "Pvm" and not("Clue" in self.skill or "Ehb" in self.skill or "Colosseum Glory" in self.skill):
            rtn_str += f" has reached {self.xp} in {self.skill} kills!" 
        elif self.type == "Pvm" and ("Clue" in self.skill):
            idx = self.skill.find("Clue_") + 5
            rtn_str += f" has completed {self.xp} {self.skill[idx:]} clues!" 
        elif self.type == "Skill" and ("Ehp" in self.skill):
            rtn_str += f" has reached {self.xp} EHP" 
        elif self.type == "Pvm" and ("Ehb" in self.skill):
            rtn_str += f" has reached {self.xp} EHB" 
        elif self.type == "Skill" and not ("Ehp" in self.skill):
            if self.xp == "99" :
                rtn_str += f" has reached level {self.xp} in {self.skill}"
            else:
                rtn_str += f" has reached {self.xp} xp in {self.skill}!" 
        else:
            rtn_str += f" has reached {self.xp} in {self.skill}!"
        return rtn_str

class TempleOsrs():
    
    def __init__(self, id: str="2288"):
        self.id = id
        self.__last_current_achievements = []
        self.logger = logging.getLogger("TempleOsrs")

    async def get_cc_current_achievements(self, debug: bool=False) -> tuple:
        if not debug:
            #resp = requests.get("https://templeosrs.com/api/group_achievements.php", params={'id':self.id})
            resp = await self.__call_api("https://templeosrs.com/api/group_achievements.php", {'id':self.id})
            if resp.ok:
                items = self.__parse_achievements(resp.content)
                return self.__compare_new_current_achievements(items)
            else:
                self.logger.error(f"Request to templeosrs failed with status code: {resp.status_code} with reason: {resp.reason}")
                return [], False
        else:

            resp = resp_test
            items = self.__parse_achievements(resp)
            
            
            for item in items:
                print(item)

        
    def __parse_achievements(self, response: str) -> list:
        # first convert from binary
        try:
            response = json.loads(response.decode())
            items = []
            # print(response["data"])
            for x in response["data"]:
                items.append(Achievement(x))
            return items
        except Exception as e:
            self.logger.error(f"Api response can't be decoded with error: {e}")

    def __read_time_file(self, time_file:str=FILE_LOCATION)->str:
        time_in_file = ""
        
        with open(time_file, "r") as tf:
            time_in_file = tf.readline()
            time_in_file = time_in_file.strip()
            unix = tf.readline()
            unix.strip()
        if len(unix)<1:
            unix = int(time.time()) - 2592000
        return time_in_file, unix
    
    def __write_time_file(self,time_to_write:str, unix_time_to_write:str, time_file:str=FILE_LOCATION)->None:
        with open(time_file, "w") as tf:
            tf.writelines([str(time_to_write),"\n", str(unix_time_to_write)])

    def __compare_new_current_achievements(self, new_current: list)-> tuple:
        new_list = []
        new_current_list = []
        last_check_time, unix_time = self.__read_time_file()

        monthly_check = ((int(time.time()) - int(unix_time)) / 2592000) >= 1
        
        if new_current[0].date <= last_check_time:
            # Nothing to do, no new elements
            pass
        else:
            self.__write_time_file(time_to_write=new_current[0].date, unix_time_to_write=int(unix_time))
            for achiev in new_current:
                if achiev not in self.__last_current_achievements and achiev.date > last_check_time:
                    new_list.append(achiev)
                    new_current_list.append(achiev)
                elif len(new_list) < 20:
                    new_current_list.append(achiev) 
            # we only want to print NEW achievements, but we want to keep track of all of the ones the api
            # will return to us, so the next time we poll, we don't print ones we have already printed!
            self.__last_current_achievements = new_current_list
        return new_list, monthly_check

    async def __call_api(self, url: str, params: dict):
        loop = asyncio.get_event_loop()
        future1 = loop.run_in_executor(None,  partial(requests.get, url, params=params))
        resp = await future1
        #resp = requests.get(url, params=params)
        try:
            resp.raise_for_status()
        except HTTPError as httpError:
            self.logger.exception(f"Call API Method threw HTTP Error: {httpError}")
        # a short sleep to give a chance for the bot to call home (avoid weird random errors popping up >:/)
        await asyncio.sleep(0.5)
        return resp

    async def __check_to_sleep(self, count:int, seconds_to_sleep:int=45) -> None:
        if count % 50 == 0:
            self.logger.info(f"Reached 50 requests, sleeping for {seconds_to_sleep} seconds")
            await asyncio.sleep(seconds_to_sleep)
            
    async def get_cc_monthly_achievements(self, debug: bool=False) -> list:
        lists = [[] for i in range(5)]
        metric = ["Overall_level", "Overall", "boss", "Ehb", "Ehp"]
        count = 0
        if not debug:
            #resp = requests.get("https://templeosrs.com/api/groupmembers.php", params={'id':self.id})
            resp = await self.__call_api("https://templeosrs.com/api/groupmembers.php", {'id':self.id})
            if resp.ok:
                members = self.__parse_members(resp.content)
                self.logger.info(f"Retrieved monthly group members list, len: {len(members)}")
                time_now, unix_time_then = self.__read_time_file(FILE_LOCATION)
                unix_time_now = int(time.time())
                self.logger.info(f"Times are: time_now: {time_now}, unix_time_then: {unix_time_then} and unix_time_now: {unix_time_now}")
                for member in members:
                    
                    resp_old = await self.__call_api("https://templeosrs.com/api/player_stats.php", {'player':member, 'bosses':'1','date':unix_time_then})
                    count += 1
                    old_player_resp_parsed = self.__parse_members(resp_old.content)
                    # print(member,count)
                    await self.__check_to_sleep(count)
                    
                    if resp_old.ok and "data" in old_player_resp_parsed:
                        
                        resp_new = await self.__call_api("https://templeosrs.com/api/player_stats.php", {'player':member, 'bosses':'1','date':unix_time_now})
                        count += 1
                        new_player_resp_parsed = self.__parse_members(resp_new.content)
                        #print(member, count)
                        await self.__check_to_sleep(count)
                        
                        if resp_new.ok and "data" in new_player_resp_parsed:
                            
                            for i, metric_name in enumerate(metric):
                                lists[i].append(self.__calc_player_difference(metric_name, old_player_resp_parsed, new_player_resp_parsed))
                # sort all lists from high to low
                lists = [sorted(li,key= lambda x: x[1], reverse=True) for li in lists if li[1] is not None]

                list_of_strings = [f"The top 5 players in the CC for the period: {datetime.datetime.fromtimestamp(int(unix_time_then)).strftime('%Y/%m/%d')} - {datetime.datetime.fromtimestamp(unix_time_now).strftime('%Y/%m/%d')}"]
                
                for i, metric_name in enumerate(metric):
                    list_of_strings.append(self.__create_monthly_message(lists[i],metric_name))

                self.__write_time_file(time_now, str(unix_time_now), FILE_LOCATION)

                # self.logger.info(f"output strings: {list_of_strings}")

                return list_of_strings
                
            else:
                self.logger.error(f"Request to templeosrs failed with status code: {resp.status_code} with reason: {resp.reason}")
                return []
        else:

            resp = members_resp
            print(len(resp))
            items = self.__parse_members(resp)
            member_0 = items[0]
            
            #resp = requests.get("https://templeosrs.com/api/player_stats.php", params={'player':member_0, 'bosses':'1','date':'1670088882'})
            resp = old_player_resp
            
            old_player_resp_parsed = self.__parse_members(resp)
            
            #if resp.ok:
            #    print(resp.content)
            #resp1 = requests.get("https://templeosrs.com/api/player_stats.php", params={'player':member_0, 'bosses':'1','date':int(time.time())})
            resp1 = new_player_resp
            new_player_resp_parsed = self.__parse_members(resp1)
            #if resp1.ok:
            #    print(resp1.content)

            for i, metric_name in enumerate(metric):
                lists[i].append(self.__calc_player_difference(metric_name, old_player_resp_parsed, new_player_resp_parsed))
            
            lists = [sorted(li,key= lambda x: x[1], reverse=True) for li in lists]

            print(lists[0])
            print(lists[1])
            print(lists[2])
            print(lists[3])
            print(lists[4])

            list_of_strings = [f"The top 5 players in the CC for the period: {datetime.datetime.fromtimestamp(1670088882).strftime('%Y/%m/%d')} - {datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y/%m/%d')}"]
            for i, metric_name in enumerate(metric):
                list_of_strings.append(self.__create_monthly_message(lists[i],metric_name))

            for i in list_of_strings:
                print(i)

    def __calc_player_difference(self, metric: str, old_player: dict, new_player:dict) -> tuple:
        count = 0
        try:
            if metric == "boss":
                for boss in bosses:
                    count += int(new_player["data"].get(boss, 0)) - int(old_player["data"].get(boss, 0))
            else:
                count = new_player["data"].get(metric, 0) - old_player["data"].get(metric, 0)
            return (new_player["data"]["info"]["Username"], count)
        except KeyError as ke:
            self.logger.error(f"There was a key error while calculating player difference: {ke} the data was: {new_player} \n and: {old_player}")

    
    def __parse_members(self, response: str) -> dict:
        # convert from binary
        try:
            response = json.loads(response.decode())
            
            return response
        except Exception as e:
            self.logger.error(f"Api response can't be decoded with error: {e} in __parse_members func")

    def __create_monthly_message(self, to_analyse: list, metric: str, num_to_highlight:int = 5 ) -> str:
        
        str_to_return = ""
        
        if num_to_highlight > len(to_analyse):
            num_to_highlight = len(to_analyse)
        match metric:
            case "Overall_level":
                str_to_return = f"```Number of levels gained in the last month by the top {num_to_highlight} players in the CC: \n\n"
                for i in range(num_to_highlight):
                    str_to_return += f'{to_analyse[i][0]} - {to_analyse[i][1]:,} levels\n'
                str_to_return +="```"
            case "Overall":
                str_to_return = f"```(Most) Total exp gained in the last month by the top {num_to_highlight} players in the CC: \n\n"
                for i in range(num_to_highlight):
                    str_to_return += f'{to_analyse[i][0]} - {to_analyse[i][1]:,} EXP\n'
                str_to_return +="```"
            case "boss":
                str_to_return = f"```(Most) boss kc gained in the last month by the top {num_to_highlight} players in the CC: \n\n"
                for i in range(num_to_highlight):
                    str_to_return += f'{to_analyse[i][0]} - {to_analyse[i][1]:,} total KC\n'
                str_to_return +="```"
            case "Ehb":
                str_to_return = f"```(Most) efficient boss hours gained in the last month by the top {num_to_highlight} players in the CC: \n\n"
                for i in range(num_to_highlight):
                    str_to_return += f'{to_analyse[i][0]} - {to_analyse[i][1]:,.3f} EHB\n'
                str_to_return +="```"
            case "Ehp":
                str_to_return = f"```(Most) efficient hours played in the last month by the top {num_to_highlight} players in the CC: \n\n"
                for i in range(num_to_highlight):
                    str_to_return += f'{to_analyse[i][0]} - {to_analyse[i][1]:,.3f} EHP\n'
                str_to_return +="```"
        return str_to_return

    async def cheat(self):
        t = time.time()
        resp = await self.__call_api("https://templeosrs.com/api/player_stats.php", {'player':"iamxerxes", 'bosses':'1','date':t})
        print(resp.text)


if __name__ == "__main__":
   #print(int(time.time()))
    
    #print(str(int(time.time())))
    TO = TempleOsrs()
    #TO.get_cc_monthly_achievements(debug=True)
    asyncio.run(TO.cheat())
    
    
    