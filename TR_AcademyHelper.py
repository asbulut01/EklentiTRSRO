from phBot import *
import threading
import phBotChat
import struct
import time
import QtBind
import json
import os

pName = 'TR_AcademyHelper'
pVersion = '3.0'
gui = QtBind.init(__name__,pName)
lblCizgi1 = QtBind.createList(gui,10,10,200,250)
lblProfil = QtBind.createLabel(gui,'Yapılandırma Adı:', 19, 225)
tbxProfil = QtBind.createLineEdit(gui,"", 104, 223, 90, 19)
lblNot = QtBind.createLabel(gui,'<font color="red">Not:</font> Yapılandırma Adını Boş Bırakarak<br>Kaydet Yapınız. Yeniden Yükleme<br>Sırasında Ayarlarınız Yüklenecektir.', 19, 175)
btnSaveConfig = QtBind.createButton(gui,'btnSaveConfig_clicked',"  Kaydet  ", 25, 140)
btnLoadConfig = QtBind.createButton(gui,'btnLoadConfig_clicked',"  Geri Yükle  ", 115, 140)
lblPTMaster = QtBind.createLabel(gui,'Parti Lideri:', 25, 20)
tbxPTMaster = QtBind.createLineEdit(gui,"", 96, 18, 95, 19)
lblAMaster = QtBind.createLabel(gui,'Akademi Lideri:', 22, 50)
tbxAMaster = QtBind.createLineEdit(gui,"", 96, 48, 95, 19)
lblSoru = QtBind.createLabel(gui,'Sorunuz:', 25, 80)
tbxSoru = QtBind.createLineEdit(gui,"", 96, 78, 95, 19)
lblCevap = QtBind.createLabel(gui,'Cevabınız:', 25, 110)
tbxCevap = QtBind.createLineEdit(gui,"", 96, 108, 95, 19)
lblCizgi2 = QtBind.createList(gui, 211, 10, 200, 250)
lblBuff = QtBind.createLabel(gui,'↓  Otomatik Akademi Bufflama   ↓', 231, 20)
btnBuff = QtBind.createButton(gui,'buffNow', '   Şimdi Buffla  ', 266, 50)
lblSüre = QtBind.createLabel(gui,'      Dakika Sonra Başlat', 256, 90)
txtMinutes = QtBind.createLineEdit(gui,"63", 244, 89, 25, 20)
btnSüreB = QtBind.createButton(gui,'buffTimer', ' Süreyi Başlat  ', 266, 125)
btnSüreS = QtBind.createButton(gui,'stopTimer', ' Süreyi Durdur ', 266, 165)
lblTimeLeft = QtBind.createLabel(gui,'Kalan Süre: 00:00', 266, 200)
def getPath():
	return get_config_dir()+pName+"\\"
def getConfig(name):
	if not name:
		name = pName;
	return getPath()+name+".json"
def loadDefaultConfig():
	# DATAYI TEMİZLE
	QtBind.setText(gui,tbxProfil,"")
	QtBind.setText(gui,tbxPTMaster,"")
	QtBind.setText(gui,tbxAMaster,"")
	QtBind.setText(gui,tbxSoru,"")
	QtBind.setText(gui,tbxCevap,"")
def loadConfigs(fileName=""):
	loadDefaultConfig()
	if os.path.exists(getConfig(fileName)):
		data = {}
		with open(getConfig(fileName),"r") as f:
			data = json.load(f)
		QtBind.setText(gui,tbxProfil,fileName)
		if "PTMASTER" in data:
			QtBind.setText(gui,tbxPTMaster,data["PTMASTER"])
		if "AMASTER" in data:
			QtBind.setText(gui,tbxAMaster,data["AMASTER"])
		if "SORU" in data:
			QtBind.setText(gui,tbxSoru,data["SORU"])
		if "CEVAP" in data:
			QtBind.setText(gui,tbxCevap,data["CEVAP"])
		return True
	return False
def saveConfigs(fileName=""):
	data = {}
	data["PTMASTER"] = QtBind.text(gui,tbxPTMaster)
	data["AMASTER"] = QtBind.text(gui,tbxAMaster)
	data["SORU"] = QtBind.text(gui,tbxSoru)
	data["CEVAP"] = QtBind.text(gui,tbxCevap)
	with open(getConfig(fileName),"w") as f:
		f.write(json.dumps(data,indent=4,sort_keys=True))
