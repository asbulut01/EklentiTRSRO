from phBot import *
from threading import Timer
import phBotChat
import QtBind
import struct
import random
import json
import os
import sqlite3
import urllib.request

name = 'EsyaBildir'
version = 2.2
NewestVersion = 0

gui = QtBind.init(__name__, name)

tbxLeaders = QtBind.createLineEdit(gui,"",470,41,110,20)
lstLeaders = QtBind.createList(gui,470,62,110,70)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked'," Lider Ekle ",581,39)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked'," Lider Sil ",581,61)
metaby = QtBind.createLabel(gui,'edited by hakankahya\n Special THX TheMoB',475,200)
metaby2 = QtBind.createLabel(gui,'Hata ve Öneriler için\n Discord = hakankahya ',475,150)
lstInfo = QtBind.createList(gui,15,42,450,220)
btnkarakter = QtBind.createButton(gui,'btnkarakter_clicked'," Karakter Bilgi ",15,11)
btnelixir = QtBind.createButton(gui,'btnelixir_clicked'," Elixir/Enhancer Bilgi ",91,11)
btnevent = QtBind.createButton(gui,'btnevent_clicked'," Event Bilgi ",197,11)
btncoin = QtBind.createButton(gui,'btncoin_clicked'," Coin Bilgi ",272,11)
btnstone = QtBind.createButton(gui,'btnstone_clicked'," Stone Bilgi ",347,11)
btnfgw = QtBind.createButton(gui,'btnfgw_clicked'," FGW Bilgi ",422,11)

def btnkarakter_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'- ENV : Envanterin boş yuvasını bildirir.\n- GOLD : Suanki Altını Bildirir.\n- EXP : Suanki LV ve EXP bildirir.\n- SP : Suan ki SP Miktarını belirtir.\n- JOBEXP : JOB EXP bildirir.\n- KESE : Meslek kesesindeki boşluğu bildirir.(Uzmanlik)')

def btnelixir_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'     "Verilen Komutlar Envanter, Pet ve Deponuzu Kontrol Etmektedir."\n- INCELX : Incomplete Intensifying Elixir miktarını bildirir.\n- 8ELX : Lv.8 Intensifying Elixir miktarını bildirir.\n- 9ELX : Lv.9 Intensifying Elixir miktarını bildirir.\n- 10ELX : Lv.10 Intensifying Elixir miktarını bildirir.\n- 11ELX : Lv.11 Intensifying Elixir miktarını bildirir.\n- ENH12 : 12th Grade Enhancer miktarını bildirir.\n- ENH13 : 13th Grade Enhancer miktarını bildirir.\n- ENH14 : 14th Grade Enhancer miktarını bildirir.\n- ENH15 : 15th Grade Enhancer miktarını bildirir.\n- ENH16 : 16th Grade Enhancer miktarını bildirir.\n- ENH17 : 17th Grade Enhancer miktarını bildirir.')

def btnevent_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'     "Verilen Komutlar Envanter, Pet ve Deponuzu Kontrol Etmektedir."\n- FLOWER : Tüm ciceklerin miktarını bildirir.\n- ZERK : Berserker Regeneration Potion miktarını bildirir.\n- PANDORA : Pandora Box miktarını bildirir.\n- MS : Monster Summon Scroll Miktarını Bildirir.\n- CATA : Alchemy Catalyst miktarını bildirir.\n- ICE : Dondurma(event) miktarını bildirir.\n- LBOX : Lucky Box miktarını bildirir.\n- PLEDGE : Pledge Sag ve Sol miktarını bildirir.\n- ALI : AliBaba Seal miktarını bildirir.\n- RUBBER : Rubber Piece miktarını bildirir.\n- THANKS : Thanks event Harf miktarını bildirir.\n- FLAKE : Snow Flake miktarını bildirir.\n- HLWN : Halloween Caddy miktarını bildirir.')

def btncoin_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'     "Verilen Komutlar Envanter, Pet ve Deponuzu Kontrol Etmektedir."\n- COIN : Envanterdeki Gold/Silver/Iron/Copper/Arena Coin miktarını bildirir.\n- COMBATI : Coin of Combativeness (Party) ve Coin of Combativeness (Individual)\nMiktarını bildirir.')

def btnstone_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'     "Verilen Komutlar Envanter, Pet ve Deponuzu Kontrol Etmektedir."\n- 8BLUE : 8DG Blue Stonelerin Miktarını bildirir.\n- 8BLUE2 : 8DG Blue Stonelerin Miktarını bildirir.\n- 9BLUE : 9DG Blue Stonelerin Miktarını bildirir.\n- 9BLUE2 : 9DG Blue Stonelerin Miktarını bildirir.\n- 10BLUE : 10DG Blue Stonelerin Miktarını bildirir.\n- 10BLUE2 : 10DG Blue Stonelerin Miktarını bildirir.\n- 11BLUE : 11DG Blue Stonelerin Miktarını bildirir.\n- 11BLUE2 : 11DG Blue Stonelerin Miktarını bildirir.\n- 8STAT : 8DG Stat Stonelerin Miktarını bildirir.\n- 8STAT2 : 8DG Stat Stonelerin Miktarını bildirir.\n- 9STAT : 9DG Stat Stonelerin Miktarını bildirir.\n- 9STAT2 : 9DG Stat Stonelerin Miktarını bildirir.\n- 10STAT : 10DG Stat Stonelerin Miktarını bildirir.')
    QtBind.append(gui,lstInfo,'- 10STAT2 : 10DG Stat Stonelerin Miktarını bildirir.\n- 11STAT : 11DG Stat Stonelerin Miktarını bildirir.\n- 11STAT2 : 11DG Stat Stonelerin Miktarını bildirir.\n- 8LUCK : 8DG Luck Stonelerin Miktarını bildirir.\n- 9LUCK : 9DG Luck Stonelerin Miktarını bildirir.\n- 10LUCK : 10DG Luck Stonelerin Miktarını bildirir.\n- 11LUCK : 11DG Luck Stonelerin Miktarını bildirir.\n- 8STEADY : 8DG Steady Stonelerin Miktarını bildirir.\n- 9STEADY : 9DG Steady Stonelerin Miktarını bildirir.\n- 10STEADY : 10DG Steady Stonelerin Miktarını bildirir.\n- 11STEADY : 11DG Steady Stonelerin Miktarını bildirir.')

def btnfgw_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'     "Verilen Komutlar Envanter, Pet ve Deponuzu Kontrol Etmektedir."\n- 8FGW1 : (8DG SUN) Kolay Düşen Kartların miktarını bildirir.\n- 8FGW2 : (8DG SUN) Zor Düşen Kartların miktarını bildirir.\n- 9FGW1 : (9DG SUN) Kolay Düşen Kartların miktarını bildirir.\n- 9FGW2 : (9DG SUN) Zor Düşen Kartların miktarını bildirir.\n- 10FGW1 : (10DG MOON) Kolay Düşen Kartların miktarını bildirir.\n- 10FGW2 : (10DG MOON) Zor Düşen Kartların miktarını bildirir.\n- 11FGW1 : (11DG EGYPY A) Kolay Düşen Kartların miktarını bildirir.\n- 11FGW2 : (11DG EGPTY A) Zor Düşen Kartların miktarını bildirir.')

def connected():
	global inGame
	inGame = None

def joined_game():
	loadConfigs()

