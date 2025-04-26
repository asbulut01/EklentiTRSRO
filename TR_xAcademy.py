from phBot import *
import QtBind
from threading import Timer
from datetime import datetime
from datetime import timedelta
import struct
import random
import json
import os
import subprocess

pName = 'TR_xAcademy'

SEQUENCE_DEFAULT_NUMBER = 100
NOTIFICATION_SOUND_PATH = 'c:\\Windows\\Media\\chimes.wav'

isCreatingCharacter = False
isDeletingCharacter = False
CreatingNickname = ""
isRestarted = False

gui = QtBind.init(__name__, pName)
cbxEnabled = QtBind.createCheckBox(gui, 'cbxDoNothing', 'Aktif', 6, 9)

_x = 350
_y = 10
lblProfileName = QtBind.createLabel(gui, "Config profil adı :", _x, _y)
tbxProfileName = QtBind.createLineEdit(gui, "", _x + 102, _y - 3, 110, 19)
btnSaveConfig = QtBind.createButton(gui, 'btnSaveConfig_clicked', "  Kaydet  ", _x + 102 + 110 + 3, _y - 5)
btnLoadConfig = QtBind.createButton(gui, 'btnLoadConfig_clicked', "  Yükle  ", _x + 102 + 110 + 3 + 75, _y - 5)

_x = 6
_y = 40
cbxSelectChar = QtBind.createCheckBox(gui,'cbxDoNothing','Seç: 1-40Lv',_x,_y-1)
cbxSelectChar2 = QtBind.createCheckBox(gui,'cbxDoNothing','Seç: 1-29Lv',_x+80,_y-1)
cbxSelectChar3 = QtBind.createCheckBox(gui,'cbxDoNothing','Seç: 1-20Lv',_x+160,_y-1)
cbxSelectCharOnAcademy = QtBind.createCheckBox(gui,'cbxDoNothing','Seç: 40-50Lv',_x+240,_y-1)
_y+=20
cbxCreateChar = QtBind.createCheckBox(gui,'cbxDoNothing','Oluştur',_x,_y-1)
_y+=20
cbxDeleteChar = QtBind.createCheckBox(gui,'cbxDoNothing','Sil - 40-50Lv Arasındaki Karakterler.',_x,_y-1)

_x = 518
_y = 40
lblNickname = QtBind.createLabel(gui, "Karakter Adı :", _x, _y)
tbxNickname = QtBind.createLineEdit(gui, "", _x + 94, _y - 3, 102, 19)
_y += 20
lblSequence = QtBind.createLabel(gui, "Karakter Sırası :", _x, _y)
tbxSequence = QtBind.createLineEdit(gui, "", _x + 95, _y - 3, 101, 19)
_y += 20
lblRace = QtBind.createLabel(gui, "Karakter Irk'ı :", _x, _y)
cmbxRace = QtBind.createCombobox(gui, _x + 72, _y - 3, 124, 19)
QtBind.append(gui, cmbxRace, "CH")
QtBind.append(gui, cmbxRace, "EU")

_y = 130
_x = 6
lblFullCharacters = QtBind.createLabel(gui, "Daha fazla karakter oluşturmak mümkün değilse aşağıdaki eylemler gerçekleştirilecek :", _x, _y)
_y += 20
lblCMD = QtBind.createLabel(gui, "Sistem komutu (CMD) çalıştır :", _x + 10, _y)
tbxCMD = QtBind.createLineEdit(gui, "", 163, _y - 3, 205, 19)
_y += 20
cbxExit = QtBind.createCheckBox(gui, 'cbxDoNothing', 'Botu kapat', _x + 9, _y)
_y += 20
cbxNotification_Full = QtBind.createCheckBox(gui, 'cbxDoNothing', 'phBot bildirimi göster', _x + 9, _y)
_y += 20
cbxSound_Full = QtBind.createCheckBox(gui, 'cbxDoNothing', 'Ses çal.  Yol : ', _x + 9, _y)
tbxSound_Full = QtBind.createLineEdit(gui, '', 128, _y - 1, 240, 19)
_y += 20
cbxLog_Full = QtBind.createCheckBox(gui, 'cbxDoNothing', 'Dosyaya kaydet', _x + 9, _y)

