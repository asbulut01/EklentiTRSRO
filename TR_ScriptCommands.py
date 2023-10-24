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
version = 2.1
NewestVersion = 0

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

gui = QtBind.init(__name__, name)
LvlSaveName = QtBind.createLabel(gui,' Kayıt Adı = ',15,13)
SaveName = QtBind.createLineEdit(gui,"",80,10,120,20)
RecordBtn = QtBind.createButton(gui, 'button_start', '   Kayda Başla   ', 215, 10)
Display = QtBind.createList(gui,15,40,283,150)
ShowCommandsBtn = QtBind.createButton(gui, 'button_ShowCmds', ' Akışı Göster \n Kaydedilen Kod ', 20, 200)
DeleteCommandsBtn = QtBind.createButton(gui, 'button_DelCmds', ' Kodları Sil ', 120, 200)
ShowPacketsBtn = QtBind.createButton(gui, 'button_ShowPackets', ' Paketleri Göster ', 210, 200)
cbxShowPackets = QtBind.createCheckBox(gui, 'cbxAuto_clicked',' Paketleri Göster ', 330, 10)

def ResetSkip():
	global SkipCommand
	SkipCommand = False

def LeaveParty(args):
	if get_party():
		inject_joymax(0x7061,b'',False)
		log('Eklenti: Leaving Party')
	return 0

def Notification(args):
	if len(args) == 3:
		title = args[1]
		message = args[2]
		show_notification(title, message)
		return 0
	log('Eklenti: Yanlış Bildirim Komutu')
	return 0

def NotifyList(args):
	if len(args) == 2:
		message = args[1]
		create_notification(message)
		return 0
	log('Eklenti: Yanlış Liste Bildir Komutu')
	return 0

def PlaySound(args):
	FileName = args[1]
	if os.path.exists(path + FileName):
		play_wav(path + FileName)
		log('Eklenti: [%s] Çalınıyor...' %FileName)
		return 0
	log('Eklenti: Ses Dosyası [%s] bulunamadı.' %FileName)
	return 0

def SetScript(args):
	name = args[1]
	if os.path.exists(path + name):
		set_training_script(path + name)
		log('Eklenti: Komut Dosyası [%s] olarak değiştirildi.' %name)
		return 0
	log('Eklenti: Komut [%s] Bulunamadı.' %name)
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
		log('Eklenti: Bot [%s] de Kapatılacak.' %CloseBotAt)
	elif type == 'at':
		CloseBotAt = time
		log('Eklenti: Bot [%s] de Kapatılacak.' %CloseBotAt)
	return 0

def Terminate():
	log("Eklenti: Bot Kapatılıyor...")
	os.kill(os.getpid(),9)

def GoClientless(args):
	pid = get_client()['pid']
	if pid:
		os.kill(pid, signal.SIGTERM)
		return 0
	log('Eklenti: Client Açık Değil.')
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
		log('Eklenti: Bot [%s] den Başlatılacak.' %StartBotAt)
	elif type == 'at':
		StartBotAt = time
		log('Eklenti: Bot [%s] den Başlatılacak.' %StartBotAt)
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
			log('Eklenti: Takibe başlanıyor [%s]' %player)
			return 0
		else:
			log('Eklenti: Oyuncu [%s] Yakın Değil, Devam ediliyor.' %player)
			SkipCommand = True
			Timer(1.0, start_bot, ()).start()
			Timer(30.0, ResetSkip, ()).start()
			return 0
	log('Eklenti: Yanlış Başlangıç Takip Biçimi')
	return 0

def RemoveSkill(args):
	locale = get_locale()
	if locale == 18 or locale == 22 or locale == 54 or locale == 56 or locale == 59 or locale == 61 or locale == 65:
		RemSkill = args[1]
		skills = get_active_skills()
		for ID, skill in skills.items():
			if skill['name'] == RemSkill:
				packet = b'\x01\x05'
				packet += struct.pack('<I', ID)
				packet += b'\x00'
				inject_joymax(0x7074,packet,False)
				log('Eklenti: Beceri Kaldırılıyor [%s]' %RemSkill)
				return 0
		log('Eklenti: Beceri Aktif Değil.')
		return 0
	log('Eklenti: Eklenti Bu Sunucuda Çalışmamaktadır.')
	return 0

def Drop(args):
	locale = get_locale()
	if locale == 18 or locale == 22 or locale == 54 or locale == 56 or locale == 59 or locale == 61 or locale == 65:
		DropItem = args[1]
		items = get_inventory()['items']
		for slot, item in enumerate(items):
			if item:
				name = item['name']
				if name == DropItem:
					p = b'\x07' # static stuff maybe
					p += struct.pack('B', slot)
					log('Eklenti: Dropping item [%s][%s]' %(item['quantity'],name))
					inject_joymax(0x7034,p,True)
					return 0
		log(r'Eklenti: Bırakacak Eşyan Yok.')
		return 0
	log('Eklenti: Eklenti Bu Sunucuda Çalışmamaktadır.')
	return 0

