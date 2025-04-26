from phBot import *
from threading import Timer
import random
import struct
import os
import sqlite3
import json
import QtBind
from time import sleep

pName = 'TR_xAutoDungeon'

DIMENSIONAL_COOLDOWN_DELAY = 7200
WAIT_DROPS_DELAY_MAX = 10
COUNT_MOBS_DELAY = 1.0

character_data = None
itemUsedByPlugin = None
dimensionalItemActivated = None

gui = QtBind.init(__name__, pName)

lblMobs = QtBind.createLabel(gui, '#   Yok Sayılacak Mob\'ları Ekleyin.    #\n#          Canavar Sayacından         #', 31, 6)
tbxMobs = QtBind.createLineEdit(gui, "", 31, 35, 100, 20)
lstMobs = QtBind.createList(gui, 31, 56, 176, 203)
lstMobsData = []
btnAddMob = QtBind.createButton(gui, 'btnAddMob_clicked', "    Ekle    ", 132, 34)
btnRemMob = QtBind.createButton(gui, 'btnRemMob_clicked', "     Kaldır     ", 80, 258)

lblMonsterCounter = QtBind.createLabel(gui, "#                 Canavar Sayacı                 #", 520, 6)
lstMonsterCounter = QtBind.createList(gui, 520, 23, 197, 237)
QtBind.append(gui, lstMonsterCounter, 'Ad (Tip)')

lblPreferences = QtBind.createLabel(gui, "#             Canavar Sayacı Tercihleri            #", 240, 6)
lstIgnore = []
lstOnlyCount = []

_y = 26
lblGeneral = QtBind.createLabel(gui, 'Genel (0)', 240, _y)
cbxIgnoreGeneral = QtBind.createCheckBox(gui, 'cbxIgnoreGeneral_clicked', 'Yoksay', 345, _y)
cbxOnlyCountGeneral = QtBind.createCheckBox(gui, 'cbxOnlyCountGeneral_clicked', 'Sadece Say', 405, _y)
_y += 20
lblChampion = QtBind.createLabel(gui, 'Şampiyon (1)', 240, _y)
cbxIgnoreChampion = QtBind.createCheckBox(gui, 'cbxIgnoreChampion_clicked', 'Yoksay', 345, _y)
cbxOnlyCountChampion = QtBind.createCheckBox(gui, 'cbxOnlyCountChampion_clicked', 'Sadece Say', 405, _y)
_y += 20
lblGiant = QtBind.createLabel(gui, 'Giant (4)', 240, _y)
cbxIgnoreGiant = QtBind.createCheckBox(gui, 'cbxIgnoreGiant_clicked', 'Yoksay', 345, _y)
cbxOnlyCountGiant = QtBind.createCheckBox(gui, 'cbxOnlyCountGiant_clicked', 'Sadece Say', 405, _y)
_y += 20
lblTitan = QtBind.createLabel(gui, 'Titan (5)', 240, _y)
cbxIgnoreTitan = QtBind.createCheckBox(gui, 'cbxIgnoreTitan_clicked', 'Yoksay', 345, _y)
cbxOnlyCountTitan = QtBind.createCheckBox(gui, 'cbxOnlyCountTitan_clicked', 'Sadece Say', 405, _y)
_y += 20
lblStrong = QtBind.createLabel(gui, 'Güçlü (6)', 240, _y)
cbxIgnoreStrong = QtBind.createCheckBox(gui, 'cbxIgnoreStrong_clicked', 'Yoksay', 345, _y)
cbxOnlyCountStrong = QtBind.createCheckBox(gui, 'cbxOnlyCountStrong_clicked', 'Sadece Say', 405, _y)
_y += 20
lblElite = QtBind.createLabel(gui, 'Elit (7)', 240, _y)
cbxIgnoreElite = QtBind.createCheckBox(gui, 'cbxIgnoreElite_clicked', 'Yoksay', 345, _y)
cbxOnlyCountElite = QtBind.createCheckBox(gui, 'cbxOnlyCountElite_clicked', 'Sadece Say', 405, _y)
_y += 20
lblUnique = QtBind.createLabel(gui, 'Unique (8)', 240, _y)
cbxIgnoreUnique = QtBind.createCheckBox(gui, 'cbxIgnoreUnique_clicked', 'Yoksay', 345, _y)
cbxOnlyCountUnique = QtBind.createCheckBox(gui, 'cbxOnlyCountUnique_clicked', 'Sadece Say', 405, _y)
_y += 20
lblParty = QtBind.createLabel(gui, 'Genel Parti (16)', 240, _y)
cbxIgnoreParty = QtBind.createCheckBox(gui, 'cbxIgnoreParty_clicked', 'Yoksay', 345, _y)
cbxOnlyCountParty = QtBind.createCheckBox(gui, 'cbxOnlyCountParty_clicked', 'Sadece Say', 405, _y)
_y += 20
lblChampionParty = QtBind.createLabel(gui, 'Şampiyon Parti (17)', 240, _y)
cbxIgnoreChampionParty = QtBind.createCheckBox(gui, 'cbxIgnoreChampionParty_clicked', 'Yoksay', 345, _y)
cbxOnlyCountChampionParty = QtBind.createCheckBox(gui, 'cbxOnlyCountChampionParty_clicked', 'Sadece Say', 405, _y)
_y += 20
lblGiantParty = QtBind.createLabel(gui, 'Giant Parti (20)', 240, _y)
cbxIgnoreGiantParty = QtBind.createCheckBox(gui, 'cbxIgnoreGiantParty_clicked', 'Yoksay', 345, _y)
cbxOnlyCountGiantParty = QtBind.createCheckBox(gui, 'cbxOnlyCountGiantParty_clicked', 'Sadece Say', 405, _y)