def getPath():
    return get_config_dir() + pName + "\\"

def getConfig(name):
    if not name:
        name = pName
    return getPath() + name + ".json"

def loadDefaultConfig():
    QtBind.setText(gui, tbxProfileName, "")
    QtBind.setChecked(gui, cbxEnabled, False)
    QtBind.setChecked(gui,cbxSelectChar,True)
    QtBind.setChecked(gui,cbxSelectChar2,False)
    QtBind.setChecked(gui,cbxSelectChar3,False)
    QtBind.setChecked(gui, cbxCreateChar, True)
    QtBind.setChecked(gui, cbxDeleteChar, True)
    QtBind.setChecked(gui, cbxSelectCharOnAcademy, False)
    QtBind.setText(gui, tbxNickname, "")
    QtBind.setText(gui, tbxSequence, str(SEQUENCE_DEFAULT_NUMBER))
    QtBind.setText(gui, cmbxRace, "CH")
    QtBind.setText(gui, tbxCMD, "")
    QtBind.setChecked(gui, cbxNotification_Full, False)
    QtBind.setChecked(gui, cbxSound_Full, False)
    QtBind.setText(gui, tbxSound_Full, NOTIFICATION_SOUND_PATH)
    QtBind.setChecked(gui, cbxLog_Full, False)
    QtBind.setChecked(gui, cbxExit, False)

def loadConfigs(fileName=""):
    loadDefaultConfig()
    if os.path.exists(getConfig(fileName)):
        data = {}
        with open(getConfig(fileName), "r") as f:
            data = json.load(f)
        QtBind.setText(gui, tbxProfileName, fileName)
        if "Enabled" in data and data['Enabled']:
            QtBind.setChecked(gui, cbxEnabled, True)
        if "SelectChar" in data and not data['SelectChar']:
            QtBind.setChecked(gui,cbxSelectChar,False)
        if "SelectChar2" in data and not data['SelectChar2']:
            QtBind.setChecked(gui,cbxSelectChar2,False)
        if "SelectChar3" in data and not data['SelectChar3']:
            QtBind.setChecked(gui,cbxSelectChar3,False)
        if "CreateChar" in data and not data['CreateChar']:
            QtBind.setChecked(gui, cbxCreateChar, False)
        if "DeleteChar" in data and not data['DeleteChar']:
            QtBind.setChecked(gui, cbxDeleteChar, False)
        if "SelectCharOnAcademy" in data and data['SelectCharOnAcademy']:
            QtBind.setChecked(gui, cbxSelectCharOnAcademy, True)
        if "Nickname" in data:
            QtBind.setText(gui, tbxNickname, data["Nickname"])
        if "Sequence" in data and data["Sequence"]:
            QtBind.setText(gui, tbxSequence, data["Sequence"])
        if "Race" in data:
            QtBind.setText(gui, cmbxRace, data["Race"])
        if "CMD" in data:
            QtBind.setText(gui, tbxCMD, data["CMD"])
        if "NotificationFull" in data and data['NotificationFull']:
            QtBind.setChecked(gui, cbxNotification_Full, True)
        if "SoundFull" in data and data['SoundFull']:
            QtBind.setChecked(gui, cbxNotification_Full, True)
        if "SoundFullPath" in data and data["SoundFullPath"]:
            QtBind.setText(gui, tbxSound_Full, data["SoundFullPath"])
        if "LogFull" in data and data['LogFull']:
            QtBind.setChecked(gui, cbxLog_Full, True)
        if "Exit" in data and data['Exit']:
            QtBind.setChecked(gui, cbxExit, True)

        return True
    return False