def OpenphBot(args):
	cmdargs = args[1]
	if os.path.exists(path + "phBot.exe"):
		subprocess.Popen(path + "phBot.exe " + cmdargs)
		log('Eklenti: Yeni phBot Açılıyor...')
		return 0
	log('Eklenti: Bot Yolu Geçersiz.')
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
				log('Eklenti: Bot Başlatılıyor..')
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
		log('Eklenti: Lütfen Özel Komut Dosyası Için Bir Ad Girin')
		return
	if BtnStart == False:
		BtnStart = True
		QtBind.setText(gui,RecordBtn,'   Kaydı Durdur  ')
		log('Eklenti: Başladı, Lütfen Kayda Başlatmak Için NPCyi Seçin.')

	elif BtnStart == True:	
		log('Eklenti: Kayıt Tamamlandı.')
		Name = QtBind.text(gui,SaveName)
		SaveNPCPackets(Name,RecordedPackets)
		BtnStart = False
		QtBind.setText(gui,RecordBtn,'   Kaydı Başlat   ')
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
		log('Eklenti: Kaydedilmiş Komut Yok!')

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
						log('Eklenti: Özel NPC Komutu [%s] Silindi' %name)
						Timer(1.0, button_ShowCmds, ()).start()
						return
			else:
				log('Eklenti: Özel NPC Komutu [%s] mevcut değil' %Name)
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
	log("Eklenti: Özel NPC Komutu Kaydedildi.")

def CustomNPC(args):
	global SkipCommand
	if SkipCommand:
		SkipCommand = False
		return 0
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
		log("Eklenti: Injected (Opcode). 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	NumofPackets = len(ExecutedPackets) - 1
	if Index < NumofPackets:
		Index += 1
		Timer(2.0, InjectPackets, ()).start()

	elif Index == NumofPackets:
		global SkipCommand
		log('Eklenti: Özel NPC Komutu Tamamlandı.')
		Index = 0
		ExecutedPackets = []
		Timer(30.0, ResetSkip, ()).start()
		SkipCommand = True
		start_bot()

def handle_silkroad(opcode, data):
	global Recording, BtnStart, RecordedPackets
	if data == None:
		return True
	if BtnStart:
		if opcode == 0x7045:
			Recording = True
			log('Eklenti: Kayıt Başladı')
			RecordedPackets.append("0x" + '{:02X}'.format(opcode) + ":" + ' '.join('{:02X}'.format(x) for x in data))
			if QtBind.isChecked(gui,cbxShowPackets):
				log("Eklenti: Recorded (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
		if Recording == True:
			if opcode != 0x7045:
				RecordedPackets.append("0x" + '{:02X}'.format(opcode) + ":" + ' '.join('{:02X}'.format(x) for x in data))
				if QtBind.isChecked(gui,cbxShowPackets):
					log("Eklenti: Recorded (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))

	return True

def CheckForUpdate():
	global NewestVersion
	if NewestVersion == 0:
		try:
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_ScriptCommands.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8")).split()
				for num, line in enumerate(lines):
					if line == 'version':
						NewestVersion = int(lines[num+2].replace(".",""))
						CurrentVersion = int(str(version).replace(".",""))
						if NewestVersion > CurrentVersion:
							log('Eklenti: Yeni bir güncelleme var = [%s]!' % name)
							lblUpdate = QtBind.createLabel(gui,'Yeni Bir Güncelleme Mevcut. Yüklemek için Tıkla ->',100,283)
							button1 = QtBind.createButton(gui, 'button_update', ' Güncelle ', 350, 280)
		except:
			pass

def button_update():
	path = get_config_dir()[:-7]
	if os.path.exists(path + "Plugins/" + "TR_ScriptCommands.py"):
		try:
			os.rename(path + "Plugins/" + "TR_ScriptCommands.py", path + "Plugins/" + "TR_ScriptCommandsBACKUP.py")
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_ScriptCommands.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8"))
				with open(path + "Plugins/" + "TR_ScriptCommands.py", "w+") as f:
					f.write(lines)
					os.remove(path + "Plugins/" + "TR_ScriptCommandsBACKUP.py")
					log('Eklenti Başarıyla Güncellendi, Kullanmak için Eklentiyi Yeniden Yükleyin.')
		except Exception as ex:
			log('Güncelleme Hatası [%s] Lütfen Manuel Olarak Güncelleyin veya daha Sonra Tekrar Deneyin.' %ex)

CheckForUpdate()

log('Eklenti:%s v%s Yuklendi. // edit by hakankahya' % (name,version))