_y += 30
cbxAcceptForgottenWorld = QtBind.createCheckBox(gui, 'cbxAcceptForgottenWorld_checked', 'Unutulmuş Dünya davetlerini kabul et', 240, _y)

def cbxIgnoreGeneral_clicked(checked):
    Checkbox_Checked(checked, "lstIgnore", 0)

def cbxOnlyCountGeneral_clicked(checked):
    Checkbox_Checked(checked, "lstOnlyCount", 0)

def cbxIgnoreChampion_clicked(checked):
    Checkbox_Checked(checked, "lstIgnore", 1)

def cbxOnlyCountChampion_clicked(checked):
    Checkbox_Checked(checked, "lstOnlyCount", 1)

def cbxIgnoreGiant_clicked(checked):
    Checkbox_Checked(checked, "lstIgnore", 4)

def cbxOnlyCountGiant_clicked(checked):
    Checkbox_Checked(checked, "lstOnlyCount", 4)

def cbxIgnoreTitan_clicked(checked):
    Checkbox_Checked(checked, "lstIgnore", 5)

def cbxOnlyCountTitan_clicked(checked):
    Checkbox_Checked(checked, "lstOnlyCount", 5)

def cbxIgnoreStrong_clicked(checked):
    Checkbox_Checked(checked, "lstIgnore", 6)

def cbxOnlyCountStrong_clicked(checked):
    Checkbox_Checked(checked, "lstOnlyCount", 6)

def cbxIgnoreElite_clicked(checked):
    Checkbox_Checked(checked, "lstIgnore", 7)

def cbxOnlyCountElite_clicked(checked):
    Checkbox_Checked(checked, "lstOnlyCount", 7)

def cbxIgnoreUnique_clicked(checked):
    Checkbox_Checked(checked, "lstIgnore", 8)

def cbxOnlyCountUnique_clicked(checked):
    Checkbox_Checked(checked, "lstOnlyCount", 8)

def cbxIgnoreParty_clicked(checked):
    Checkbox_Checked(checked, "lstIgnore", 16)

def cbxOnlyCountParty_clicked(checked):
    Checkbox_Checked(checked, "lstOnlyCount", 16)

def cbxIgnoreChampionParty_clicked(checked):
    Checkbox_Checked(checked, "lstIgnore", 17)

def cbxOnlyCountChampionParty_clicked(checked):
    Checkbox_Checked(checked, "lstOnlyCount", 17)

def cbxIgnoreGiantParty_clicked(checked):
    Checkbox_Checked(checked, "lstIgnore", 20)

def cbxOnlyCountGiantParty_clicked(checked):
    Checkbox_Checked(checked, "lstOnlyCount", 20)

def cbxAcceptForgottenWorld_checked(checked):
    saveConfigs()

def Checkbox_Checked(checked, gListName, mobType):
    gListReference = globals()[gListName]
    if checked:
        gListReference.append(mobType)
    else:
        gListReference.remove(mobType)
    saveConfigs()

def getPath():
    return get_config_dir() + pName + "\\"

def getConfig():
    return getPath() + character_data['server'] + "_" + character_data['name'] + ".json"