def getPath():
	return get_config_dir()+name+"\\"

def getConfig():
	return getPath()+inGame['server'] + "_" + inGame['name'] + ".json"

def isJoined():
	global inGame
	inGame = get_character_data()
	if not (inGame and "name" in inGame and inGame["name"]):
		inGame = None
	return inGame

def loadDefaultConfig():
	QtBind.clear(gui,lstLeaders)

def loadConfigs():
	loadDefaultConfig()
	if isJoined():
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)
			if "Leaders" in data:
				for nickname in data["Leaders"]:
					QtBind.append(gui,lstLeaders,nickname)

def btnAddLeader_clicked():
	if inGame:
		player = QtBind.text(gui,tbxLeaders)
		if player and not lstLeaders_exist(player):
			data = {}
			if os.path.exists(getConfig()):
				with open(getConfig(), 'r') as f:
					data = json.load(f)
			if not "Leaders" in data:
				data['Leaders'] = []
			data['Leaders'].append(player)
			with open(getConfig(),"w") as f:
				f.write(json.dumps(data, indent=4, sort_keys=True))
			QtBind.append(gui,lstLeaders,player)
			QtBind.setText(gui, tbxLeaders,"")
			log('Eklenti [EsyaBildir]: Lider Eklendi. ['+player+']')

def btnRemLeader_clicked():
	if inGame:
		selectedItem = QtBind.text(gui,lstLeaders)
		if selectedItem:
			if os.path.exists(getConfig()):
				data = {"Leaders":[]}
				with open(getConfig(), 'r') as f:
					data = json.load(f)
				try:
					data["Leaders"].remove(selectedItem)
					with open(getConfig(),"w") as f:
						f.write(json.dumps(data, indent=4, sort_keys=True))
				except:
					pass 
			QtBind.remove(gui,lstLeaders,selectedItem)
			log('Eklenti [EsyaBildir]: Lider Silindi. ['+selectedItem+']')

def lstLeaders_exist(nickname):
	nickname = nickname.lower()
	players = QtBind.getItems(gui,lstLeaders)
	for i in range(len(players)):
		if players[i].lower() == nickname:
			return True
	return False