def saveConfigs(fileName=""):
    data = {}
    data["Enabled"] = QtBind.isChecked(gui, cbxEnabled)
    data["SelectChar"] = QtBind.isChecked(gui,cbxSelectChar)
    data["SelectChar2"] = QtBind.isChecked(gui,cbxSelectChar2)
    data["SelectChar3"] = QtBind.isChecked(gui,cbxSelectChar3)
    data["CreateChar"] = QtBind.isChecked(gui, cbxCreateChar)
    data["DeleteChar"] = QtBind.isChecked(gui, cbxDeleteChar)
    data["SelectCharOnAcademy"] = QtBind.isChecked(gui, cbxSelectCharOnAcademy)
    data["Nickname"] = QtBind.text(gui, tbxNickname)
    sequence = QtBind.text(gui, tbxSequence)
    if sequence.isnumeric():
        data["Sequence"] = sequence
    else:
        data["Sequence"] = str(SEQUENCE_DEFAULT_NUMBER)
        QtBind.setText(gui, tbxSequence, data["Sequence"])
    data["Race"] = QtBind.text(gui, cmbxRace)

    data["CMD"] = QtBind.text(gui, tbxCMD)
    data["NotificationFull"] = QtBind.isChecked(gui, cbxNotification_Full)
    data["SoundFull"] = QtBind.isChecked(gui, cbxSound_Full)
    data["SoundFullPath"] = QtBind.text(gui, tbxSound_Full)
    data["LogFull"] = QtBind.isChecked(gui, cbxLog_Full)
    data["Exit"] = QtBind.isChecked(gui, cbxExit)
    with open(getConfig(fileName), "w") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))

def btnSaveConfig_clicked():
    strConfigName = QtBind.text(gui, tbxProfileName)
    saveConfigs(strConfigName)
    if strConfigName:
        log('Eklenti: Profil [' + strConfigName + '] ayarları kaydedildi')
    else:
        log("Eklenti: Ayarlar kaydedildi")

def btnLoadConfig_clicked():
    strConfigName = QtBind.text(gui, tbxProfileName)
    if loadConfigs(strConfigName):
        if strConfigName:
            log("Eklenti: Profil [" + strConfigName + "] ayarları yüklendi")
        else:
            log("Eklenti: Ayarlar yüklendi")
    elif strConfigName:
        log("Eklenti: Profil [" + strConfigName + "] bulunamadı")

def CreateCharacter():
    race = QtBind.text(gui, cmbxRace)
    if race != 'EU':
        race = 'CH'

        model = get_monster_string('CHAR_CH_MAN_ADVENTURER')
        chest = get_item_string('ITEM_CH_M_CLOTHES_01_BA_A_DEF')
        legs = get_item_string('ITEM_CH_M_CLOTHES_01_LA_A_DEF')
        shoes = get_item_string('ITEM_CH_M_CLOTHES_01_FA_A_DEF')
        weapon = get_item_string('ITEM_CH_SWORD_01_A_DEF')
    else:
        race = 'EU'

        model = get_monster_string('CHAR_EU_MAN_NOBLE')
        chest = get_item_string('ITEM_EU_M_CLOTHES_01_BA_A_DEF')
        legs = get_item_string('ITEM_EU_M_CLOTHES_01_LA_A_DEF')
        shoes = get_item_string('ITEM_EU_M_CLOTHES_01_FA_A_DEF')
        weapon = get_item_string('ITEM_EU_TSTAFF_01_A_DEF')

    if not model or not chest or not legs or not shoes or not weapon:
        log('Eklenti: Hata, CodeName bu sunucuda değişti')
        return

    global isCreatingCharacter
    isCreatingCharacter = True
    log('Eklenti: Karakter oluşturuluyor [' + CreatingNickname + '] (' + race + ')')
    p = b'\x01'
    p += struct.pack('<H', len(CreatingNickname))
    p += CreatingNickname.encode('ascii')
    p += struct.pack('<I', model['model'])
    p += struct.pack('<B', 0)
    p += struct.pack('<I', chest['model'])
    p += struct.pack('<I', legs['model'])
    p += struct.pack('<I', shoes['model'])
    p += struct.pack('<I', weapon['model'])
    inject_joymax(0x7007, p, False)

    Timer(2.5, Inject_RequestCharacterList).start()

