from phBot import *
from threading import Timer
import QtBind
import struct
import json
import urllib.request
import os
import time

name = 'TR_AutoCursed'
version = 2.0
NewestVersion = 0
path = get_config_dir() + name + "\\"

gui = QtBind.init(__name__, name)

lblCurrentSkills = QtBind.createLabel(gui,'Mevcut Beceriler',70,10)
lstCurrentSkills = QtBind.createList(gui,10,30,200,200)
buttonGetSkills = QtBind.createButton(gui, 'button_get_skills', ' Mevcut Becerileri Yenile ', 60, 240)

lblRemoveSkills = QtBind.createLabel(gui,'Kaldırılacak Beceriler',350,10)
lstRemoveSkills = QtBind.createList(gui,300,30,200,200)
lblSave = QtBind.createLabel(gui,'Otomatik Olarak Kaydedilir',350,240)

lblMasteries = QtBind.createLabel(gui,'Uzmanlıklar',580,10)
ComboMasteries = QtBind.createCombobox(gui,530,32,160,22)
button2 = QtBind.createButton(gui, 'button_get_masteries', '       Uzmanlıkları Yenile      ', 540, 70)
button3 = QtBind.createButton(gui, 'button_add_mastery', '           Uzmanlıgı Sil            ', 540, 105)
button4 = QtBind.createButton(gui, 'button_add_all_skills', '  Uzmanlıktaki Becerileri Sil ', 540, 140)

button = QtBind.createButton(gui, 'button_add', ' Ekle ', 215, 100)
button1 = QtBind.createButton(gui, 'button_remove', ' Sil ', 215, 125)
cbxEnable = QtBind.createCheckBox(gui, 'cbxEnable_clicked',' Etkin ', 225, 70)


def cbxEnable_clicked(checked):
	SaveConfig()

def button_add_all_skills():
	SelectedMastery = QtBind.text(gui, ComboMasteries)
	if not SelectedMastery:
		log('Eklenti: Lütfen Bir Uzmanlık Secin !')
		return
	MasteryID = GetMasteryID(SelectedMastery)
	skills = get_skills()
	for ID, skill in skills.items():
		if skill['mastery'] == MasteryID:
			if not lstRemoveSkill_exist(skill['name']):
				QtBind.append(gui,lstRemoveSkills,skill['name'])
	SaveConfig()	

def button_add_mastery():
	SelectedMastery = QtBind.text(gui, ComboMasteries)
	if not SelectedMastery:
		log('Eklenti: Lütfen Bir Uzmanlık Secin !')
		return
	if not lstRemoveSkill_exist(SelectedMastery + ' Mastery'):
		QtBind.append(gui,lstRemoveSkills,SelectedMastery + ' Mastery')
		SaveConfig()

def button_get_masteries():
	QtBind.clear(gui,ComboMasteries)
	Masteries = get_mastery()
	for ID, mastery in Masteries.items():
		if mastery['level'] > 0:
			QtBind.append(gui,ComboMasteries,mastery['name'])

def button_get_skills():
	skills = get_skills()
	for ID, skill in skills.items():
		QtBind.append(gui,lstCurrentSkills,skill['name'])


def button_add():
	selectedSkill = QtBind.text(gui,lstCurrentSkills)
	if not lstRemoveSkill_exist(selectedSkill):
		QtBind.append(gui,lstRemoveSkills,selectedSkill)
		SaveConfig()

def button_remove():
	selectedSkill = QtBind.text(gui,lstRemoveSkills)
	QtBind.remove(gui,lstRemoveSkills,selectedSkill)
	SaveConfig()


def lstRemoveSkill_exist(skill):
	RemoveSkills = QtBind.getItems(gui,lstRemoveSkills)
	for RemSkill in RemoveSkills:
		if RemSkill.lower() == skill.lower():
			return True
	return False