def loadDefaultConfig():
    global lstMobsData, lstIgnore, lstOnlyCount
    lstMobsData = []
    QtBind.clear(gui, lstMobs)
    lstIgnore = []
    QtBind.setChecked(gui, cbxIgnoreGeneral, False)
    QtBind.setChecked(gui, cbxIgnoreChampion, False)
    QtBind.setChecked(gui, cbxIgnoreGiant, False)
    QtBind.setChecked(gui, cbxIgnoreTitan, False)
    QtBind.setChecked(gui, cbxIgnoreStrong, False)
    QtBind.setChecked(gui, cbxIgnoreElite, False)
    QtBind.setChecked(gui, cbxIgnoreUnique, False)
    QtBind.setChecked(gui, cbxIgnoreParty, False)
    QtBind.setChecked(gui, cbxIgnoreChampionParty, False)
    QtBind.setChecked(gui, cbxIgnoreGiantParty, False)
    lstOnlyCount = []
    QtBind.setChecked(gui, cbxOnlyCountGeneral, False)
    QtBind.setChecked(gui, cbxOnlyCountChampion, False)
    QtBind.setChecked(gui, cbxOnlyCountGiant, False)
    QtBind.setChecked(gui, cbxOnlyCountTitan, False)
    QtBind.setChecked(gui, cbxOnlyCountStrong, False)
    QtBind.setChecked(gui, cbxOnlyCountElite, False)
    QtBind.setChecked(gui, cbxOnlyCountUnique, False)
    QtBind.setChecked(gui, cbxOnlyCountParty, False)
    QtBind.setChecked(gui, cbxOnlyCountChampionParty, False)
    QtBind.setChecked(gui, cbxOnlyCountGiantParty, False)
    QtBind.setChecked(gui, cbxAcceptForgottenWorld, False)

def loadConfigs():
    loadDefaultConfig()
    if isJoined() and os.path.exists(getConfig()):
        data = {}
        with open(getConfig(), "r") as f:
            data = json.load(f)
        if "Ignore Names" in data:
            global lstMobsData
            lstMobsData = data["Ignore Names"]
            for name in lstMobsData:
                QtBind.append(gui, lstMobs, name)

        if "Ignore Types" in data:
            global lstIgnore
            for t in data["Ignore Types"]:
                if t == 8:
                    QtBind.setChecked(gui, cbxIgnoreUnique, True)
                elif t == 7:
                    QtBind.setChecked(gui, cbxIgnoreElite, True)
                elif t == 6:
                    QtBind.setChecked(gui, cbxIgnoreStrong, True)
                elif t == 5:
                    QtBind.setChecked(gui, cbxIgnoreTitan, True)
                elif t == 4:
                    QtBind.setChecked(gui, cbxIgnoreGiant, True)
                elif t == 1:
                    QtBind.setChecked(gui, cbxIgnoreChampion, True)
                elif t == 0:
                    QtBind.setChecked(gui, cbxIgnoreGeneral, True)
                elif t == 16:
                    QtBind.setChecked(gui, cbxIgnoreParty, True)
                elif t == 17:
                    QtBind.setChecked(gui, cbxIgnoreChampionParty, True)
                elif t == 20:
                    QtBind.setChecked(gui, cbxIgnoreGiantParty, True)
                else:
                    continue
                lstIgnore.append(t)

        if "OnlyCount Types" in data:
            global lstOnlyCount
            for t in data["OnlyCount Types"]:
                if t == 8:
                    QtBind.setChecked(gui, cbxOnlyCountUnique, True)
                elif t == 7:
                    QtBind.setChecked(gui, cbxOnlyCountElite, True)
                elif t == 6:
                    QtBind.setChecked(gui, cbxOnlyCountStrong, True)
                elif t == 5:
                    QtBind.setChecked(gui, cbxOnlyCountTitan, True)
                elif t == 4:
                    QtBind.setChecked(gui, cbxOnlyCountGiant, True)
                elif t == 1:
                    QtBind.setChecked(gui, cbxOnlyCountChampion, True)
                elif t == 0:
                    QtBind.setChecked(gui, cbxOnlyCountGeneral, True)
                elif t == 16:
                    QtBind.setChecked(gui, cbxOnlyCountParty, True)
                elif t == 17:
                    QtBind.setChecked(gui, cbxOnlyCountChampionParty, True)
                elif t == 20:
                    QtBind.setChecked(gui, cbxOnlyCountGiantParty, True)
                else:
                    continue
                lstOnlyCount.append(t)

        if 'Accept ForgottenWorld' in data and data['Accept ForgottenWorld']:
            QtBind.setChecked(gui, cbxAcceptForgottenWorld, True)