def Inject_RequestCharacterList():
    inject_joymax(0x7007, b'\x02', False)

def Inject_DeleteCharacter(charName):
    p = b'\x03'
    p += struct.pack('<H', len(charName))
    p += charName.encode('ascii')
    inject_joymax(0x7007, p, False)

def Inject_CheckName(charName):
    p = b'\x04'
    p += struct.pack('<H', len(charName))
    p += charName.encode('ascii')
    inject_joymax(0x7007, p, False)

def GetRandomNick():
    names = ["Aegon", "Aerys", "Aemon", "Aeron", "Alliser", "Areo", "Bran", "Bronn", "Benjen", "Brynden", "Beric",
             "Balon", "Bowen", "Craster", "Davos", "Daario", "Doran", "Darrik", "Dyron", "Eddard", "Edric", "Euron",
             "Edmure", "Gendry", "Gilly", "Gregor", "GreyWorm", "Hoster", "Jon", "Jaime", "Jorah", "Joffrey", "Jeor",
             "Jaqen", "Jojen", "Janos", "Kevan", "Khal", "Lancel", "Loras", "Maekar", "Mace", "Mance", "Nestor",
             "Oberyn", "Petyr", "Podrick", "Quentyn", "Robert", "Robb", "Ramsay", "Roose", "Rickon", "Rickard",
             "Rhaegar", "Renly", "Rodrik", "Randyll", "Samwell", "Sandor", "Stannis", "Stefon", "Tywin", "Tyrion",
             "Theon", "Tormund", "Trystane", "Tommen", "Val", "Varys", "Viserys", "Victarion", "Vimar", "Walder",
             "Wyman", "Yoren", "Yohn", "Zane"]
    name = names[random.randint(0, len(names) - 1)]
    if len(name) < 12:
        maxWidth = 12 - len(name)
        if maxWidth > 4:
            maxWidth = 4
        numbers = pow(10, maxWidth) - 1
        name = str(name) + (str(random.randint(0, numbers))).zfill(maxWidth)
    return name

def GetSequence():
    sequence = QtBind.text(gui, tbxSequence)
    if sequence.isnumeric():
        sequence = int(sequence)
    else:
        sequence = SEQUENCE_DEFAULT_NUMBER

    QtBind.setText(gui, tbxSequence, str(sequence + 1))
    saveConfigs(QtBind.text(gui, tbxProfileName))

    return sequence

def GetNickSequence(nickname):
    seq = str(GetSequence())
    nick = nickname + seq
    nickLength = len(nick)
    if nickLength > 12:
        nickLength -= 12
        nick = nickname[:-nickLength] + seq
    return nick

def createNickname():
    global CreatingNickname
    customName = QtBind.text(gui, tbxNickname)
    if customName:
        CreatingNickname = GetNickSequence(customName)
    else:
        CreatingNickname = GetRandomNick()
    log("Eklenti: Takma ad kontrol ediliyor [" + CreatingNickname + "]")
    Inject_CheckName(CreatingNickname)

def KillBot():
    log("Eklenti: Bot kapatılıyor...")
    os.kill(os.getpid(), 9)

def RestartBotWithCommandLine():
    global isRestarted
    if isRestarted:
        return
    isRestarted = True
    cmd = ' '.join(get_command_line_args())
    subprocess.Popen(cmd)
    log("Eklenti: Botunuz 5 saniye içinde kapatılacak..")
    Timer(5.0, KillBot).start()

