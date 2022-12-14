from phBot import *
from threading import Timer
from time import sleep
import phBotChat
import QtBind
import struct
import random
import json
import os
import time

pName = 'xEşyaBildir'

# ______________________________ Initializing ______________________________ #

# Graphic user interface
gui = QtBind.init(__name__, pName)

tbxLeaders = QtBind.createLineEdit(gui,"",525,10,110,20)
lstLeaders = QtBind.createList(gui,525,32,110,70)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked',"    Ekle   ",635,9)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked',"     Sil     ",635,32)
metaby = QtBind.createLabel(gui,'edited by hakankahya',575,270)
QtBind.createLabel(gui,'Tüm parti envanterinizi kontrol etmek için ekli liderden komutlar yazın',12,12)
QtBind.createLabel(gui, '- ENV : Envanterin boş yuvasını bildirir.\n- GOLD : Şuanki Altını Bildirir.\n- EXP : Şuanki LV , EXP ve SP bildirir.\n- JOBEXP : JOB EXP bildirir.\n- POUCH : Meslek kesesini bildirir.(Uzmanlik)\n- LAMP : Envanterdeki Lambaları bildirir.\n- SOX : Envanter, Pet ve Deponuzdaki sox ögelerini bildirir.(Kuşanmişlar hariç)\n- FLOWER : Envanter ve Deponuzdaki çiçegi bildirir.\n- ICE : Envanterinizdeki dondurma(event)bildirir.\n- PANDORA : Envanter, Pet ve Deponuzdaki Pandora Kutusunu bildirir.\n- MS : Envanter, Pet ve Deponuzdaki MSS Bildirir.\n- LUCK : Envanter, Pet ve Deponuzdaki Lucky Stoneleri bildirir.\n- STEADY : Envanter, Pet ve Deponuzdaki Stedy Stoneleri Bildirir.\n- ELIXIR : Envanter, Pet ve Deponuzdaki toplam Elixir miktarını bildirir.\n- BLUESTONE : Envanter, Pet ve Deponuzdaki toplam Blue Stone miktarını bildirir.\n- BLUESTONE2 : Envanter, Pet ve Deponuzdaki toplam Blue Stone miktarını bildirir.\n- STATSTONE : Envanter, Pet ve Deponuzdaki toplam Stat Stone miktarını bildirir.\n- STATSTONE2 : Envanter, Pet ve Deponuzdaki toplam Stat Stone miktarını bildirir.', 15, 45)


# ______________________________ Methods ______________________________ #

# Return xControl folder path
def getPath():
    return get_config_dir() + pName + "\\"


# Return character configs path (JSON)
def getConfig():
    return getPath() + inGame['server'] + "_" + inGame['name'] + ".json"


# Check if character is ingame
def isJoined():
    global inGame
    inGame = get_character_data()
    if not (inGame and "name" in inGame and inGame["name"]):
        inGame = None
    return inGame


# Load default configs
def loadDefaultConfig():
    # Clear data
    QtBind.clear(gui, lstLeaders)


# Loads all config previously saved
def loadConfigs():
    loadDefaultConfig()
    if isJoined():
        # Check config exists to load
        if os.path.exists(getConfig()):
            data = {}
            with open(getConfig(), "r") as f:
                data = json.load(f)
            if "Leaders" in data:
                for nickname in data["Leaders"]:
                    QtBind.append(gui, lstLeaders, nickname)

# Add leader to the list
def btnAddLeader_clicked():
    if inGame:
        player = QtBind.text(gui, tbxLeaders)
        # Player nickname it's not empty
        if player and not lstLeaders_exist(player):
            # Init dictionary
            data = {}
            # Load config if exist
            if os.path.exists(getConfig()):
                with open(getConfig(), 'r') as f:
                    data = json.load(f)
            # Add new leader
            if not "Leaders" in data:
                data['Leaders'] = []
            data['Leaders'].append(player)

            # Replace configs
            with open(getConfig(), "w") as f:
                f.write(json.dumps(data, indent=4, sort_keys=True))
            QtBind.append(gui, lstLeaders, player)
            QtBind.setText(gui, tbxLeaders, "")
            log('Plugin: Lider Eklendi. [' + player + ']')


