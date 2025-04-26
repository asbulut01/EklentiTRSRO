from phBot import *
import urllib.request
from threading import Timer
from datetime import datetime, timedelta
import datetime
import os
import signal
import struct
import subprocess
import json
import QtBind

name = 'TR_ScriptCommands'

path = get_config_dir()[:-7]

StartBotAt = 0
CloseBotAt = 0
CheckStartTime = False
CheckCloseTime = False
SkipCommand = False
delay_counter = 0
BtnStart = False
Recording = False
RecordedPackets = []
ExecutedPackets = []
Index = 0
StopBot = True

gui = QtBind.init(__name__, name)
LvlSaveName = QtBind.createLabel(gui,'Kaydetme Adı ',10,13)
SaveName = QtBind.createLineEdit(gui,"",80,10,120,20)
RecordBtn = QtBind.createButton(gui, 'button_start', ' Kayda Başla ', 220, 10)
Display = QtBind.createList(gui,20,50,280,180)
ShowCommandsBtn = QtBind.createButton(gui, 'button_ShowCmds', ' Kayıtlı Komutları \n Göster ', 20, 240)
DeleteCommandsBtn = QtBind.createButton(gui, 'button_DelCmds', ' Komutu Sil ', 120, 240)
ShowPacketsBtn = QtBind.createButton(gui, 'button_ShowPackets', ' Paketleri Göster ', 220, 240)
cbxShowPackets = QtBind.createCheckBox(gui, 'cbxAuto_clicked','Paketleri Göster ', 330, 10)

def ResetSkip():
	global SkipCommand
	SkipCommand = False

def LeaveParty(args):
	if get_party():
		inject_joymax(0x7061,b'',False)
		log('TR_ScriptCommands: Partiden Ayrılıyor')
	return 0

def Notification(args):
	if len(args) == 3:
		title = args[1]
		message = args[2]
		show_notification(title, message)
		return 0
	log('TR_ScriptCommands: Yanlış Notification komutu')
	return 0

def NotifyList(args):
	if len(args) == 2:
		message = args[1]
		create_notification(message)
		return 0
	log('TR_ScriptCommands: Yanlış NotifyList komutu')
	return 0

def PlaySound(args):
	FileName = args[1]
	if os.path.exists(path + FileName):
		play_wav(path + FileName)
		log('TR_ScriptCommands: [%s] Çalınıyor' %FileName)
		return 0
	log('TR_ScriptCommands: [%s] Ses dosyası mevcut değil' %FileName)
	return 0

def SetScript(args):
	name = args[1]
	if os.path.exists(path + name):
		set_training_script(path + name)
		log('TR_ScriptCommands: Script [%s] olarak değiştiriliyor' %name)
		return 0
	log('TR_ScriptCommands: [%s] Scripti mevcut değil' %name)
	return 0

def CloseBot(args):
	global CloseBotAt, CheckCloseTime
	CheckCloseTime = True
	if len(args) == 1:
		Terminate()
		return 0
	type = args[1]
	time = args[2]
	if type == 'in':
		CloseBotAt = str(datetime.datetime.now() + timedelta(minutes=int(time)))[11:16]
		log('TR_ScriptCommands: Bot [%s] de kapatılacak' %CloseBotAt)
	elif type == 'at':
		CloseBotAt = time
		log('TR_ScriptCommands: Bot [%s] de kapatılacak' %CloseBotAt)
	return 0

def Terminate():
	log("TR_ScriptCommands: Bot kapatılıyor...")
	os.kill(os.getpid(),9)

def GoClientless(args):
	pid = get_client()['pid']
	if pid:
		os.kill(pid, signal.SIGTERM)
		return 0
	log('TR_ScriptCommands: Client açık değil!')
	return 0

def StartBot(args):
	global StartBotAt, CheckStartTime, SkipCommand
	if SkipCommand:
		SkipCommand = False
		return 0
	stop_bot()
	type = args[1]
	time = args[2]
	CheckStartTime = True
	if type == 'in':
		StartBotAt = str(datetime.datetime.now() + timedelta(minutes=int(time)))[11:16]
		log('TR_ScriptCommands: Bot [%s] de başlatılacak' %StartBotAt)
	elif type == 'at':
		StartBotAt = time
		log('TR_ScriptCommands: Bot [%s] de başlatılacak' %StartBotAt)
	return 0

def StopStart(args):
	global SkipCommand
	if SkipCommand:
		SkipCommand = False
		return 0
	stop_bot()
	Timer(1.0, start_bot, ()).start()
	Timer(30.0, ResetSkip, ()).start()
	SkipCommand = True
	return 0

