from phBot import *
import urllib.request
from threading import Timer
from datetime import datetime, timedelta
import datetime
import os
import signal
import struct
import subprocess
import json
import QtBind

name = 'TR_ScriptCommands'
version = 2.6

#get phbot folder path
path = get_config_dir()[:-7]

StartBotAt = 0
CloseBotAt = 0
CheckStartTime = False
CheckCloseTime = False
SkipCommand = False
delay_counter = 0
BtnStart = False
Recording = False
RecordedPackets = []
ExecutedPackets = []
Index = 0
StopBot = True

gui = QtBind.init(__name__, name)
LvlSaveName = QtBind.createLabel(gui,'Kaydıt İsmi ',10,13)
SaveName = QtBind.createLineEdit(gui,"",80,10,120,20)
RecordBtn = QtBind.createButton(gui, 'button_start', ' Kaydı Başlat ', 220, 10)
Display = QtBind.createList(gui,20,50,280,180)
ShowCommandsBtn = QtBind.createButton(gui, 'button_ShowCmds', ' Komutları Göster ', 20, 240)
DeleteCommandsBtn = QtBind.createButton(gui, 'button_DelCmds', ' Komutu Sil ', 120, 240)
ShowPacketsBtn = QtBind.createButton(gui, 'button_ShowPackets', ' Paketleri Göster ', 220, 240)
cbxShowPackets = QtBind.createCheckBox(gui, 'cbxAuto_clicked','Paketleri Göster ', 330, 10)

#backup
def ResetSkip():
    global SkipCommand
    SkipCommand = False

def LeaveParty(args):
    if get_party():
        inject_joymax(0x7061,b'',False)
        log('Eklenti: Partiden çıkılıyor')
    return 0

#Notification,title,message..show a windows notification, bot must be minimized
def Notification(args):
    if len(args) == 3:
        title = args[1]
        message = args[2]
        show_notification(title, message)
        return 0
    log('Eklenti: Hatalı Bildirim komutu')
    return 0

#NotifyList,message.. Create a notification in the list
def NotifyList(args):
    if len(args) == 2:
        message = args[1]
        create_notification(message)
        return 0
    log('Eklenti: Hatalı NotifyList komutu')
    return 0

#PlaySound,ding.wav...wav file must be in your phbot folder
def PlaySound(args):
    FileName = args[1]
    if os.path.exists(path + FileName):
        play_wav(path + FileName)
        log('Eklenti: [%s] oynatılıyor' %FileName)
        return 0
    log('Eklenti: [%s] ses dosyası mevcut değil' %FileName)
    return 0

#example - SetScript,Mobs103.txt
#script must be in your phbot folder
def SetScript(args):
    name = args[1]
    if os.path.exists(path + name):
        set_training_script(path + name)
        log('Eklenti: Komut [%s] olarak değiştirildi' %name)
        return 0
    log('Eklenti: [%s] komutu mevcut değil' %name)
    return 0

#CloseBot..kills the bot immediately
#CloseBot,in,5... kills the bot in 5 mins
#CloseBot,at,05:30..kills the bot at a specific time.. 24hour clock
def CloseBot(args):
    global CloseBotAt, CheckCloseTime
    CheckCloseTime = True
    if len(args) == 1:
        Terminate()
        return 0
    type = args[1]
    time = args[2]
    if type == 'in':
        CloseBotAt = str(datetime.datetime.now() + timedelta(minutes=int(time)))[11:16]
        log('Eklenti: Bot [%s] da kapatılacak' %CloseBotAt)
    elif type == 'at':
        CloseBotAt = time
        log('Eklenti: Bot [%s] da kapatılacak' %CloseBotAt)
    return 0

def Terminate():
    log("Eklenti: Bot kapatılıyor...")
    os.kill(os.getpid(),9)

#GoClientless.. Kills the Client instantly
def GoClientless(args):
    pid = get_client()['pid']
    if pid:
        os.kill(pid, signal.SIGTERM)
        return 0
    log('Eklenti: İstemci açık değil!')
    return 0