def handle_joymax(opcode, data):
    if opcode == 0xB007 and QtBind.isChecked(gui, cbxEnabled):
        locale = get_locale()
        try:
            global isCreatingCharacter, isDeletingCharacter
            index = 0
            action = data[index]
            index += 1
            success = data[index]
            index += 1
            if action == 1:
                if isCreatingCharacter:
                    isCreatingCharacter = False
                    if success == 1:
                        log("Eklenti: Karakter başarıyla oluşturuldu!")
                    else:
                        log("Eklenti: Karakter oluşturma başarısız oldu")
            elif action == 3:
                if isDeletingCharacter:
                    isDeletingCharacter = False
                    if success == 1:
                        log("Eklenti: Karakter başarıyla silindi!")
                    else:
                        log("Eklenti: Karakter silme başarısız oldu")
            elif action == 4:
                if isCreatingCharacter:
                    if success == 1:
                        log("Eklenti: Takma ad kullanılabilir!")
                        CreateCharacter()
                    else:
                        log("Eklenti: Takma ad zaten alınmış!")
                        Timer(1.0, createNickname).start()
            elif action == 2:
                if success == 1:
                    charList = []
                    nChars = data[index]
                    index += 1
                    log("Eklenti: TR_xAcademy karakter listesi: " + ("Yok" if not nChars else ""))
                    for i in range(nChars):
                        character = {}
                        character['model_id'] = struct.unpack_from('<I', data, index)[0]
                        index += 4
                        charLength = struct.unpack_from('<H', data, index)[0]
                        index += 2
                        character['name'] = struct.unpack_from('<' + str(charLength) + 's', data, index)[0].decode(
                            'cp1252')
                        index += charLength

                        if locale == 18 or locale == 54 or locale == 56 or locale == 59 or locale == 61 or locale == 65:
                            index += 2 + struct.unpack_from('<H', data, index)[0]

                        index += 1
                        character['level'] = data[index]
                        index += 1
                        index += 8
                        index += 2
                        index += 2
                        index += 2

                        if locale == 18 or locale == 54 or locale == 56 or locale == 59 or locale == 61 or locale == 65:
                            index += 4

                        index += 4
                        index += 4

                        if locale == 18 or locale == 54 or locale == 56 or locale == 59 or locale == 61 or locale == 65:
                            index += 2

                        character['is_deleting'] = data[index]
                        index += 1

                        if locale == 18 or locale == 54 or locale == 56 or locale == 59 or locale == 61 or locale == 65:
                            index += 4

                        if character['is_deleting']:
                            minutesLeft = struct.unpack_from('<I', data, index)[0]
                            character['deleted_at'] = datetime.now() + timedelta(minutes=minutesLeft)
                            index += 4

                        index += 1
                        if data[index]:
                            index += 1
                            strLength = struct.unpack_from('<H', data, index)[0]
                            index += (2 + strLength)
                        else:
                            index += 1

                        character['academy_type'] = data[index]
                        index += 1
                        forCount = data[index]
                        index += 1
                        for j in range(forCount):
                            index += 4
                            index += 1
                        forCount = data[index]
                        index += 1
                        for j in range(forCount):
                            index += 4
                            index += 1

                        charList.append(character)
                        log(str(i + 1) + ") " + character['name'] + " (Lv." + str(
                            character['level']) + ")" + (" [* " + character['deleted_at'].strftime('%H:%M %d/%m/%Y') +
                                                       "]" if character['is_deleting'] else ""))

                    if locale == 18 or locale == 54 or locale == 56 or locale == 59 or locale == 61 or locale == 65:
                        index += 1

                    try:
                        if i == (nChars - 1):
                            data[index]
                            log("Eklenti: [Uyarı] Paket kısmen ayrıştırıldı.")
                    except:
                        try:
                            data[index - 1]
                        except:
                            log("Eklenti: [Uyarı] Paket kısmen ayrıştırıldı.")

                    try:
                        OnCharacterList(charList)
                    except Exception as innerEx:
                        log("Eklenti: " + str(innerEx))
        except Exception as ex:
            log("Eklenti: Hata [" + str(ex) + "] - " + pName + " bu sunucuda çalışmıyor!")
            log("Desteğe ihtiyacınız varsa, lütfen bana tüm bunları özel mesaj yoluyla gönderin:")
            log("Veri [" + ("Yok" if not data else ' '.join('{:02X}'.format(x) for x in data)) + "] Yerel [" + str(locale) + "]")
    return True


