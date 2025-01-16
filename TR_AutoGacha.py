from phBot import *
from threading import Timer
import QtBind
import struct
import os
import time
import re
import urllib.request

name = 'TR_AutoGacha'
version = 2.1

gui = QtBind.init(__name__, name)


searchbar = QtBind.createLineEdit(gui,"",20,10,320,20)
buttonsearch = QtBind.createButton(gui, 'buttonsearch_clicked', 'Ara', 350, 10)
cbxpremium = QtBind.createCheckBox(gui, 'cbxpremium_clicked','Premium', 450, 10)
cbxnormal = QtBind.createCheckBox(gui, 'cbxpremium_clicked','Normal', 520, 10)
cbxall = QtBind.createCheckBox(gui, 'cbxallicked','Tümü', 590, 10)

founditems = QtBind.createList(gui,20,50,690,210)

buttonexchange = QtBind.createButton(gui, 'buttonexchange_clicked', 'Tümünü Takasla', 20, 280)

StopBot = False
GachaItems = []

def buttonsearch_clicked():
	if not QtBind.isChecked(gui,cbxpremium) and not QtBind.isChecked(gui,cbxnormal) and not QtBind.isChecked(gui,cbxall):
		log('Eklenti: Lütfen bir seçenek seçin, Premium/Normal ya da Tümü')
		return
	QtBind.clear(gui,founditems)
	ItemIDs = GetTümüItemIDs()
	AraText = QtBind.text(gui,searchbar)
	for itemid in ItemIDs:
		ItemData = get_item(itemid)
		ServerName = ItemData['servername']
		Rarity = "(Magic)" if 'A_RARE' in ServerName else "(Rare)" if 'B_RARE' in ServerName else "(Legend)" if 'C_RARE' in ServerName else ""
		Name = ItemData['name']
		if AraText.lower() in Name.lower():
			GachaData = GetGachaByItemID(itemid)
			if QtBind.isChecked(gui,cbxpremium):
				if "ITEM_EVENT" not in ServerName:
					QtBind.append(gui,founditems,f"{GachaData['gacha_id']} - Name: [{Name} {Rarity}]{GetBlues(GachaData['param1'])} -- ServerName: [{ServerName}]")
			if QtBind.isChecked(gui,cbxnormal):
				if "ITEM_EVENT" in ServerName:
					QtBind.append(gui,founditems,f"{GachaData['gacha_id']} - Name: [{Name} {Rarity}]{GetBlues(GachaData['param1'])} -- ServerName: [{ServerName}]")
			if QtBind.isChecked(gui,cbxall):
				QtBind.append(gui,founditems,f"{GachaData['gacha_id']} - Name: [{Name} {Rarity}]{GetBlues(GachaData['param1'])} -- ServerName: [{ServerName}]")


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
		log('Eklenti: Lütfen bir ödül öğesi seçin')
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
		log('Eklenti: Kazanan bir kartınız var, takas yapılmayacak')
		if StopBot:
			start_bot()
		return
	npcs = get_npcs()
	ItemName = get_item(int(GetItemIDByGachaID(GachaID)))['name']
	for key, npc in npcs.items():
		if "GACHA" in npc['servername'] and "gori" not in npc['name'].lower():
			CardSlots = GetCardSlots()
			if len(CardSlots) == 0:
				log('Eklenti: Hiç kartınız yok')
				return
			for slot in CardSlots:
				p = struct.pack('<I', key)
				p += struct.pack('<H', int(GachaID))
				p += b'\x00\x00'
				p += struct.pack('B',slot)
				if get_locale() == 18:
					p += b'\x00'
				inject_joymax(0x7118, p, False)
				log(f'Eklenti: Gacha Kartı Takas Ediliyor - slot[{slot}] için öğe [{ItemName}]')
				time.sleep(3.0)
			if StopBot:
				start_bot()
			log('Eklenti: Tüm kartların takası tamamlandı')
			return
	log('Eklenti: NPC bulunamadı. Gacha NPC\'sinin yakınında değilsiniz')
	return

#ExchangeGacha,gachaid,true/false
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

def GetTümüItemIDs():
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

log('Eklenti: [%s] Sürüm %s Yüklendi. // edit by hakankahya' % (name,version))