def StartTrace(args):
	global SkipCommand
	if SkipCommand:
		SkipCommand = False
		return 0
	elif len(args) == 2:
		stop_bot()
		player = args[1]
		if start_trace(player):
			log('TR_ScriptCommands: [%s] izlenmeye başlanıyor' %player)
			return 0
		else:
			log('TR_ScriptCommands: [%s] yakınlarda değil.. Devam ediliyor' %player)
			SkipCommand = True
			Timer(1.0, start_bot, ()).start()
			Timer(30.0, ResetSkip, ()).start()
			return 0
	log('TR_ScriptCommands: Yanlış StartTrace formatı')
	return 0

def RemoveSkill(args):
	RemSkill = args[1]
	skills = get_active_skills()
	for ID, skill in skills.items():
		if skill['name'] == RemSkill:
			packet = b'\x01\x05'
			packet += struct.pack('<I', ID)
			packet += b'\x00'
			inject_joymax(0x7074,packet,False)
			log('TR_ScriptCommands: [%s] Yeteneği kaldırılıyor' %RemSkill)
			return 0
	log('TR_ScriptCommands: Yetenek aktif değil')
	return 0

def Drop(args):
	DropItem = args[1]
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			name = item['name']
			if name == DropItem:
				p = b'\x07'
				p += struct.pack('B', slot)
				log('TR_ScriptCommands: [%s][%s] düşürülüyor' %(item['quantity'],name))
				inject_joymax(0x7034,p,True)
				return 0
	log(r'TR_ScriptCommands: Düşürülecek öğeniz yok')
	return 0

def OpenphBot(args):
	cmdargs = args[1]
	if os.path.exists(path + "phBot.exe"):
		subprocess.Popen(path + "phBot.exe " + cmdargs)
		log('TR_ScriptCommands: Yeni bir bot açılıyor')
		return 0
	log('TR_ScriptCommands: Geçersiz bot yolu')
	return 0

def DismountPet(args):
	PetType = args[1].lower()
	if PetType == 'pick':
		log('TR_ScriptCommands: Toplama petinden inemezsin')
		return 0
	pets = get_pets()
	if pets:
		for id,pet in pets.items():
			if pet['type'] == PetType:
				p = b'\x00'
				p += struct.pack('I',id)
				inject_joymax(0x70CB,p, False)
				return 0
	return 0

def UnsummonPet(args):
	PetType = args[1].lower()
	pets = get_pets()
	if pets:
		for id,pet in pets.items():
			if pet['type'] == PetType:
				p = struct.pack('I',id)
				if PetType == 'transport' or PetType == 'horse':
					inject_joymax(0x70C6,p, False)
				else:
					inject_joymax(0x7116,p, False)
				log(f'TR_ScriptCommands: [{PetType}] Çağrısı Geri Alınıyor')
				return 0
	return 0

def ResetWeapons(args):
	Items = 'all'
	if len(args) == 2:
		Items = args[1].lower()
	path = get_config_dir()
	CharData = get_character_data()
	ConfigFile = f"{CharData['server']}_{CharData['name']}.{get_profile()}.json" if len(get_profile()) > 0 else f"{CharData['server']}_{CharData['name']}.json"
	if os.path.exists(path + ConfigFile):
		with open(path + ConfigFile,"r") as f:
			Configdata = json.load(f)
			if Items == 'all':
				Configdata['Inventory'] = {"Primary": 0, "Secondary": 0, "Shield": 0}
			if Items == 'primary':
				Configdata['Inventory']['Primary'] = 0
			if Items == 'secondary':
				Configdata['Inventory']['Secondary'] = 0
			if Items == 'shield':
				Configdata['Inventory']['Shield'] = 0
			with open(path + ConfigFile ,"w") as f:
				f.write(json.dumps(Configdata, indent=4))
				log('TR_ScriptCommands: Silahlar sıfırlandı')
				set_profile(get_profile())
				return 0
	return 0

def SetArea(args):
	if len(args) == 2:
		set_training_area(args[1])
		log(f"TR_ScriptCommands: Eğitim alanı [{args[1]}] olarak değiştirildi")
		return 0
	log('TR_ScriptCommands: Lütfen bir eğitim alanı adı belirtin')
	return 0

def CalcRadiusFromME(Px,Py):
	my = get_position()
	dist = ((my['x'] - Px)**2 + (my['y'] - Py)**2)**0.5
	return dist