# Remove leader selected from list
def btnRemLeader_clicked():
    if inGame:
        selectedItem = QtBind.text(gui, lstLeaders)
        if selectedItem:
            if os.path.exists(getConfig()):
                data = {"Leaders": []}
                with open(getConfig(), 'r') as f:
                    data = json.load(f)
                try:
                    # remove leader nickname from file if exists
                    data["Leaders"].remove(selectedItem)
                    with open(getConfig(), "w") as f:
                        f.write(json.dumps(data, indent=4, sort_keys=True))
                except:
                    pass  # just ignore file if doesn't exist
            QtBind.remove(gui, lstLeaders, selectedItem)
            log('Plugin: Lider Silindi. [' + selectedItem + ']')


# Return True if nickname exist at the leader list
def lstLeaders_exist(nickname):
    nickname = nickname.lower()
    players = QtBind.getItems(gui, lstLeaders)
    for i in range(len(players)):
        if players[i].lower() == nickname:
            return True
    return False


def handleChatCommand(msg):
    # Try to split message
    args = msg.split(' ', 1)
    # Check if the format is correct and is not empty
    if len(args) != 2 or not args[0] or not args[1]:
        return
    # Split correctly the message
    t = args[0].lower()
    if t == 'private' or t == 'note':
        # then check message is not empty
        argsExtra = args[1].split(' ', 1)
        if len(argsExtra) != 2 or not argsExtra[0] or not argsExtra[1]:
            return
        args.pop(1)
        args += argsExtra
    # Check message type
    sent = False
    if t == "all":
        sent = phBotChat.All(args[1])
    elif t == "private":
        sent = phBotChat.Private(args[1], args[2])
    elif t == "party":
        sent = phBotChat.Party(args[1])
    elif t == "guild":
        sent = phBotChat.Guild(args[1])
    elif t == "union":
        sent = phBotChat.Union(args[1])
    elif t == "note":
        sent = phBotChat.Note(args[1], args[2])
    elif t == "stall":
        sent = phBotChat.Stall(args[1])
    elif t == "global":
        sent = phBotChat.Global(args[1])
    if sent:
        log('Plugin: Mesaj "' + t + '" başarıyla gönderildi!')

