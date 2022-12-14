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

name = 'xKomut'

#get phbot folder path
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
LvlSaveName = QtBind.createLabel(gui,'Kayıt Adı ',10,13)
SaveName = QtBind.createLineEdit(gui,"",60,10,121,20)
RecordBtn = QtBind.createButton(gui, 'button_start', ' Kaydı Başlat ', 185, 8)
Display = QtBind.createList(gui,15,40,245,180)
ShowCommandsBtn = QtBind.createButton(gui, 'button_ShowCmds', ' Akımı Göster ', 10, 230)
DeleteCommandsBtn = QtBind.createButton(gui, 'button_DelCmds', ' Komut Sil ', 90, 230)
ShowPacketsBtn = QtBind.createButton(gui, 'button_ShowPackets', ' Paketleri Göster ', 170, 230)
cbxShowPackets = QtBind.createCheckBox(gui, 'cbxAuto_clicked','Paket İçeriğini Göster! ', 65, 260)
QtBind.createLabel(gui,' ↓ Geçerli komutların listesi : ↓',300,10)
QtBind.createLabel(gui, '- LeaveParty : Partiden Ayrılır.\n- Notification,title,message : Simge durumunda bildirim gönderir.\n- NotifyList,message : Yeni bildirim ekle.\n- PlaySound,ding.wav : Belirtilen Sesi Çalar.\n- SetScript,scriptname.txt : Komut dosyası phbot klasöründe olmalıdır. \n- CloseBot : Botu Kapatır.\n- CloseBot,in,X : Botu x Dakika içinde Kapatır. Örn : CloseBot,in,5\n- CloseBot,at,00:00 : Botu x Saatte Kapatır. Örn : CloseBot,at,00:00\n- StartBot,in,X : Botu Durdurur ve x Dakika Sonra Başlatır. Örn : StartBot,in,5\n- StartBot,at,00:00 : Botu Durdurur ve x saatinde Başlatır. Örn : StartBot,at,00:00\n- GoClientless : Clienti Anında Düşürür.\n- StopStart : 1 Saniyede botu durdurur ve başlatır\n- StartTrace,player : Bir oyuncuyu takibe başlar.\n- RemoveSkill,skillname : Etkinse beceriyi kaldırır.\n- Drop,itemname : Belirtilen Eşyayı Yere Bırakır.\n- OpenphBot,commandlinearguments : Belirtilen bilgilerle yeni bot açar.\n- CustomNPC,savedname : Kayıt ettiğin NPC Komutunu dosyaya ekler.', 265, 30)
metaby = QtBind.createLabel(gui,'edited by hakankahya',500,260)

#backup
def ResetSkip():
	global SkipCommand
	SkipCommand = False

def LeaveParty(args):
	if get_party():
		inject_joymax(0x7061,b'',False)
		log('Plugin: Partiden Ayrıldı.')
	return 0

#Notification,title,message..show a windows notification, bot must be minimized
def Notification(args):
	if len(args) == 3:
		title = args[1]
		message = args[2]
		show_notification(title, message)
		return 0
	log('Plugin: Yanlış Bildirim komutu!')
	return 0

#NotifyList,message.. Create a notification in the list
def NotifyList(args):
	if len(args) == 2:
		message = args[1]
		create_notification(message)
		return 0
	log('Plugin: Yanlış Bildirim Listesi komutu!')
	return 0

#PlaySound,ding.wav...wav file must be in your phbot folder
def PlaySound(args):
	FileName = args[1]
	if os.path.exists(path + FileName):
		play_wav(path + FileName)
		log('Plugin: Oynatılıyor [%s]' %FileName)
		return 0
	log('Plugin: Ses Dosyası yok! [%s]' %FileName)
	return 0

#example - SetScript,Mobs103.txt
#script must be in your phbot folder
def SetScript(args):
	name = args[1]
	if os.path.exists(path + name):
		set_training_script(path + name)
		log('Plugin: Komut Dosyasını şu şekilde değiştirildi → [%s]' %name)
		return 0
	log('Plugin: Komut [%s] Bulunamadı.' %name)
	return 0

