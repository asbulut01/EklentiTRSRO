from phBot import *
import threading
import QtBind
import struct
import json
import os

pName = 'TR_GP_Donate'
pVersion = '1.0'

gui = QtBind.init(__name__,pName)
lblCizgi1 = QtBind.createList(gui,10,10,200,250)
chk_autoDonate = QtBind.createCheckBox(gui, 'toggle_autoDonate', 'Lv Alınca GP Bağışla', 50, 220)
btn_donate50 = QtBind.createButton(gui, 'donate50GP', '  50 GP Bağışla  ', 65, 25)
btn_donate100 = QtBind.createButton(gui, 'donate100GP', ' 100 GP Bağışla ', 65, 55)
btn_donate500 = QtBind.createButton(gui, 'donate500GP', ' 500 GP Bağışla ', 65, 85)
btn_donate1000 = QtBind.createButton(gui, 'donate1000GP', '1000 GP Bağışla', 65, 115)
btn_donate1950 = QtBind.createButton(gui, 'donate1950GP', '1950 GP Bağışla', 65, 145)
btn_donateAll = QtBind.createButton(gui, 'donate_All', 'Tamamını Bağışla', 65, 175)
lblNot = QtBind.createLabel(gui,'<font color="red">Not:</font> Eklenti Her Yüklemede 50 GP Lv Bağışlama Özelliği Aktif Olacaktır.<br>Arayüz Üzerinde Belirlenen GP Bağışlaması Manuel Olarak Yapılabilir.<br>Lider Olarak Eklenen Kişiler de Komut Yardımı ile GP Bağışlama Yaptırabilir.<br><br><font color="red">Komutlar:</font> GP50 ... GP1950 Yazarak Belirlenen Sayıdaki GP bağışlanır.<br>GPHepsi Komutu ile Tamamı Bağışlanır.', 215, 155)
auto_donate = False

tbxLeaders = QtBind.createLineEdit(gui,"",211,10,110,20)
lstLeaders = QtBind.createList(gui,211,30,110,85)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked'," Ekle ",320,9)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"                 Sil               ",210,115)

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

def connected():
	global inGame
	inGame = None

def joined_game():
	loadConfigs()

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
			log('Eklenti: ['+player+'] Lider Olarak Atandı.')

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
			log('Eklenti: ['+selectedItem+'] Liderlikten Çıkarıldı.')

def lstLeaders_exist(nickname):
	nickname = nickname.lower()
	players = QtBind.getItems(gui,lstLeaders)
	for i in range(len(players)):
		if players[i].lower() == nickname:
			return True
	return False

def handle_chat(t,player,msg):
	if t == 11:
		msg = msg.split(': ',1)[1]
	if player and lstLeaders_exist(player) or t == 100:
		if msg == "GP50":
			donate50GP()
			log("Eklenti: Chat Komutu ile 50 GP Bağışlandı.")
		elif msg == "GP100":
			donate100GP()
			log("Eklenti: Chat Komutu ile 100 GP Bağışlandı.")
		elif msg == "GP500":
			donate500GP()
			log("Eklenti: Chat Komutu ile 500 GP Bağışlandı.")
		elif msg == "GP1000":
			donate1000GP()
			log("Eklenti: Chat Komutu ile 1000 GP Bağışlandı.")
		elif msg == "GP1950":
			donate1950GP()
			log("Eklenti: Chat Komutu ile 1950 GP Bağışlandı.")
		elif msg == "GPHepsi":
			donate_All()
			log("Eklenti: Chat Komutu Tüm GP Bağışlandı.")

def toggle_autoDonate(checked):
    global auto_donate
    auto_donate = checked

def convert_to_bytearray(strData):
	data = bytearray()
	strDataLen = len(strData)
	for i in range(0, strDataLen, 2):
		data.append(int(strData[i:i+2], 16))
	return data

def donate50GP():
	log("50 GP bağışlandı.")
	inject_joymax(0x7258, convert_to_bytearray('32 00 00 00'), False)

def donate100GP():
	log("100 GP bağışlandı.")
	inject_joymax(0x7258, convert_to_bytearray('64 00 00 00'), False)

def donate500GP():
	log("500 GP bağışlandı.")
	inject_joymax(0x7258, convert_to_bytearray('F4 01 00 00'), False)

def donate1000GP():
	log("1000 GP bağışlandı.")
	inject_joymax(0x7258, convert_to_bytearray('E8 03 00 00'), False)

def donate1950GP():
	log("1950 GP bağışlandı.")
	inject_joymax(0x7258, convert_to_bytearray('9E 07 00 00'), False)

def handle_event(t, data):
	if t == 10 and auto_donate:
		donate50GP()
		toggle_autoDonate(False)

def handle_joymax(opcode, data):
	global pressed
	if opcode == 0x304E and pressed:
		pressed = False
		eventId = struct.unpack_from('<H', data, 0)[0]
		if eventId == 4113:
			currentGP = struct.unpack_from('<I', data, 2)[0]
			packed = struct.pack('<I', currentGP)
			if currentGP > 0:
			    log('Eklenti: ' + 'Şuan [' + str(currentGP) + '] GP mevcut, Tamamı Bağışlandı.')
			    inject_joymax(0x7258, packed, False)	
	return True

pressed = False

def donate_All():
	global pressed
	pressed = True
	inject_joymax(0x7258, struct.pack('<I', 1), False)

log('Eklenti:'+pName+' v'+pVersion+' Yuklendi. // edit by hakankahya')

if os.path.exists(getPath()):
	loadConfigs()
else:
	os.makedirs(getPath())
	log('Eklenti:'+pName+' Klasoru Oluşturuldu.')

QtBind.setChecked(gui, chk_autoDonate, True)
toggle_autoDonate(True)