def checkInv(arg):
    weapon = 0
    protector = 0
    accessory = 0
    shield = 0
    flower1 = 0
    flower2 = 0
    flower3 = 0
    flower4 = 0
    flower5 = 0
    blue1 = 0
    blue2 = 0
    blue3 = 0
    blue4 = 0
    blue5 = 0
    blue6 = 0
    blue7 = 0
    blue8 = 0
    blue9 = 0
    blue10 = 0
    blue11 = 0
    blue12 = 0
    blue13 = 0
    blue14 = 0
    stat1 = 0
    stat2 = 0
    stat3 = 0
    stat4 = 0
    stat5 = 0
    stat6 = 0
    stat7 = 0
    stat8 = 0
    stat9 = 0
    stat10 = 0
    stat11 = 0
    stat12 = 0
    stat13 = 0
    stat14 = 0
    pandora = 0
    ms = 0
    luck = 0
    steady = 0
    cream = 0
    lamp = 0
    dLamp = 0
    sunItems = 0
    items = []
    items = get_inventory()['items'][13:]

    if items:
        for item in items:
            if item is not None:
                # log(item["name"])
                if "Lv.11" in item['name'] and "(Weapon)" in item['name']:
                    weapon += item['quantity']
                if "Lv.11" in item['name'] and "(Armor)" in item['name']:
                    protector += item['quantity']
                if "Lv.11" in item['name'] and "(Accessory)" in item['name']:
                    accessory += item['quantity']
                if "Lv.11" in item['name'] and "(Shield)" in item['name']:
                    shield += item['quantity']
                if "Flower" in item['name'] and "Evil" in item['name']:
                    flower1 += item['quantity']
                if "Flower" in item['name'] and "Illusion" in item['name']:
                    flower2 += item['quantity']
                if "Flower" in item['name'] and "Life" in item['name']:
                    flower3 += item['quantity']
                if "Flower" in item['name'] and "Energy" in item['name']:
                    flower4 += item['quantity']
                if "Flower" in item['name'] and "Whirling" in item['name']:
                    flower5 += item['quantity']
                if "Lvl.11" in item['name'] and "Str" in item['name']:
                    blue1 += item['quantity']
                if "Lvl.11" in item['name'] and "Int" in item['name']:
                    blue2 += item['quantity']
                if "Lvl.11" in item['name'] and "master" in item['name']:
                    blue3 += item['quantity']
                if "Lvl.11" in item['name'] and "strikes" in item['name']:
                    blue4 += item['quantity']
                if "Lvl.11" in item['name'] and "discipline" in item['name']:
                    blue5 += item['quantity']
                if "Lvl.11" in item['name'] and "penetration" in item['name']:
                    blue6 += item['quantity']
                if "Lvl.11" in item['name'] and "dodging" in item['name']:
                    blue7 += item['quantity']
                if "Lvl.11" in item['name'] and "stamina" in item['name']:
                    blue8 += item['quantity']
                if "Lvl.11" in item['name'] and "magic" in item['name']:
                    blue9 += item['quantity']
                if "Lvl.11" in item['name'] and "fogs" in item['name']:
                    blue10 += item['quantity']
                if "Lvl.11" in item['name'] and "air" in item['name']:
                    blue11 += item['quantity']
                if "Lvl.11" in item['name'] and "fire" in item['name']:
                    blue12 += item['quantity']
                if "Lvl.11" in item['name'] and "immunity" in item['name']:
                    blue13 += item['quantity']
                if "Lvl.11" in item['name'] and "revival" in item['name']:
                    blue14 += item['quantity']
                if "Lvl.11" in item['name'] and "courage" in item['name']:
                    stat1 += item['quantity']
                if "Lvl.11" in item['name'] and "warriors" in item['name']:
                    stat2 += item['quantity']
                if "Lvl.11" in item['name'] and "philosophy" in item['name']:
                    stat3 += item['quantity']
                if "Lvl.11" in item['name'] and "meditation" in item['name']:
                    stat4 += item['quantity']
                if "Lvl.11" in item['name'] and "challenge" in item['name']:
                    stat5 += item['quantity']
                if "Lvl.11" in item['name'] and "focus" in item['name']:
                    stat6 += item['quantity']
                if "Lvl.11" in item['name'] and "flesh" in item['name']:
                    stat7 += item['quantity']
                if "Lvl.11" in item['name'] and "life" in item['name']:
                    stat8 += item['quantity']
                if "Lvl.11" in item['name'] and "mind" in item['name']:
                    stat9 += item['quantity']
                if "Lvl.11" in item['name'] and "spirit" in item['name']:
                    stat10 += item['quantity']
                if "Lvl.11" in item['name'] and "dodging" in item['name']:
                    stat11 += item['quantity']
                if "Lvl.11" in item['name'] and "agility" in item['name']:
                    stat12 += item['quantity']
                if "Lvl.11" in item['name'] and "training" in item['name']:
                    stat13 += item['quantity']
                if "Lvl.11" in item['name'] and "prayer" in item['name']:
                    stat14 += item['quantity']
                if "Pandora's Box" in item['name'] and "" in item['name']:
                    pandora += item['quantity']
                if "Monster Summon Scroll (ekip kullanir)" in item['name'] and "" in item['name']:
                    ms += item['quantity']
                if "Magic stone of luck(Lvl.11)" in item['name'] and "" in item['name']:
                    luck += item['quantity']
                if "Magic stone of steady(Lvl.11)" in item['name'] and "" in item['name']:
                    steady += item['quantity']
                if "ITEM_ETC_E090722_" in item['servername'] and "ICECREAM" in item['servername']:
                    cream += item['quantity']
                if "Genie’s Lamp" in item['name']:
                    lamp += item['quantity']
                if "Dirty Lamp" in item['name']:
                    dLamp += item['quantity']
                if 'RARE' in item['servername'] and 'EVENT' not in item['servername'] and 'ARCHEMY' not in item[
                    'servername']:
                    sunItems += 1

    pets = get_pets()

    if pets != []:
        for p in pets.keys():
            pet = pets[p]
            if pet['type'] in 'pick':
                for petItems in pet['items']:
                    if petItems != None:
                        if "Lv.11" in petItems['name'] and "(Weapon)" in petItems['name']:
                            weapon += petItems['quantity']
                        if "Lv.11" in petItems['name'] and "(Armor)" in petItems['name']:
                            protector += petItems['quantity']
                        if "Lv.11" in petItems['name'] and "(Accessory)" in petItems['name']:
                            accessory += petItems['quantity']
                        if "Lv.11" in petItems['name'] and "(Shield)" in petItems['name']:
                            shield += petItems['quantity']
                        if "Flower" in petItems['name'] and "Evil" in petItems['name']:
                            flower1 += petItems['quantity']
                        if "Flower" in petItems['name'] and "Illusion" in petItems['name']:
                            flower2 += petItems['quantity']
                        if "Flower" in petItems['name'] and "Life" in petItems['name']:
                            flower3 += petItems['quantity']
                        if "Flower" in petItems['name'] and "Energy" in petItems['name']:
                            flower4 += petItems['quantity']
                        if "Flower" in petItems['name'] and "Whirling" in petItems['name']:
                            flower5 += petItems['quantity']
                        if "Lvl.11" in item['name'] and "Str" in item['name']:
                            blue1 += item['quantity']
                        if "Lvl.11" in item['name'] and "Int" in item['name']:
                            blue2 += item['quantity']
                        if "Lvl.11" in item['name'] and "master" in item['name']:
                            blue3 += item['quantity']
                        if "Lvl.11" in item['name'] and "strikes" in item['name']:
                            blue4 += item['quantity']
                        if "Lvl.11" in item['name'] and "discipline" in item['name']:
                            blue5 += item['quantity']
                        if "Lvl.11" in item['name'] and "penetration" in item['name']:
                            blue6 += item['quantity']
                        if "Lvl.11" in item['name'] and "dodging" in item['name']:
                            blue7 += item['quantity']
                        if "Lvl.11" in item['name'] and "stamina" in item['name']:
                            blue8 += item['quantity']
                        if "Lvl.11" in item['name'] and "magic" in item['name']:
                            blue9 += item['quantity']
                        if "Lvl.11" in item['name'] and "fogs" in item['name']:
                            blue10 += item['quantity']
                        if "Lvl.11" in item['name'] and "air" in item['name']:
                            blue11 += item['quantity']
                        if "Lvl.11" in item['name'] and "fire" in item['name']:
                            blue12 += item['quantity']
                        if "Lvl.11" in item['name'] and "immunity" in item['name']:
                            blue13 += item['quantity']
                        if "Lvl.11" in item['name'] and "revival" in item['name']:
                            blue14 += item['quantity']
                        if "Lvl.11" in item['name'] and "courage" in item['name']:
                            stat1 += item['quantity']
                        if "Lvl.11" in item['name'] and "warriors" in item['name']:
                            stat2 += item['quantity']
                        if "Lvl.11" in item['name'] and "philosophy" in item['name']:
                            stat3 += item['quantity']
                        if "Lvl.11" in item['name'] and "meditation" in item['name']:
                            stat4 += item['quantity']
                        if "Lvl.11" in item['name'] and "challenge" in item['name']:
                            stat5 += item['quantity']
                        if "Lvl.11" in item['name'] and "focus" in item['name']:
                            stat6 += item['quantity']
                        if "Lvl.11" in item['name'] and "flesh" in item['name']:
                            stat7 += item['quantity']
                        if "Lvl.11" in item['name'] and "life" in item['name']:
                            stat8 += item['quantity']
                        if "Lvl.11" in item['name'] and "mind" in item['name']:
                            stat9 += item['quantity']
                        if "Lvl.11" in item['name'] and "spirit" in item['name']:
                            stat10 += item['quantity']
                        if "Lvl.11" in item['name'] and "dodging" in item['name']:
                            stat11 += item['quantity']
                        if "Lvl.11" in item['name'] and "agility" in item['name']:
                            stat12 += item['quantity']
                        if "Lvl.11" in item['name'] and "training" in item['name']:
                            stat13 += item['quantity']
                        if "Lvl.11" in item['name'] and "prayer" in item['name']:
                            stat14 += item['quantity']
                        if "Pandora's Box" in petItems['name'] and "" in petItems['name']:
                            pandora += petItems['quantity']
                        if "Monster Summon Scroll (ekip kullanir)" in petItems['name'] and "" in petItems['name']:
                            ms += petItems['quantity']
                        if "Magic stone of steady(Lvl.11)" in petItems['name'] and "" in petItems['name']:
                            steady += petItems['quantity']
                        if "Magic stone of luck(Lvl.11)" in petItems['name'] and "" in petItems['name']:
                            luck += petItems['quantity']
                        if "ITEM_ETC_E090722_" in petItems['servername'] and "ICECREAM" in petItems['servername']:
                            cream += petItems['quantity']
                        if "Genie’s Lamp" in petItems['name']:
                            lamp += petItems['quantity']
                        if "Dirty Lamp" in petItems['name']:
                            dLamp += petItems['quantity']
                        if 'RARE' in petItems['servername'] and 'EVENT' not in petItems[
                            'servername'] and 'ARCHEMY' not in petItems['servername']:
                            sunItems += 1

    storages = []
    storages = get_storage()['items']
    
    if storages:
        for item in storages:
            if item is not None:
                if "Lv.11" in item['name'] and "(Weapon)" in item['name']:
                    weapon += item['quantity']
                if "Lv.11" in item['name'] and "(Armor)" in item['name']:
                    protector += item['quantity']
                if "Lv.11" in item['name'] and "(Accessory)" in item['name']:
                    accessory += item['quantity']
                if "Lv.11" in item['name'] and "(Shield)" in item['name']:
                    shield += item['quantity']
                if "Flower" in item['name'] and "Evil" in item['name']:
                    flower1 += item['quantity']
                if "Flower" in item['name'] and "Illusion" in item['name']:
                    flower2 += item['quantity']
                if "Flower" in item['name'] and "Life" in item['name']:
                    flower3 += item['quantity']
                if "Flower" in item['name'] and "Energy" in item['name']:
                    flower4 += item['quantity']
                if "Flower" in item['name'] and "Whirling" in item['name']:
                    flower5 += item['quantity']
                if "Lvl.11" in item['name'] and "Str" in item['name']:
                    blue1 += item['quantity']
                if "Lvl.11" in item['name'] and "Int" in item['name']:
                    blue2 += item['quantity']
                if "Lvl.11" in item['name'] and "master" in item['name']:
                    blue3 += item['quantity']
                if "Lvl.11" in item['name'] and "strikes" in item['name']:
                    blue4 += item['quantity']
                if "Lvl.11" in item['name'] and "discipline" in item['name']:
                    blue5 += item['quantity']
                if "Lvl.11" in item['name'] and "penetration" in item['name']:
                    blue6 += item['quantity']
                if "Lvl.11" in item['name'] and "dodging" in item['name']:
                    blue7 += item['quantity']
                if "Lvl.11" in item['name'] and "stamina" in item['name']:
                    blue8 += item['quantity']
                if "Lvl.11" in item['name'] and "magic" in item['name']:
                    blue9 += item['quantity']
                if "Lvl.11" in item['name'] and "fogs" in item['name']:
                    blue10 += item['quantity']
                if "Lvl.11" in item['name'] and "air" in item['name']:
                    blue11 += item['quantity']
                if "Lvl.11" in item['name'] and "fire" in item['name']:
                    blue12 += item['quantity']
                if "Lvl.11" in item['name'] and "immunity" in item['name']:
                    blue13 += item['quantity']
                if "Lvl.11" in item['name'] and "revival" in item['name']:
                    blue14 += item['quantity']
                if "Lvl.11" in item['name'] and "courage" in item['name']:
                    stat1 += item['quantity']
                if "Lvl.11" in item['name'] and "warriors" in item['name']:
                    stat2 += item['quantity']
                if "Lvl.11" in item['name'] and "philosophy" in item['name']:
                    stat3 += item['quantity']
                if "Lvl.11" in item['name'] and "meditation" in item['name']:
                    stat4 += item['quantity']
                if "Lvl.11" in item['name'] and "challenge" in item['name']:
                    stat5 += item['quantity']
                if "Lvl.11" in item['name'] and "focus" in item['name']:
                    stat6 += item['quantity']
                if "Lvl.11" in item['name'] and "flesh" in item['name']:
                    stat7 += item['quantity']
                if "Lvl.11" in item['name'] and "life" in item['name']:
                    stat8 += item['quantity']
                if "Lvl.11" in item['name'] and "mind" in item['name']:
                    stat9 += item['quantity']
                if "Lvl.11" in item['name'] and "spirit" in item['name']:
                    stat10 += item['quantity']
                if "Lvl.11" in item['name'] and "dodging" in item['name']:
                    stat11 += item['quantity']
                if "Lvl.11" in item['name'] and "agility" in item['name']:
                    stat12 += item['quantity']
                if "Lvl.11" in item['name'] and "training" in item['name']:
                    stat13 += item['quantity']
                if "Lvl.11" in item['name'] and "prayer" in item['name']:
                    stat14 += item['quantity']
                if "Pandora's Box" in item['name'] and "" in item['name']:
                    pandora += item['quantity']
                if "Monster Summon Scroll (ekip kullanir)" in item['name'] and "" in item['name']:
                    ms += item['quantity']
                if "Magic stone of luck(Lvl.11)" in item['name'] and "" in item['name']:
                    luck += item['quantity']
                if "Magic stone of steady(Lvl.11)" in item['name'] and "" in item['name']:
                    steady += item['quantity']
                if "ITEM_ETC_E090722_" in item['servername'] and "ICECREAM" in item['servername']:
                    cream += item['quantity']
                if "Genie’s Lamp" in item['name']:
                    lamp += item['quantity']
                if "Dirty Lamp" in item['name']:
                    dLamp += item['quantity']
                if 'RARE' in item['servername'] and 'EVENT' not in item['servername'] and 'ARCHEMY' not in item[
                    'servername']:
                    sunItems += 1

    if arg == "Elixir":
        handleChatCommand("party Elixir; Weapon " + str(weapon) + " , Armor " + str(protector) + " , Shield " + str(shield) + " , Accessory " + str(accessory))
    if arg == "Flower3":
        handleChatCommand("party Flower; Life " + str(flower3) + " , Energy " + str(flower4) + " , Evil " + str(flower1) + " , Illusion " + str(flower2) + " , Whirling " + str(flower5))
    if arg == "BlueStone":
        handleChatCommand("party STR " + str(blue1) + " , INT " + str(blue2) + " , MASTER " + str(blue3) + " , STRIKES " + str(blue4) + " , DSCPLNE " + str(blue5) + " , PNTRTON " + str(blue6) + " , DODGING " + str(blue7) + " , STAMINA " + str(blue8))
    if arg == "BlueStone2":
        handleChatCommand("party MAGIC " + str(blue9) + " , FOGS " + str(blue10) + " , AIR " + str(blue11) + " , FIRE " + str(blue12) + " , IMMUNITY " + str(blue13) + " , REVIVAL " + str(blue14))
    if arg == "StatStone":
        handleChatCommand("party COURAGE " + str(blue1) + " , WARRIORS " + str(blue2) + " , PHILOSOPHY " + str(blue3) + " , MEDITATION " + str(blue4) + " , CHALLENGE " + str(blue5) + " , FOCUS " + str(blue6) + " , FLESH " + str(blue7))
    if arg == "StatStone2":
        handleChatCommand("party LIFE " + str(blue8) + " , MIND " + str(blue9) + " , SPIRIT " + str(blue10) + " , DODGING " + str(blue11) + " , AGILITY " + str(blue12) + " , TRAINING " + str(blue13) + " , PRAYER " + str(blue14))
    if arg == "Cream":
        handleChatCommand("party Ice Cream " + str(cream))
    if arg == "Pandora":
        handleChatCommand("party Pandora " + str(pandora))
    if arg == "Ms":
        handleChatCommand("party Monster Summon Scroll " + str(ms))
    if arg == "Luck":
        handleChatCommand("party Magic stone of luck " + str(luck))
    if arg == "Steady":
        handleChatCommand("party Magic stone of steady " + str(steady))
    if arg == "Lamp":
        handleChatCommand("party Genie’s Lamp " + str(lamp) + " -- Dirty Lamp " + str(dLamp))
    if arg == "Sox":
        handleChatCommand("party " + str(sunItems) + " Parca SoX Ogesi")


