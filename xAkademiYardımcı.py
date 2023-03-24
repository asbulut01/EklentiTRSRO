from phBot import *
import phBot
import struct
import threading
import QtBind
import time

pName = 'xAkademiYardımcı'

# ______________________________ Initializing ______________________________ #

# Graphic user interface
gui = QtBind.init(__name__,pName)
QtBind.createLabel(gui, 'Silkroad Online Türkiye Otomatik Akademi Buff ve Guild Puanı Bağışlama Eklentisine Hoşgeldiniz.', 10, 15)
QtBind.createLabel(gui, '↓  Otomatik Akademi Bufflama   ↓', 20, 40)
QtBind.createLabel(gui, '↓  Guild Puanı Bağışlama   ↓', 270, 40)
QtBind.createButton(gui, 'buffNow', '      Hemen Buffla      ', 40, 70)
QtBind.createButton(gui, 'buffTimer', ' Zamanlamayı Başlat ', 40, 100)
QtBind.createButton(gui, 'stopTimer', 'Zamanlamayı Durdur ', 40, 130)
second = QtBind.createLabel(gui, 'Zamanlama :           Dakika ', 30, 175)
txtMinutes = QtBind.createLineEdit(gui, '30', 95, 170, 25, 20)
QtBind.createButton(gui,'DonateGP_50',"  50 GP Bağışla  ",285,70)
QtBind.createButton(gui,'DonateGP_100'," 100 GP Bağışla ",285,100)
QtBind.createButton(gui,'DonateGP_200'," 200 GP Bağışla ",285,130)
QtBind.createButton(gui,'DonateGP_500'," 500 GP Bağışla ",285,160)
QtBind.createButton(gui,'DonateGP_1000',"1000 GP Bağışla",285,190)
QtBind.createButton(gui,'DonateGP_2950',"2950 GP Bağışla",285,220)
QtBind.createButton(gui,'DonateGP_All',"Tamamını Bağışla",285,250)
QtBind.createList(gui,220,40,1,240)
metaby = QtBind.createLabel(gui,'edited by hakankahya',590,298)

# ______________________________ DonateGP ______________________________ #

def DonateGP(quantity=None):
	if quantity == None:
		quantity = phBot.get_character_data()['sp']
		if quantity == 0:
			return
	phBot.inject_joymax(0x7258,struct.pack('I', quantity),False)
    
def handle_joymax(opcode, data):
	global pressed
	if opcode == 0x304E and pressed:
		pressed = False
		eventId = struct.unpack_from('<H', data, 0)[0]
		if eventId == 4113:
			currentGP = struct.unpack_from('<I', data, 2)[0]
			packed = struct.pack('<I', currentGP)
			if currentGP > 0:
			    log('Plugin: ' + 'şuan [' + str(currentGP) + '] GP mevcut, Bagişlandı..')
			    inject_joymax(0x7258, packed, False)	
	return True

pressed = False

def DonateGP_All():
	global pressed
	pressed = True
	inject_joymax(0x7258, struct.pack('<I', 1), False)

# ______________________________ AkademiBuff ______________________________ #

iCounter=0
iCounter2=0
tmr=threading.Timer
tmr2=threading.Timer

def buffNow():
	log('Akademi Buff Aktif edildi.')
	inject_joymax(0x7483,b'', False)
    
def buffTimer():
	log('Zamanlama Başlatıldı!')
	counter=QtBind.text(gui, txtMinutes)
	global iCounter,tmr,tmr2,iCounter2
	iCounter=int(counter)
	iCounter*=60
	iCounter2=iCounter/60
	tmr = threading.Timer(iCounter, buffForTimer) 
	tmr.start()
	tmr2=threading.Timer(60, showLeft) 
	tmr2.start()
	
def stopTimer():
	log('Zamanlama Durduruldu!')
	global tmr,tmr2
	tmr.cancel()
	tmr2.cancel()
    
def buffForTimer():
	buffNow()
	global iCounter,tmr,iCounter2
	iCounter2=iCounter/60
	tmr = threading.Timer(iCounter, buffForTimer) 
	tmr.start()
    
def showLeft():
	global tmr2,iCounter2
	iCounter2-=1
	tmr2=threading.Timer(60, showLeft) 
	tmr2.start()
    
# Donate by using conditions

def DonateGP_50():
	DonateGP(50) 
	log('Plugin: 50 GP Bağışlandı')
    
def DonateGP_100():
	DonateGP(100) 
	log('Plugin: 100 GP Bağışlandı')
    
def DonateGP_200():
	DonateGP(200) 
	log('Plugin: 200 GP Bağışlandı')

def DonateGP_500():
	DonateGP(500) 
	log('Plugin: 500 GP Bağışlandı')

def DonateGP_1000():
	DonateGP(1000) 
	log('Plugin: 1000 GP Bağışlandı')

def DonateGP_2950():
	DonateGP(2950) 
	log('Plugin: 2950 GP Bağışlandı')
    
# Plugin load success
log('Plugin: %s Yüklendi! Çalışıyor...' % (__name__))
