from phBot import *
from threading import Timer
import struct
import QtBind
import urllib.request

name = 'TR_ItemStorage'

gui = QtBind.init(__name__, name)

button = QtBind.createButton(gui, 'button_getlist', '  Listeyi Al  ', 20, 20)
button = QtBind.createButton(gui, 'button_claim', '  Seçileni Al  ', 200, 20)
button = QtBind.createButton(gui, 'button_claimall', '  Hepsini Al  ', 400, 20)
lstItems = QtBind.createList(gui,10,62,580,200)

def button_getlist():
	global count
	count = 0
	QtBind.clear(gui,lstItems)
	OpenItemList(1)

def button_claim():
    SelectedItem = QtBind.text(gui,lstItems)
    if not SelectedItem:
        log('TR_ItemStorage: Lütfen bir öğe seçin.')
        return
    try:
        messageID = SelectedItem.split(" ")[0].strip("[]")
        receiveItem(int(messageID))
    except ValueError:
        log(f'TR_ItemStorage: Geçersiz öğe seçildi: "{SelectedItem}"')
    except IndexError:
        log(f'TR_ItemStorage: Beklenmeyen liste öğesi formatı: "{SelectedItem}"')

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
				if locale == 18 or locale == 56 or locale == 59:
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
						log(f"TR_ItemStorage: Item Storage verilerini ayrıştırırken hata oluştu. [{data}] [{get_locale()}]")
						pass
				else:
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
						log(f"TR_ItemStorage: Item Storage verilerini ayrıştırırken hata oluştu. [{data}] [{get_locale()}]")
						pass

			log(f"TR_ItemStorage: Sayfa kontrolü tamamlandı [{CurrentPage}] / [{PageCount}]")
			if CurrentPage < PageCount:
				Timer(1.0,OpenItemList,[CurrentPage+1]).start()
			else:
				log(f"TR_ItemStorage: Tüm kontrol tamamlandı, toplam öğe [{count}]")

	if opcode == 0xB558:
		if data[0] == 2:
			log(f"TR_ItemStorage: İpek öğesi toplanamadı, envanteriniz dolu mu?")

	return True

def OpenItemList(page):
	p = struct.pack('B',page)
	inject_joymax(0x7557,p, False)

def receiveItem(messageID):
	p = struct.pack('<Q', messageID)
	inject_joymax(0x7558 , p, False)

log(f'Eklenti: {name} başarıyla yüklendi.')