def TurnInHearts():
	npcs = get_npcs()
	for key, npc in npcs.items():
		if 'POTION' in npc['servername']:
			log("Eklenti: Dönüstürülüyor = Cursed Hearts")
			p = struct.pack('<I', key)
			inject_joymax(0x7045,p, False)
			p += b'\x0A'
			inject_joymax(0x7046,p, False)
			Timer(1.0, inject_joymax, [0x30D4, b'\x05', False]).start()
			Timer(1.2, inject_joymax, [0x30D4, b'\x05', False]).start()
			Timer(1.4, inject_joymax, [0x7515, b'\x1D\x00\x00\x00\x00', False]).start()
			Timer(4.0, AcceptQuest, ()).start()
			return
	log('Eklenti: Bir Iksirci NPCsine Yakın Degilsin.')

def AcceptQuest():
	npcs = get_npcs()
	for key, npc in npcs.items():
		if 'POTION' in npc['servername']:
			log("Eklenti: Görev Kabul Edildi.")
			p = struct.pack('<I', key)
			inject_joymax(0x7045,p, False)
			p += b'\x0A'
			inject_joymax(0x7046,p, False)
			Timer(1.0, inject_joymax, [0x30D4, b'\x05', False]).start()
			Timer(1.2, inject_joymax, [0x30D4, b'\x05', False]).start()
			Timer(4.0, EnterSkillRemoval, ()).start()
			return
	log('Eklenti: Bir Iksirci NPCsine Yakın Degilsin.')

def EnterSkillRemoval():
	npcs = get_npcs()
	for key, npc in npcs.items():
		if 'POTION' in npc['servername']:
			log("Eklenti: Beceri Kaldırma Penceresine Girme")
			p = struct.pack('<I', key)
			inject_joymax(0x7045,p, False)
			p += b'\x0A'
			Timer(1.0, inject_joymax, [0x30D4, b'\x06', False]).start()
			Timer(3.0, EditSkill, ()).start()
			return
	log('Eklenti: Bir Iksirci NPCsine Yakın Degilsin.')
			
def ExitNPC():
	npcs = get_npcs()
	for key, npc in npcs.items():
		if 'POTION' in npc['servername']:
			inject_joymax(0x704B, struct.pack('<I', key), False)
			log("Eklenti: NPCden Cıkılıyor.")
			return

def EditSkill():
	RemoveSkills = QtBind.getItems(gui,lstRemoveSkills)
	if len(RemoveSkills) == 0:
		log('Eklenti: Kaldırılacak Başka Beceri Yok...')
		ExitNPC()
		return
	PotionQty = int(GetPotionCount())
	if PotionQty == 0:
		log('Eklenti: Hic Resuscitation Potion bulunmuyor...')
		ExitNPC()
		return
	if CheckIfOnlyMasteriesLeft():
		for Mastery in RemoveSkills:
			PotionQty = int(GetPotionCount())
			Mastery = Mastery.strip(' Mastery')
			MasteryLevel = GetMasteryLevel(Mastery)
			MasteryID = GetMasteryID(Mastery)
			Deduction = MasteryLevel - PotionQty
			p = b'\x59\x0E\x00\x00'
			p += struct.pack('<I', MasteryID)
			if PotionQty >= MasteryLevel:
				p += b'\x00'
				log('Eklenti: Uzmanlık [%s] Silindi' %Mastery)
				QtBind.remove(gui,lstRemoveSkills,Mastery+' Mastery')
				SaveConfig()
			if PotionQty < MasteryLevel:
				p += struct.pack('b', Deduction)
				log('Eklenti: Düsürülen Uzmanlık [%s] [%s] den [%s] a Cekildi.' %(Mastery,MasteryLevel,Deduction))
			inject_joymax(0x7203,p, False)
			time.sleep(1)
		ExitNPC()
		return
	skill = GetHighestSkill()
	SkillID = GetSkillID(skill)
	SkillLevel = int(GetSkillLevel(skill))
	p = b'\x59\x0E\x00\x00'
	p += struct.pack('<I', SkillID)
	if PotionQty >= SkillLevel:
		p += b'\x00'
		log('Eklenti: Beceri Silindi [%s]' %skill)
		QtBind.remove(gui,lstRemoveSkills,skill)
		SaveConfig()
	if PotionQty < SkillLevel:
		Deduction = SkillLevel - PotionQty
		p += struct.pack('b', Deduction)
		log('Eklenti: Düsürülen Beceri [%s] [%s] den [%s] a Cekildi.' %(skill,SkillLevel,Deduction))
	inject_joymax(0x7202,p, False)
	Timer(1.0, EditSkill, ()).start()