#CloseBot..kills the bot immediately
#CloseBot,in,5... kills the bot in 5 mins
#CloseBot,at,05:30..kills the bot at a specific time.. 24hour clock
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
		log('Plugin: Bot Kapatılıyor [%s]' %CloseBotAt)
	elif type == 'at':
		CloseBotAt = time
		log('Plugin: Bot Kapatılıyor [%s]' %CloseBotAt)
	return 0

def Terminate():
	log("Plugin: Bot Kapatılıyor...")
	os.kill(os.getpid(),9)

#GoClientless.. Kills the Client instantly
def GoClientless(args):
	pid = get_client()['pid']
	if pid:
		os.kill(pid, signal.SIGTERM)
		return 0
	log('Plugin: Client düşürülüyor.')
	return 0


#Stop and Start the bot at specified time
#Ex StartBot,in,5.. Starts bot in 5 mins
#Ex StartBot,at,05:30.. Starts bot at specified time.. 24hour clock
def StartBot(args):
	global StartBotAt, CheckStartTime, SkipCommand
	#avoid bot doing command again after restarting
	if SkipCommand:
		SkipCommand = False
		return 0
	stop_bot()
	type = args[1]
	time = args[2]
	CheckStartTime = True
	if type == 'in':
		StartBotAt = str(datetime.datetime.now() + timedelta(minutes=int(time)))[11:16]
		log('Plugin: Bot Başlatılıyor [%s]' %StartBotAt)
	elif type == 'at':
		StartBotAt = time
		log('Plugin: Bot Başlatılıyor [%s]' %StartBotAt)
	return 0

#StopStart..Stops and starts the bot 1 second later
def StopStart(args):
	global SkipCommand
	#avoid bot doing command again after restarting
	if SkipCommand:
		SkipCommand = False
		return 0
	stop_bot()
	Timer(1.0, start_bot, ()).start()
	#some cases the bot may not pass over the command again when starting again
	Timer(30.0, ResetSkip, ()).start()
	SkipCommand = True
	return 0

#StartTrace,player..Starts tracing a player
def StartTrace(args):
	global SkipCommand
	#avoid bot doing command again after restarting
	if SkipCommand:
		SkipCommand = False
		return 0
	elif len(args) == 2:
		stop_bot()
		player = args[1]
		if start_trace(player):
			log('Plugin: Takip Başladı. [%s]' %player)
			return 0
		else:
			log('Plugin: Oyuncu [%s] yakın değil.. Devam' %player)
			SkipCommand = True
			Timer(1.0, start_bot, ()).start()
			#some cases the bot may not pass over the command again when starting again
			Timer(30.0, ResetSkip, ()).start()
			return 0
	log('Plugin: Yanlış Başlangıç izleme biçimi')
	return 0

#RemoveSkill,skillname...Remove the skill if active
def RemoveSkill(args):
	locale = get_locale()
	if locale == 18 or locale == 56:
		RemSkill = args[1]
		skills = get_active_skills()
		for ID, skill in skills.items():
			if skill['name'] == RemSkill:
				packet = b'\x01\x05'
				packet += struct.pack('<I', ID)
				packet += b'\x00'
				inject_joymax(0x7074,packet,False)
				log('Plugin: Beceriyi kaldırma [%s]' %RemSkill)
				return 0
		log('Plugin: Beceri aktif değil')
		return 0
	log('Plugin: Yalnızca ISRO veya TRSROda Çalışır.')
	return 0

#Drop,itemname... drops the first stack of the specified item
def Drop(args):
	locale = get_locale()
	if locale == 18 or locale == 56:
		DropItem = args[1]
		items = get_inventory()['items']
		for slot, item in enumerate(items):
			if item:
				name = item['name']
				if name == DropItem:
					p = b'\x07' # static stuff maybe
					p += struct.pack('B', slot)
					log('Plugin: Öğeyi bırakma [%s][%s]' %(item['quantity'],name))
					inject_joymax(0x7034,p,True)
					return 0
		log(r'Plugin: Bırakacak Eşyaların Yok.')
		return 0
	log('Plugin: Yalnızca ISRO veya TRSROda Çalışır.')
	return 0

