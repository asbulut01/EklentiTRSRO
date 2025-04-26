from phBot import *
from threading import Timer
import struct
import QtBind
import urllib.request

name = 'TR_RewardsCollector'

CollectMessageID = 0

gui = QtBind.init(__name__, name)

button = QtBind.createButton(gui, 'button_collect', '  Ödülleri Topla ', 20, 20)

def button_collect():
	log('TR_RewardsCollector: Tüm Ödüller Alınıyor...')
	GetMessages()

def handle_joymax(opcode,data):
	global CollectMessageID
	if opcode == 0x38DD and data[0] == 1 and data[1] == 1:
		log('TR_RewardsCollector: Ödül Mesajı Alındı...')
		CollectMessageID = struct.unpack_from('<Q', data, 2)[0]

	if opcode == 0xB0DE:
		if data[0] == 2 and data[1] == 5 and data[2] == 7 and data[3] == 220:
			log('TR_RewardsCollector: Mesajlar Alınırken Hata Oluştu... Lütfen ışınlanın')
			return True
		if data[0] == 1 and data[1] == 5:
			messageCount = struct.unpack_from('<H', data, 2)[0]
			Index = 6
			for i in range(messageCount):
				try:
					Index += 1
					messageID = struct.unpack_from('<Q', data, Index)[0]
					Index += 9
					MessageSenderLength = struct.unpack_from('<H', data, Index)[0]
					Index += 2
					messageSender = struct.unpack_from('<' + str(MessageSenderLength) + 's',data,Index)[0].decode('cp1252')
					log(messageSender)
					Index += MessageSenderLength
					messageTypeLength = struct.unpack_from('<H', data, Index)[0]
					Index += 2
					messageType = struct.unpack_from('<' + str(messageTypeLength*2) + 's',data,Index)[0].decode('utf-16')
					log(messageType)
					Index += messageTypeLength*2
					Index += 8
					itemAmount = struct.unpack_from('<B', data, Index)[0]
					Index += (itemAmount * 4) + 1

					if "UIIT_" in messageType:
						if GetRemainingSlots() < 3:
							log('TR_RewardsCollector: Öğeleri Almak için Yeterli Envanter Yuvası Yok...')
							return True
						receiveItemFromMessage(messageID)
				except Exception as ex:
					pass
	return True

def GetMessages():
	p = b'\x05'
	inject_joymax(0x70DE,p, False)

def receiveItemFromMessage(messageID):
	p = b'\x01'
	p += struct.pack('<Q', messageID)
	inject_joymax(0x70DF, p, False)
	log('TR_RewardsCollector: [%s] Mesajından Öğeler Alınıyor' %messageID)

def DeleteMessage(messageID):
	p = b'\x04\x01'
	p += struct.pack('<Q', messageID)
	inject_joymax(0x70DE, p, False)
	log('TR_RewardsCollector: [%s] Mesajı Siliniyor' %messageID)

def GetRemainingSlots():
	Size = get_inventory()['size'] - 13
	Items = get_inventory()['items']
	TotalItems = 0
	for slot, Item in enumerate(Items):
		if slot >= 13:
			if Item:
				TotalItems += 1
	return Size - TotalItems

def teleported():
	global CollectMessageID
	if CollectMessageID != 0:
		if GetRemainingSlots() < 3:
			log('TR_RewardsCollector: Öğeleri Almak için Yeterli Envanter Yuvası Yok...')
			return
		Timer(5.0, receiveItemFromMessage, [CollectMessageID]).start()
		CollectMessageID = 0

log(f'Eklenti: {name} başarıyla yüklendi.')