def GetMasteryLevel(Mastery):
	Masteries = get_mastery()
	for ID, mastery in Masteries.items():
		if mastery['name'] == Mastery:
			return mastery['level']

def CheckIfOnlyMasteriesLeft():
	RemoveSkills = QtBind.getItems(gui,lstRemoveSkills)
	if not RemoveSkills:
		return False
	for skill in RemoveSkills:
		if 'Mastery' not in skill:
			return False
	return True 

def GetMasteryID(SelectedMastery):
	Masteries = get_mastery()
	for ID, mastery in Masteries.items():
		if mastery['name'] == SelectedMastery:
			return ID

def GetHighestSkill():
	HighestID = 0
	RemoveSkills = QtBind.getItems(gui,lstRemoveSkills)
	for skill in RemoveSkills:
		if 'Mastery' not in skill:
			SkillID = GetSkillID(skill)
			if SkillID > HighestID:
				HighestID = SkillID
				HighestSkill = skill
	return HighestSkill

def AutoCursed(args):
	if QtBind.isChecked(gui,cbxEnable):
		PotionQty = int(GetPotionCount())
		delay = PotionQty * 400 + 35000
		TurnInHearts()
		return delay
	return 0

def GetSkillLevel(name):
	skills = get_skills()
	for ID, skill in skills.items():
		if skill['name'] == name:
			level = skill['servername'][-2:]
			return level

def GetSkillID(name):
	skills = get_skills()
	for ID, skill in skills.items():
		if skill['name'] == name:
			return ID

def GetPotionCount():
	Total = 0
	items = get_inventory()['items']
	for slot, item in enumerate(items):
		if item:
			name = item['name']
			quantity = item['quantity']
			if name == r"Resuscitation potion":
				Total += quantity
	return Total

def joined_game():
	Timer(4.0, LoadConfigs, ()).start()

def GetConfig():
	return path + get_character_data()['server'] + "_" + get_character_data()['name'] + ".json"

def SaveConfig():
	data = {}
	data['Enable'] = QtBind.isChecked(gui,cbxEnable)
	data["RemoveSkills"] = QtBind.getItems(gui,lstRemoveSkills)
	with open(GetConfig(),"w") as f:
		f.write(json.dumps(data, indent=4))

def LoadConfigs():
	if os.path.exists(GetConfig()):
		data = {}
		with open(GetConfig(),"r") as f:
			data = json.load(f)
		if "Enable" in data:
			QtBind.setChecked(gui,cbxEnable,data["Enable"])
		if "RemoveSkills" in data:
			QtBind.clear(gui,lstRemoveSkills)
			for skill in data['RemoveSkills']:
				QtBind.append(gui,lstRemoveSkills,skill)

def CheckForUpdate():
	global NewestVersion
	if NewestVersion == 0:
		try:
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_AutoCursed.py', headers={'User-Agent': 'Mozilla/5.0'})
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
	if os.path.exists(path + "Plugins/" + "TR_AutoCursed.py"):
		try:
			os.rename(path + "Plugins/" + "TR_AutoCursed.py", path + "Plugins/" + "TR_AutoCursedBACKUP.py")
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_AutoCursed.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8"))
				with open(path + "Plugins/" + "TR_AutoCursed.py", "w+") as f:
					f.write(lines)
					os.remove(path + "Plugins/" + "TR_AutoCursedBACKUP.py")
					log('Eklenti Başarıyla Güncellendi, Kullanmak için Eklentiyi Yeniden Yükleyin.')
		except Exception as ex:
			log('Güncelleme Hatası [%s] Lütfen Manuel Olarak Güncelleyin veya daha Sonra Tekrar Deneyin.' %ex)

CheckForUpdate()

Timer(1.0, LoadConfigs, ()).start()
log('Eklenti:%s v%s Yuklendi. // edit by hakankahya' % (name,version))

if not os.path.exists(path):
	os.makedirs(path)
	log('Eklenti:%s Klasörü Olusturuldu.' % name)
