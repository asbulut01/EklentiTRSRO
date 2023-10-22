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
version = 2.5
NewestVersion = 0

gui = QtBind.init(__name__, name)

tbxLeaders = QtBind.createLineEdit(gui,"",470,41,110,20)
lstLeaders = QtBind.createList(gui,470,62,110,70)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked'," Lider Ekle ",581,39)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked'," Lider Sil ",581,61)
metaby = QtBind.createLabel(gui,'edited by hakankahya',475,200)
metaby2 = QtBind.createLabel(gui,'Hata ve Öneriler için\n Discord = hakankahya ',475,150)
lstInfo = QtBind.createList(gui,15,42,450,220)
btnkarakter = QtBind.createButton(gui,'btnkarakter_clicked'," Karakter Bilgi ",15,11)
btnelixir = QtBind.createButton(gui,'btnelixir_clicked'," Elixir/Enhancer Bilgi ",91,11)
btnevent = QtBind.createButton(gui,'btnevent_clicked'," Event Bilgi ",197,11)
btncoin = QtBind.createButton(gui,'btncoin_clicked'," Coin Bilgi ",272,11)
btnstone = QtBind.createButton(gui,'btnstone_clicked'," Stone Bilgi ",347,11)
btnfgw = QtBind.createButton(gui,'btnfgw_clicked'," Fgw Bilgi ",422,11)
btnegpty = QtBind.createButton(gui,'btnegpty_clicked'," Egpty Set Bilgi ",497,11)

def btnkarakter_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'- ENV : Envanterin boş yuvasını bildirir.\n- GOLD : Suanki Altını Bildirir.\n- EXP : Suanki LV ve EXP bildirir.\n- SP : Suan ki SP Miktarını belirtir.\n- JOBEXP : JOB EXP bildirir.\n- KESE : Meslek kesesindeki boşluğu bildirir.(Uzmanlik)\n- SOX : Sox Miktarını Bildirir.(Giyilmişler ve Job Setler Haric)')

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
    QtBind.append(gui,lstInfo,'     "Verilen Komutlar Envanter, Pet ve Deponuzu Kontrol Etmektedir."\n- 8FGW1 : (8DG SUN) Kolay Düşen Kartların miktarını bildirir.\n- 8FGW2 : (8DG SUN) Zor Düşen Kartların miktarını bildirir.\n- 9FGW1 : (9DG SUN) Kolay Düşen Kartların miktarını bildirir.\n- 9FGW2 : (9DG SUN) Zor Düşen Kartların miktarını bildirir.\n- 10FGW1 : (10DG MOON) Kolay Düşen Kartların miktarını bildirir.\n- 10FGW2 : (10DG MOON) Zor Düşen Kartların miktarını bildirir.\n- 11FGW1 : (11DG EGYPY A) Kolay Düşen Kartların miktarını bildirir.\n- 11FGW2 : (11DG EGPTY A) Zor Düşen Kartların miktarını bildirir.\n- FADED : Faded Bead Miktarını Bildirir.')

