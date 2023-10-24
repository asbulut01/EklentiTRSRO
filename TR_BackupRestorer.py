from phBot import *
from datetime import datetime
from threading import Timer
import shutil
import QtBind
import json
import urllib.request
import os

name = 'TR_BackupRestorer'
version = 2.0
NewestVersion = 0
path = get_config_dir() + 'Backup'

gui = QtBind.init(__name__, name)

Configs = {"Profiles": []}
Loaded = False

lstProfiles = QtBind.createList(gui,10,50,150,200)
lblProfiles = QtBind.createLabel(gui,'Karakter Profilleri (json)',30,23)

ProfileDates = QtBind.createList(gui,180,50,200,200)
lblProfileDates = QtBind.createLabel(gui,'Mevcut Yedekleme Tarihleri',220,23)
btnRestore = QtBind.createButton(gui, 'button_restore', ' Seçileni Geri Yükle ', 230, 260)

lblChar = QtBind.createLabel(gui,'Karakter Adı ',400,50)
txtChar = QtBind.createLineEdit(gui,"",470,48,120,20)
lblServer = QtBind.createLabel(gui,'Sunucu Adı ',400,80)
txtServer = QtBind.createLineEdit(gui,"",470,78,120,20)
btnLoadProfiles = QtBind.createButton(gui, 'button_load', ' Profilleri Yükle ', 470, 120)

def button_load():
	global Loaded, Configs
	Configs = {"Profiles": []}
	QtBind.clear(gui,lstProfiles)
	Server = QtBind.text(gui, txtServer)
	Char = QtBind.text(gui, txtChar)
	if not Server or not Char:
		log('Eklenti: Aramak İçin Sunucu ve Karakter Adı Giriniz.')
		return
	AllConfigs = os.listdir(path)
	for Config in AllConfigs:
		if Config.endswith('.json'):
			Config = Config[:-5]
			server = Config[:len(Server)]
			if Server == server:
				char = Config[len(Server)+1:len(Server + Char)+1]
				if Char == char:
					if '.' in Config:
						profile = Config[len(Server + Char)+2:].split('_')[0]
						if len(profile) > 0:
							date = Config[len(Server + Char)+2:].split('_')[1]
							if CheckIfProfileExist(profile):
								AddDate(profile,date)
							else:
								data = {'Profile': profile, 'Backups': [date]}
								Configs['Profiles'].append(data)
					else:
						profile = 'Default'	
						date = Config[len(Server + Char)+2:].split('_')[0]
						if CheckIfProfileExist(profile):
							AddDate(profile,date)
						else:
							data = {'Profile': profile, 'Backups': [date]}
							Configs['Profiles'].append(data)
	
	Loaded = True
	AppendProfiles()					

def button_restore():
	SelectedProfile = QtBind.text(gui,lstProfiles)
	SelectedDate = QtBind.text(gui,ProfileDates).split(' ')[0]
	Server = QtBind.text(gui, txtServer)
	Char = QtBind.text(gui, txtChar)
	if not SelectedProfile or not SelectedDate:
		log('Eklenti: Profil Ve Yedekleme Tarihi Seçin..')
		return

	BackupFileName = BuildFileName('Backup',Server,Char,SelectedProfile,SelectedDate)
	ExistingFileName = BuildFileName('Existing',Server,Char,SelectedProfile,SelectedDate)
	ExistingPath = path[:-7] + '/' + ExistingFileName
	BackupPath = path + '/' + BackupFileName
	RestoreBackup(BackupPath,ExistingPath,SelectedDate)
	

def BuildFileName(type,server,charname,profile,date=''):
	FileName = server + '_' + charname
	if profile == 'Default':
		if type == 'Existing':
			FileName = FileName + '.json'
		elif type == 'Backup':
			FileName = FileName + '_' + date + '.json'
	
	else:
		if type == 'Existing':
			FileName = FileName + '.' + profile + '.json'
		elif type == 'Backup':
			FileName = FileName + '.' + profile + '_' + date + '.json'
	return FileName

def AddDate(profile,date):
	Profiles = Configs['Profiles']
	for slot, item in enumerate(Profiles):
		if item:
			Profile = item['Profile']
			if Profile == profile:
				item['Backups'].append(date)



def CheckIfProfileExist(profile):
	Profiles = Configs['Profiles']
	for slot, item in enumerate(Profiles):
		if item:
			Profile = item['Profile']
			if Profile == profile:
				return True
	return False


def AppendProfiles():
	Profiles = Configs['Profiles']
	for slot, item in enumerate(Profiles):
		if item:
			Profile = item['Profile']
			QtBind.append(gui,lstProfiles,Profile)

def LoadBackups(profile):
	QtBind.clear(gui,ProfileDates)
	Profiles = Configs['Profiles']
	for slot, item in enumerate(Profiles):
		if item:
			Profile = item['Profile']
			if Profile == profile:
				dates = item['Backups']
				for date in dates:
					Age = CalculateAge(date)
					date = date + ' (%s Gün Önce)' %Age
					QtBind.append(gui,ProfileDates,date)

def CalculateAge(date):
	backup = str(date)
	CurrentTime = datetime.now()
	BackupDate = datetime.strptime(backup, '%Y-%m-%d')
	Age = CurrentTime - BackupDate
	return Age.days

def RestoreBackup(BackupPath,ExistingPath,date):
	try:
		shutil.copyfile(BackupPath,ExistingPath)
		log('Eklenti: [%s] Yedeklemesi Başarıyla Geri Yüklendi.' %date)
	except Exception as ex:
		log('Eklenti: Geri Yükleme Hatası [%s]')

PreviouslySelected = ''
def event_loop():
	global PreviouslySelected
	if Loaded:
		SelectedProfile = QtBind.text(gui,lstProfiles)
		if PreviouslySelected != SelectedProfile:
			PreviouslySelected = SelectedProfile
			LoadBackups(SelectedProfile)

def CheckForUpdate():
	global NewestVersion
	if NewestVersion == 0:
		try:
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_BackupRestorer.py', headers={'User-Agent': 'Mozilla/5.0'})
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
	if os.path.exists(path + "Plugins/" + "TR_BackupRestorer.py"):
		try:
			os.rename(path + "Plugins/" + "TR_BackupRestorer.py", path + "Plugins/" + "TR_BackupRestorerBACKUP.py")
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_BackupRestorer.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8"))
				with open(path + "Plugins/" + "TR_BackupRestorer.py", "w+") as f:
					f.write(lines)
					os.remove(path + "Plugins/" + "TR_BackupRestorerBACKUP.py")
					log('Eklenti Başarıyla Güncellendi, Kullanmak için Eklentiyi Yeniden Yükleyin.')
		except Exception as ex:
			log('Güncelleme Hatası [%s] Lütfen Manuel Olarak Güncelleyin veya daha Sonra Tekrar Deneyin.' %ex)

CheckForUpdate()

log('Eklenti:%s v%s Yuklendi. // edit by hakankahya' % (name,version))
