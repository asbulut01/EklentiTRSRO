from phBot import *
import QtBind
import json
import os

name = 'TR_ConditionCopier'
version = 2.0
NewestVersion = 0
path = get_config_dir()

gui = QtBind.init(__name__, name)

lblCharName = QtBind.createLabel(gui,'Karakter Adı',85,20)
lblCharFrom = QtBind.createLabel(gui,'Nereden',20,50)
txtCharFrom = QtBind.createLineEdit(gui,"",75,48,120,20)
lblCharTo = QtBind.createLabel(gui,'Nereye',20,80)
txtCharTo = QtBind.createLineEdit(gui,"",75,78,120,20)

lblServerName = QtBind.createLabel(gui,'Sunucu Adı',240,20)
txtServerFrom = QtBind.createLineEdit(gui,"",220,48,120,20)
txtServerTo = QtBind.createLineEdit(gui,"",220,78,120,20)


lblProfileName = QtBind.createLabel(gui,'Profil Adı',390,20)
txtProfileFrom = QtBind.createLineEdit(gui,"",370,48,120,20)
txtProfileTo = QtBind.createLineEdit(gui,"",370,78,120,20)

btnCopy = QtBind.createButton(gui, 'button_copy', ' Koşulları Kopyala ', 70, 120)

lblNot = QtBind.createLabel(gui,'<font color="red">Not:</font> Kopyalama Sırasında "Invalid control character at:" Benzeri Hata Alınması Durumunda<br>Hatada Belirlenen Satırı Config Dosyasındaki Karakterin .json Dosyasını Kontrol Ediniz.<br>Satır Aralığında Bulunan "NUL" Ifadelerini Siliniz. Kayıt Ediniz ve Tekrar Deneyin.', 20, 160)


def button_copy():
    try:
        FromChar = QtBind.text(gui,txtCharFrom)
        FromServer = QtBind.text(gui,txtServerFrom)
        FromProfile = QtBind.text(gui,txtProfileFrom)
        if not FromChar:
            log('Eklenti: Lütfen Kopyalanacak Karakterin Adı Giriniz. Bkn : Nereden')
            return
        if not FromServer:
            log('Eklenti: Lütfen Kopyalanacak Sunucunun Adı Giriniz. Bkn : Nereden')
            return
        FromFile = "%s_%s.json" %(FromServer,FromChar)
        if len(FromProfile) > 0:
            FromFile = "%s_%s.%s.json" %(FromServer,FromChar,FromProfile)

        if not os.path.exists(path + FromFile):
            log('Eklenti: [%s] Yapılandırması Bulunamadı. "Nereden" Kısmını Kontrol Edin.' % FromFile)
            return

        with open(path + FromFile, "r", encoding='utf-8') as f:
            Fromdata = json.load(f)
            FromConditions = Fromdata['Conditions']

        ToChar = QtBind.text(gui,txtCharTo)
        ToServer = QtBind.text(gui,txtServerTo)
        ToProfile = QtBind.text(gui,txtProfileTo)
        if not ToChar:
            log('Eklenti: Lütfen Uygulanacak Karakterin Adı Giriniz. Bkn : Nereye')
            return
        if not ToServer:
            log('Eklenti: Lütfen Uygulanacak Sunucunun Adı Giriniz. Bkn : Nereye')
            return
        ToFile = "%s_%s.json" %(ToServer,ToChar)
        if len(ToProfile) > 0:
            ToFile = "%s_%s.%s.json" %(ToServer,ToChar,ToProfile)

        if not os.path.exists(path + ToFile):
            log('Eklenti: [%s] Yapılandırması Bulunamadı. "Nereye" Kısmını Kontrol Edin.' % ToFile)
            return

        with open(path + ToFile, "r", encoding='utf-8') as f:
            Todata = json.load(f)
            Todata['Conditions'] = FromConditions

        with open(path + ToFile, "w", encoding='utf-8') as f:
            f.write(json.dumps(Todata, indent=4))

        log('Eklenti: Koşullar [%s] den [%s] ye Başarıyla Kopyalandı.' %(FromFile, ToFile))

    except Exception as e:
        log('Eklenti: Koşullar Kopyalanırken Bir Hata Oluştu: %s' % str(e))

def CheckForUpdate():
	global NewestVersion
	if NewestVersion == 0:
		try:
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_ConditionCopier.py', headers={'User-Agent': 'Mozilla/5.0'})
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
	if os.path.exists(path + "Plugins/" + "TR_ConditionCopier.py"):
		try:
			os.rename(path + "Plugins/" + "TR_ConditionCopier.py", path + "Plugins/" + "TR_ConditionCopierBACKUP.py")
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_ConditionCopier.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8"))
				with open(path + "Plugins/" + "TR_ConditionCopier.py", "w+") as f:
					f.write(lines)
					os.remove(path + "Plugins/" + "TR_ConditionCopierBACKUP.py")
					log('Eklenti Başarıyla Güncellendi, Kullanmak için Eklentiyi Yeniden Yükleyin.')
		except Exception as ex:
			log('Güncelleme Hatası [%s] Lütfen Manuel Olarak Güncelleyin veya daha Sonra Tekrar Deneyin.' %ex)

CheckForUpdate()

log('Eklenti:%s v%s Yuklendi. // edit by hakankahya' % (name,version))