def btnegpty_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'     "Verilen Komutlar Envanter, Pet ve Deponuzu Kontrol Etmektedir."\n- SETA : Egpty A Grade Eşya Miktarını Bildirir.(Giyilmişler Haric)\n Sadece Drop Sayısını bildirir.(Silah - Kıyafet - Kalkan - Yüzük) \n- SETB : Egpty B Grade Eşya Miktarını Bildirir.(Giyilmişler Haric)\n Sadece Drop Sayısını bildirir.(Silah - Kıyafet - Kalkan - Yüzük)')

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
    aGrade = 0
    bGrade = 0

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
                if "ITEM_ETC_ARENA_COIN" in item['servername']:
                    arena += item['quantity']
                if "ITEM_ETC_SD_TOKEN_04" in item['servername']:
                    qgold += item['quantity']
                if "ITEM_ETC_SD_TOKEN_03" in item['servername']:
                    silver += item['quantity']
                if "ITEM_ETC_SD_TOKEN_02" in item['servername']:
                    iron += item['quantity']
                if "ITEM_ETC_SD_TOKEN_01" in item['servername']:
                    copper += item['quantity']
                if "ITEM_ETC_SURVIVAL_ARENA_PARTY_COIN" in item['servername']:
                    combativeness1 += item['quantity']
                if "ITEM_ETC_SURVIVAL_ARENA_SOLO_COIN" in item['servername']:
                    combativeness2 += item['quantity']
                if "Alchemy catalyst" in item['name']:
                    catalyst += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_STR_11" in item['servername']:
                    str11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_STR_10" in item['servername']:
                    str10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_STR_09" in item['servername']:
                    str9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_STR_08" in item['servername']:
                    str8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_INT_11" in item['servername']:
                    int11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_INT_10" in item['servername']:
                    int10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_INT_09" in item['servername']:
                    int9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_INT_08" in item['servername']:
                    int8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_DUR_11" in item['servername']:
                    master11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_DUR_10" in item['servername']:
                    master10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_DUR_09" in item['servername']:
                    master9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_DUR_08" in item['servername']:
                    master8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_HR_11" in item['servername']:
                    strikes11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_HR_10" in item['servername']:
                    strikes10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_HR_09" in item['servername']:
                    strikes9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_HR_08" in item['servername']:
                    strikes8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_BLOCK_11" in item['servername']:
                    discipline11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_BLOCK_10" in item['servername']:
                    discipline10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_BLOCK_09" in item['servername']:
                    discipline9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_BLOCK_08" in item['servername']:
                    discipline8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_CRITICAL_11" in item['servername']:
                    penetration11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_CRITICAL_10" in item['servername']:
                    penetration10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_CRITICAL_09" in item['servername']:
                    penetration9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_CRITICAL_08" in item['servername']:
                    penetration8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ER_11" in item['servername']:
                    dodging11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ER_10" in item['servername']:
                    dodging10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ER_09" in item['servername']:
                    dodging9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ER_08" in item['servername']:
                    dodging8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_HP_11" in item['servername']:
                    stamina11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_HP_10" in item['servername']:
                    stamina10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_HP_09" in item['servername']:
                    stamina9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_HP_08" in item['servername']:
                    stamina8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_MP_11" in item['servername']:
                    magic11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_MP_10" in item['servername']:
                    magic10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_MP_09" in item['servername']:
                    magic9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_MP_08" in item['servername']:
                    magic8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_FROSTBITE_11" in item['servername']:
                    fogs11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_FROSTBITE_10" in item['servername']:
                    fogs10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_FROSTBITE_09" in item['servername']:
                    fogs9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_FROSTBITE_08" in item['servername']:
                    fogs8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ESHOCK_11" in item['servername']:
                    air11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ESHOCK_10" in item['servername']:
                    air11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ESHOCK_09" in item['servername']:
                    air9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ESHOCK_08" in item['servername']:
                    air8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_BURN_11" in item['servername']:
                    fire11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_BURN_10" in item['servername']:
                    fire10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_BURN_09" in item['servername']:
                    fire9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_BURN_08" in item['servername']:
                    fire8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_POISON_11" in item['servername']:
                    immunity11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_POISON_10" in item['servername']:
                    immunity10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_POISON_09" in item['servername']:
                    immunity9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_POISON_08" in item['servername']:
                    immunity8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ZOMBIE_11" in item['servername']:
                    revival11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ZOMBIE_10" in item['servername']:
                    revival10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ZOMBIE_09" in item['servername']:
                    revival9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_ZOMBIE_08" in item['servername']:
                    revival8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PA_11" in item['servername']:
                    courage11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PA_10" in item['servername']:
                    courage10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PA_09" in item['servername']:
                    courage9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PA_08" in item['servername']:
                    courage8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PASTR_11" in item['servername']:
                    warriors11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PASTR_10" in item['servername']:
                    warriors10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PASTR_09" in item['servername']:
                    warriors9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PASTR_08" in item['servername']:
                    warriors8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MA_11" in item['servername']:
                    philosophy11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MA_10" in item['servername']:
                    philosophy10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MA_09" in item['servername']:
                    philosophy9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MA_08" in item['servername']:
                    philosophy8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAINT_11" in item['servername']:
                    meditation11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAINT_10" in item['servername']:
                    meditation10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAINT_09" in item['servername']:
                    meditation9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAINT_08" in item['servername']:
                    meditation8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_CRITICAL_11" in item['servername']:
                    challenge11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_CRITICAL_10" in item['servername']:
                    challenge10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_CRITICAL_09" in item['servername']:
                    challenge9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_CRITICAL_08" in item['servername']:
                    challenge8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_HR_11" in item['servername']:
                    focus11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_HR_10" in item['servername']:
                    focus10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_HR_09" in item['servername']:
                    focus9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_HR_08" in item['servername']:
                    focus8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PD_11" in item['servername']:
                    flesh11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PD_10" in item['servername']:
                    flesh10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PD_09" in item['servername']:
                    flesh9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PD_08" in item['servername']:
                    flesh8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PDSTR_11" in item['servername']:
                    life11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PDSTR_10" in item['servername']:
                    life10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PDSTR_09" in item['servername']:
                    life9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PDSTR_08" in item['servername']:
                    life8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MD_11" in item['servername']:
                    mind11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MD_10" in item['servername']:
                    mind10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MD_09" in item['servername']:
                    mind9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MD_08" in item['servername']:
                    mind8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MDINT_11" in item['servername']:
                    spirit11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MDINT_10" in item['servername']:
                    spirit10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MDINT_09" in item['servername']:
                    spirit9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MDINT_08" in item['servername']:
                    spirit8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_ER_11" in item['servername']:
                    dodgings11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_ER_10" in item['servername']:
                    dodgings10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_ER_09" in item['servername']:
                    dodgings9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_ER_08" in item['servername']:
                    dodgings8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_BR_11" in item['servername']:
                    agility11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_BR_10" in item['servername']:
                    agility10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_BR_09" in item['servername']:
                    agility9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_BR_08" in item['servername']:
                    agility8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PAR_11" in item['servername']:
                    training11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PAR_10" in item['servername']:
                    training10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PAR_09" in item['servername']:
                    training9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_PAR_08" in item['servername']:
                    training8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAR_11" in item['servername']:
                    prayer11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAR_10" in item['servername']:
                    prayer10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAR_09" in item['servername']:
                    prayer9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAR_08" in item['servername']:
                    prayer8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_LUCK_08" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_LUCK_08" in item['servername']:
                    luckst8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_SOLID_08" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_SOLID_08" in item['servername']:
                    steadyst8 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_LUCK_09" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_LUCK_09" in item['servername']:
                    luckst9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_SOLID_09" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_SOLID_09" in item['servername']:
                    steadyst9 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_LUCK_10" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_LUCK_10" in item['servername']:
                    luckst10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_SOLID_10" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_SOLID_10" in item['servername']:
                    steadyst10 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_LUCK_11" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_LUCK_11" in item['servername']:
                    luckst11 += item['quantity']
                if "ITEM_ETC_ARCHEMY_MAGICSTONE_SOLID_11" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_SOLID_11" in item['servername']:
                    steadyst11 += item['quantity']
                if "ITEM_ETC_E060517_MON_GENERATION_BOX" in item['servername'] or "ITEM_EVENT_GENERATION_BOX" in item['servername'] or "ITEM_EVENT_RENT_E100222_MON_GENERATION_BOX" in item['servername']:
                    pandora += item['quantity']
                if "ITEM_ETC_E060517_SUMMON_PARTY_SCROLL" in item['servername'] or "ITEM_ETC_E060526_SUMMON_PARTY_SCROLL_A" in item['servername'] or "ITEM_EVENT_RENT_E100222_SUMMON_SCROLL" in item['servername']:
                    ms += item['quantity']
                if "ITEM_ETC_E090121_LUCKYBOX" in item['servername'] or "ITEM_ETC_E120118_LUCKYBOX" in item['servername']:
                    luckybox += item['quantity']
                if "ITEM_ETC_E070523_LEFT_HEART" in item['servername']:
                    pledge1 += item['quantity']
                if "ITEM_ETC_E070523_RIGHT_HEART" in item['servername']:
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
                if "ITEM_TALISMAN_TOGUI_RED_TEARS" in item['servername']:
                    card1 += item['quantity']
                if "ITEM_TALISMAN_TOGUI_WESTERN_SCRIPTURES" in item['servername']:
                    card2 += item['quantity']
                if "ITEM_TALISMAN_TOGUI_TOGUI_MASK" in item['servername']:
                    card3 += item['quantity']
                if "ITEM_TALISMAN_TOGUI_RED_TALISMAN" in item['servername']:
                    card4 += item['quantity']
                if "ITEM_TALISMAN_TOGUI_PUPPETS" in item['servername']:
                    card5 += item['quantity']
                if "ITEM_TALISMAN_TOGUI_KITCHEN_KNIFE" in item['servername']:
                    card6 += item['quantity']
                if "ITEM_TALISMAN_TOGUI_ELDER_STAFF" in item['servername']:
                    card7 += item['quantity']
                if "ITEM_TALISMAN_TOGUI_SPELL_PAPERS" in item['servername']:
                    card8 += item['quantity']
                if "ITEM_TALISMAN_FLAME_FIRE_FLOWER" in item['servername']:
                    card9 += item['quantity']
                if "ITEM_TALISMAN_FLAME_HORNED_CATTLE" in item['servername']:
                    card10 += item['quantity']
                if "ITEM_TALISMAN_FLAME_FLAME_OF_OBLIVION" in item['servername']:
                    card11 += item['quantity']
                if "ITEM_TALISMAN_FLAME_FLAME_PAPERS" in item['servername']:
                    card12 += item['quantity']
                if "ITEM_TALISMAN_FLAME_HEARTHSTONE_FLAME" in item['servername']:
                    card13 += item['quantity']
                if "ITEM_TALISMAN_FLAME_ENCHANTRESS_NECKLACE" in item['servername']:
                    card14 += item['quantity']
                if "ITEM_TALISMAN_FLAME_HONGHAEAH_ARMOR" in item['servername']:
                    card15 += item['quantity']
                if "ITEM_TALISMAN_FLAME_FIRE_DRAGON_SWORD" in item['servername']:
                    card16 += item['quantity']
                if "ITEM_TALISMAN_WRECK_A_SILVER_PENDANT" in item['servername']:
                    card17 += item['quantity']
                if "ITEM_TALISMAN_WRECK_A_COBALT_EMERALD" in item['servername']:
                    card18 += item['quantity']
                if "ITEM_TALISMAN_WRECK_A_LOGBOOK" in item['servername']:
                    card19 += item['quantity']
                if "ITEM_TALISMAN_WRECK_A_LOVE_LETTER" in item['servername']:
                    card20 += item['quantity']
                if "ITEM_TALISMAN_WRECK_A_PORTRAIT_WOMAN" in item['servername']:
                    card21 += item['quantity']
                if "ITEM_TALISMAN_WRECK_A_JEWELRY_BOX" in item['servername']:
                    card22 += item['quantity']
                if "ITEM_TALISMAN_WRECK_A_DIAMOND_WATCHES" in item['servername']:
                    card23 += item['quantity']
                if "ITEM_TALISMAN_WRECK_A_MERMAID_TEARS" in item['servername']:
                    card24 += item['quantity']
                if "ITEM_TALISMAN_WRECK_B_BROKEN_KEY" in item['servername']:
                    card25 += item['quantity']
                if "ITEM_TALISMAN_WRECK_B_LARGE_TONGS" in item['servername']:
                    card26 += item['quantity']
                if "ITEM_TALISMAN_WRECK_B_PHANTOM_HALF" in item['servername']:
                    card27 += item['quantity']
                if "ITEM_TALISMAN_WRECK_B_EVIL_HEART" in item['servername']:
                    card28 += item['quantity']
                if "ITEM_TALISMAN_WRECK_B_REVENGEFUL_SPIRIT_BEADS" in item['servername']:
                    card29 += item['quantity']
                if "ITEM_TALISMAN_WRECK_B_HOOK_HAND" in item['servername']:
                    card30 += item['quantity']
                if "ITEM_TALISMAN_WRECK_B_SERENITY_TEARS" in item['servername']:
                    card31 += item['quantity']
                if "ITEM_TALISMAN_WRECK_B_COMMANDER_PATCH" in item['servername']:
                    card32 += item['quantity']
                if "ITEM_ETC_SKILLPOINT_STONE" in item['servername']:
                    faded += item['quantity']
                if 'RARE' in item['servername'] and 'EVENT' not in item['servername'] and 'ARCHEMY' not in item[
                    'servername'] and 'ITEM_TRADE' not in item['servername']:
                    sunItems += 1
                if 'SET_A_RARE' in item['servername']:
                    aGrade += 1
                if 'SET_B_RARE' in item['servername']:
                    bGrade += 1

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
        phBotChat.Private(player,"Magic stone of luck "  + str(luckst8))
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
        phBotChat.Private(player,"" + str(sunItems) + " Parca SoX Eşyası")
    if arg == "SetA":
        phBotChat.Private(player,"" + str(aGrade) + " Parca Egpty Eşyası")
    if arg == "SetB":
        phBotChat.Private(player,"" + str(bGrade) + " Parca Egpty Eşyası")

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
        elif msg == "SETA":
            checkInv("SetA",player)
        elif msg == "SETB":
            checkInv("SetB",player)

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
