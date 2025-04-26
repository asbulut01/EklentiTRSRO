from phBot import *
from threading import Timer
import QtBind
import struct
import os
import time
import re
import urllib.request

name = 'TR_AutoGacha'

gui = QtBind.init(__name__, name)

searchbar = QtBind.createLineEdit(gui,"",20,10,320,20)
buttonsearch = QtBind.createButton(gui, 'buttonsearch_clicked', 'Ara', 350, 10)
cbxpremium = QtBind.createCheckBox(gui, 'cbxpremium_clicked','Premium', 450, 10)
cbxnormal = QtBind.createCheckBox(gui, 'cbxpremium_clicked','Normal', 520, 10)
cbxall = QtBind.createCheckBox(gui, 'cbxallicked','Tümü', 590, 10)
founditems = QtBind.createList(gui,20,50,690,210)
buttonexchange = QtBind.createButton(gui, 'buttonexchange_clicked', 'Tümünü Takas Et', 20, 280)

StopBot = False
GachaItems = []

def buttonsearch_clicked():
	if not QtBind.isChecked(gui,cbxpremium) and not QtBind.isChecked(gui,cbxnormal) and not QtBind.isChecked(gui,cbxall):
		log('TR_AutoGacha: Lütfen bir Seçenek Belirleyin, Premium/Normal')
		return
	QtBind.clear(gui,founditems)
	ItemIDs = GetAllItemIDs()
	SearchText = QtBind.text(gui,searchbar)
	for itemid in ItemIDs:
		ItemData = get_item(itemid)
		ServerName = ItemData['servername']
		Rarity = "(YILDIZ / SOX)" if 'A_RARE' in ServerName else "(AY / MOON)" if 'B_RARE' in ServerName else "(GÜNEŞ / SUN)" if 'C_RARE' in ServerName else ""
		Name = ItemData['name']
		if SearchText.lower() in Name.lower():
			GachaData = GetGachaByItemID(itemid)
			if QtBind.isChecked(gui,cbxpremium):
				if "ITEM_EVENT" not in ServerName:
					QtBind.append(gui,founditems,f"{GachaData['gacha_id']} - Eşya Adı: [{Name} {Rarity}]{GetBlues(GachaData['param1'])} -- Eşya Kodu: [{ServerName}]")
			if QtBind.isChecked(gui,cbxnormal):
				if "ITEM_EVENT" in ServerName:
					QtBind.append(gui,founditems,f"{GachaData['gacha_id']} - Eşya Adı: [{Name} {Rarity}]{GetBlues(GachaData['param1'])} -- Eşya Kodu: [{ServerName}]")
			if QtBind.isChecked(gui,cbxall):
				QtBind.append(gui,founditems,f"{GachaData['gacha_id']} - Eşya Adı: [{Name} {Rarity}]{GetBlues(GachaData['param1'])} -- Eşya Kodu: [{ServerName}]")


def buttonexchange_clicked():
	n = get_gacha()
	for x in n:
		log(str(x))
	global StopBot
	StopBot = False
	SelectedItem = QtBind.text(gui,founditems)
	if SelectedItem:
		GachaID = int(SelectedItem.split('-')[0].strip(' '))
	else:
		log('TR_AutoGacha: Lütfen bir Ödül Öğesi Seçin')
		return
	Timer(0.1, ExchangeCards, [GachaID]).start() #avoid locking the bot & client

def GetCardSlots():
	CardSlots = []
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			if item['name'] in ["Magic POP Card", "Premium Magic POP Card (VIP)", "Premium Magic POP Card"] or "GACHA_CARD" in item['servername'] and "coupon" not in item['name'].lower():
				CardSlots.append(slot)
	return CardSlots

def HasWinner():
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			if "CARD_WIN" in item['servername']:
				return True
	return False

def ExchangeCards(GachaID):
	if HasWinner():
		log('TR_AutoGacha: Kazanan Bir Kartınız Var, Takas Yapılmayacak')
		if StopBot:
			start_bot()
		return
	npcs = get_npcs()
	ItemName = get_item(int(GetItemIDByGachaID(GachaID)))['name']
	for key, npc in npcs.items():
		if "GACHA" in npc['servername'] and "gori" not in npc['name'].lower():
			CardSlots = GetCardSlots()
			if len(CardSlots) == 0:
				log('TR_AutoGacha: Hiç Kartınız Yok')
				return
			for slot in CardSlots:
				p = struct.pack('<I', key)
				p += struct.pack('<H', int(GachaID))
				p += b'\x00\x00'
				p += struct.pack('B',slot)
				if get_locale() == 18:
					p += b'\x00'
				inject_joymax(0x7118, p, False)
				log(f'TR_AutoGacha: Gacha Kartı Takas Ediliyor - yuva[{slot}] öğe için [{ItemName}]')
				time.sleep(3.0)
			if StopBot:
				start_bot()
			log('TR_AutoGacha: Tüm kartlar takas edildi')
			return
	log('TR_AutoGacha: NPC bulunamadı. Bir Gacha NPC\'sinin yakınında değilsiniz')
	return

def ExchangeGacha(args):
	global StopBot
	GachaID = int(args[1])
	StopBot = True
	if len(args) == 3:
		State = args[2]
		if State.lower() == 'true':
			StopBot = True
		if State.lower() == 'false':
			StopBot = False
	if StopBot:
		stop_bot()
	Timer(0.1, ExchangeCards, [GachaID]).start()
	return 0

def GetAllItemIDs():
	global GachaItems
	Items = []
	if len(GachaItems) == 0:
		GachaItems = get_gacha()
	for item in GachaItems:
		ItemID = item['id']
		Items.append(ItemID)
	return Items

def GetGachaByItemID(ItemID):
	global GachaItems
	if len(GachaItems) == 0:
		GachaItems = get_gacha()
	for item in GachaItems:
		if item['id'] == int(ItemID):
			return item

def GetItemIDByGachaID(GachaID):
	global GachaItems
	if len(GachaItems) == 0:
		GachaItems = get_gacha()
	for item in GachaItems:
		if item['gacha_id'] == int(GachaID):
			return item['id']

def GetBlues(param1):
	n = ""
	if len(param1) != 0:
		Stats = re.findall(r"<(.*?)>", str(param1))
		for stat in Stats:
			type = stat.split(":")[0]
			if type == "M":
				stat = stat.split(",")
				Name = stat[0].replace("M:","")
				Value = stat[2]
				n = n + (f"{Name}:{Value} ")
	return f"-[{n.rstrip()}]" if len(n) > 0 else ""

log(f'Eklenti: {name} başarıyla yüklendi.')