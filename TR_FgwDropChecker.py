from phBot import *
import QtBind
import re
import os
import json
from threading import *
import threading
import time

pName = 'TR_FgwDropChecker'
pVersion = '1.0.5'

gui = QtBind.init(__name__,pName)
lblCard = QtBind.createLabel(gui,'Talisman Düşenler Listesi ',10,5)
lblPetBuff = QtBind.createLabel(gui,'Pet Buff Düşenler Listesi ',160,5)
lblShield = QtBind.createLabel(gui,'Power Shield Düşenler Listesi ',310,5)
lblAlert = QtBind.createLabel(gui,'Alarm Listesi ',462,145)
btnAddItem = QtBind.createButton(gui,'btnAddItem_clicked',"      Ekle     ",610,185)
btnRemItem = QtBind.createButton(gui,'btnRemItem_clicked',"     Kaldır     ",610,215)
tbxItems = QtBind.createLineEdit(gui,"",610,160,110,20)
cbxEventLoop = QtBind.createCheckBox(gui, 'EventLoop_checked','Eşya Kontrolü',610,20)
QtBind.createButton(gui,'clearlistgui',"  Listeyi Temizle (Talisman) ",460,20)
QtBind.createButton(gui,'clearlistgui2',"  Listeyi Temizle (Pet Buff) ",460,50)
QtBind.createButton(gui,'clearlistgui3',"  Listeyi Temizle (Power Shield) ",460,80)
QtBind.createButton(gui,'clearlistgui4',"  Listeyi Temizle (Tümü) ",460,110)
list1 = QtBind.createList(gui,10,20,140,280)
list2 = QtBind.createList(gui,160,20,140,280)
list3 = QtBind.createList(gui,310,20,140,280)
list4 = QtBind.createList(gui,460,160,140,140)
checklist = []
checklist2 = []
uids = set()
cbxSoxDrop = QtBind.createCheckBox(gui,'gcdrop_clicked','Eşya Alarmı',610,40)
FIXSOUNDPATH = 'c:\\Windows\\Media\\chimes.wav'

def EventLoop_checked(checked):
	saveConfigs()

def gcdrop_clicked(checked):
	saveConfigs()

def saveConfigs():
	if isJoined():
		data = {}
		data['Items'] = checklist2
		data['Items2'] = checklist
		data['Item Drop Alert'] = QtBind.isChecked(gui,cbxSoxDrop)
		data['Item Drop Checker'] = QtBind.isChecked(gui,cbxEventLoop)
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))

def getPath():
	return get_config_dir()+pName+"\\"

def getConfig():
	return getPath()+inGame['server'] + "_" + inGame['name'] + ".json"

def isJoined():
	global inGame
	inGame = get_character_data()
	if not (inGame and "name" in inGame and inGame["name"]):
		inGame = None
	return inGame

def loadDefaultConfig():
	QtBind.clear(gui,list4)
	QtBind.setChecked(gui,cbxEventLoop,False)
	QtBind.setChecked(gui,cbxSoxDrop,False)

def loadConfigs():
	loadDefaultConfig()
	if isJoined():
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)
			if "Items" in data:
				for nickname in data["Items"]:
					QtBind.append(gui,list4,nickname)
					checklist2.append(nickname)
			if 'Item Drop Checker' in data and data['Item Drop Checker']:
				QtBind.setChecked(gui,cbxEventLoop,True)
			if 'Item Drop Alert' in data and data['Item Drop Alert']:
				QtBind.setChecked(gui,cbxSoxDrop,True)

def btnAddItem_clicked():
	if isJoined():
		player = QtBind.text(gui,tbxItems)
		if player and not lstItems_exist(player):
			data = {}
			if os.path.exists(getConfig()):
				with open(getConfig(), 'r') as f:
					data = json.load(f)
			if not "Items" in data:
				data['Items'] = []
			data['Items'].append(player)
			if not "Item Drop Checker" in data:
				data['Item Drop Checker'] = []
			data['Item Drop Checker'] = QtBind.isChecked(gui,cbxEventLoop)
			with open(getConfig(),"w") as f:
				f.write(json.dumps(data, indent=4, sort_keys=True))
			checklist2.append(player)
			QtBind.append(gui,list4,player)
			QtBind.setText(gui, tbxItems,"")
			log('Plugin: Eşya eklendi ['+player+']')
	else:
		log('Plugin: Eşya eklemek için karakterin oyunda olması gerekir.')