#Stop and Start the bot at specified time
#Ex StartBot,in,5.. Starts bot in 5 mins
#Ex StartBot,at,05:30.. Starts bot at specified time.. 24hour clock
def StartBot(args):
    global StartBotAt, CheckStartTime, SkipCommand
    #avoid bot doing command again after restarting
    if SkipCommand:
        SkipCommand = False
        return 0
    stop_bot()
    type = args[1]
    time = args[2]
    CheckStartTime = True
    if type == 'in':
        StartBotAt = str(datetime.datetime.now() + timedelta(minutes=int(time)))[11:16]
        log('Eklenti: Bot [%s] da başlatılacak' %StartBotAt)
    elif type == 'at':
        StartBotAt = time
        log('Eklenti: Bot [%s] da başlatılacak' %StartBotAt)
    return 0

#StopStart..Stops and starts the bot 1 second later
def StopStart(args):
    global SkipCommand
    #avoid bot doing command again after restarting
    if SkipCommand:
        SkipCommand = False
        return 0
    stop_bot()
    Timer(1.0, start_bot, ()).start()
    #some cases the bot may not pass over the command again when starting again
    Timer(30.0, ResetSkip, ()).start()
    SkipCommand = True
    return 0

#StartTrace,player..Starts tracing a player
def StartTrace(args):
    global SkipCommand
    #avoid bot doing command again after restarting
    if SkipCommand:
        SkipCommand = False
        return 0
    elif len(args) == 2:
        stop_bot()
        player = args[1]
        if start_trace(player):
            log('Eklenti: [%s] takip ediliyor' %player)
            return 0
        else:
            log('Eklenti: Oyuncu [%s] yakın değil.. Devam ediyor' %player)
            SkipCommand = True
            Timer(1.0, start_bot, ()).start()
            #some cases the bot may not pass over the command again when starting again
            Timer(30.0, ResetSkip, ()).start()
            return 0
    log('Eklenti: Hatalı StartTrace formatı')
    return 0

#RemoveSkill,skillname...Remove the skill if active
def RemoveSkill(args):
    RemSkill = args[1]
    skills = get_active_skills()
    for ID, skill in skills.items():
        if skill['name'] == RemSkill:
            packet = b'\x01\x05'
            packet += struct.pack('<I', ID)
            packet += b'\x00'
            inject_joymax(0x7074,packet,False)
            log('Eklenti: [%s] yeteneği kaldırılıyor' %RemSkill)
            return 0
    log('Eklenti: Yetenek aktif değil')
    return 0

#Drop,itemname... drops the first stack of the specified item
def Drop(args):
    DropItem = args[1]
    items = get_inventory()['items']
    for slot, item in enumerate(items):
        if item:
            name = item['name']
            if name == DropItem:
                p = b'\x07' # static stuff maybe
                p += struct.pack('B', slot)
                log('Eklenti: [%s][%s] eşyası bırakılıyor' %(item['quantity'],name))
                inject_joymax(0x7034,p,True)
                return 0
    log(r'Eklenti: Bırakılacak eşya yok')
    return 0

#OpenphBot,commandlinearguments..opens a bot with the specified arguements
def OpenphBot(args):
    cmdargs = args[1]
    if os.path.exists(path + "phBot.exe"):
        subprocess.Popen(path + "phBot.exe " + cmdargs)
        log('Eklenti: Yeni bir bot açılıyor')
        return 0
    log('Eklenti: Geçersiz bot yolu')
    return 0

#DismountPet,transport
def DismountPet(args):
    PetType = args[1].lower()
    if PetType == 'pick':
        log('Eklenti: Pick pet inemez')
        return 0
    pets = get_pets()
    if pets:
        for id,pet in pets.items():
            if pet['type'] == PetType:
                p = b'\x00'
                p += struct.pack('I',id)
                inject_joymax(0x70CB,p, False)
                return 0
    return 0