def checkGold():
    gold = 0;

    chars = []
    chars = get_character_data()

    if chars != []:
        gold += chars['gold']

    goldS = format(gold, ",")

    handleChatCommand("party Suan " + str(goldS) + " Altin var. ")


def checkExp():
    data = get_character_data()
    currentExp = data['current_exp']
    level = data['level']
    maxExp = data['max_exp']
    exp = float((100 * currentExp) / maxExp)

    handleChatCommand("party Seviye: " + str(level) + " - Tecrube : %" + str("{:.2f}".format(exp)))


def inventorySpace():
    size = 0
    usingSpace = 0

    items = []
    items = get_inventory()['items'][12:]
    size = get_inventory()['size'] - 12

    if items != []:
        for item in items:
            if item != None:
                usingSpace += 1

    size -= 1
    usingSpace -= 1
    handleChatCommand("party Bos Alan " + str(size - usingSpace) + "  ---->  " + str(usingSpace) + "/" + str(size))

def checkJob():
    data = get_character_data()
    currentExp = data['job_current_exp']
    maxExp = data['job_max_exp']
    exp = float((100 * currentExp) / maxExp)
    
    handleChatCommand("party Job Exp: %" + str("{:.2f}".format(exp)))

def specialtyGoodsBox():
    i = 0
    j = 0
    pouch = get_job_pouch()
    items = []
    items = get_job_pouch()["items"]
    if items != []:
        for item in items:
            j = j + 1
            if item is not None:
                i = i + item["quantity"]

    handleChatCommand("party Specialty -> " + str(i) + " / " + str(j * 5))


