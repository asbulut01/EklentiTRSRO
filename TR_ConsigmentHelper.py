from phBot import *
import phBotChat
import QtBind
from datetime import datetime
import time
import json
import os
import struct
from threading import Timer

pName = 'TR_ConsigmentHelper'
pVersion = '2.0'

gui = QtBind.init(__name__,pName)
lsthunterstatus = []
lstthiefstatus = []
lblCons = QtBind.createLabel(gui,"Konsinye Kayıtları",6,10)
lstCons = QtBind.createList(gui,2,30,440,190)
lblCheck = QtBind.createLabel(gui,"Konsinye Ayarları",450,10)
lstCheck = QtBind.createList(gui,450,30,230,240)
lblCheckbox = QtBind.createLabel(gui,"Otomatik Yerleştir.",460,40)
jobthief = QtBind.createCheckBox(gui, 'checkbox_clicked_hunter', 'Avcı', 460, 60)
jobhunter = QtBind.createCheckBox(gui, 'checkbox_clicked_thief', 'Hırsız', 530, 60)
jobnotify = QtBind.createCheckBox(gui, 'checkbox_clicked_notify', 'Sevkiyat Başlamadan Önce Haber Ver.', 460, 80)
jobnotifystart = QtBind.createCheckBox(gui, 'checkbox_clicked_notifystart', 'Başladığında Bildir.', 460, 100)
jobnotifyend = QtBind.createCheckBox(gui, 'checkbox_clicked_notifyend', 'Sona Erdiğinde Bildir', 460, 120)
joblogs = QtBind.createCheckBox(gui, 'checkbox_clicked_joblogs', 'Bildirimleri Kaydet.', 460, 140)
clear = QtBind.createButton(gui, 'clear_clicked', 'Olay Kutularını Temizle', 455, 200)
clearlogs = QtBind.createButton(gui, 'clearlog_clicked', 'Kayıtları Temizle', 580, 200)
btnSaveConfig = QtBind.createButton(gui,'saveConfigs',"Ayarları Kaydet",460,165)
lsthunterstatus = QtBind.createList(gui,2,240,200,30)
lstthiefstatus = QtBind.createList(gui,240,240,200,30)

character_data = None
party_data = None
chat_data = {}
isOnline = False
hasStall = False
isActived = False
isAutoRefresh = False
jobselect = []
inGame = None

def getlogs():
	return get_log_dir()+pName+"\\"

def getPath():
   return get_config_dir()+pName+"\\"

def getConfig():
   return getPath()+inGame['server'] + "_" + inGame['name'] + ".json"

def getconslogs():
   return getPath()+inGame['server'] + "_" + inGame['name'] + "_Logs" + ".txt"

def logconslogs():
	return logging.basicConfig(filename=getconslogs,format="%(asctime)s %(message)s",filemode="a",level=logging.INFO)

def isJoined():
	global inGame
	inGame = get_character_data()
	if not (inGame and "name" in inGame and inGame["name"]):
		inGame = None
	return inGame

def loadDefaultConfig():
	QtBind.setChecked(gui,jobthief,False)
	QtBind.setChecked(gui,jobhunter,False)
	QtBind.setChecked(gui,jobnotify,False)
	QtBind.setChecked(gui,jobnotifystart,False)
	QtBind.setChecked(gui,jobnotifyend,False)
	QtBind.setChecked(gui,joblogs,False)

def loadConfigs():
	loadDefaultConfig()
	global jobselect
	if isJoined():
		if os.path.exists(getConfig()):
			data = {}
			with open(getConfig(),"r") as f:
				data = json.load(f)
				if "Thief" in data and data["Thief"]:
					QtBind.setChecked(gui,jobthief,True)
				else:
					 QtBind.setChecked(gui,jobthief,False)   
				if "Hunter" in data and data["Hunter"]:
					QtBind.setChecked(gui,jobhunter,True)
				else:
					 QtBind.setChecked(gui,jobhunter,False) 
				if "Notify" in data and data["Notify"]:
					QtBind.setChecked(gui,jobnotify,True)
				else:
					 QtBind.setChecked(gui,jobnotify,False) 
				if "Starting Notify" in data and data["Starting Notify"]:
					QtBind.setChecked(gui,jobnotifystart,True)
				else:
					 QtBind.setChecked(gui,jobnotifystart,False) 
				if "Ending Notify" in data and data["Ending Notify"]:
					QtBind.setChecked(gui,jobnotifyend,True)
				else:
					 QtBind.setChecked(gui,jobnotifyend,False)
				if "Job Logs" in data and data["Job Logs"]:
					QtBind.setChecked(gui,joblogs,True)
				else:
					 QtBind.setChecked(gui,joblogs,False)
				for job in data["jobselect"]:
					  jobselect.append(job)

