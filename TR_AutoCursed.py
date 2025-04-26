from phBot import *
from threading import Timer
import QtBind
import struct
import json
import urllib.request
import os
import time

name = 'TR_AutoCursed'

path = get_config_dir() + name + "\\"

gui = QtBind.init(__name__, name)

lblCurrentSkills = QtBind.createLabel(gui,'Mevcut Yetenekler',70,10)
lstCurrentSkills = QtBind.createList(gui,10,30,200,200)
buttonGetSkills = QtBind.createButton(gui, 'button_get_skills', 'Mevcut Yetenekleri Getir', 60, 240)

lblRemoveSkills = QtBind.createLabel(gui,'Kaldırılacak Yetenekler',350,10)
lstRemoveSkills = QtBind.createList(gui,300,30,200,200)
lblSave = QtBind.createLabel(gui,'Otomatik Kayıt Edilir',350,240)

lblMasteries = QtBind.createLabel(gui,'Ustalıklar',580,10)
ComboMasteries = QtBind.createCombobox(gui,530,32,160,22)
button2 = QtBind.createButton(gui, 'button_get_masteries', '  Ustalıkları Getir ', 570, 70)
button3 = QtBind.createButton(gui, 'button_add_mastery', '  Kaldırılacak Ustalık Ekle ', 550, 105)
button4 = QtBind.createButton(gui, 'button_add_all_skills', '  Seçilen Ustalığın Tüm Yeteneklerini Ekle ', 505, 140)

button = QtBind.createButton(gui, 'button_add', '  Ekle  ', 215, 100)
button1 = QtBind.createButton(gui, 'button_remove', '  Kaldır  ', 215, 125)
cbxEnable = QtBind.createCheckBox(gui, 'cbxEnable_clicked','Aktif Et', 225, 80)

def cbxEnable_clicked(checked):
	SaveConfig()

def button_add_all_skills():
	SelectedMastery = QtBind.text(gui, ComboMasteries)
	if not SelectedMastery:
		log('TR_AutoCursed: Lütfen bir Ustalık Seçin')
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
		log('TR_AutoCursed: Lütfen bir Ustalık Seçin')
		return
	if not lstRemoveSkill_exist(SelectedMastery + ' Ustalığı'):
		QtBind.append(gui,lstRemoveSkills,SelectedMastery + ' Ustalığı')
		SaveConfig()

def button_get_masteries():
    QtBind.clear(gui,ComboMasteries)
    Masteries = get_mastery()
    if Masteries:
        for ID, mastery in Masteries.items():
            if mastery['level'] > 0:
                QtBind.append(gui,ComboMasteries,mastery['name'])
    else:
        log('TR_AutoCursed: Ustalıklar alınamadı. Karakter oyunda mı?')

def button_get_skills():
    skills = get_skills()
    if skills:
        for ID, skill in skills.items():
            QtBind.append(gui,lstCurrentSkills,skill['name'])
    else:
        log('TR_AutoCursed: Yetenekler alınamadı. Karakter oyunda mı?')

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
			log("TR_AutoCursed: Lanetli Kalpler Teslim Ediliyor")
			p = struct.pack('<I', key)
			inject_joymax(0x7045,p, False)
			p += b'\x0A'
			inject_joymax(0x7046,p, False)
			Timer(1.0, inject_joymax, [0x30D4, b'\x05', False]).start()
			Timer(1.2, inject_joymax, [0x30D4, b'\x05', False]).start()
			Timer(1.4, inject_joymax, [0x7515, b'\x1D\x00\x00\x00\x00', False]).start()
			Timer(4.0, AcceptQuest, ()).start()
			return
	log('TR_AutoCursed: İksir NPC\'sinin yakınında değilsiniz')

def AcceptQuest():
	npcs = get_npcs()
	for key, npc in npcs.items():
		if 'POTION' in npc['servername']:
			log("TR_AutoCursed: Görev Kabul Ediliyor")
			p = struct.pack('<I', key)
			inject_joymax(0x7045,p, False)
			p += b'\x0A'
			inject_joymax(0x7046,p, False)
			Timer(1.0, inject_joymax, [0x30D4, b'\x05', False]).start()
			Timer(1.2, inject_joymax, [0x30D4, b'\x05', False]).start()
			Timer(4.0, EnterSkillRemoval, ()).start()
			return
	log('TR_AutoCursed: İksir NPC\'sinin yakınında değilsiniz')

def EnterSkillRemoval():
	npcs = get_npcs()
	for key, npc in npcs.items():
		if 'POTION' in npc['servername']:
			log("TR_AutoCursed: Yetenek Kaldırma Penceresine Giriliyor")
			p = struct.pack('<I', key)
			inject_joymax(0x7045,p, False)
			p += b'\x0A'
			Timer(1.0, inject_joymax, [0x30D4, b'\x06', False]).start()
			Timer(3.0, EditSkill, ()).start()
			return
	log('TR_AutoCursed: İksir NPC\'sinin yakınında değilsiniz')

def ExitNPC():
	npcs = get_npcs()
	for key, npc in npcs.items():
		if 'POTION' in npc['servername']:
			inject_joymax(0x704B, struct.pack('<I', key), False)
			log("TR_AutoCursed: NPC'den Çıkılıyor")
			return

def EditSkill():
	RemoveSkills = QtBind.getItems(gui,lstRemoveSkills)
	if len(RemoveSkills) == 0:
		log('TR_AutoCursed: Kaldırılacak Başka Yetenek Yok...')
		ExitNPC()
		return
	PotionQty = int(GetPotionCount())
	if PotionQty == 0:
		log('TR_AutoCursed: Hiç Diriliş İksiriniz Yok..')
		ExitNPC()
		return
	if CheckIfOnlyMasteriesLeft():
		for Mastery in RemoveSkills:
			PotionQty = int(GetPotionCount())
			Mastery = Mastery[:-8]
			MasteryLevel = GetMasteryLevel(Mastery)
			MasteryID = GetMasteryID(Mastery)
			Deduction = MasteryLevel - PotionQty
			p = b'\x59\x0E\x00\x00'
			p += struct.pack('<I', MasteryID)
			if PotionQty >= MasteryLevel:
				p += b'\x00'
				log('TR_AutoCursed: Ustalık [%s] Kaldırıldı.' %Mastery)
				QtBind.remove(gui,lstRemoveSkills,Mastery+' Ustalığı')
				SaveConfig()
			if PotionQty < MasteryLevel:
				p += struct.pack('b', Deduction)
				log('TR_AutoCursed: Ustalık [%s] Seviyesi [%s] den [%s] e Düşürüldü.' %(Mastery,MasteryLevel,Deduction))
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
		log('TR_AutoCursed: Yetenek [%s] Kaldırıldı.' %skill)
		QtBind.remove(gui,lstRemoveSkills,skill)
		SaveConfig()
	if PotionQty < SkillLevel:
		Deduction = SkillLevel - PotionQty
		p += struct.pack('b', Deduction)
		log('TR_AutoCursed: Yetenek [%s] Seviyesi [%s] den [%s] e Düşürüldü.' %(skill,SkillLevel,Deduction))
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
		if 'Ustalığı' not in skill:
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
		if 'Ustalığı' not in skill:
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

Timer(1.0, LoadConfigs, ()).start()
log(f'Eklenti: {name} başarıyla yüklendi.')

if not os.path.exists(path):
	os.makedirs(path)
	log('TR_AutoCursed: Klasör oluşturuldu.')