def checkInv(arg, player):
    weapon1 = 0
    weapon2 = 0
    weapon3 = 0
    weapon4 = 0
    weapon5 = 0
    eweapon1 = 0
    eweapon2 = 0
    eweapon3 = 0
    eweapon4 = 0
    eweapon5 = 0
    eweapon6 = 0
    protector1 = 0
    protector2 = 0
    protector3 = 0
    protector4 = 0
    protector5 = 0
    eprotector1 = 0
    eprotector2 = 0
    eprotector3 = 0
    eprotector4 = 0
    eprotector5 = 0
    eprotector6 = 0
    accessory1 = 0
    accessory2 = 0
    accessory3 = 0
    accessory4 = 0
    accessory5 = 0
    eaccessory1 = 0
    eaccessory2 = 0
    eaccessory3 = 0
    eaccessory4 = 0
    eaccessory5 = 0
    eaccessory6 = 0
    shield1 = 0
    shield2 = 0
    shield3 = 0
    shield4 = 0
    shield5 = 0
    eshield1 = 0
    eshield2 = 0
    eshield3 = 0
    eshield4 = 0
    eshield5 = 0
    eshield6 = 0
    arena = 0
    qgold = 0
    silver = 0
    iron = 0
    copper = 0
    flower1 = 0
    flower2 = 0
    flower3 = 0
    flower4 = 0
    flower5 = 0
    catalyst = 0
    str8 = 0
    str9 = 0
    str10 = 0
    str11 = 0
    int8 = 0
    int9 = 0
    int10 = 0
    int11 = 0
    master8 = 0
    master9 = 0
    master10 = 0
    master11 = 0
    strikes8 = 0
    strikes9 = 0
    strikes10 = 0
    strikes11 = 0
    discipline8 = 0
    discipline9 = 0
    discipline10 = 0
    discipline11 = 0
    penetration8 = 0
    penetration9 = 0
    penetration10 = 0
    penetration11 = 0
    dodging8 = 0
    dodging9 = 0
    dodging10 = 0
    dodging11 = 0
    stamina8 = 0
    stamina9 = 0
    stamina10 = 0
    stamina11 = 0
    magic8 = 0
    magic9 = 0
    magic10 = 0
    magic11 = 0
    fogs8 = 0
    fogs9 = 0
    fogs10 = 0
    fogs11 = 0
    air8 = 0
    air9 = 0
    air10 = 0
    air11 = 0
    fire8 = 0
    fire9 = 0
    fire10 = 0
    fire11 = 0
    immunity8 = 0
    immunity9 = 0
    immunity10 = 0
    immunity11 = 0
    revival8 = 0
    revival9 = 0
    revival10 = 0
    revival11 = 0
    courage8 = 0
    courage9 = 0
    courage10 = 0
    courage11 = 0
    warriors8 = 0
    warriors9 = 0
    warriors10 = 0
    warriors11 = 0
    philosophy8 = 0
    philosophy9 = 0
    philosophy10 = 0
    philosophy11 = 0
    meditation8 = 0
    meditation9 = 0
    meditation10 = 0
    meditation11 = 0
    challenge8 = 0
    challenge9 = 0
    challenge10 = 0
    challenge11 = 0
    focus8 = 0
    focus9 = 0
    focus10 = 0
    focus11 = 0
    flesh8 = 0
    flesh9 = 0
    flesh10 = 0
    flesh11 = 0
    life8 = 0
    life9 = 0
    life10 = 0
    life11 = 0
    mind8 = 0
    mind9 = 0
    mind10 = 0
    mind11 = 0
    spirit8 = 0
    spirit9 = 0
    spirit10 = 0
    spirit11 = 0
    dodgings8 = 0
    dodgings9 = 0
    dodgings10 = 0
    dodgings11 = 0
    agility8 = 0
    agility9 = 0
    agility10 = 0
    agility11 = 0
    training8 = 0
    training9 = 0
    training10 = 0
    training11 = 0
    prayer8 = 0
    prayer9 = 0
    prayer10 = 0
    prayer11 = 0
    luckst8 = 0
    steadyst8 = 0
    luckst9 = 0
    steadyst9 = 0
    luckst10 = 0
    steadyst10 = 0
    luckst11 = 0
    steadyst11 = 0
    berserker = 0
    combativeness1 = 0
    combativeness2 = 0
    pandora = 0
    ms = 0
    luckybox = 0
    pledge1 = 0
    pledge2 = 0
    alibabaseal = 0
    rubber = 0
    snowflake = 0
    halloweencandy = 0
    T1 = 0
    T2 = 0
    T3 = 0
    T4 = 0
    T5 = 0
    T6 = 0
    cream = 0
    lamp = 0
    dLamp = 0
    card1 = 0
    card2 = 0
    card3 = 0
    card4 = 0
    card5 = 0
    card6 = 0
    card7 = 0
    card8 = 0
    card9 = 0
    card10 = 0
    card11 = 0
    card12 = 0
    card13 = 0
    card14 = 0
    card15 = 0
    card16 = 0
    card17 = 0
    card18 = 0
    card19 = 0
    card20 = 0
    card21 = 0
    card22 = 0
    card23 = 0
    card24 = 0
    card25 = 0
    card26 = 0
    card27 = 0
    card28 = 0
    card29 = 0
    card30 = 0
    card31 = 0
    card32 = 0
    faded = 0
    sunItems = 0

    inventory = get_inventory()
    storage = get_storage()
    pets = get_pets()
    inventory_items = []
    storage_items = []
    pet_items = []
    if inventory and 'items' in inventory:
        inventory_items = inventory['items'][13:]
    if storage and 'items' in storage:
        storage_items = storage['items']
    if pets:
        for p in pets.keys():
            pet = pets[p]
            if pet['type'] in 'pick':
                pet_items.extend(pet.get('items', []))
    all_items = inventory_items + storage_items + pet_items
    if all_items:
        for item in all_items:
            if item is not None:
                if "Incomplete" in item['name'] and "Weapon" in item['name']:
                    weapon5 += item['quantity']
                if "Incomplete" in item['name'] and "Armor" in item['name']:
                    protector5 += item['quantity']
                if "Incomplete" in item['name'] and "Accessory" in item['name']:
                    accessory5 += item['quantity']
                if "Incomplete" in item['name'] and "Shield" in item['name']:
                    shield5 += item['quantity']
                if "Lv.8" in item['name'] and "Weapon" in item['name']:
                    weapon1 += item['quantity']
                if "Lv.8" in item['name'] and "Armor" in item['name']:
                    protector1 += item['quantity']
                if "Lv.8" in item['name'] and "Accessory" in item['name']:
                    accessory1 += item['quantity']
                if "Lv.8" in item['name'] and "Shield" in item['name']:
                    shield1 += item['quantity']
                if "Lv.9" in item['name'] and "Weapon" in item['name']:
                    weapon2 += item['quantity']
                if "Lv.9" in item['name'] and "Armor" in item['name']:
                    protector2 += item['quantity']
                if "Lv.9" in item['name'] and "Accessory" in item['name']:
                    accessory2 += item['quantity']
                if "Lv.9" in item['name'] and "Shield" in item['name']:
                    shield2 += item['quantity']
                if "Lv.10" in item['name'] and "Weapon" in item['name']:
                    weapon3 += item['quantity']
                if "Lv.10" in item['name'] and "Armor" in item['name']:
                    protector3 += item['quantity']
                if "Lv.10" in item['name'] and "Accessory" in item['name']:
                    accessory3 += item['quantity']
                if "Lv.10" in item['name'] and "Shield" in item['name']:
                    shield3 += item['quantity']
                if "Lv.11" in item['name'] and "Weapon" in item['name']:
                    weapon4 += item['quantity']
                if "Lv.11" in item['name'] and "Armor" in item['name']:
                    protector4 += item['quantity']
                if "Lv.11" in item['name'] and "Accessory" in item['name']:
                    accessory4 += item['quantity']
                if "Lv.11" in item['name'] and "Shield" in item['name']:
                    shield4 += item['quantity']
                if "12th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                    eweapon1 += item['quantity']
                if "12th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                    eprotector1 += item['quantity']
                if "12th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                    eaccessory1 += item['quantity']
                if "12th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                    eshield1 += item['quantity']
                if "13th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                    eweapon2 += item['quantity']
                if "13th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                    eprotector2 += item['quantity']
                if "13th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                    eaccessory2 += item['quantity']
                if "13th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                    eshield2 += item['quantity']
                if "14th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                    eweapon3 += item['quantity']
                if "14th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                    eprotector3 += item['quantity']
                if "14th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                    eaccessory3 += item['quantity']
                if "14th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                    eshield3 += item['quantity']
                if "15th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                    eweapon4 += item['quantity']
                if "15th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                    eprotector4 += item['quantity']
                if "15th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                    eaccessory4 += item['quantity']
                if "15th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                    eshield4 += item['quantity']
                if "16th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                    eweapon5 += item['quantity']
                if "16th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                    eprotector5 += item['quantity']
                if "16th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                    eaccessory5 += item['quantity']
                if "16th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                    eshield5 += item['quantity']
                if "17th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                    eweapon6 += item['quantity']
                if "17th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                    eprotector6 += item['quantity']
                if "17th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                    eaccessory6 += item['quantity']
                if "17th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                    eshield6 += item['quantity']
                if "Flower" in item['name'] and "Evil" in item['name']:
                    flower1 += item['quantity']
                if "Flower" in item['name'] and "Illusion" in item['name']:
                    flower2 += item['quantity']
                if "Flower" in item['name'] and "Life" in item['name']:
                    flower3 += item['quantity']
                if "Flower" in item['name'] and "Energy" in item['name']:
                    flower4 += item['quantity']
                if "Flower" in item['name'] and "Whirling" in item['name']:
                    flower5 += item['quantity']
                if "Coin" in item['name'] and "Arena" in item['name']:
                    arena += item['quantity']
                if "Coin" in item['name'] and "Gold" in item['name']:
                    gold += item['quantity']
                if "Coin" in item['name'] and "Silver" in item['name']:
                    silver += item['quantity']
                if "Coin" in item['name'] and "Iron" in item['name']:
                    iron += item['quantity']
                if "Coin" in item['name'] and "Copper" in item['name']:
                    copper += item['quantity']
                if "Coin of Combativeness" in item['name'] and "Party" in item['name']:
                    combativeness1 += item['quantity']
                if "Coin of Combativeness" in item['name'] and "Individual" in item['name']:
                    combativeness2 += item['quantity']
                if "Alchemy catalyst" in item['name'] and "" in item['name']:
                    catalyst += item['quantity']
                if "Lvl.11" in item['name'] and "Str" in item['name']:
                    str11 += item['quantity']
                if "Lvl.10" in item['name'] and "Str" in item['name']:
                    str10 += item['quantity']
                if "Lvl.9" in item['name'] and "Str" in item['name']:
                    str9 += item['quantity']
                if "Lvl.8" in item['name'] and "Str" in item['name']:
                    str8 += item['quantity']
                if "Lvl.11" in item['name'] and "Int" in item['name']:
                    int11 += item['quantity']
                if "Lvl.10" in item['name'] and "Int" in item['name']:
                    int10 += item['quantity']
                if "Lvl.9" in item['name'] and "Int" in item['name']:
                    int9 += item['quantity']
                if "Lvl.8" in item['name'] and "Int" in item['name']:
                    int8 += item['quantity']
                if "Lvl.11" in item['name'] and "master" in item['name']:
                    master11 += item['quantity']
                if "Lvl.10" in item['name'] and "master" in item['name']:
                    master10 += item['quantity']
                if "Lvl.9" in item['name'] and "master" in item['name']:
                    master9 += item['quantity']
                if "Lvl.8" in item['name'] and "master" in item['name']:
                    master8 += item['quantity']
                if "Lvl.11" in item['name'] and "strikes" in item['name']:
                    strikes11 += item['quantity']
                if "Lvl.10" in item['name'] and "strikes" in item['name']:
                    strikes10 += item['quantity']
                if "Lvl.9" in item['name'] and "strikes" in item['name']:
                    strikes9 += item['quantity']
                if "Lvl.8" in item['name'] and "strikes" in item['name']:
                    strikes8 += item['quantity']
                if "Lvl.11" in item['name'] and "discipline" in item['name']:
                    discipline11 += item['quantity']
                if "Lvl.10" in item['name'] and "discipline" in item['name']:
                    discipline10 += item['quantity']
                if "Lvl.9" in item['name'] and "discipline" in item['name']:
                    discipline9 += item['quantity']
                if "Lvl.8" in item['name'] and "discipline" in item['name']:
                    discipline8 += item['quantity']
                if "Lvl.11" in item['name'] and "penetration" in item['name']:
                    penetration11 += item['quantity']
                if "Lvl.10" in item['name'] and "penetration" in item['name']:
                    penetration10 += item['quantity']
                if "Lvl.9" in item['name'] and "penetration" in item['name']:
                    penetration9 += item['quantity']
                if "Lvl.8" in item['name'] and "penetration" in item['name']:
                    penetration8 += item['quantity']
                if "Lvl.11" in item['name'] and "dodging" in item['name']:
                    dodging11 += item['quantity']
                if "Lvl.10" in item['name'] and "dodging" in item['name']:
                    dodging10 += item['quantity']
                if "Lvl.9" in item['name'] and "dodging" in item['name']:
                    dodging9 += item['quantity']
                if "Lvl.8" in item['name'] and "dodging" in item['name']:
                    dodging8 += item['quantity']
                if "Lvl.11" in item['name'] and "stamina" in item['name']:
                    stamina11 += item['quantity']
                if "Lvl.10" in item['name'] and "stamina" in item['name']:
                    stamina10 += item['quantity']
                if "Lvl.9" in item['name'] and "stamina" in item['name']:
                    stamina9 += item['quantity']
                if "Lvl.8" in item['name'] and "stamina" in item['name']:
                    stamina8 += item['quantity']
                if "Lvl.11" in item['name'] and "magic" in item['name']:
                    magic11 += item['quantity']
                if "Lvl.10" in item['name'] and "magic" in item['name']:
                    magic10 += item['quantity']
                if "Lvl.9" in item['name'] and "magic" in item['name']:
                    magic9 += item['quantity']
                if "Lvl.8" in item['name'] and "magic" in item['name']:
                    magic8 += item['quantity']
                if "Lvl.11" in item['name'] and "fogs" in item['name']:
                    fogs11 += item['quantity']
                if "Lvl.10" in item['name'] and "fogs" in item['name']:
                    fogs10 += item['quantity']
                if "Lvl.9" in item['name'] and "fogs" in item['name']:
                    fogs9 += item['quantity']
                if "Lvl.8" in item['name'] and "fogs" in item['name']:
                    fogs8 += item['quantity']
                if "Lvl.11" in item['name'] and "air" in item['name']:
                    air11 += item['quantity']
                if "Lvl.10" in item['name'] and "air" in item['name']:
                    air11 += item['quantity']
                if "Lvl.9" in item['name'] and "air" in item['name']:
                    air9 += item['quantity']
                if "Lvl.8" in item['name'] and "air" in item['name']:
                    air8 += item['quantity']
                if "Lvl.11" in item['name'] and "fire" in item['name']:
                    fire11 += item['quantity']
                if "Lvl.10" in item['name'] and "fire" in item['name']:
                    fire10 += item['quantity']
                if "Lvl.9" in item['name'] and "fire" in item['name']:
                    fire9 += item['quantity']
                if "Lvl.8" in item['name'] and "fire" in item['name']:
                    fire8 += item['quantity']
                if "Lvl.11" in item['name'] and "immunity" in item['name']:
                    immunity11 += item['quantity']
                if "Lvl.10" in item['name'] and "immunity" in item['name']:
                    immunity10 += item['quantity']
                if "Lvl.9" in item['name'] and "immunity" in item['name']:
                    immunity9 += item['quantity']
                if "Lvl.8" in item['name'] and "immunity" in item['name']:
                    immunity8 += item['quantity']
                if "Lvl.11" in item['name'] and "revival" in item['name']:
                    revival11 += item['quantity']
                if "Lvl.10" in item['name'] and "revival" in item['name']:
                    revival10 += item['quantity']
                if "Lvl.9" in item['name'] and "revival" in item['name']:
                    revival9 += item['quantity']
                if "Lvl.8" in item['name'] and "revival" in item['name']:
                    revival8 += item['quantity']
                if "Lvl.11" in item['name'] and "courage" in item['name']:
                    courage11 += item['quantity']
                if "Lvl.10" in item['name'] and "courage" in item['name']:
                    courage10 += item['quantity']
                if "Lvl.9" in item['name'] and "courage" in item['name']:
                    courage9 += item['quantity']
                if "Lvl.8" in item['name'] and "courage" in item['name']:
                    courage8 += item['quantity']
                if "Lvl.11" in item['name'] and "warriors" in item['name']:
                    warriors11 += item['quantity']
                if "Lvl.10" in item['name'] and "warriors" in item['name']:
                    warriors10 += item['quantity']
                if "Lvl.9" in item['name'] and "warriors" in item['name']:
                    warriors9 += item['quantity']
                if "Lvl.8" in item['name'] and "warriors" in item['name']:
                    warriors8 += item['quantity']
                if "Lvl.11" in item['name'] and "philosophy" in item['name']:
                    philosophy11 += item['quantity']
                if "Lvl.10" in item['name'] and "philosophy" in item['name']:
                    philosophy10 += item['quantity']
                if "Lvl.9" in item['name'] and "philosophy" in item['name']:
                    philosophy9 += item['quantity']
                if "Lvl.8" in item['name'] and "philosophy" in item['name']:
                    philosophy8 += item['quantity']
                if "Lvl.11" in item['name'] and "meditation" in item['name']:
                    meditation11 += item['quantity']
                if "Lvl.10" in item['name'] and "meditation" in item['name']:
                    meditation10 += item['quantity']
                if "Lvl.9" in item['name'] and "meditation" in item['name']:
                    meditation9 += item['quantity']
                if "Lvl.8" in item['name'] and "meditation" in item['name']:
                    meditation8 += item['quantity']
                if "Lvl.11" in item['name'] and "challenge" in item['name']:
                    challenge11 += item['quantity']
                if "Lvl.10" in item['name'] and "challenge" in item['name']:
                    challenge10 += item['quantity']
                if "Lvl.9" in item['name'] and "challenge" in item['name']:
                    challenge9 += item['quantity']
                if "Lvl.8" in item['name'] and "challenge" in item['name']:
                    challenge8 += item['quantity']
                if "Lvl.11" in item['name'] and "focus" in item['name']:
                    focus11 += item['quantity']
                if "Lvl.10" in item['name'] and "focus" in item['name']:
                    focus10 += item['quantity']
                if "Lvl.9" in item['name'] and "focus" in item['name']:
                    focus9 += item['quantity']
                if "Lvl.8" in item['name'] and "focus" in item['name']:
                    focus8 += item['quantity']
                if "Lvl.11" in item['name'] and "flesh" in item['name']:
                    flesh11 += item['quantity']
                if "Lvl.10" in item['name'] and "flesh" in item['name']:
                    flesh10 += item['quantity']
                if "Lvl.9" in item['name'] and "flesh" in item['name']:
                    flesh9 += item['quantity']
                if "Lvl.8" in item['name'] and "flesh" in item['name']:
                    flesh8 += item['quantity']
                if "Lvl.11" in item['name'] and "life" in item['name']:
                    life11 += item['quantity']
                if "Lvl.10" in item['name'] and "life" in item['name']:
                    life10 += item['quantity']
                if "Lvl.9" in item['name'] and "life" in item['name']:
                    life9 += item['quantity']
                if "Lvl.8" in item['name'] and "life" in item['name']:
                    life8 += item['quantity']
                if "Lvl.11" in item['name'] and "mind" in item['name']:
                    mind11 += item['quantity']
                if "Lvl.10" in item['name'] and "mind" in item['name']:
                    mind10 += item['quantity']
                if "Lvl.9" in item['name'] and "mind" in item['name']:
                    mind9 += item['quantity']
                if "Lvl.8" in item['name'] and "mind" in item['name']:
                    mind8 += item['quantity']
                if "Lvl.11" in item['name'] and "spirit" in item['name']:
                    spirit11 += item['quantity']
                if "Lvl.10" in item['name'] and "spirit" in item['name']:
                    spirit10 += item['quantity']
                if "Lvl.9" in item['name'] and "spirit" in item['name']:
                    spirit9 += item['quantity']
                if "Lvl.8" in item['name'] and "spirit" in item['name']:
                    spirit8 += item['quantity']
                if "Lvl.11" in item['name'] and "Attribute stone of dodging" in item['name']:
                    dodgings11 += item['quantity']
                if "Lvl.10" in item['name'] and "Attribute stone of dodging" in item['name']:
                    dodgings10 += item['quantity']
                if "Lvl.9" in item['name'] and "Attribute stone of dodging" in item['name']:
                    dodgings9 += item['quantity']
                if "Lvl.8" in item['name'] and "Attribute stone of dodging" in item['name']:
                    dodgings8 += item['quantity']
                if "Lvl.11" in item['name'] and "agility" in item['name']:
                    agility11 += item['quantity']
                if "Lvl.10" in item['name'] and "agility" in item['name']:
                    agility10 += item['quantity']
                if "Lvl.9" in item['name'] and "agility" in item['name']:
                    agility9 += item['quantity']
                if "Lvl.8" in item['name'] and "agility" in item['name']:
                    agility8 += item['quantity']
                if "Lvl.11" in item['name'] and "training" in item['name']:
                    training11 += item['quantity']
                if "Lvl.10" in item['name'] and "training" in item['name']:
                    training10 += item['quantity']
                if "Lvl.9" in item['name'] and "training" in item['name']:
                    training9 += item['quantity']
                if "Lvl.8" in item['name'] and "training" in item['name']:
                    training8 += item['quantity']
                if "Lvl.11" in item['name'] and "prayer" in item['name']:
                    prayer11 += item['quantity']
                if "Lvl.10" in item['name'] and "prayer" in item['name']:
                    prayer10 += item['quantity']
                if "Lvl.9" in item['name'] and "prayer" in item['name']:
                    prayer9 += item['quantity']
                if "Lvl.8" in item['name'] and "prayer" in item['name']:
                    prayer8 += item['quantity']
                if "Magic stone of luck(Lvl.8)" in item['name']:
                    luckst8 += item['quantity']
                if "Magic stone of steady(Lvl.8)" in item['name']:
                    steadyst8 += item['quantity']
                if "Magic stone of luck(Lvl.9)" in item['name']:
                    luckst9 += item['quantity']
                if "Magic stone of steady(Lvl.9)" in item['name']:
                    steadyst9 += item['quantity']
                if "Magic stone of luck(Lvl.10)" in item['name']:
                    luckst10 += item['quantity']
                if "Magic stone of steady(Lvl.10)" in item['name']:
                    steadyst10 += item['quantity']
                if "Magic stone of luck(Lvl.11)" in item['name']:
                    luckst11 += item['quantity']
                if "Magic stone of steady(Lvl.11)" in item['name']:
                    steadyst11 += item['quantity']
                if "Pandora's Box" in item['name']:
                    pandora += item['quantity']
                if "Monster Summon Scroll (ekip kullanir)" in item['name']:
                    ms += item['quantity']
                if "Lucky Box" in item['name']:
                    luckybox += item['quantity']
                if "Pledge of Love(Left)" in item['name']:
                    pledge1 += item['quantity']
                if "Pledge of Love(Right)" in item['name']:
                    pledge2 += item['quantity']
                if "AliBaba Seal" in item['name']:
                    alibabaseal += item['quantity']
                if "Rubber Piece" in item['name']:
                    rubber += item['quantity']
                if "T (Event Item)" in item['name']:
                    T1 += item['quantity']
                if "H (Event Item)" in item['name']:
                    T2 += item['quantity']
                if "A (Event Item)" in item['name']:
                    T3 += item['quantity']
                if "N (Event Item)" in item['name']:
                    T4 += item['quantity']
                if "K (Event Item)" in item['name']:
                    T5 += item['quantity']
                if "S (Event Item)" in item['name']:
                    T6 += item['quantity']
                if "Snow flake" in item['name']:
                    snowflake += item['quantity']
                if "Halloween Candy" in item['name']:
                    halloweencandy += item['quantity']
                if "Berserker Regeneration Potion" in item['name']:
                    berserker += item['quantity']
                if "ITEM_ETC_E090722_" in item['servername'] and "ICECREAM" in item['servername']:
                    cream += item['quantity']
                if "Genie’s Lamp" in item['name']:
                    lamp += item['quantity']
                if "Dirty Lamp" in item['name']:
                    dLamp += item['quantity']
                if "Red tears" in item['name']:
                    card1 += item['quantity']
                if "Western scriptures" in item['name']:
                    card2 += item['quantity']
                if "Togui mask" in item['name']:
                    card3 += item['quantity']
                if "Red talisman" in item['name']:
                    card4 += item['quantity']
                if "Puppet" in item['name']:
                    card5 += item['quantity']
                if "Dull kitchen knife" in item['name']:
                    card6 += item['quantity']
                if "Elder staff" in item['name']:
                    card7 += item['quantity']
                if "Spell paper" in item['name']:
                    card8 += item['quantity']
                if "Fire flower" in item['name']:
                    card9 += item['quantity']
                if "Horned cattle" in item['name']:
                    card10 += item['quantity']
                if "Flame of oblivion" in item['name']:
                    card11 += item['quantity']
                if "Flame paper" in item['name']:
                    card12 += item['quantity']
                if "Hearthstone flame" in item['name']:
                    card13 += item['quantity']
                if "Enchantress necklace" in item['name']:
                    card14 += item['quantity']
                if "Honghaeah armor" in item['name']:
                    card15 += item['quantity']
                if "Fire dragon sword" in item['name']:
                    card16 += item['quantity']
                if "Silver pendant" in item['name']:
                    card17 += item['quantity']
                if "Cobalt emerald" in item['name']:
                    card18 += item['quantity']
                if "Logbook" in item['name']:
                    card19 += item['quantity']
                if "Love letter" in item['name']:
                    card20 += item['quantity']
                if "Portrait of a woman" in item['name']:
                    card21 += item['quantity']
                if "Jewelry box" in item['name']:
                    card22 += item['quantity']
                if "Diamond watch" in item['name']:
                    card23 += item['quantity']
                if "Mermaid’s" in item['name'] and "tears"in item['name']:
                    card24 += item['quantity']
                if "Broken Key" in item['name']:
                    card25 += item['quantity']
                if "Large tong" in item['name']:
                    card26 += item['quantity']
                if "Phantom harp" in item['name']:
                    card27 += item['quantity']
                if "Evil’s" in item['name'] and "heart" in item['name']:
                    card28 += item['quantity']
                if "Vindictive" in item['name'] and "sprit’s bead" in item['name']:
                    card29 += item['quantity']
                if "Hook hand" in item['name']:
                    card30 += item['quantity']
                if "Sereness's" in item['name'] and "tears" in item['name']:
                    card31 += item['quantity']
                if "Commander's" in item['name'] and "patch" in item['name']:
                    card32 += item['quantity']
                if "Faded Bead" in item['name']:
                    faded += item['quantity']
                if 'RARE' in item['servername'] and 'EVENT' not in item['servername'] and 'ARCHEMY' not in item[
                    'servername']:
                    sunItems += 1

    if arg == "ElixirInc":
        phBotChat.Private(player,"Incomplete Weapon " + str(weapon5) + " , Incomplete Armor " + str(protector5) + " , Incomplete Shield " + str(shield5) + " , Incomplete Accessory " + str(accessory5))
    if arg == "Elixir8":
        phBotChat.Private(player,"8DG Elixir; Weapon " + str(weapon1) + " , Armor " + str(protector1) + " , Shield " + str(shield1) + " , Accessory " + str(accessory1))
    if arg == "Elixir9":
        phBotChat.Private(player,"9DG Elixir; Weapon " + str(weapon2) + " , Armor " + str(protector2) + " , Shield " + str(shield2) + " , Accessory " + str(accessory2))
    if arg == "Elixir10":
        phBotChat.Private(player,"10DG Elixir; Weapon " + str(weapon3) + " , Armor " + str(protector3) + " , Shield " + str(shield3) + " , Accessory " + str(accessory3))
    if arg == "Elixir11":
        phBotChat.Private(player,"11DG Elixir; Weapon " + str(weapon4) + " , Armor " + str(protector4) + " , Shield " + str(shield4) + " , Accessory " + str(accessory4))
    if arg == "Enhancer12":
        phBotChat.Private(player,"12DG ENHANCER; Weapon " + str(eweapon1) + " , Armor " + str(eprotector1) + " , Shield " + str(eshield1) + " , Accessory " + str(eaccessory1))
    if arg == "Enhancer13":
        phBotChat.Private(player,"13DG ENHANCER; Weapon " + str(eweapon2) + " , Armor " + str(eprotector2) + " , Shield " + str(eshield2) + " , Accessory " + str(eaccessory2))
    if arg == "Enhancer14":
        phBotChat.Private(player,"14DG ENHANCER; Weapon " + str(eweapon3) + " , Armor " + str(eprotector3) + " , Shield " + str(eshield3) + " , Accessory " + str(eaccessory3))
    if arg == "Enhancer15":
        phBotChat.Private(player,"15DG ENHANCER; Weapon " + str(eweapon4) + " , Armor " + str(eprotector4) + " , Shield " + str(eshield4) + " , Accessory " + str(eaccessory4))
    if arg == "Enhancer16":
        phBotChat.Private(player,"16DG ENHANCER; Weapon " + str(eweapon5) + " , Armor " + str(eprotector5) + " , Shield " + str(eshield5) + " , Accessory " + str(eaccessory5))
    if arg == "Enhancer17":
        phBotChat.Private(player,"17DG ENHANCER; Weapon " + str(eweapon6) + " , Armor " + str(eprotector6) + " , Shield " + str(eshield6) + " , Accessory " + str(eaccessory6))
    if arg == "Flower3":
        phBotChat.Private(player,"Flower; Life " + str(flower3) + " , Energy " + str(flower4) + " , Evil " + str(flower1) + " , Illusion " + str(flower2) + " , Whirling " + str(flower5))
    if arg == "Combatii":
        phBotChat.Private(player,"Coin of Combativeness (Party) " + str(combativeness1) + " , Coin of Combativeness (Individual) " + str(combativeness2))
    if arg == "8Blue":
        phBotChat.Private(player,"8DG STR " + str(str8) + " , INT " + str(int8) + " , MASTER " + str(master8) + " , STRIKES " + str(strikes8) + " , DSCPLNE " + str(discipline8) + " , PNTRTON " + str(penetration8) + " , DODGING " + str(dodging8) + " , STAMINA " + str(stamina8))
    if arg == "9Blue":
        phBotChat.Private(player,"9DG STR " + str(str9) + " , INT " + str(int9) + " , MASTER " + str(master9) + " , STRIKES " + str(strikes9) + " , DSCPLNE " + str(discipline9) + " , PNTRTON " + str(penetration9) + " , DODGING " + str(dodging9) + " , STAMINA " + str(stamina9))
    if arg == "10Blue":
        phBotChat.Private(player,"10DG STR " + str(str10) + " , INT " + str(int10) + " , MASTER " + str(master10) + " , STRIKES " + str(strikes10) + " , DSCPLNE " + str(discipline10) + " , PNTRTON " + str(penetration10) + " , DODGING " + str(dodging10) + " , STAMINA " + str(stamina10))
    if arg == "11Blue":
        phBotChat.Private(player,"11DG STR " + str(str11) + " , INT " + str(int11) + " , MASTER " + str(master11) + " , STRIKES " + str(strikes11) + " , DSCPLNE " + str(discipline11) + " , PNTRTON " + str(penetration11) + " , DODGING " + str(dodging11) + " , STAMINA " + str(stamina11))
    if arg == "8Blue2":
        phBotChat.Private(player,"8DG MAGIC " + str(magic8) + " , FOGS " + str(fogs8) + " , AIR " + str(air8) + " , FIRE " + str(fire8) + " , IMMUNITY " + str(immunity8) + " , REVIVAL " + str(revival8))
    if arg == "9Blue2":
        phBotChat.Private(player,"9DG MAGIC " + str(magic9) + " , FOGS " + str(fogs9) + " , AIR " + str(air9) + " , FIRE " + str(fire9) + " , IMMUNITY " + str(immunity9) + " , REVIVAL " + str(revival9))
    if arg == "10Blue2":
        phBotChat.Private(player,"10DG MAGIC " + str(magic10) + " , FOGS " + str(fogs10) + " , AIR " + str(air10) + " , FIRE " + str(fire10) + " , IMMUNITY " + str(immunity10) + " , REVIVAL " + str(revival10))
    if arg == "11Blue2":
        phBotChat.Private(player,"11DG MAGIC " + str(magic11) + " , FOGS " + str(fogs11) + " , AIR " + str(air11) + " , FIRE " + str(fire11) + " , IMMUNITY " + str(immunity11) + " , REVIVAL " + str(revival11))
    if arg == "8Stat":
        phBotChat.Private(player,"8DG COURAGE " + str(courage8) + " , WARRIORS " + str(warriors8) + " , PHILOSOPHY " + str(philosophy8) + " , MEDITATION " + str(meditation8) + " , CHALLENGE " + str(challenge8) + " , FOCUS " + str(focus8) + " , FLESH " + str(flesh8))
    if arg == "9Stat":
        phBotChat.Private(player,"9DG COURAGE " + str(courage9) + " , WARRIORS " + str(warriors9) + " , PHILOSOPHY " + str(philosophy9) + " , MEDITATION " + str(meditation9) + " , CHALLENGE " + str(challenge9) + " , FOCUS " + str(focus9) + " , FLESH " + str(flesh9))
    if arg == "10Stat":
        phBotChat.Private(player,"10DG COURAGE " + str(courage10) + " , WARRIORS " + str(warriors10) + " , PHILOSOPHY " + str(philosophy10) + " , MEDITATION " + str(meditation10) + " , CHALLENGE " + str(challenge10) + " , FOCUS " + str(focus10) + " , FLESH " + str(flesh10))
    if arg == "11Stat":
        phBotChat.Private(player,"11DG COURAGE " + str(courage11) + " , WARRIORS " + str(warriors11) + " , PHILOSOPHY " + str(philosophy11) + " , MEDITATION " + str(meditation11) + " , CHALLENGE " + str(challenge11) + " , FOCUS " + str(focus11) + " , FLESH " + str(flesh11))
    if arg == "8Stat2":
        phBotChat.Private(player,"8DG LIFE " + str(life8) + " , MIND " + str(mind8) + " , SPIRIT " + str(spirit8) + " , DODGING " + str(dodgings8) + " , AGILITY " + str(agility8) + " , TRAINING " + str(training8) + " , PRAYER " + str(prayer8))
    if arg == "9Stat2":
        phBotChat.Private(player,"9DG LIFE " + str(life9) + " , MIND " + str(mind9) + " , SPIRIT " + str(spirit9) + " , DODGING " + str(dodgings9) + " , AGILITY " + str(agility9) + " , TRAINING " + str(training9) + " , PRAYER " + str(prayer9))
    if arg == "10Stat2":
        phBotChat.Private(player,"10DG LIFE " + str(life10) + " , MIND " + str(mind10) + " , SPIRIT " + str(spirit10) + " , DODGING " + str(dodgings10) + " , AGILITY " + str(agility10) + " , TRAINING " + str(training10) + " , PRAYER " + str(prayer10))
    if arg == "11Stat2":
        phBotChat.Private(player,"11DG LIFE " + str(life11) + " , MIND " + str(mind11) + " , SPIRIT " + str(spirit11) + " , DODGING " + str(dodgings11) + " , AGILITY " + str(agility11) + " , TRAINING " + str(training11) + " , PRAYER " + str(prayer11))
    if arg == "Coin":
        phBotChat.Private(player,"Gold Coin " + str(qgold) + " , Silver Coin " + str(silver) + " , Iron Coin " + str(iron) + " , Copper Coin " + str(copper) + " , Arena Coin " + str(arena))
    if arg == "Catalyst":
        phBotChat.Private(player,"Alchemy Catalyst " + str(catalyst))
    if arg == "Cream":
        phBotChat.Private(player,"Ice Cream " + str(cream))
    if arg == "luckyboxx":
        phBotChat.Private(player,"Lucky Box " + str(luckybox))
    if arg == "Pledges":
        phBotChat.Private(player,"Pledge of Love(Left) " + str(pledge1) + " , Pledge of Love(Right) " + str(pledge2))
    if arg == "Pandora":
        phBotChat.Private(player,"Pandora " + str(pandora))
    if arg == "alibabaseall":
        phBotChat.Private(player,"AliBaba Seal " + str(alibabaseal))
    if arg == "Rubberr":
        phBotChat.Private(player,"Rubber Piece " + str(rubber))
    if arg == "Thanks":
        phBotChat.Private(player,"T > " + str(T1) + " , H > " + str(T2) + " , A > " + str(T3) + " , N > " + str(T4) + " , K > " + str(T5) + " , S > " + str(T6))
    if arg == "Snoww":
        phBotChat.Private(player,"Snow flake " + str(snowflake))
    if arg == "halloweencandyy":
        phBotChat.Private(player,"Halloween Candy " + str(halloweencandy))
    if arg == "Zerk":
        phBotChat.Private(player,"Berserker Regeneration Potion " + str(berserker))
    if arg == "Ms":
        phBotChat.Private(player,"Monster Summon Scroll " + str(ms))
    if arg == "luck8":
        phBotChat.Private(player,"Magic stone of luck " + str(luckst8))
    if arg == "steady8":
        phBotChat.Private(player,"Magic stone of steady " + str(steadyst8))
    if arg == "luck9":
        phBotChat.Private(player,"Magic stone of luck " + str(luckst9))
    if arg == "steady9":
        phBotChat.Private(player,"Magic stone of steady " + str(steadyst9))
    if arg == "luck10":
        phBotChat.Private(player,"Magic stone of luck " + str(luckst10))
    if arg == "steady10":
        phBotChat.Private(player,"Magic stone of steady " + str(steadyst10))
    if arg == "luck11":
        phBotChat.Private(player,"Magic stone of luck " + str(luckst11))
    if arg == "steady11":
        phBotChat.Private(player,"Magic stone of steady " + str(steadyst11))
    if arg == "Lamp":
        phBotChat.Private(player,"Genie’s Lamp " + str(lamp) + " -- Dirty Lamp " + str(dLamp))
    if arg == "fgw8dgeasy":
        phBotChat.Private(player,"Red tears" + str(card1) + " , Western scriptures " + str(card2) + " , Togui mask " + str(card3) + " , Red talisman " + str(card4) + " , Puppet " + str(card5) + " , Dull kitchen knife " + str(card6))
    if arg == "fgw8dghard":
        phBotChat.Private(player,"Elder staff " + str(card7) + " , Spell paper " + str(card8))
    if arg == "fgw9dgeasy":
        phBotChat.Private(player,"Fire flower " + str(card9) + " , Horned cattle " + str(card10) + " , Flame of oblivion " + str(card11) + " , Flame paper " + str(card12) + " , Hearthstone flame " + str(card13) + " , Enchantress necklace " + str(card14))
    if arg == "fgw9dghard":
        phBotChat.Private(player,"Honghaeah armor " + str(card15) + " , Fire dragon sword " + str(card16))
    if arg == "fgw10dgeasy":
        phBotChat.Private(player,"Silver pendant " + str(card17) + " , Cobalt emerald " + str(card18) + " , Logbook " + str(card19) + " , Love letter " + str(card20) + " , Portrait of a woman " + str(card21) + " , Jewelry box " + str(card22))
    if arg == "fgw10dghard":
        phBotChat.Private(player,"Diamond watch " + str(card23) + " , Mermaid’s tears " + str(card24))
    if arg == "fgw11dgeasy":
        phBotChat.Private(player,"Broken Key " + str(card25) + " , Large tong " + str(card26) + " , Phantom harp " + str(card27) + " , Evil’s heart " + str(card28) + " , Vindictive sprit’s bead " + str(card29) + " , Hook hand " + str(card30))
    if arg == "fgw11dghard":
        phBotChat.Private(player,"Sereness’s tears " + str(card31) + " , Commander’s patch " + str(card32))
    if arg == "faded":
        phBotChat.Private(player,"Faded Bead " + str(faded))
    if arg == "Sox":
        phBotChat.Private(player,"" + str(sunItems) + " Parca SoX Ogesi")