def saveConfigs():
	if isJoined():
		global jobselect
		data = {}
		data["Thief"] = QtBind.isChecked(gui,jobthief)
		data["Hunter"] = QtBind.isChecked(gui,jobhunter)
		data["Notify"] = QtBind.isChecked(gui,jobnotify)
		data["Starting Notify"] = QtBind.isChecked(gui,jobnotifystart)
		data["Ending Notify"] = QtBind.isChecked(gui,jobnotifyend)
		data["Logs"] = QtBind.getItems(gui,lstCons)
		data["Job Logs"] = QtBind.isChecked(gui,joblogs)
		data["jobselect"] = jobselect
		with open(getConfig(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Eklenti: "+pName+" Yapılandırması Kaydedildi.")

def connected():
	global inGame
	inGame = None

def joined_game():
	loadConfigs()

def checkbox_clicked_joblogs(checked):
	log('Eklenti: Konsinye Kayıt Bildirimleri %s.' % checked)
	global jobselect
	jobselect.append("4")
	return True

def checkbox_clicked_notify(checked):
	log('Eklenti: Sevkiyat Başlamadan Haber Ver %s.' % checked)
	global jobselect
	jobselect.append("3")
	return True

def checkbox_clicked_notifystart(checked):
	log('Eklenti: Başladığında Bildir %s.' % checked)
	global jobselect
	jobselect.append("31")
	return True

def checkbox_clicked_notifyend(checked):
	log('Eklenti: Sonlandığında Bildir %s.' % checked)
	global jobselect
	jobselect.append("32")
	return True

def checkbox_clicked_hunter(checked):
	log('Eklenti: Avcı Seçeneği Seçildi.')
	global jobselect
	jobselect.clear()
	jobselect.append("1")
	return True

def checkbox_clicked_thief(checked):
	log('Eklenti: Hırsız Seçeneği Seçildi.')
	global jobselect
	jobselect.clear()
	jobselect.append("2")
	return True

def clear_clicked():
		log('Temizlendi.')
		global jobselect
		jobselect.clear()
		QtBind.setChecked(gui,joblogs,False)
		QtBind.setChecked(gui,jobthief,False)
		QtBind.setChecked(gui,jobhunter,False)
		QtBind.setChecked(gui,jobnotify,False)
		QtBind.setChecked(gui,jobnotifystart,False)
		QtBind.setChecked(gui,jobnotifyend,False)
		os.remove(getPath()+inGame['server'] + "_" + inGame['name'] + ".json")
		return True

def clearlog_clicked():
		log('Konsinye Kayıtları Temizlendi.')
		QtBind.clear(gui,lstCons)
		return True

def handle_joymax(opcode, data): 
	global party_data,hasStall,jobselect,currentconst,currentconsh
	if opcode == 0x300C:
		updateType = data[0]
		if updateType == 29:
			eventType = data[2]
			date = datetime.now().strftime('%H:%M:%S')
			if eventType == 1:
					progressType = data[3]
					if progressType == 0:
						log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Avcı Ticareti 10 Dakika içinde Başlayacak.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
						QtBind.clear(gui,lsthunterstatus)
						QtBind.append(gui,lsthunterstatus, "[%s]  Avcı 10 Dakika." %date)
						QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Avcı Ticareti 10 Dakika Içinde Başlayacak." %date)
						if "4" in jobselect:
													create_notification('Avcı 10 Dakika.')
						if "3" in jobselect:
							play_wav('C:/Windows/Media/uyarı.wav')
						elif len(jobselect) == 1 and "3" in jobselect:
							show_notification('Avcı Kervanı', '10 Dakika içinde Başlayacak')
							play_wav('C:/Windows/Media/uyarı.wav')
					elif progressType == 1:
						townType = data[4]
						if "31" in jobselect:
							play_wav('C:/Windows/Media/Alarm03.wav')
						if townType == 0:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Avcı Ticareti Jangan'dan Başladı.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Avcı Ticareti Jangan'dan Başladı." %date)
							QtBind.clear(gui,lsthunterstatus)
							QtBind.append(gui,lsthunterstatus, "[%s]  Avcı - Jangan." %date)
							if "4" in jobselect:
															create_notification('Avcı - Jangan.')
						elif townType == 1:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Avcı Ticareti Donwhang'dan Başladı.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Scorpion: 7,5 dk - Den: 19 dk - Maong: 26 dk           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							QtBind.clear(gui,lsthunterstatus)
							QtBind.append(gui,lsthunterstatus, "[%s]  Avcı - Donwhang." %date)
							if "4" in jobselect:
															create_notification('Avcı - Donwhang.')
						elif townType == 2:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Avcı Ticareti Samarkand'dan Başladı.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Avcı Ticareti Samarkand'dan Başladı." %date)
							QtBind.clear(gui,lsthunterstatus)
							QtBind.append(gui,lsthunterstatus, "[%s]  Avcı - Samarkand." %date)
							if "4" in jobselect:
															create_notification('Avcı - Samarkand.')
						elif townType == 3:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Avcı Ticareti Constantinople'den Başladı.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Avcı Ticareti Constantinople'den Başladı." %date)
							QtBind.clear(gui,lsthunterstatus)
							QtBind.append(gui,lsthunterstatus, "[%s]  Avcı - Constantinople." %date)
							
							if "4" in jobselect:
															create_notification('Avcı - Constantinople.')
						elif townType == 4:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Hunter trade started from 4.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Hunter trade started from 4." %date)
						elif townType == 5:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Hunter trade started from 5.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
						elif townType == 6:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Hunter trade started from 6.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
						elif townType == 7:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Hunter trade started from 7.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
					elif progressType == 2:
						log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Avcı Ticareti Sona Erdi.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
						QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Avcı Ticareti Sona Erdi." %date)
						QtBind.clear(gui,lsthunterstatus)
						QtBind.append(gui,lsthunterstatus, "[%s]  Avcı Sona Erdi." %date)
						
						if "4" in jobselect:
							create_notification('Avcı Sona Erdi.')
						if "32" in jobselect:
							play_wav('C:/Windows/Media/uyarı.wav')
						if "1" in jobselect:                                                      
							log("Bot started after ending of Hunter consigment.")
						return True
			elif eventType == 2:
					progressType = data[3]
					if progressType == 0:
						log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Hırsız Ticareti 10 Dakika içinde Başlayacak.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
						QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Hırsız Ticareti 10 Dakika içinde Başlayacak. " %date)
						QtBind.clear(gui,lstthiefstatus)
						QtBind.append(gui,lstthiefstatus, "[%s]  Hırsız 10 Dakika." %date)
						
						if "4" in jobselect:
							create_notification('Hırsız 10 Dakika.')
						if "3" in jobselect:
							show_notification('Hırsız Ticareti', '10 Dakika içinde Başlayacak')
							play_wav('C:/Windows/Media/uyarı.wav')
						elif len(jobselect) == 1 and "3" in jobselect:
							show_notification('Hırsız Ticareti', '10 Dakika içinde Başlayacak')
							play_wav('C:/Windows/Media/uyarı.wav')
					elif progressType == 1:
						townType = data[4]
						if "31" in jobselect:
							play_wav('C:/Windows/Media/Alarm03.wav')
						if townType == 0:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Hırsız Ticareti Jangan'dan Başladı.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Hırsız Ticareti Jangan'dan Başladı." %date)
							QtBind.clear(gui,lstthiefstatus)
							QtBind.append(gui,lstthiefstatus, "[%s]  Hırsız - Jangan." %date)
							if "4" in jobselect:
								create_notification('Hırsız - Jangan.')
						if townType == 1:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Hırsız Ticareti Donwhang'dan Başladı.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Scorpion: 7,5 dk - Den: 19 dk - Maong: 26 dk.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							QtBind.clear(gui,lstthiefstatus)
							QtBind.append(gui,lstthiefstatus, "[%s]  Hırsız - Donwhang." %date)
							if "4" in jobselect:
																create_notification('Hırsız - Donwhang')
						elif townType == 2:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Hırsız Ticareti Samarkand'dan Başladı.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Hırsız Ticareti Samarkand'dan Başladı." %date)
							QtBind.clear(gui,lstthiefstatus)
							QtBind.append(gui,lstthiefstatus, "[%s]  Hırsız - Samarkand." %date)
							if "4" in jobselect:
																create_notification('Hırsız - Samarkand.')
						elif townType == 3:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Hırsız Ticareti Constantinople'den Başladı.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Hırsız Ticareti Constantinople'den Başladı." %date)
							QtBind.clear(gui,lstthiefstatus)
							QtBind.append(gui,lstthiefstatus, "[%s]  Hırsız - Constantinople." %date)
							if "4" in jobselect:
																create_notification('Hırsız - Constantinople.')
						elif townType == 4:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Thief trade started from 4.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
							QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Thief trade started from 4." %date)
						elif townType == 5:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Thief trade started from 5.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
						elif townType == 6:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Thief trade started from 6.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
						elif townType == 7:
							log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Thief trade started from 7.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
					elif progressType == 2:
						log("ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ           Eklenti: [Konsinye] Hırsız Ticareti Sona Erdi.           ˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣˣ")
						QtBind.append(gui,lstCons,"[%s]                 [Konsinye] Hırsız Ticareti Sona Erdi." %date)
						QtBind.clear(gui,lstthiefstatus)
						QtBind.append(gui,lstthiefstatus, "[%s]  Hırsız Sona Erdi." %date)
						
						if "4" in jobselect:
													create_notification('Hırsız Sona Erdi.')
						if "32" in jobselect:
								play_wav('C:/Windows/Media/uyarı.wav')
						if "2" in jobselect:						
							log("Bot started after ending of Thief consigment.")
						return True
	return True

def event_loop():
		date

log('Eklenti: '+pName+' v'+pVersion+' Yuklendi. // edit by hakankahya')

if os.path.exists(getPath()):
	loadConfigs()
else:
	os.makedirs(getPath())
	log('Eklenti: '+pName+' Klasörü Oluşturuldu.')
