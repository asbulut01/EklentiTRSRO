from phBot import *
from threading import Timer
import QtBind
import struct
import urllib.request

name = 'TR_CarnivalBalloon'
version = '2.0'
NewestVersion = 0

INFLATE_BALLOON_LEVEL_STOP = 6
INFLATE_BALLOON_LEVELUP_DELAY = 1.0

gui = QtBind.init(__name__,name)

txtOpcode = QtBind.createLineEdit(gui,"",85,45,40,20)
btnSetLevel = QtBind.createButton(gui,'btnSetLevel_clicked'," Seviyeyi Ayarla ",135,45)
lblLevel = QtBind.createLabel(gui,' Mevcut Seviye: ' + str(INFLATE_BALLOON_LEVEL_STOP) ,75,85)
btnBaslat = QtBind.createButton(gui,'InflateBalloons'," Balonları Uçurmaya Başla ",75,120)

def btnSetLevel_clicked():
    INFLATE_BALLOON_LEVEL_STOP = int(QtBind.text(gui,txtOpcode))
    QtBind.setText(gui,lblLevel,' Mevcut Seviye: ' + str(INFLATE_BALLOON_LEVEL_STOP))

def GetItemByExpression(_lambda):
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			if _lambda(item['name'],item['servername']):
				item['slot'] = slot
				return item
	return None

def InflateNewBalloon():
	item = GetItemByExpression(lambda n,s: s.startswith('ITEM_ETC_E101216_BALLOON_'))
	if item:
		global inflatingLevel
		inflatingLevel = 1
		p = struct.pack('B',item['slot'])
		p += b'\x30\x0C\x09\x00'
		log('Eklenti: Using "'+item['name']+'"...')
		inject_joymax(0x704C,p,True)
		Timer(INFLATE_BALLOON_LEVELUP_DELAY,LevelUpBalloon).start()
	else:
		global isInflating
		isInflating = False
		log('Eklenti: Balon Bulunamadı, Return Çekiliyor..')
		use_return_scroll()
		start_bot()

def LevelUpBalloon():
	global inflatingLevel
	if inflatingLevel >= INFLATE_BALLOON_LEVEL_STOP:
		log('Eklenti: Balon Ödülünü Alındı. (Lv.'+str(inflatingLevel)+')')
		inject_joymax(0x7574,b'\x02',False)
		inflatingLevel = 0
		Timer(INFLATE_BALLOON_LEVELUP_DELAY,LevelUpBalloon).start()
	elif inflatingLevel:
		log('Eklenti: Balon Şişiriliyor...')
		inject_joymax(0x7574,b'\x01',False)
		Timer(INFLATE_BALLOON_LEVELUP_DELAY,LevelUpBalloon).start()
	else:
		InflateNewBalloon()

def InflateBalloons():
	if not isInflating:
		inflate_balloons([])

def inflate_balloons(args):
	item = GetItemByExpression(lambda n,s: s.startswith('ITEM_ETC_E101216_BALLOON_'))
	if item:
		stop_bot()
		global isInflating
		isInflating = True
		log('Eklenti: Balonlar Şişirilmeye Başlandı...')
		Timer(0.001,InflateNewBalloon).start()
	else:
		log('Eklenti: Envanterinizde Balon Bulunmuyor.')
	return 0

def handle_joymax(opcode,data):
	if opcode == 0xB574 and isInflating:
		if data[0] == 1:
			global inflatingLevel
			if data[1] == 1:
				inflatingLevel += 1
			elif data[1] == 2:
				inflatingLevel = 0
	return True

def CheckForUpdate():
	global NewestVersion
	if NewestVersion == 0:
		try:
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_CarnivalBalloon.py', headers={'User-Agent': 'Mozilla/5.0'})
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
	if os.path.exists(path + "Plugins/" + "TR_CarnivalBalloon.py"):
		try:
			os.rename(path + "Plugins/" + "TR_CarnivalBalloon.py", path + "Plugins/" + "TR_CarnivalBalloonBACKUP.py")
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_CarnivalBalloon.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8"))
				with open(path + "Plugins/" + "TR_CarnivalBalloon.py", "w+") as f:
					f.write(lines)
					os.remove(path + "Plugins/" + "TR_CarnivalBalloonBACKUP.py")
					log('Eklenti Başarıyla Güncellendi, Kullanmak için Eklentiyi Yeniden Yükleyin.')
		except Exception as ex:
			log('Güncelleme Hatası [%s] Lütfen Manuel Olarak Güncelleyin veya daha Sonra Tekrar Deneyin.' %ex)

CheckForUpdate()

log('Eklenti:%s v%s Yuklendi. // edit by hakankahya' % (name,version))