def handle_chat(t, player, msg):
    if player and lstLeaders_exist(player) or t == 100:
        if msg == "ENV":
            size = 0
            usingSpace = 0
            items = []
            items = get_inventory()['items'][12:]
            size = get_inventory()['size'] - 12
            if items != []:
                for item in items:
                    if item != None:
                        usingSpace += 1
            size -= 1
            usingSpace -= 1
            phBotChat.Private(player,"Bos Alan " + str(size - usingSpace) + "  ---->  " + str(usingSpace) + "/" + str(size))
        elif msg == "EXP":
            data = get_character_data()
            currentExp = data['current_exp']
            level = data['level']
            maxExp = data['max_exp']
            exp = float((100 * currentExp) / maxExp)
            phBotChat.Private(player,"Seviye: " + str(level) + " - EXP : %" + str("{:.2f}".format(exp)))
        elif msg == "JOBEXP":
            data = get_character_data()
            currentExp = data['job_current_exp']
            maxExp = data['job_max_exp']
            exp = float((100 * currentExp) / maxExp)
            phBotChat.Private(player,"Job Exp: %" + str("{:.2f}".format(exp)))
        elif msg == "GOLD":
            gold = 0;
            chars = []
            chars = get_character_data()
            if chars != []:
                gold += chars['gold']
            goldS = format(gold, ",")
            phBotChat.Private(player,"Suan " + str(goldS) + " Altin var. ")
        elif msg == "KESE":
            i = 0
            j = 0
            pouch = get_job_pouch()
            items = []
            items = get_job_pouch()["items"]
            if items != []:
                for item in items:
                    j = j + 1
                    if item is not None:
                        i = i + item["quantity"]
            phBotChat.Private(player,"Specialty -> " + str(i) + " / " + str(j * 5))
        elif msg == "SP":
            sp = 0;
            chars = []
            chars = get_character_data()
            if chars != []:
                sp += chars['sp']
            spS = format(sp, ",")
            phBotChat.Private(player,"Suan " + str(spS) + " Skill Point var. ")
        elif msg == "INCELX":
            checkInv("ElixirInc",player)
        elif msg == "8ELX":
            checkInv("Elixir8",player)
        elif msg == "9ELX":
            checkInv("Elixir9",player)
        elif msg == "10ELX":
            checkInv("Elixir10",player)
        elif msg == "11ELX":
            checkInv("Elixir11",player)
        elif msg == "ENH12":
            checkInv("Enhancer12",player)
        elif msg == "ENH13":
            checkInv("Enhancer13",player)
        elif msg == "ENH14":
            checkInv("Enhancer14",player)
        elif msg == "ENH15":
            checkInv("Enhancer15",player)
        elif msg == "ENH16":
            checkInv("Enhancer16",player)
        elif msg == "ENH17":
            checkInv("Enhancer17",player)
        elif msg == "8BLUE":
            checkInv("8Blue",player)
        elif msg == "9BLUE":
            checkInv("9Blue",player)
        elif msg == "10BLUE":
            checkInv("10Blue",player)
        elif msg == "11BLUE":
            checkInv("11Blue",player)
        elif msg == "8BLUE2":
            checkInv("8Blue2",player)
        elif msg == "9BLUE2":
            checkInv("9Blue2",player)
        elif msg == "10BLUE2":
            checkInv("10Blue2",player)
        elif msg == "11BLUE2":
            checkInv("11Blue2",player)
        elif msg == "8STAT":
            checkInv("8Stat",player)
        elif msg == "9STAT":
            checkInv("9Stat",player)
        elif msg == "10STAT":
            checkInv("10Stat",player)
        elif msg == "11STAT":
            checkInv("11Stat",player)
        elif msg == "8STAT2":
            checkInv("8Stat2",player)
        elif msg == "9STAT2":
            checkInv("9Stat2",player)
        elif msg == "10STAT2":
            checkInv("10Stat2",player)
        elif msg == "11STAT2":
            checkInv("11Stat2",player)
        elif msg == "FLOWER":
            checkInv("Flower3",player)
        elif msg == "PANDORA":
            checkInv("Pandora",player)
        elif msg == "8LUCK":
            checkInv("luck8",player)
        elif msg == "9LUCK":
            checkInv("luck9",player)
        elif msg == "10LUCK":
            checkInv("luck10",player)
        elif msg == "11LUCK":
            checkInv("luck11",player)
        elif msg == "8STEADY":
            checkInv("steady8",player)
        elif msg == "9STEADY":
            checkInv("steady9",player)
        elif msg == "10STEADY":
            checkInv("steady10",player)
        elif msg == "11STEADY":
            checkInv("steady11",player)
        elif msg == "MS":
            checkInv("Ms",player)
        elif msg == "ICE":
            checkInv("Cream",player)
        elif msg == "LBOX":
            checkInv("luckyboxx",player)
        elif msg == "PLEDGE":
            checkInv("Pledges",player)
        elif msg == "ALI":
            checkInv("alibabaseall",player)
        elif msg == "RUBBER":
            checkInv("Rubberr",player)
        elif msg == "THANKS":
            checkInv("Thanks",player)
        elif msg == "FLAKE":
            checkInv("Snoww",player)
        elif msg == "HLWN":
            checkInv("halloweencandyy",player)
        elif msg == "ZERK":
            checkInv("Zerk",player)
        elif msg == "LAMP":
            checkInv("Lamp",player)
        elif msg == "SOX":
            checkInv("Sox",player)
        elif msg == "COIN":
            checkInv("Coin",player)
        elif msg == "COMBATI":
            checkInv("Combatii",player)
        elif msg == "CATA":
            checkInv("Catalyst",player)
        elif msg == "8FGW1":
            checkInv("fgw8dgeasy",player)
        elif msg == "8FGW2":
            checkInv("fgw8dghard",player)
        elif msg == "9FGW1":
            checkInv("fgw9dgeasy",player)
        elif msg == "9FGW2":
            checkInv("fgw9dghard",player)
        elif msg == "10FGW1":
            checkInv("fgw10dgeasy",player)
        elif msg == "10FGW2":
            checkInv("fgw10dghard",player)
        elif msg == "11FGW1":
            checkInv("fgw11dgeasy",player)
        elif msg == "11FGW2":
            checkInv("fgw11dghard",player)
        elif msg == "FADED":
            checkInv("faded",player)