def ExchangePlayer(args):
	if len(args) == 2:
		PlayerName = args[1]
		party = get_party()
		if not party:
			log(f"TR_ScriptCommands: Partide değilsin!, Takas yapılamaz")
			return 0
		for key, player in party.items():
			if player['name'] == PlayerName:
				radius = CalcRadiusFromME(player['x'],player['y'])
				if player['player_id'] <= 0 or radius > 20:
					log(f"TR_ScriptCommands: Oyuncu [{player['name']}] menzil dışında! Takas yapılamaz")
					return 0
				log(f"TR_ScriptCommands: [{player['name']}] ile takas yapılıyor")
				p = struct.pack('<I', player['player_id'])
				inject_joymax(0x7081,p,True)
				return 0
		log(f"TR_ScriptCommands: Oyuncu [{PlayerName}] partinde değil! Takas yapılamaz")
		return 0
	log(f"TR_ScriptCommands: Lütfen takas edilecek bir oyuncu belirtin! Takas yapılamaz")
	return 0

def ChangeBotOption(args):
	if len(args) <= 3 or len(args) >= 7:
		log(f"TR_ScriptCommands: Yanlış Format, ayar değiştirilemiyor.")
		return 0
	value = args[1]
	path = get_config_dir()
	CharData = get_character_data()
	ConfigFile = f"{CharData['server']}_{CharData['name']}.{get_profile()}.json" if len(get_profile()) > 0 else f"{CharData['server']}_{CharData['name']}.json"
	if os.path.exists(path + ConfigFile):
		with open(path + ConfigFile,"r") as f:
			Configdata = json.load(f)
			if len(args) == 4:
				try:
					data = Configdata[args[2]][args[3]]
				except:
					log('TR_ScriptCommands: Yanlış json anahtarı, ayar değiştirilemiyor')
					return 0
				if type(data) == list:
					Configdata[args[2]][args[3]].append(value)
				else:
					Configdata[args[2]][args[3]] = value

			if len(args) == 5:
				try:
					data = Configdata[args[2]][args[3]][args[4]]
				except:
					log('TR_ScriptCommands: Yanlış json anahtarı, ayar değiştirilemiyor')
					return 0
				if type(data) == list:
					Configdata[args[2]][args[3]][args[4]].append(value)
				else:
					Configdata[args[2]][args[3]][args[4]] = value

			if len(args) == 6:
				try:
					data = Configdata[args[2]][args[3]][args[4]][args[5]]
				except:
					log('TR_ScriptCommands: Yanlış json anahtarı, ayar değiştirilemiyor')
					return 0
				if type(data) == list:
					Configdata[args[2]][args[3]][args[4]][args[5]].append(value)
				else:
					Configdata[args[2]][args[3]][args[4]][args[5]] = value

			with open(path + ConfigFile ,"w") as f:
				f.write(json.dumps(Configdata, indent=4))
				log('TR_ScriptCommands: Ayarlar Başarıyla Değiştirildi')
				set_profile(get_profile())
				return 0

def event_loop():
	global delay_counter, CheckStartTime, SkipCommand, CheckCloseTime
	if CheckStartTime:
		delay_counter += 500
		if delay_counter >= 60000:
			delay_counter = 0
			CurrentTime = str(datetime.datetime.now())[11:16]
			if CurrentTime == StartBotAt:
				CheckStartTime = False
				SkipCommand = True
				log('TR_ScriptCommands: Bot başlatılıyor')
				start_bot()

	elif CheckCloseTime:
		delay_counter += 500
		if delay_counter >= 60000:
			delay_counter = 0
			CurrentTime = str(datetime.datetime.now())[11:16]
			if CurrentTime == CloseBotAt:
				CheckCloseTime = False
				Terminate()

def button_start():
	global BtnStart, RecordedPackets
	if len(QtBind.text(gui,SaveName)) <= 0:
		log('TR_ScriptCommands: Lütfen Özel Script Komutu için bir Ad Girin')
		return
	if BtnStart == False:
		BtnStart = True
		QtBind.setText(gui,RecordBtn,' Kaydı Durdur ')
		log('TR_ScriptCommands: Kayıt başladı, lütfen kayda başlamak için NPC\'yi seçin')

	elif BtnStart == True:
		log('TR_ScriptCommands: Kayıt Tamamlandı')
		Name = QtBind.text(gui,SaveName)
		SaveNPCPackets(Name,RecordedPackets)
		BtnStart = False
		QtBind.setText(gui,RecordBtn,' Kayda Başla ')
		Recording = False
		RecordedPackets = []
		Timer(1.0, button_ShowCmds, ()).start()

def button_ShowCmds():
	QtBind.clear(gui,Display)
	data = {}
	if os.path.exists(path + "CustomNPC.json"):
		with open("CustomNPC.json","r") as f:
			data = json.load(f)
			for name in data:
				QtBind.append(gui,Display,name)
	else:
		log('TR_ScriptCommands: Kayıtlı Komut Yok')