def btnRemItem_clicked():
	if isJoined():
		selectedItem = QtBind.text(gui,list4)
		if selectedItem:
			if os.path.exists(getConfig()):
				data = {"Items":[]}
				with open(getConfig(), 'r') as f:
					data = json.load(f)
				try:
					data["Items"].remove(selectedItem)
					with open(getConfig(),"w") as f:
						f.write(json.dumps(data, indent=4, sort_keys=True))
				except:
					pass
			checklist2.remove(selectedItem)
			QtBind.remove(gui,list4,selectedItem)
			log('Plugin: Eşya kaldırıldı ['+selectedItem+']')
	else:
		log('Plugin: Eşya kaldırmak için karakterin oyunda olması gerekir.')

def lstItems_exist(nickname):
	nickname = nickname.lower()
	players = QtBind.getItems(gui,list4)
	for i in range(len(players)):
		if players[i].lower() == nickname:
			return True
	return False

def connected():
	global inGame
	inGame = None

def joined_game():
	loadConfigs()

def event_loop():
	drops = get_drops()
	pattern = "TALISMAN"
	pattern2 = "PET2_ENC"
	pattern3 = "PET2_ASS"
	pattern4 = "PET2_PRO"
	pattern5 = "ITEM_EU_SHIELD_11_SET_A_RARE"
	pattern6 = "ITEM_CH_SHIELD_11_SET_A_RARE"
	servername = ''
	if QtBind.isChecked(gui,cbxEventLoop) :
		if drops is not None:
			for drop in drops:
				currentUid = drop
				name = drops[drop]['name']
				servername = drops[drop]['servername']
				itemdata = "%s" % (name)
				itemdata2 = "%s" % (name)
				itemdata3 = "%s" % (name)
				result = re.search(pattern, servername)
				result2 = re.search(pattern2, servername) or re.search(pattern3, servername) or re.search(pattern4, servername)
				result3 = re.search(pattern5, servername) or re.search(pattern6, servername)
				if result and currentUid not in uids:
					QtBind.append(gui,list1,itemdata)
					checklist.append(itemdata)
				if result2 and currentUid not in uids:
					QtBind.append(gui,list2,itemdata2)
					checklist.append(itemdata2)
				if result3 and currentUid not in uids:
					QtBind.append(gui,list3,itemdata3)
					checklist.append(itemdata3)
				if result or result2 or result3 and currentUid not in uids :
					for name in checklist :
						if name in checklist2:
							soxdroptrigger()
							checklist.clear()
				uids.add(currentUid)

def soxdroptrigger():
	if QtBind.isChecked(gui,cbxSoxDrop):
		x = threading.Thread(target=soxdropalert)
		x.start()

def soxdropalert():
	for x in range(1,11):
		play_wav(FIXSOUNDPATH)
		time.sleep(1.0)
		if x == 10 :
			QtBind.setChecked(gui,cbxSoxDrop,True)

def teleported():
	uids.clear()

def clearlistgui() :
	QtBind.clear(gui,list1)

def clearlistgui2() :
	QtBind.clear(gui,list2)

def clearlistgui3() :
	QtBind.clear(gui,list3)

def clearlistgui4() :
	QtBind.clear(gui,list1)
	QtBind.clear(gui,list2)
	QtBind.clear(gui,list3)

log('Eklenti: '+pName+' başarıyla yüklendi')

if os.path.exists(getPath()):
	loadConfigs()
else:
	os.makedirs(getPath())
	log('Eklenti: '+pName+' klasörü oluşturuldu, ** Lütfen Eklentiler Sekmesini Yeniden Yükleyin **')