def CheckForUpdate():
	global NewestVersion
	if NewestVersion == 0:
		try:
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/EsyaBildir.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8")).split()
				for num, line in enumerate(lines):
					if line == 'version':
						NewestVersion = int(lines[num+2].replace(".",""))
						CurrentVersion = int(str(version).replace(".",""))
						if NewestVersion > CurrentVersion:
							log('Eklenti : Yeni bir güncelleme var = [%s]!' % name)
							lblUpdate = QtBind.createLabel(gui,'Yeni Bir Güncelleme Mevcut. Yüklemek için Tıkla ->',100,283)
							button1 = QtBind.createButton(gui, 'button_update', ' Güncelle ', 350, 280)
		except:
			pass

def button_update():
	path = get_config_dir()[:-7]
	if os.path.exists(path + "Plugins/" + "EsyaBildir.py"):
		try:
			os.rename(path + "Plugins/" + "EsyaBildir.py", path + "Plugins/" + "EsyaBildirBACKUP.py")
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/EsyaBildir.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8"))
				with open(path + "Plugins/" + "EsyaBildir.py", "w+") as f:
					f.write(lines)
					os.remove(path + "Plugins/" + "EsyaBildirBACKUP.py")
					log('Eklenti Başarıyla Güncellendi, Kullanmak için Eklentiyi Yeniden Yükleyin.')
		except Exception as ex:
			log('Güncelleme Hatası [%s] Lütfen Manuel Olarak Güncelleyin veya daha Sonra Tekrar Deneyin.' %ex)

CheckForUpdate()

log('Eklenti : %s v%s Yuklendi. // edit by hakankahya' % (name,version))

if os.path.exists(getPath()):
	loadConfigs()
else:
	os.makedirs(getPath())
	log('Eklenti : %s klasoru olusturuldu.' % (name))