def button_DelCmds():
	Name = QtBind.text(gui,Display)
	QtBind.clear(gui,Display)
	data = {}
	if Name:
		with open("CustomNPC.json","r") as f:
			data = json.load(f)
			for name, value in list(data.items()):
				if name == Name:
					del data[name]
					with open("CustomNPC.json","w") as f:
						f.write(json.dumps(data, indent=4))
						log('TR_ScriptCommands: Özel NPC Komutu [%s] Silindi' %name)
						Timer(1.0, button_ShowCmds, ()).start()
						return
			else:
				log('TR_ScriptCommands: Özel NPC Komutu [%s] mevcut değil' %Name)
				Timer(1.0, button_ShowCmds, ()).start()

def button_ShowPackets():
	Name = QtBind.text(gui,Display)
	QtBind.clear(gui,Display)
	data = {}
	if Name:
		with open("CustomNPC.json","r") as f:
			data = json.load(f)
			for name in data:
				if name == Name:
					Packets = data[name]['Packets']
					for packet in Packets:
						QtBind.append(gui,Display,packet)

def GetPackets(Name):
	global ExecutedPackets
	data = {}
	with open("CustomNPC.json","r") as f:
		data = json.load(f)
		for name in data:
			if name == Name:
				ExecutedPackets = data[name]['Packets']

def SaveNPCPackets(Name,Packets=[]):
	data = {}
	if os.path.exists(path + "CustomNPC.json"):
		with open("CustomNPC.json","r") as f:
			data = json.load(f)
	else:
		data = {}
	data[Name] = {"Packets": Packets}
	with open("CustomNPC.json","w") as f:
		f.write(json.dumps(data, indent=4))
	log("TR_ScriptCommands: Özel NPC Komutu Kaydedildi")

def CustomNPC(args):
	global SkipCommand, StopBot
	if SkipCommand:
		SkipCommand = False
		return 0
	if len(args) < 2:
		log('TR_ScriptCommands: Yanlış komut.')
		return 0
	StopBot = True
	if len(args) == 3:
		State = args[2]
		if State.lower() == 'true':
			StopBot = True
		if State.lower() == 'false':
			StopBot = False
	if StopBot:
		stop_bot()
	Name = args[1]
	GetPackets(Name)
	Timer(0.5, InjectPackets, ()).start()
	return 0

def InjectPackets():
	global Index, ExecutedPackets
	opcode = int(ExecutedPackets[Index].split(':')[0],16)
	dataStr = ExecutedPackets[Index].split(':')[1].replace(' ','')
	LendataStr = len(dataStr)
	data = bytearray()
	for i in range(0,int(LendataStr),2):
			data.append(int(dataStr[i:i+2],16))
	inject_joymax(opcode, data, False)
	if QtBind.isChecked(gui,cbxShowPackets):
		log("TR_ScriptCommands: Enjekte Edildi (Opcode) 0x" + '{:02X}'.format(opcode) + " (Veri) "+ ("Yok" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	NumofPackets = len(ExecutedPackets) - 1
	if Index < NumofPackets:
		Index += 1
		Timer(2.0, InjectPackets, ()).start()

	elif Index == NumofPackets:
		global SkipCommand
		log('TR_ScriptCommands: Özel NPC Komutu Tamamlandı')
		Index = 0
		ExecutedPackets = []
		Timer(30.0, ResetSkip, ()).start()
		SkipCommand = True
		if StopBot:
			start_bot()

def handle_silkroad(opcode, data):
	global Recording, BtnStart, RecordedPackets
	if data == None:
		return True
	if BtnStart:
		if opcode == 0x7045 or opcode == 0x7C45:
			Recording = True
			log('TR_ScriptCommands: Kayıt Başladı')
			RecordedPackets.append("0x" + '{:02X}'.format(opcode) + ":" + ' '.join('{:02X}'.format(x) for x in data))
			if QtBind.isChecked(gui,cbxShowPackets):
				log("TR_ScriptCommands: Kaydedildi (Opcode) 0x" + '{:02X}'.format(opcode) + " (Veri) "+ ("Yok" if not data else ' '.join('{:02X}'.format(x) for x in data)))
		if Recording == True:
			if opcode != 0x7045 or opcode != 0x7C45:
				RecordedPackets.append("0x" + '{:02X}'.format(opcode) + ":" + ' '.join('{:02X}'.format(x) for x in data))
				if QtBind.isChecked(gui,cbxShowPackets):
					log("TR_ScriptCommands: Kaydedildi (Opcode) 0x" + '{:02X}'.format(opcode) + " (Veri) "+ ("Yok" if not data else ' '.join('{:02X}'.format(x) for x in data)))

	return True

log(f'Eklenti: {name} başarıyla yüklendi.')