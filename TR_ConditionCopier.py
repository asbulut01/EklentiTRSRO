from phBot import *
import QtBind
import json
import os

name = 'TR_ConditionCopier'
version = 2.1
path = get_config_dir()

gui = QtBind.init(__name__, name)

lblCharName = QtBind.createLabel(gui,'Karakter Adı',85,20)
lblCharFrom = QtBind.createLabel(gui,'Kopyala Kaynak',20,50)
txtCharFrom = QtBind.createLineEdit(gui,"",75,48,120,20)
lblCharTo = QtBind.createLabel(gui,'Kopyala Hedef',20,80)
txtCharTo = QtBind.createLineEdit(gui,"",75,78,120,20)

lblServerName = QtBind.createLabel(gui,'Sunucu Adı',240,20)
txtServerFrom = QtBind.createLineEdit(gui,"",220,48,120,20)
txtServerTo = QtBind.createLineEdit(gui,"",220,78,120,20)

lblProfileName = QtBind.createLabel(gui,'Profil Adı',390,20)
txtProfileFrom = QtBind.createLineEdit(gui,"",370,48,120,20)
txtProfileTo = QtBind.createLineEdit(gui,"",370,78,120,20)

btnCopy = QtBind.createButton(gui, 'button_copy', ' Koşulları Kopyala ', 70, 120)

def button_copy():
	FromChar = QtBind.text(gui,txtCharFrom)
	FromServer = QtBind.text(gui,txtServerFrom)
	FromProfile = QtBind.text(gui,txtProfileFrom)
	if FromChar == '':
		log('Eklenti: Lütfen KAYNAK karakter adını giriniz')
		return
	if FromServer == '':
		log('Eklenti: Lütfen KAYNAK sunucu adını giriniz')
		return
	FromFile = "%s_%s.json" %(FromServer,FromChar)
	if len(FromProfile) > 0:
		FromFile = "%s_%s.%s.json" %(FromServer,FromChar,FromProfile)
	if os.path.exists(path + FromFile):
		with open(path + FromFile,"r", encoding = "utf-8") as f:
			Fromdata = json.load(f)
			FromConditions = Fromdata['Conditions']
	else:
		log('Eklenti: KAYNAK yapılandırma dosyası mevcut değil')
		return

	ToChar = QtBind.text(gui,txtCharTo)
	ToServer = QtBind.text(gui,txtServerTo)
	ToProfile = QtBind.text(gui,txtProfileTo)
	if ToChar == '':
		log('Eklenti: Lütfen HEDEF karakter adını giriniz')
		return
	if ToServer == '':
		log('Eklenti: Lütfen HEDEF sunucu adını giriniz')
		return
	ToFile = "%s_%s.json" %(ToServer,ToChar)
	if len(ToProfile) > 0:
		ToFile = "%s_%s.%s.json" %(ToServer,ToChar,ToProfile)
	if os.path.exists(path + ToFile):
		with open(path + ToFile,"r", encoding = "utf-8") as f:
			Todata = json.load(f)
			Todata['Conditions'] = FromConditions
	else:
		log('Eklenti: HEDEF yapılandırma dosyası mevcut değil')
		return
	log(str(FromConditions))
	with open(path + ToFile ,"w", encoding = "utf-8") as f:
		f.write(json.dumps(Todata, indent=4,))
		log('Eklenti: Koşullar başarıyla [%s] konumundan [%s] konumuna kopyalandı' %(FromFile,ToFile))

log('Eklenti: [%s] Sürüm %s Yüklendi. // edit by hakankahya' % (name,version))