def checkGuild():
    items = []
    items = get_guild_storage()['items']

    sunItems = [0 for i in range(11)]
    moonItems = [0 for i in range(10)]
    sosItems = [0 for i in range(10)]

    if items != []:
        for item in items:
            if item != None:
                if 'RARE' in item['servername'] and 'EVENT' not in item['servername'] and 'ARCHEMY' not in item[
                    'servername']:
                    # split = item['servername'].split('_')
                    log(item['servername'])
                    # dg = int(str(split[4]))
                    dg = [int(s) for s in item['servername'].split('_') if s.isdigit()][0]
                    if dg < 11:
                        if '_C_' in item['servername']:
                            sunItems[dg - 1] += 1
                        elif '_B_' in item['servername']:
                            moonItems[dg - 1] += 1
                        elif '_A_' in item['servername']:
                            sosItems[dg - 1] += 1
                    else:
                        if '_A_' in item['servername']:
                            sunItems[10] += 1

    i = 1
    for x in sunItems:
        log(str(i) + " " + str(x) + "\t")
        i = i + 1


# ______________________________ Events ______________________________ #

# Called when the bot successfully connects to the game server
def connected():
    global inGame
    inGame = None


# Called when the character enters the game world
def joined_game():
    loadConfigs()
    
# All chat messages received are sent to this function
def handle_chat(t, player, msg):
    i = 0;
    j = 0;
    k = 0;
    l = 0;
    # Check player at leader list or a Discord message
    if player and lstLeaders_exist(player) or t == 100:

        if msg == "ENV":
            inventorySpace()
        elif msg == "EXP":
            checkExp()
        elif msg == "JOBEXP":
            checkJob()
        elif msg == "GOLD":
            checkGold()
        elif msg == "ELIXIR":
            checkInv("Elixir")
        elif msg == "BLUESTONE":
            checkInv("BlueStone")
        elif msg == "BLUESTONE2":
            checkInv("BlueStone2")
        elif msg == "STATSTONE":
            checkInv("StatStone")
        elif msg == "STATSTONE2":
            checkInv("StatStone2")
        elif msg == "FLOWER":
            checkInv("Flower3") 
        elif msg == "PANDORA":
            checkInv("Pandora") 
        elif msg == "LUCK":
            checkInv("Luck") 
        elif msg == "STEADY":
            checkInv("Steady") 
        elif msg == "MS":
            checkInv("Ms") 
        elif msg == "ICE":
            checkInv("Cream") 
        elif msg == "ACC":
            checkInv("Accessory")
        elif msg == "LAMP":
            checkInv("Lamp")
        elif msg == "SOX":
            checkInv("Sox")

# Called every 500ms
# def event_loop():


# Plugin loaded
log("Plugin: "+pName+" Yüklendi! Çalışıyor...")

if os.path.exists(getPath()):
	# Adding RELOAD plugin support
	loadConfigs()
else:
	# Creating configs folder
	os.makedirs(getPath())
	log('Plugin: '+pName+' klasörü oluŞturuldu.')