def btnSaveConfig_clicked():
	strConfigName = QtBind.text(gui,tbxProfil)
	saveConfigs(strConfigName)
	if strConfigName:
		log('Eklenti: ['+strConfigName+'] Yapılandırma Adıyla Kaydedildi.')
	else:
		log("Eklenti: Kayıt Oluşturuldu.")
def btnLoadConfig_clicked():
	strConfigName = QtBind.text(gui,tbxProfil)
	if loadConfigs(strConfigName):
		if strConfigName:
			log("Eklenti: ["+strConfigName+"] Yapılandırması Yüklendi.")
		else:
			log("Eklenti: Yükleme Başarılı.")
	elif strConfigName:
		log("Eklenti: ["+strConfigName+"] Yapılandırma Bulunamadı.")
questionPartyTime = None
questionPartyCharName = ""
questionPartyRID = 0
questionPartyJID = 0
questionAcademyTime = None
questionAcademyCharName = ""
questionAcademyRID = 0
questionAcademyJID = 0
iCounter = 0
iCounter2 = 0
tmr = threading.Timer
tmr2 = threading.Timer
# ______________________________ METHODLAR ______________________________ #
# PAKET ENJEKSIYON
def Inject_PartyMatchJoinResponse(requestID,joinID,response):
	p  	= struct.pack('I', requestID)
	p += struct.pack('I', joinID)
	p += struct.pack('B',1 if response else 0)
	inject_joymax(0x308D,p,False)
# PAKET ENJEKSIYON
def Inject_AcademyMatchJoinResponse(requestID,joinID,response):
	p = struct.pack('I', requestID)
	p += struct.pack('I', joinID)
	p += struct.pack('B',1 if response else 0)
	inject_joymax(0x347F,p,False)
# ______________________________ ETKINLIKLER ______________________________ #
def handle_joymax(opcode,data):
	# PT KATILIM GONDERDIGINDE
	if opcode == 0x706D and QtBind.text(gui,tbxCevap):
		try:
			# ISTEKLER YERINE GETIRILDIGINDE DATAYI KAYDET
			global questionPartyTime,questionPartyRID,questionPartyJID,questionPartyCharName
			questionPartyTime = time.time()
			index=0
			questionPartyRID = struct.unpack_from('<I',data,index)[0]
			index+=4
			questionPartyJID = struct.unpack_from('<I',data,index)[0]
			index+=22
			charLength = struct.unpack_from('<H',data,index)[0]
			index+=2
			questionPartyCharName = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')
			# SIFREYI SORMAK ICIN SORU GONDERMEK
			phBotChat.Private(questionPartyCharName,QtBind.text(gui,tbxSoru))
		except:
			log("Eklenti: Ayrıştırma Hatası,Bu Serverde Kullanılamaz..")
			log("Destek Için Iletişime Geçiniz..")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(get_locale())+"]")
	# AKADEMI KATILIM GONDERDIGINDE
	elif opcode == 0x747E and QtBind.text(gui,tbxCevap):
		try:
			# ISTEKLER YERINE GETIRILDIGINDE DATAYI KAYDET
			global questionAcademyTime,questionAcademyRID,questionAcademyJID,questionAcademyCharName	
			questionAcademyTime = time.time()
			index=0
			questionAcademyRID = struct.unpack_from('<I',data,index)[0]
			index+=4
			questionAcademyJID = struct.unpack_from('<I',data,index)[0]
			index+=18
			charLength = struct.unpack_from('<H',data,index)[0]
			index+=2
			questionAcademyCharName = struct.unpack_from('<' + str(charLength) + 's',data,index)[0].decode('cp1252')
			# SIFREYI SORMAK ICIN SORU GONDERMEK
			phBotChat.Private(questionAcademyCharName,QtBind.text(gui,tbxSoru))
		except:
			log("Eklenti: Ayrıştırma Hatası,Bu Serverde Kullanılamaz..")
			log("Destek Için Iletişime Geçiniz..")
			log("Data [" + ("None" if not data else ' '.join('{:02X}'.format(x) for x in data))+"] Locale ["+str(get_locale())+"]")
	return True