def OnCharacterList(CharList):
    for character in CharList:
        if not character['is_deleting']:
            charName = character['name']
            charLevel = character['level']
            charAcademyType = character['academy_type']

            if charLevel >= 40 and charLevel <= 50 and charAcademyType != 0:
                if QtBind.isChecked(gui, cbxSelectCharOnAcademy):
                    log("Eklenti: Karakter seçiliyor [" + charName + "] (Hala Akademide)")
                    select_character(charName)
                    return

            if charLevel >= 40 and charLevel <= 50:
                if QtBind.isChecked(gui, cbxDeleteChar):
                    global isDeletingCharacter
                    isDeletingCharacter = True
                    log("Eklenti: Karakter siliniyor [" + charName + "] (40 ile 50 seviye arasında)")
                    Inject_DeleteCharacter(charName)
                    Timer(3.0, Inject_RequestCharacterList).start()
                    return

            if charLevel < 40:
                if QtBind.isChecked(gui,cbxSelectChar):
                    log("Eklenti: Karakter Seçildi ["+charName+"] (Seviye 40ın Altında)")
                    select_character(charName)
                    return
            if charLevel < 29:
                if QtBind.isChecked(gui,cbxSelectChar2):
                    log("Eklenti: Karakter Seçildi ["+charName+"] (Seviye 29ın Altında)")
                    select_character(charName)
                    return
            if charLevel < 20:
                if QtBind.isChecked(gui,cbxSelectChar3):
                    log("Eklenti: Karakter Seçildi ["+charName+"] (Seviye 20ın Altında)")
                    select_character(charName)
                    return

    if len(CharList) < 4:
        if QtBind.isChecked(gui, cbxCreateChar):
            global isCreatingCharacter
            isCreatingCharacter = True
            Timer(3.0, createNickname).start()
    else:
        errMessage = "Eklenti: Yeni bir karakter oluşturmak için yeterli alan yok!"
        log(errMessage)

        cmd = QtBind.text(gui, tbxCMD)
        if cmd:
            log("Eklenti: Komut yürütülmeye çalışılıyor [" + cmd + "]")
            subprocess.Popen(cmd)

        if QtBind.isChecked(gui, cbxNotification_Full):
            show_notification(pName + ' v' + pVersion, errMessage)

        if QtBind.isChecked(gui, cbxSound_Full):
            try:
                path = QtBind.text(gui, tbxSound_Full)
                play_wav(path if path else NOTIFICATION_SOUND_PATH)
            except:
                pass

        if QtBind.isChecked(gui, cbxLog_Full):
            from datetime import datetime
            logText = datetime.now().strftime('%m/%d/%Y - %H:%M:%S') + ': ' + errMessage
            profileName = QtBind.text(gui, tbxProfileName)
            logText += '\nKullanılan Profil: ' + (profileName if profileName else 'Yok')
            with open(getPath() + '_log.txt', 'a') as f:
                f.write(logText)

        if QtBind.isChecked(gui, cbxExit):
            log("Eklenti: Botunuz 5 saniye içinde kapatılacak..")
            Timer(5.0, KillBot).start()

log('Eklenti: ' + pName + ' başarıyla yüklendi')

if os.path.exists(getPath()):
    useDefaultConfig = True
    bot_args = get_command_line_args()
    if bot_args:
        for i in range(len(bot_args)):
            param = bot_args[i].lower()
            if param.startswith('-xacademy-config='):
                configName = param[17:]
                if loadConfigs(configName):
                    log("Eklenti: " + pName + " profili [" + configName + "] komut satırından yüklendi")
                    useDefaultConfig = False
                else:
                    log("Eklenti: " + pName + " profili [" + configName + "] bulunamadı")
                break
    if useDefaultConfig:
        loadConfigs()

else:
    loadDefaultConfig()
    os.makedirs(getPath())
    log('Eklenti: "' + pName + '" klasörü oluşturuldu')