#UnsummonPet,fellow
def UnsummonPet(args):
    PetType = args[1].lower()
    pets = get_pets()
    if pets:
        for id,pet in pets.items():
            if pet['type'] == PetType:
                p = struct.pack('I',id)
                if PetType == 'transport' or PetType == 'horse':
                    inject_joymax(0x70C6,p, False)
                else:
                    inject_joymax(0x7116,p, False)
                log(f'Eklenti: [{PetType}] pet geri çağrılıyor')
                return 0
    return 0

#ResetWeapons,all or ResetWeapons,primary or ResetWeapons,secondary or ResetWeapons,shield
def ResetWeapons(args):
    Items = 'all'
    if len(args) == 2:
        Items = args[1].lower()
    path = get_config_dir()
    CharData = get_character_data()
    ConfigFile = f"{CharData['server']}_{CharData['name']}.{get_profile()}.json" if len(get_profile()) > 0 else f"{CharData['server']}_{CharData['name']}.json"
    if os.path.exists(path + ConfigFile):
        with open(path + ConfigFile,"r") as f:
            Configdata = json.load(f)
            if Items == 'all':
                Configdata['Inventory'] = {"Primary": 0, "Secondary": 0, "Shield": 0}
            if Items == 'primary':
                Configdata['Inventory']['Primary'] = 0
            if Items == 'secondary':
                Configdata['Inventory']['Secondary'] = 0
            if Items == 'shield':
                Configdata['Inventory']['Shield'] = 0
            with open(path + ConfigFile ,"w") as f:
                f.write(json.dumps(Configdata, indent=4))
                log('Eklenti: Silahlar sıfırlandı')
                set_profile(get_profile())
                return 0
    return 0

#SetArea,trainingareaname
def SetArea(args):
    if len(args) == 2:
        set_training_area(args[1])
        log(f"Eklenti: Eğitim alanı [{args[1]}] olarak değiştirildi")
        return 0
    log('Eklenti: Lütfen bir eğitim alanı ismi belirtin')
    return 0

def CalcRadiusFromME(Px,Py):
    my = get_position()
    dist = ((my['x'] - Px)**2 + (my['y'] - Py)**2)**0.5
    return dist
	
#ExchangePlayer,playername.... player must be in your party
def ExchangePlayer(args):
    if len(args) == 2:
        PlayerName = args[1]
        party = get_party()
        if not party:
            log(f"Eklenti: Partide değilsiniz, takas yapılamaz")
            return 0
        for key, player in party.items():
            if player['name'] == PlayerName:
                radius = CalcRadiusFromME(player['x'],player['y'])
                if player['player_id'] <= 0 or radius > 20:
                    log(f"Eklenti: Oyuncu [{player['name']}] menzil dışında! Takas yapılamaz")
                    return 0
                log(f"Eklenti: [{player['name']}] ile takas başlatılıyor")
                p = struct.pack('<I', player['player_id'])
                inject_joymax(0x7081,p,True)
                return 0
        log(f"Eklenti: Oyuncu [{PlayerName}] partide değil! Takas yapılamaz")
        return 0
    log(f"Eklenti: Lütfen takas yapılacak bir oyuncu belirtin")
    return 0