# SORU CEVAPLAMA KOSULLARI
def handle_chat(t,charName,message):
	# OZEL MESAJ KONTROLU
	if t != 2:
		return
	# SIFRE KURULDUYSA DEVAM ET
	if not QtBind.text(gui,tbxCevap):
		return
	# SORULARI KONTROL ET
	if message == QtBind.text(gui,tbxSoru):
		# MASTER OLMAYANLARA CEVAP HAZIRLAMA
		if QtBind.text(gui,tbxPTMaster) == charName or QtBind.text(gui,tbxAMaster) == charName:
			phBotChat.Private(charName,QtBind.text(gui,tbxCevap))
		else:
			phBotChat.Private(charName,"Sendeki Bu Kafayla SRO oynanmaz.")
		return
	# CEVAPLARI KONTROL ET
	if charName == questionPartyCharName:
		# PT KATILIM BEKLEME SURESI
		now = time.time()
		if now - questionPartyTime < 10:
			# CEVAP KONTROLÜ
			if message == QtBind.text(gui,tbxCevap):
				log("Eklenti: "+charName+" Doğru Şifre ile Partiye Giriş Yaptı.")
				Inject_PartyMatchJoinResponse(questionPartyRID,questionPartyJID,True)
			else:
				log("Eklenti: "+charName+" Yanlış Şifre ile Reddedildi.")
				Inject_PartyMatchJoinResponse(questionPartyRID,questionPartyJID,False)
			return
	if charName == questionAcademyCharName:
		# AKADEMI KATILIM BEKLEME SURESI 
		now = time.time()
		if now - questionAcademyTime < 10:
			# CEVAP KONTROLÜ
			if message == QtBind.text(gui,tbxCevap):
				log("Eklenti: "+charName+" Doğru Şifre ile Akademiye Giriş Yaptı.")
				Inject_AcademyMatchJoinResponse(questionAcademyRID,questionAcademyJID,True)
			else:
				log("Eklenti: "+charName+" Yanlış Şifre ile Reddedildi.")
				Inject_AcademyMatchJoinResponse(questionAcademyRID,questionAcademyJID,False)
			return
def buffNow():
	log('Akademi Buff Şimdi Kullanıldı.')
	inject_joymax(0x7483,b'', False)
def buffTimer():
    log('Zamanlama Başlatıldı!')
    global iCounter,tmr,iCounter2, isTimerStopped
    isTimerStopped = False
    iCounter=int(QtBind.text(gui, txtMinutes)) * 60
    iCounter2=iCounter/60
    tmr = threading.Timer(iCounter, buffForTimer) 
    tmr.start()
    showLeft()
def stopTimer():
    log('Zamanlama Durduruldu!')
    global tmr,tmr2, isTimerStopped
    isTimerStopped = True
    tmr.cancel()
    tmr2.cancel()
def buffForTimer():
    buffNow()
    global iCounter,tmr,iCounter2
    iCounter2=iCounter/60
    if not isTimerStopped:
        tmr = threading.Timer(iCounter, buffForTimer) 
        tmr.start()
def showLeft():
    global tmr2,iCounter2, isTimerStopped
    if not isTimerStopped:
        minutes = int(iCounter2)
        seconds = int((iCounter2 - minutes) * 60)
        QtBind.setText(gui, lblTimeLeft, f"Kalan Süre: {minutes:02}:{seconds:02}")
        iCounter2-=1/60.0
        tmr2=threading.Timer(1, showLeft) 
        tmr2.start()
log('Eklenti:'+pName+' v'+pVersion+' Yuklendi. // edit by hakankahya')
if os.path.exists(getPath()):
	useDefaultConfig = True 
	bot_args = get_command_line_args()
	if bot_args:
		for i in range(len(bot_args)):
			param = bot_args[i].lower()
			if param.startswith('-TR_AcademyHelper-config='):
				configName = param[17:]
				if loadConfigs(configName):
					log("Eklenti: "+pName+" Profil ["+configName+"] Komut ile Yüklendi.")
					useDefaultConfig = False
				else:
					log("Eklenti: "+pName+" Profil ["+configName+"] Komutu Bulunamadı.")
				break
	if useDefaultConfig:
		loadConfigs()
else:
	loadDefaultConfig()
	os.makedirs(getPath())
	log('Eklenti:'+pName+' Klasoru Olusturuldu, Yapılandırmaların Burada Saklanacak.')