#OpenphBot,commandlinearguments..opens a bot with the specified arguements
def OpenphBot(args):
	cmdargs = args[1]
	if os.path.exists(path + "phBot.exe"):
		subprocess.Popen(path + "phBot.exe " + cmdargs)
		log('Plugin: Yeni bir bot açılıyor...')
		return 0
	log('Plugin: Bot Yolu geçersiz.')
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
				log('Plugin: Bot Başlatıldı.')
				start_bot()

	elif CheckCloseTime:
		delay_counter += 500
		if delay_counter >= 60000:
			delay_counter = 0
			CurrentTime = str(datetime.datetime.now())[11:16]
			if CurrentTime == CloseBotAt:
				CheckCloseTime = False
				Terminate()

#-----------------Custom Script Command Stuffs-----------------

def button_start():
	global BtnStart, RecordedPackets
	if len(QtBind.text(gui,SaveName)) <= 0:
		log('Plugin: Lütfen Özel Komut Dosyası için bir Ad Girin!')
		return
	if BtnStart == False:
		BtnStart = True
		QtBind.setText(gui,RecordBtn,' Kaydı Durdur ')
		log('Plugin: Kayıt Başladı, NPC seçimlerini yapın.')

	elif BtnStart == True:	
		log('Plugin: Kayıt Tamamlandı')
		Name = QtBind.text(gui,SaveName)
		SaveNPCPackets(Name,RecordedPackets)
		BtnStart = False
		QtBind.setText(gui,RecordBtn,' Kayıt Başladı ')
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
		log('Plugin: Şu Anda Kaydedilmiş Komut Yok!')

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
						log('Plugin: Özel NPC Komutu Silindi [%s]' %name)
						Timer(1.0, button_ShowCmds, ()).start()
						return
			else:
				log('Plugin: Özel NPC Komutu yok [%s]' %Name)
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
	log("Plugin: Özel NPC Komutu Kaydedildi.")


def CustomNPC(args):
	global SkipCommand
	if SkipCommand:
		SkipCommand = False
		return 0
	stop_bot()
	Name = args[1]
	GetPackets(Name)
	#avoid the bot closing the npc window
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
		log("Plugin: Injected (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
	NumofPackets = len(ExecutedPackets) - 1
	if Index < NumofPackets:
		Index += 1
		Timer(2.0, InjectPackets, ()).start()

	elif Index == NumofPackets:
		global SkipCommand
		log('Plugin: Bitmiş Özel NPC Komutu.')
		Index = 0
		ExecutedPackets = []
		#some cases the bot may not pass over the command when starting again
		Timer(30.0, ResetSkip, ()).start()
		SkipCommand = True
		start_bot()


def handle_silkroad(opcode, data):
	global Recording, BtnStart, RecordedPackets
	if data == None:
		return True
	if BtnStart:
		#select NPC to start recording
		if opcode == 0x7045:
			Recording = True
			log('Plugin: Recording Started')
			RecordedPackets.append("0x" + '{:02X}'.format(opcode) + ":" + ' '.join('{:02X}'.format(x) for x in data))
			if QtBind.isChecked(gui,cbxShowPackets):
				log("Plugin: Recorded (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
		if Recording == True:
			if opcode != 0x7045:
				RecordedPackets.append("0x" + '{:02X}'.format(opcode) + ":" + ' '.join('{:02X}'.format(x) for x in data))
				if QtBind.isChecked(gui,cbxShowPackets):
					log("Plugin: Recorded (Opcode) 0x" + '{:02X}'.format(opcode) + " (Data) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))

	return True

log('Plugin: %s Yüklendi! Çalışıyor...' % (__name__))