#ChangeBotOption,value,key,key,key,key.... example ChangeBotOption,true,Town,Return,Death
def ChangeBotOption(args):
    if len(args) <= 3 or len(args) >= 7:
        log(f"Eklenti: Hatalı format, ayar değiştirilemiyor.")
        return 0
    value = args[1]
    path = get_config_dir()
    CharData = get_character_data()
    ConfigFile = f"{CharData['server']}_{CharData['name']}.{get_profile()}.json" if len(get_profile()) > 0 else f"{CharData['server']}_{CharData['name']}.json"
    if os.path.exists(path + ConfigFile):
        with open(path + ConfigFile,"r") as f:
            Configdata = json.load(f)
            if len(args) == 4:
                try:
                    data = Configdata[args[2]][args[3]]
                except:
                    log('Eklenti: Hatalı json anahtarı, ayar değiştirilemiyor')
                    return 0					
                if type(data) == list:
                    Configdata[args[2]][args[3]].append(value)
                else:
                    Configdata[args[2]][args[3]] = value
                
            if len(args) == 5:
                try:
                    data = Configdata[args[2]][args[3]][args[4]]
                except:
                    log('Eklenti: Hatalı json anahtarı, ayar değiştirilemiyor')
                    return 0
                if type(data) == list:
                    Configdata[args[2]][args[3]][args[4]].append(value)
                else:
                    Configdata[args[2]][args[3]][args[4]] = value
                
            if len(args) == 6:
                try:
                    data = Configdata[args[2]][args[3]][args[4]][args[5]]
                except:
                    log('Eklenti: Hatalı json anahtarı, ayar değiştirilemiyor')
                    return 0
                if type(data) == list:
                    Configdata[args[2]][args[3]][args[4]][args[5]].append(value)
                else:
                    Configdata[args[2]][args[3]][args[4]][args[5]] = value
                
            with open(path + ConfigFile ,"w") as f:
                f.write(json.dumps(Configdata, indent=4))
                log('Eklenti: Ayarlar başarıyla değiştirildi')
                set_profile(get_profile())
                return 0

def event_loop():
    global delay_counter, CheckStartTime, SkipCommand, CheckCloseTime
    if CheckStartTime:
        delay_counter += 500
        if delay_counter >= 60000:
            delay_counter = 0
            CurrentTime = str(datetime.datetime.now())[11:16]
            if CurrentTime == StartBotAt:
                CheckStartTime = False
                SkipCommand = True
                log('Eklenti: Bot başlatılıyor')
                start_bot()

    elif CheckCloseTime:
        delay_counter += 500
        if delay_counter >= 60000:
            delay_counter = 0
            CurrentTime = str(datetime.datetime.now())[11:16]
            if CurrentTime == CloseBotAt:
                CheckCloseTime = False
                Terminate()

#-----------------Custom Script Command Stuffs-----------------

def button_start():
    global BtnStart, RecordedPackets
    if len(QtBind.text(gui,SaveName)) <= 0:
        log('Eklenti: Lütfen Özel Komut için bir isim girin')
        return
    if BtnStart == False:
        BtnStart = True
        QtBind.setText(gui,RecordBtn,' Kaydı Durdur ')
        log('Eklenti: Kayda başlandı, lütfen kayıt için NPC seçin')
    elif BtnStart == True:
        log('Eklenti: Kayıt Tamamlandı')
        Name = QtBind.text(gui,SaveName)
        SaveNPCPackets(Name,RecordedPackets)
        BtnStart = False
        QtBind.setText(gui,RecordBtn,' Kaydı Başlat ')
        Recording = False
        RecordedPackets = []
        Timer(1.0, button_ShowCmds, ()).start()

def button_ShowCmds():
    QtBind.clear(gui,Display)
    data = {}
    if os.path.exists(path + "CustomNPC.json"):
        with open("CustomNPC.json","r") as f:
            data = json.load(f)
            for name in data:
                QtBind.append(gui,Display,name)
    else:
        log('Eklenti: Şu anda kaydedilmiş komut yok')

def button_DelCmds():
    Name = QtBind.text(gui,Display)
    QtBind.clear(gui,Display)
    data = {}
    if Name:
        with open("CustomNPC.json","r") as f:
            data = json.load(f)
            for name, value in list(data.items()):
                if name == Name:
                    del data[name]
                    with open("CustomNPC.json","w") as f:
                        f.write(json.dumps(data, indent=4))
                        log('Eklenti: Özel NPC Komutu [%s] silindi' %name)
                        Timer(1.0, button_ShowCmds, ()).start()
                        return
            else:
                log('Eklenti: Özel NPC Komutu [%s] mevcut değil' %Name)
                Timer(1.0, button_ShowCmds, ()).start()