def saveConfigs():
    if isJoined():
        data = {}
        data['OnlyCount Types'] = lstOnlyCount
        data['Ignore Types'] = lstIgnore
        data['Ignore Names'] = lstMobsData
        data['Accept ForgottenWorld'] = QtBind.isChecked(gui, cbxAcceptForgottenWorld)
        with open(getConfig(), "w") as f:
            f.write(json.dumps(data, indent=4, sort_keys=True))

def isJoined():
    global character_data
    character_data = get_character_data()
    if not (character_data and "name" in character_data and character_data["name"]):
        character_data = None
    return character_data

def btnAddMob_clicked():
    global lstMobsData
    text = QtBind.text(gui, tbxMobs)
    if text and not ListContains(text, lstMobsData):
        lstMobsData.append(text)
        QtBind.append(gui, lstMobs, text)
        QtBind.setText(gui, tbxMobs, "")
        saveConfigs()
        log('TR_xAutoDungeon: Canavar eklendi [' + text + ']')

def btnRemMob_clicked():
    global lstMobsData
    selected = QtBind.text(gui, lstMobs)
    if selected:
        lstMobsData.remove(selected)
        QtBind.remove(gui, lstMobs, selected)
        saveConfigs()
        log('TR_xAutoDungeon: Canavar kaldırıldı [' + selected + ']')

def ListContains(text, lst):
    text = text.lower()
    for i in range(len(lst)):
        if lst[i].lower() == text:
            return True
    return False

def QtBind_ItemsContains(text, lst):
    return ListContains(text, QtBind.getItems(gui, lst))

def AttackMobs(wait, isAttacking, position, radius):
    count = getMobCount(position, radius)
    if count > 0:
        if not isAttacking:
            start_bot()
            log("TR_xAutoDungeon: Bu alandaki (" + str(count) + ") canavarı öldürmeye başlanıyor. Yarıçap: " + (str(radius) if radius != None else "Maks."))
        Timer(wait, AttackMobs, [wait, True, position, radius]).start()
    else:
        log("TR_xAutoDungeon: Tüm canavarlar öldürüldü!")
        conn = GetFilterConnection()
        cursor = conn.cursor()
        WaitPickableDrops(cursor)
        conn.close()
        stop_bot()
        set_training_position(0, 0, 0, 0)
        log("TR_xAutoDungeon: Scripte geri dönülüyor...")
        Timer(2.5, move_to, [position['x'], position['y'], position['z']]).start()
        Timer(5.0, start_bot).start()

def getMobCount(position, radius):
    QtBind.clear(gui, lstMonsterCounter)
    QtBind.append(gui, lstMonsterCounter, 'Ad (Tip)')
    count = 0
    p = position if radius != None else None
    monsters = get_monsters()
    if monsters:
        for key, mob in monsters.items():
            if mob['type'] in lstIgnore:
                continue
            if len(lstOnlyCount) > 0:
                if not mob['type'] in lstOnlyCount:
                    continue
            elif ListContains(mob['name'], lstMobsData):
                continue
            if radius != None:
                if round(GetDistance(p['x'], p['y'], mob['x'], mob['y']), 2) > radius:
                    continue
            QtBind.append(gui, lstMonsterCounter, mob['name'] + ' (' + str(mob['type']) + ')')
            count += 1
    return count

def GetDistance(ax, ay, bx, by):
    return ((bx - ax) ** 2 + (by - ay) ** 2) ** (0.5)

def GetFilterConnection():
    path = get_config_dir() + character_data['server'] + '_' + character_data['name'] + '.db3'
    return sqlite3.connect(path)

def IsPickable(filterCursor, ItemID):
    return filterCursor.execute('SELECT EXISTS(SELECT 1 FROM pickfilter WHERE id=? AND pick=1 LIMIT 1)', (ItemID,)).fetchone()[0]

def WaitPickableDrops(filterCursor, waiting=0):
    if waiting >= WAIT_DROPS_DELAY_MAX:
        log("TR_xAutoDungeon: Düşenleri toplamak için zaman aşımı!")
        return
    drops = get_drops()
    if drops:
        drop = None
        for key in drops:
            value = drops[key]
            if IsPickable(filterCursor, value['model']):
                drop = value
                break
        if drop:
            log('TR_xAutoDungeon: "' + drop['name'] + '" toplamak bekleniyor...')
            sleep(1.0)
            WaitPickableDrops(filterCursor, waiting + 1)

def GetDimensionalHole(Name):
    searchByName = Name != ''
    items = get_inventory()['items']
    for slot, item in enumerate(items):
        if item:
            match = False
            if searchByName:
                match = (Name == item['name'])
            else:
                itemData = get_item(item['model'])
                match = (itemData['tid1'] == 3 and itemData['tid2'] == 12 and itemData['tid3'] == 7)

            if match:
                item['slot'] = slot
                return item
    return None

