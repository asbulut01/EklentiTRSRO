from phBot import *
from threading import Timer
import struct
import QtBind
import urllib.request

name = 'TR_RewardsCollector'
version = 2.0
NewestVersion = 0

gui = QtBind.init(__name__, name)

button = QtBind.createButton(gui, 'button_collect', '  Ödülleri Topla  ', 20, 20)

def button_collect():
	log('Eklenti: Tüm Ödülleri Alınıyor...')
	GetMessages()

def handle_joymax(opcode,data):
	if opcode == 0x38DD and data[0] == 1 and data[1] == 1:
		log('Eklenti: Ödül Mesajı Alındı...')
		messageID = struct.unpack_from('<Q', data, 2)[0]
		if GetRemainingSlots() < 3:
			log('Eklenti: Öğeleri Talep Etmek için Yeterli Envanter Alanı Yok!')
			return True
		Timer(25.0, receiveItemFromMessage, [messageID]).start()

	if opcode == 0xB0DE:
		if data[0] == 2 and data[1] == 5 and data[2] == 7 and data[3] == 220:
			log('Eklenti: Mesaj Alınırken Hata Oluştu, Lütfen Işınlanın!')
			return True
		if data[0] == 1 and data[1] == 5:	
			messageCount = data[5]
			Index = 6
			for i in range(messageCount):
				Index += 1
				messageID = struct.unpack_from('<Q', data, Index)[0]
				Index += 9
				MessageLength = struct.unpack_from('<H', data, Index)[0]
				Index += (MessageLength + 2)
				messageTypeLength = struct.unpack_from('<H', data, Index)[0]
				Index += 2
				messageType = struct.unpack_from('<' + str(messageTypeLength - 4) + 's',data,(Index + 4))[0].decode('cp1252')
				Index += messageTypeLength
				Index += 8
				itemAmount = struct.unpack_from('<B', data, Index)[0]
				Index += (itemAmount * 4) + 1

				if messageType.endswith(('UIIT_STYRIA_SERVER_TITLE', 'UIIT_INFINITY_SERVER_TITLE')):
					if GetRemainingSlots() < 3:
						log('Eklenti: Öğeleri Talep Etmek için Yeterli Envanter Alanı Yok!')
						return True
					receiveItemFromMessage(messageID)
					#Timer(0.3, DeleteMessage, [messageID]).start()
	return True

def GetMessages():
	p = b'\x05'
	inject_joymax(0x70DE,p, False)

def receiveItemFromMessage(messageID):
	p = b'\x01'
	p += struct.pack('<Q', messageID)
	inject_joymax(0x70DF, p, False)
	log('Eklenti: Mesajdaki Öğeleri Talep Etme [%s]' %messageID)

def DeleteMessage(messageID):
	p = b'\x04\x01'
	p += struct.pack('<Q', messageID)
	inject_joymax(0x70DE, p, False)
	log('Eklenti: Mesaj Siliniyor [%s]' %messageID)

def GetRemainingSlots():
	Size = get_inventory()['size'] - 13
	Items = get_inventory()['items']
	TotalItems = 0
	for slot, Item in enumerate(Items):
		if slot >= 13:
			if Item:
				TotalItems += 1
	return Size - TotalItems

def CheckForUpdate():
	global NewestVersion
	if NewestVersion == 0:
		try:
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_RewardsCollector.py', headers={'User-Agent': 'Mozilla/5.0'})
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
	if os.path.exists(path + "Plugins/" + "TR_RewardsCollector.py"):
		try:
			os.rename(path + "Plugins/" + "TR_RewardsCollector.py", path + "Plugins/" + "TR_RewardsCollectorBACKUP.py")
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_RewardsCollector.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8"))
				with open(path + "Plugins/" + "TR_RewardsCollector.py", "w+") as f:
					f.write(lines)
					os.remove(path + "Plugins/" + "TR_RewardsCollectorBACKUP.py")
					log('Eklenti Başarıyla Güncellendi, Kullanmak için Eklentiyi Yeniden Yükleyin.')
		except Exception as ex:
			log('Güncelleme Hatası [%s] Lütfen Manuel Olarak Güncelleyin veya daha Sonra Tekrar Deneyin.' %ex)

CheckForUpdate()

log('Eklenti:%s v%s Yuklendi. // edit by hakankahya' % (name,version))
