from phBot import *
from threading import Timer
import struct
import QtBind
import urllib.request

name = 'TR_ItemStorage'
version = 2.0

gui = QtBind.init(__name__, name)

button = QtBind.createButton(gui, 'button_getlist', '  Listeyi Al  ', 20, 20)
button = QtBind.createButton(gui, 'button_claim', '  Seçilenleri Talep Et  ', 200, 20)
button = QtBind.createButton(gui, 'button_claimall', '  Hepsini Talep Et  ', 400, 20)
lstItems = QtBind.createList(gui,10,62,580,200)

def button_getlist():
	global count
	count = 0
	QtBind.clear(gui,lstItems)
	OpenItemList(1)
	

def button_claim():
	SelectedItem = QtBind.text(gui,lstItems)
	messageID = SelectedItem.split(" ")[0].strip("[]")
	receiveItem(int(messageID))

def button_claimall():
	inject_joymax(0x7558 , b'\x00\x00\x00\x00\x00\x00\x00\x00', False)

count = 0

def handle_joymax(opcode,data):
	global count
	if opcode == 0xB557:
		locale = get_locale()
		if data[0] == 1:
			PageCount = struct.unpack_from('<B', data, 1)[0]
			CurrentPage = struct.unpack_from('<B', data, 2)[0]
			ItemCount = struct.unpack_from('<B', data, 3)[0]
			Index = 4
			for i in range(ItemCount):
				if locale == 18 or locale == 56: #isro and trsro
					try:
						messageID = struct.unpack_from('<Q', data, Index)[0]
						Index += 8
						Type = struct.unpack_from('<I', data, Index)[0]
						Index += 4
						if Type == 3:
							ItemID = struct.unpack_from('<I', data, Index)[0]
							ItemName = get_item(ItemID)['name']
							Index += 4
							Quantity = struct.unpack_from('<I', data, Index)[0]
							Index += 12
							QtBind.append(gui,lstItems,f"[{messageID}] - [{ItemName}]")
							count += 1
							continue
						ItemNameLength = struct.unpack_from('<H', data, Index)[0]
						Index += 2
						ItemName = struct.unpack_from('<' + str(ItemNameLength*2) + 's',data,Index)[0].decode('utf-16')
						Index += ItemNameLength*2
						Index += 12
						QtBind.append(gui,lstItems,f"[{messageID}] - [{ItemName}]")
						count += 1
					except Exception as ex:
						data = str(' '.join('{:02X}'.format(x) for x in data))
						log(f"Eklenti: Eşya Deposu verileri çözülenirken hata oluştu, bu verileri Discord'da paylaşın [{data}] [{get_locale()}]")
						pass
				else: #all other servers? based on private servers but probably doesnt work because this example only has type 3
					try:
						messageID = struct.unpack_from('<Q', data, Index)[0]
						Index += 8
						Type = struct.unpack_from('<I', data, Index)[0]
						Index += 4
						if Type == 3:
							ItemID = struct.unpack_from('<I', data, Index)[0]
							ItemName = get_item(ItemID)['name']
							Index += 4
							Quantity = struct.unpack_from('<I', data, Index)[0]
							Index += 8
							QtBind.append(gui,lstItems,f"[{messageID}] - [{ItemName}]")
							count += 1
					except Exception as ex:
						data = str(' '.join('{:02X}'.format(x) for x in data))
						log(f"Eklenti: Eşya Deposu verileri çözülenirken hata oluştu, bu verileri Discord'da paylaşın [{data}] [{get_locale()}]")
						pass	
								
			log(f"Eklenti: [{CurrentPage}] / [{PageCount}] sayfasının kontrolü tamamlandı")
			if CurrentPage < PageCount:
				Timer(1.0,OpenItemList,[CurrentPage+1]).start()
			else:
				log(f"Eklenti: Tüm kontroller tamamlandı, toplam eşya sayısı [{count}]")
				
	if opcode == 0xB558:
		if data[0] == 2:
			log(f"Eklenti: İpek eşyası alınamadı, envanteriniz dolu mu?")
	
	return True

def OpenItemList(page):
	p = struct.pack('B',page)
	inject_joymax(0x7557,p, False)


def receiveItem(messageID):
	p = struct.pack('<Q', messageID)
	inject_joymax(0x7558 , p, False)

log('Eklenti: [%s] Sürüm %s Yüklendi. // edit by hakankahya' % (name,version))