def GetDimensionalPillarUID(Name):
    npcs = get_npcs()
    if npcs:
        for uid, npc in npcs.items():
            item = get_item(npc['model'])
            if item and item['name'] == Name:
                return uid
    return 0

def EnterToDimensional(Name):
    uid = GetDimensionalPillarUID(Name)
    if uid:
        log('TR_xAutoDungeon: Boyutsal delik seçiliyor...')
        packet = struct.pack('I', uid)
        inject_joymax(0x7045, packet, False)
        sleep(1.0)
        log('TR_xAutoDungeon: Boyutsal deliğe giriliyor...')
        inject_joymax(0x704B, packet, False)
        packet += struct.pack('H', 3)
        inject_joymax(0x705A, packet, False)
        Timer(5.0, start_bot).start()
        return
    log('TR_xAutoDungeon: "' + Name + '" yakınınızda bulunamadı!')

def GoDimensionalThread(Name):
    if dimensionalItemActivated:
        Name = dimensionalItemActivated['name']
        log('TR_xAutoDungeon: ' + ('"' + Name + '"' if Name else 'Boyutsal Delik') + ' hala açık!')
        EnterToDimensional(Name)
        return
    item = GetDimensionalHole(Name)
    if item:
        log('TR_xAutoDungeon: "' + item['name'] + '" kullanılıyor...')
        p = struct.pack('B', item['slot'])
        locale = get_locale()
        if locale == 56 or locale == 18:
            p += b'\x30\x0C\x0C\x07'
        else:
            p += b'\x6C\x3E'
        global itemUsedByPlugin
        itemUsedByPlugin = item
        inject_joymax(0x704C, p, True)
    else:
        log('TR_xAutoDungeon: ' + ('"' + Name + '"' if Name else 'Boyutsal Delik') + ' envanterinizde bulunamadı')

def AttackArea(args):
    radius = None
    if len(args) >= 2:
        radius = round(float(args[1]), 2)
    p = get_position()
    if getMobCount(p, radius) > 0:
        stop_bot()
        set_training_position(p['region'], p['x'], p['y'], p['z'])
        if radius != None:
            set_training_radius(radius)
        else:
            set_training_radius(100.0)
        Timer(0.001, AttackMobs, [COUNT_MOBS_DELAY, False, p, radius]).start()
    else:
        log("TR_xAutoDungeon: Bu alanda canavar yok. Menzil: " + (str(radius) if radius != None else "Maks."))
    return 0

def GoDimensional(args):
    stop_bot()
    name = ''
    if len(args) > 1:
        name = args[1]
    Timer(0.001, GoDimensionalThread, [name]).start()
    return 0

def joined_game():
    loadConfigs()

def handle_joymax(opcode, data):
    global itemUsedByPlugin, dimensionalItemActivated
    if opcode == 0x751A:
        if QtBind.isChecked(gui, cbxAcceptForgottenWorld):
            packet = data[:4]
            packet += b'\x00\x00\x00\x00'
            packet += b'\x01'
            inject_joymax(0x751C, packet, False)
            log('Plugin: Forgotten World daveti kabul edildi!')

    elif opcode == 0xB04C:
        global itemUsedByPlugin
        if itemUsedByPlugin:
            if data[0] == 1:
                log('TR_xAutoDungeon: "' + itemUsedByPlugin['name'] + '" açıldı')
                global dimensionalItemActivated
                dimensionalItemActivated = itemUsedByPlugin

                def DimensionalCooldown():
                    global dimensionalItemActivated
                    dimensionalItemActivated = None
                Timer(DIMENSIONAL_COOLDOWN_DELAY, DimensionalCooldown).start()
                Timer(1.0, EnterToDimensional, [item_name]).start()
            else:
                log(f'Plugin: "{item_name}" açılamadı veya başka bir sorun oluştu.')
            itemUsedByPlugin = None
        return True
    elif opcode == 0xB05A:
        if len(data) > 2 and data[0] == 2 and data[1] == 39 and data[2] == 28:
            log("Plugin: Boyut kapısına girilemiyor. (muhtemelen dolu). Bot Başlatıldı.")
            start_bot()
        return True

log('Eklenti: ' + pName + ' başarıyla yüklendi')

if os.path.exists(getPath()):
    try:
        loadConfigs()
    except:
        log('TR_xAutoDungeon: ' + pName + ' config dosyası yüklenirken hata oluştu')
else:
    os.makedirs(getPath())
    log('TR_xAutoDungeon: ' + pName + ' klasörü oluşturuldu')