def button_ShowPackets():
    Name = QtBind.text(gui,Display)
    QtBind.clear(gui,Display)
    data = {}
    if Name:
        with open("CustomNPC.json","r") as f:
            data = json.load(f)
            for name in data:
                if name == Name:
                    Packets = data[name]['Packets']
                    for packet in Packets:
                        QtBind.append(gui,Display,packet)

def GetPackets(Name):
    global ExecutedPackets
    data = {}
    with open("CustomNPC.json","r") as f:
        data = json.load(f)
        for name in data:
            if name == Name:
                ExecutedPackets = data[name]['Packets']

def SaveNPCPackets(Name,Packets=[]):
    data = {}
    if os.path.exists(path + "CustomNPC.json"):
        with open("CustomNPC.json","r") as f:
            data = json.load(f)
    else:
        data = {}
    data[Name] = {"Packets": Packets}
    with open("CustomNPC.json","w") as f:
        f.write(json.dumps(data, indent=4))
    log("Eklenti: Özel NPC Komutu Kaydedildi")

#example.. CustomNPC,savedname,true
def CustomNPC(args):
    global SkipCommand, StopBot
    if SkipCommand:
        SkipCommand = False
        return 0
    if len(args) < 2:
        log('Eklenti: Geçersiz komut, CustomNPC,savedname,state kullanın')
        return 0
    StopBot = True
    if len(args) == 3:
        State = args[2]
        if State.lower() == 'true':
            StopBot = True
        if State.lower() == 'false':
            StopBot = False
    if StopBot:
        stop_bot()
    Name = args[1]
    GetPackets(Name)
    #avoid the bot closing the npc window
    Timer(0.5, InjectPackets, ()).start()
    return 0

def InjectPackets():
    global Index, ExecutedPackets
    opcode = int(ExecutedPackets[Index].split(':')[0],16)
    dataStr = ExecutedPackets[Index].split(':')[1].replace(' ','')
    LendataStr = len(dataStr)
    data = bytearray()
    for i in range(0,int(LendataStr),2):
            data.append(int(dataStr[i:i+2],16))
    inject_joymax(opcode, data, False)
    if QtBind.isChecked(gui,cbxShowPackets):
        log("Eklenti: Enjekte Edildi (Opcode) 0x" + '{:02X}'.format(opcode) + " (Veri) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
    NumofPackets = len(ExecutedPackets) - 1
    if Index < NumofPackets:
        Index += 1
        Timer(2.0, InjectPackets, ()).start()

    elif Index == NumofPackets:
        global SkipCommand
        log('Eklenti: Özel NPC Komutu Tamamlandı')
        Index = 0
        ExecutedPackets = []
        #some cases the bot may not pass over the command when starting again
        Timer(30.0, ResetSkip, ()).start()
        SkipCommand = True
        if StopBot:
            start_bot()

def handle_silkroad(opcode, data):
    global Recording, BtnStart, RecordedPackets
    if data == None:
        return True
    if BtnStart:
        #select NPC to start recording
        if opcode == 0x7045 or opcode == 0x7C45:
            Recording = True
            log('Eklenti: Kayıt Başladı')
            RecordedPackets.append("0x" + '{:02X}'.format(opcode) + ":" + ' '.join('{:02X}'.format(x) for x in data))
            if QtBind.isChecked(gui,cbxShowPackets):
                log("Eklenti: Kaydedildi (Opcode) 0x" + '{:02X}'.format(opcode) + " (Veri) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))
        if Recording == True:
            if opcode != 0x7045 or opcode != 0x7C45:
                RecordedPackets.append("0x" + '{:02X}'.format(opcode) + ":" + ' '.join('{:02X}'.format(x) for x in data))
                if QtBind.isChecked(gui,cbxShowPackets):
                    log("Eklenti: Kaydedildi (Opcode) 0x" + '{:02X}'.format(opcode) + " (Veri) "+ ("None" if not data else ' '.join('{:02X}'.format(x) for x in data)))

    return True

log('Eklenti: [%s] Sürüm %s Yüklendi. // edit by hakankahya' % (name,version))
