from phBot import *
import phBotChat
import QtBind
import json
import os
import traceback

name = 'TR_InventoryCounter'

gui = QtBind.init(__name__, name)

tbxLeaders = QtBind.createLineEdit(gui,"",470,41,110,20)
lstLeaders = QtBind.createList(gui,470,62,110,70)
btnAddLeader = QtBind.createButton(gui,'btnAddLeader_clicked'," Lider Ekle ", 581, 39)
btnRemLeader = QtBind.createButton(gui,'btnRemLeader_clicked'," Lider Sil ", 581, 61)
btnClearInfo = QtBind.createButton(gui, 'btnClearInfo_clicked', "Arayüzü\nTemizle", 597, 185)
metaby = QtBind.createLabel(gui,'edited by hakankahya', 475, 283)
label_chat_channel = QtBind.createLabel(gui,'Yanıt Kanalı:', 470, 140)
list_chat_channel_bg = QtBind.createList(gui, 470, 155, 125, 125)
lstInfo = QtBind.createList(gui,15,40,450,255)
QtBind.append(gui, lstInfo, "                   TR_InventoryCounter Eklentisine Hoşgeldiniz. ")
QtBind.append(gui, lstInfo, " ")
QtBind.append(gui, lstInfo, "   Komutlar hakkında bilgi almak için yukarıdaki butonları kullanabilirsiniz.")
QtBind.append(gui, lstInfo, " ")
QtBind.append(gui, lstInfo, "   Lider eklemek ve sohbet ayarları için sağdaki menüyü kullanın.")
QtBind.append(gui, lstInfo, " ")
QtBind.append(gui, lstInfo, "   Karakter Bilgi Harici Verilen Komutlar Envanter, Pet, ve Depo\'nuzu Kontrol Etmektedir.")
QtBind.append(gui, lstInfo, " ")
QtBind.append(gui, lstInfo, "   Herhangi Bir Hata ile Karşılaştığınızda Bildirmekten Çekinmeyin. Dc ; hakankahya")
btnkarakter = QtBind.createButton(gui,'btnkarakter_clicked'," Karakter Bilgi ", 15, 11)
btnelixir = QtBind.createButton(gui,'btnelixir_clicked'," Elixir/Enhancer Bilgi ", 91, 11)
btnevent = QtBind.createButton(gui,'btnevent_clicked'," Event Bilgi ", 197, 11)
btncoin = QtBind.createButton(gui,'btncoin_clicked'," Coin Bilgi ", 272, 11)
btnstone = QtBind.createButton(gui,'btnstone_clicked'," Stone Bilgi ", 347, 11)
btnfgw = QtBind.createButton(gui,'btnfgw_clicked'," Fgw Bilgi ", 422, 11)
btnegpty = QtBind.createButton(gui,'btnegpty_clicked'," Egpty Set Bilgi ", 497, 11)
btnstall = QtBind.createButton(gui,'btnstall_clicked'," Stall Bilgi ", 579, 11)
cbxAllChat = QtBind.createCheckBox(gui,"cbxAllChat_clicked","Genel Sohbet", 475, 160)
cbxPartyChat = QtBind.createCheckBox(gui,"cbxPartyChat_clicked","Parti Sohbet", 475, 175)
cbxGuildChat = QtBind.createCheckBox(gui,"cbxGuildChat_clicked","Guild Sohbet", 475, 190)
cbxUnionChat = QtBind.createCheckBox(gui,"cbxUnionChat_clicked","Birlik Sohbet", 475, 205)
cbxPrivateChatSender = QtBind.createCheckBox(gui,"cbxPrivateChatSender_clicked","Özel (Lider'e)", 475, 220)
cbxPrivateChatTarget = QtBind.createCheckBox(gui,"cbxPrivateChatTarget_clicked","Özel (Belirtilen)", 475, 235)
tbxTargetPrivate = QtBind.createLineEdit(gui,"",475,252,115,20)
btnSaveChatSettings = QtBind.createButton(gui,'btnSaveChatSettings_clicked'," Ayarları Kaydet ", 595, 154)
selected_chat_channel = "PrivateSender"
target_private_name = ""

def btnkarakter_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'- EXP : Suanki LV ve EXP bildirir.\n- SP : Suan ki SP Miktarını belirtir.\n- GOLD : Envanter Altın Miktarını Bildirir.\n- GOLDGUILD : Guild Deposundaki Altın Miktarını Bildirir.\n- GOLDDEPO : Depodaki Altın Miktarını Bildirir.\n- ENV : Envanterin boş yuva sayısını bildirir.\n- DEPO : Depodaki boş yuva sayısını bildirir.\n- JOBINFO : JOB Nick, Job Seviye, JOB Tipi Ve JOB Exp miktarını bildirir.\n- JOBBOX : Meslek çantasındaki doluluğu bildirir.(Uzmanlik)\n- SOX : Sox Miktarını Bildirir.(Giyilmişler ve Job Setler Haric)') #

def btnelixir_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'- INCELX : Incomplete Intensifying Elixir miktarını bildirir.\n- 8ELX : Lv.8 Intensifying Elixir miktarını bildirir.\n- 9ELX : Lv.9 Intensifying Elixir miktarını bildirir.\n- 10ELX : Lv.10 Intensifying Elixir miktarını bildirir.\n- 11ELX : Lv.11 Intensifying Elixir miktarını bildirir.\n- ENH12 : 12th Grade Enhancer miktarını bildirir.\n- ENH13 : 13th Grade Enhancer miktarını bildirir.\n- ENH14 : 14th Grade Enhancer miktarını bildirir.\n- ENH15 : 15th Grade Enhancer miktarını bildirir.\n- ENH16 : 16th Grade Enhancer miktarını bildirir.\n- ENH17 : 17th Grade Enhancer miktarını bildirir.')

def btnevent_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'- FLOWER : Tüm ciceklerin miktarını bildirir.\n- ZERK : Berserker Regeneration Potion miktarını bildirir.\n- PANDORA : Pandora Box miktarını bildirir.\n- MONSTER : Monster Summon Scroll Miktarını Bildirir.\n- CATA : Alchemy Catalyst miktarını bildirir.\n- ICE : Dondurma miktarını bildirir.\n- LUCKYBOX : Lucky Box miktarını bildirir.\n- PLEDGE : Pledge Sag ve Sol miktarını bildirir.\n- ALIBABA : AliBaba Seal miktarını bildirir.\n- RUBBER : Rubber Piece miktarını bildirir.\n- THANKS : Thanks event Harf miktarını bildirir.\n- FLAKE : Snow Flake miktarını bildirir.\n- HALLOWEN : Halloween Caddy miktarını bildirir.')

def btncoin_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'- COIN : Envanterdeki Gold/Silver/Iron/Copper/Arena Coin miktarını bildirir.\n- COMBATI : Coin of Combativeness (Party) ve Coin of Combativeness (Individual)\nMiktarını bildirir.\n- TOKEN1 : Monk\'s Token miktarını bildirir.\n- TOKEN2 : Soldier\'s Token miktarını bildirir.\n- TOKEN3 : General\'s Token miktarını bildirir.')

def btnstone_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'- 8BLUE : 8DG Blue Stonelerin Miktarını bildirir.\n- 8BLUE2 : 8DG Blue Stonelerin Miktarını bildirir.\n- 9BLUE : 9DG Blue Stonelerin Miktarını bildirir.\n- 9BLUE2 : 9DG Blue Stonelerin Miktarını bildirir.\n- 10BLUE : 10DG Blue Stonelerin Miktarını bildirir.\n- 10BLUE2 : 10DG Blue Stonelerin Miktarını bildirir.\n- 11BLUE : 11DG Blue Stonelerin Miktarını bildirir.\n- 11BLUE2 : 11DG Blue Stonelerin Miktarını bildirir.\n- 8STAT : 8DG Stat Stonelerin Miktarını bildirir.\n- 8STAT2 : 8DG Stat Stonelerin Miktarını bildirir.\n- 9STAT : 9DG Stat Stonelerin Miktarını bildirir.\n- 9STAT2 : 9DG Stat Stonelerin Miktarını bildirir.\n- 10STAT : 10DG Stat Stonelerin Miktarını bildirir.')
    QtBind.append(gui,lstInfo,'- 10STAT2 : 10DG Stat Stonelerin Miktarını bildirir.\n- 11STAT : 11DG Stat Stonelerin Miktarını bildirir.\n- 11STAT2 : 11DG Stat Stonelerin Miktarını bildirir.\n- 8LUCK : 8DG Luck Stonelerin Miktarını bildirir.\n- 9LUCK : 9DG Luck Stonelerin Miktarını bildirir.\n- 10LUCK : 10DG Luck Stonelerin Miktarını bildirir.\n- 11LUCK : 11DG Luck Stonelerin Miktarını bildirir.\n- 8STEADY : 8DG Steady Stonelerin Miktarını bildirir.\n- 9STEADY : 9DG Steady Stonelerin Miktarını bildirir.\n- 10STEADY : 10DG Steady Stonelerin Miktarını bildirir.\n- 11STEADY : 11DG Steady Stonelerin Miktarını bildirir.')

def btnfgw_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'- 8FGW1 : (8DG SUN) Kolay Düşen Kartların miktarını bildirir.\n- 8FGW2 : (8DG SUN) Zor Düşen Kartların miktarını bildirir.\n- 9FGW1 : (9DG SUN) Kolay Düşen Kartların miktarını bildirir.\n- 9FGW2 : (9DG SUN) Zor Düşen Kartların miktarını bildirir.\n- 10FGW1 : (10DG MOON) Kolay Düşen Kartların miktarını bildirir.\n- 10FGW2 : (10DG MOON) Zor Düşen Kartların miktarını bildirir.\n- 11FGW1 : (11DG EGYPY A) Kolay Düşen Kartların miktarını bildirir.\n- 11FGW2 : (11DG EGPTY A) Zor Düşen Kartların miktarını bildirir.\n- FADED : Faded Bead Miktarını Bildirir.\n- PETSTR : Fellow Pet için Increase Strength Miktarını Bildirir.\n- PETINT : Fellow Pet için Increase Intelligence Miktarını Bildirir.')

def btnegpty_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'- SETA : Egpty A Grade Eşya Miktarını Bildirir.(Giyilmişler Haric)\n Sadece Drop Sayısını bildirir.(Silah - Kıyafet - Kalkan - Yüzük) \n- SETB : Egpty B Grade Eşya Miktarını Bildirir.(Giyilmişler Haric)\n Sadece Drop Sayısını bildirir.(Silah - Kıyafet - Kalkan - Yüzük)')

def btnstall_clicked():
    QtBind.clear(gui,lstInfo)
    QtBind.append(gui,lstInfo,'- GLOBALSC : Global chatting Miktarını Bildiri.\n- REVSC : Reverse Return Scroll Miktarını Bildirir.\n- CLOCKSC : Clock of Reincarnation Miktarını Bildirir.\n- DEVILSC : Extension gear Miktarını Bildirir.\n- PREPLUS : Premium Gold Time PLUS Miktarını Bildirir.\n- HAMMER : Repair Hammer Miktarını Bildirir.\n- ASTRAL : Magic stone of Astral Miktarını Bildirir.\n- IMMORTAL : Magic stone of immortal Miktarını Bildirir.\n- ENVANTERSC : Inventory expansion item miktarını bildirir.\n- STORAGESC : Storage expansion item miktarını bildirir.\n- JOBBLUE : Sealed Magic Rune miktarını belirtir.\n- JOBARTI : Sealed Reinforcement Rune miktarını belirler.')

def btnClearInfo_clicked():
    QtBind.clear(gui, lstInfo)
    log('TR_InventoryCounter: Bilgi listesi temizlendi.')

def connected():
	global inGame
	inGame = None

def joined_game():
	loadConfigs()

def getPath():
	return get_config_dir()+name+"\\"

def getConfig():
	return getPath()+inGame['server'] + "_" + inGame['name'] + ".json"

def isJoined():
	global inGame
	inGame = get_character_data()
	if not (inGame and "name" in inGame and inGame["name"]):
		inGame = None
	return inGame

def loadDefaultConfig():
	QtBind.clear(gui,lstLeaders)

def loadConfigs():
    global selected_chat_channel, target_private_name
    loadDefaultConfig()
    if isJoined():
        config_file = getConfig()
        if os.path.exists(config_file):
            data = {}
            try:
                with open(config_file,"r", encoding='utf-8') as f:
                    data = json.load(f)
                if "Leaders" in data:
                    for nickname in data["Leaders"]:
                        QtBind.append(gui,lstLeaders,nickname)

                selected_chat_channel = data.get("ChatChannel", "PrivateSender")
                target_private_name = data.get("TargetPrivateName", "")

                QtBind.setChecked(gui, cbxAllChat, selected_chat_channel == "All")
                QtBind.setChecked(gui, cbxPartyChat, selected_chat_channel == "Party")
                QtBind.setChecked(gui, cbxGuildChat, selected_chat_channel == "Guild")
                QtBind.setChecked(gui, cbxUnionChat, selected_chat_channel == "Union")
                QtBind.setChecked(gui, cbxPrivateChatSender, selected_chat_channel == "PrivateSender")
                QtBind.setChecked(gui, cbxPrivateChatTarget, selected_chat_channel == "PrivateTarget")
                QtBind.setText(gui, tbxTargetPrivate, target_private_name)

            except Exception as e:
                log(f'TR_InventoryCounter: Config yüklenirken hata: {e}')
                selected_chat_channel = "PrivateSender"
                target_private_name = ""
                QtBind.setChecked(gui, cbxPrivateChatSender, True)
                QtBind.setText(gui, tbxTargetPrivate, "")
        else:
             selected_chat_channel = "PrivateSender"
             target_private_name = ""
             QtBind.setChecked(gui, cbxPrivateChatSender, True)
             QtBind.setText(gui, tbxTargetPrivate, "")

def saveConfigs():
    global selected_chat_channel, target_private_name
    if not isJoined():
        log('TR_InventoryCounter: Oyuna giriş yapılmamış veya karakter bilgileri alınamadı.')
        return
    if inGame:
        config_file = getConfig()
        data = {}
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except Exception as e:
                log(f'TR_InventoryCounter: Config okunurken hata (kaydetme): {e}')
                data = {"Leaders": QtBind.getItems(gui, lstLeaders)}
        target_private_name = QtBind.text(gui, tbxTargetPrivate)
        data["ChatChannel"] = selected_chat_channel
        data["TargetPrivateName"] = target_private_name
        if "Leaders" not in data:
            data["Leaders"] = []
        data["Leaders"] = QtBind.getItems(gui, lstLeaders)
        try:
            with open(config_file, "w", encoding='utf-8') as f:
                json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
        except Exception as e:
            log(f'TR_InventoryCounter: Config yazılırken hata (kaydetme): {e}')

def btnAddLeader_clicked():
	if not isJoined():
		log('TR_InventoryCounter: Oyuna giriş yapılmamış veya karakter bilgileri alınamadı.')
		return
	player = QtBind.text(gui,tbxLeaders)
	if player and not lstLeaders_exist(player):
		data = {}
		if os.path.exists(getConfig()):
			try:
				with open(getConfig(), 'r', encoding='utf-8') as f:
					data = json.load(f)
			except Exception as e:
				log(f'TR_InventoryCounter: Config okunurken hata: {e}')
				data = {}
		if not "Leaders" in data:
			data['Leaders'] = []
		if player not in data['Leaders']:
			data['Leaders'].append(player)
			try:
				with open(getConfig(),"w", encoding='utf-8') as f:
					json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
				QtBind.append(gui,lstLeaders,player)
				QtBind.setText(gui, tbxLeaders,"")
				log(f'TR_InventoryCounter: Lider Eklendi. [{player}]')
			except Exception as e:
				log(f'TR_InventoryCounter: Config yazılırken hata: {e}')
		else:
			log(f'TR_InventoryCounter: Lider zaten listede: [{player}]')
			QtBind.setText(gui, tbxLeaders,"")

def btnRemLeader_clicked():
	if not isJoined():
		log('TR_InventoryCounter: Oyuna giriş yapılmamış veya karakter bilgileri alınamadı.')
		return
	selectedItem = QtBind.text(gui,lstLeaders)
	if selectedItem:
		data = {"Leaders":[]}
		if os.path.exists(getConfig()):
			try:
				with open(getConfig(), 'r', encoding='utf-8') as f:
					data = json.load(f)
				if "Leaders" in data and selectedItem in data["Leaders"]:
					data["Leaders"].remove(selectedItem)
					try:
						with open(getConfig(),"w", encoding='utf-8') as f:
							json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
						QtBind.remove(gui,lstLeaders,selectedItem)
						log(f'TR_InventoryCounter: Lider Silindi. [{selectedItem}]')
					except Exception as e:
						log(f'TR_InventoryCounter: Config yazılırken hata (silme): {e}')
				else:
					log(f'TR_InventoryCounter: Silinecek lider bulunamadı: [{selectedItem}]')
					try:
						QtBind.remove(gui, lstLeaders, selectedItem)
					except:
						pass
			except Exception as e:
				log(f'TR_InventoryCounter: Config okunurken/işlenirken hata (silme): {e}')

def lstLeaders_exist(nickname):
	nickname_lower = nickname.lower()
	players = QtBind.getItems(gui,lstLeaders)
	for player in players:
		if player.lower() == nickname_lower:
			return True
	return False

def update_selected_channel(channel_name):
    global selected_chat_channel
    selected_chat_channel = channel_name
    QtBind.setChecked(gui, cbxAllChat, channel_name == "All")
    QtBind.setChecked(gui, cbxPartyChat, channel_name == "Party")
    QtBind.setChecked(gui, cbxGuildChat, channel_name == "Guild")
    QtBind.setChecked(gui, cbxUnionChat, channel_name == "Union")
    QtBind.setChecked(gui, cbxPrivateChatSender, channel_name == "PrivateSender")
    QtBind.setChecked(gui, cbxPrivateChatTarget, channel_name == "PrivateTarget")

def cbxAllChat_clicked(checked):
    if checked: update_selected_channel("All")

def cbxPartyChat_clicked(checked):
    if checked: update_selected_channel("Party")

def cbxGuildChat_clicked(checked):
    if checked: update_selected_channel("Guild")

def cbxUnionChat_clicked(checked):
    if checked: update_selected_channel("Union")

def cbxPrivateChatSender_clicked(checked):
    if checked: update_selected_channel("PrivateSender")

def cbxPrivateChatTarget_clicked(checked):
    if checked: update_selected_channel("PrivateTarget")

def btnSaveChatSettings_clicked():
    saveConfigs()
    log('TR_InventoryCounter: Sohbet kanalı ayarları kaydedildi.')

def send_response(command_sender, message):
    global selected_chat_channel
    channel = selected_chat_channel
    log_prefix = "TR_InventoryCounter:"

    try:
        if channel == "All":
            phBotChat.All(message)

        elif channel == "Party":
            if get_party():
                phBotChat.Party(message)
            else:
                phBotChat.Private(command_sender, f"(Partide degil >) {message}")
                log(f"{log_prefix} Parti yok, özel gönderildi.")

        elif channel == "Guild":
            if get_guild():
                phBotChat.Guild(message)
            else:
                phBotChat.Private(command_sender, f"(Guildde degil) {message}")
                log(f"{log_prefix} Guild yok, özel gönderildi.")

        elif channel == "Union":
            if get_guild():
                phBotChat.Union(message)
            else:
                phBotChat.Private(command_sender, f"(Guildde degil) {message}")
                log(f"{log_prefix} Guild yok, özel gönderildi.")

        elif channel == "PrivateSender":
            phBotChat.Private(command_sender, message)

        elif channel == "PrivateTarget":
            target_name = QtBind.text(gui, tbxTargetPrivate)
            if target_name:
                phBotChat.Private(target_name, message)
            else:
                phBotChat.Private(command_sender, "(Hedef bos!)")
                log(f"{log_prefix} Hedef boş, gönderene özel gönderildi.")

        else:
            log(f"{log_prefix} Bilinmeyen kanal '{channel}', özel gönderiliyor.")
            phBotChat.Private(command_sender, message)

    except Exception as e:
        log(f"{log_prefix} Send ERROR (Kanal: {channel}): {e}")
        try:
            phBotChat.Private(command_sender, f"(Hata!) {message}")
        except:
            pass

def checkInv(arg, player):
    weapon1 = weapon2 = weapon3 = weapon4 = weapon5 = 0
    protector1 = protector2 = protector3 = protector4 = protector5 = 0
    accessory1 = accessory2 = accessory3 = accessory4 = accessory5 = 0
    shield1 = shield2 = shield3 = shield4 = shield5 = 0
    eweapon1 = eweapon2 = eweapon3 = eweapon4 = eweapon5 = eweapon6 = 0
    eprotector1 = eprotector2 = eprotector3 = eprotector4 = eprotector5 = eprotector6 = 0
    eaccessory1 = eaccessory2 = eaccessory3 = eaccessory4 = eaccessory5 = eaccessory6 = 0
    eshield1 = eshield2 = eshield3 = eshield4 = eshield5 = eshield6 = 0
    arena = qgold = silver = iron = copper = 0
    combativeness1 = combativeness2 = 0
    flowerevil = flowerillusion = flowerlife = flowerenergy = flowerwhirling = 0
    catalyst = berserker = pandora = ms = luckybox = 0
    pledge1 = pledge2 = alibabaseal = rubber = snowflake = halloweencandy = 0
    T1 = T2 = T3 = T4 = T5 = T6 = 0
    cream = lamp = dLamp = 0
    master8 = strikes8 = discipline8 = penetration8 = dodging8 = stamina8 = magic8 = fogs8 = air8 = fire8 = immunity8 = revival8 = 0
    master9 = strikes9 = discipline9 = penetration9 = dodging9 = stamina9 = magic9 = fogs9 = air9 = fire9 = immunity9 = revival9 = 0
    master10 = strikes10 = discipline10 = penetration10 = dodging10 = stamina10 = magic10 = fogs10 = air10 = fire10 = immunity10 = revival10 = 0
    master11 = strikes11 = discipline11 = penetration11 = dodging11 = stamina11 = magic11 = fogs11 = air11 = fire11 = immunity11 = revival11 = 0
    str8 = int8 = courage8 = warriors8 = philosophy8 = meditation8 = challenge8 = focus8 = flesh8 = life8 = mind8 = spirit8 = dodgings8 = agility8 = training8 = prayer8 = 0
    str9 = int9 = courage9 = warriors9 = philosophy9 = meditation9 = challenge9 = focus9 = flesh9 = life9 = mind9 = spirit9 = dodgings9 = agility9 = training9 = prayer9 = 0
    str10 = int10 = courage10 = warriors10 = philosophy10 = meditation10 = challenge10 = focus10 = flesh10 = life10 = mind10 = spirit10 = dodgings10 = agility10 = training10 = prayer10 = 0
    str11 = int11 = courage11 = warriors11 = philosophy11 = meditation11 = challenge11 = focus11 = flesh11 = life11 = mind11 = spirit11 = dodgings11 = agility11 = training11 = prayer11 = 0
    luckst8 = steadyst8 = luckst9 = steadyst9 = luckst10 = steadyst10 = luckst11 = steadyst11 = 0
    astral8 = immortal8 = astral9 = immortal9 = astral10 = immortal10 = astral11 = immortal11 = 0
    card1 = card2 = card3 = card4 = card5 = card6 = card7 = card8 = 0
    card9 = card10 = card11 = card12 = card13 = card14 = card15 = card16 = 0
    card17 = card18 = card19 = card20 = card21 = card22 = card23 = card24 = 0
    card25 = card26 = card27 = card28 = card29 = card30 = card31 = card32 = 0
    faded = 0
    petstr = petint = 0
    aGrade = bGrade = 0
    chatglobal = chatglobalvip = reversesc = clocksc = devilres = preplus = repairhammer = inventorysc = storagesc = 0
    jobblue = jobartı = 0
    token1 = token2 = token3 = 0

    inventory = get_inventory()
    storage = get_storage()
    pets = get_pets()
    inventory_items = []
    storage_items = []
    pet_items = []
    if inventory and 'items' in inventory:
        inventory_items = inventory['items'][13:]
    if storage and 'items' in storage:
        storage_items = storage['items']
    if pets:
        for p in pets.keys():
            pet = pets[p]
            if pet['type'] in 'pick':
                pet_items.extend(pet.get('items', []))
    all_items = inventory_items + storage_items + pet_items
    if all_items:
        for item in all_items:
            if item is not None:
                if 'name' in item:
                    if "Incomplete" in item['name'] and "Weapon" in item['name']:
                        weapon5 += item['quantity']
                    if "Incomplete" in item['name'] and "Armor" in item['name']:
                        protector5 += item['quantity']
                    if "Incomplete" in item['name'] and "Accessory" in item['name']:
                        accessory5 += item['quantity']
                    if "Incomplete" in item['name'] and "Shield" in item['name']:
                        shield5 += item['quantity']
                    if "Lv.8" in item['name'] and "Weapon" in item['name']:
                        weapon1 += item['quantity']
                    if "Lv.8" in item['name'] and "Armor" in item['name']:
                        protector1 += item['quantity']
                    if "Lv.8" in item['name'] and "Accessory" in item['name']:
                        accessory1 += item['quantity']
                    if "Lv.8" in item['name'] and "Shield" in item['name']:
                        shield1 += item['quantity']
                    if "Lv.9" in item['name'] and "Weapon" in item['name']:
                        weapon2 += item['quantity']
                    if "Lv.9" in item['name'] and "Armor" in item['name']:
                        protector2 += item['quantity']
                    if "Lv.9" in item['name'] and "Accessory" in item['name']:
                        accessory2 += item['quantity']
                    if "Lv.9" in item['name'] and "Shield" in item['name']:
                        shield2 += item['quantity']
                    if "Lv.10" in item['name'] and "Weapon" in item['name']:
                        weapon3 += item['quantity']
                    if "Lv.10" in item['name'] and "Armor" in item['name']:
                        protector3 += item['quantity']
                    if "Lv.10" in item['name'] and "Accessory" in item['name']:
                        accessory3 += item['quantity']
                    if "Lv.10" in item['name'] and "Shield" in item['name']:
                        shield3 += item['quantity']
                    if "Lv.11" in item['name'] and "Weapon" in item['name']:
                        weapon4 += item['quantity']
                    if "Lv.11" in item['name'] and "Armor" in item['name']:
                        protector4 += item['quantity']
                    if "Lv.11" in item['name'] and "Accessory" in item['name']:
                        accessory4 += item['quantity']
                    if "Lv.11" in item['name'] and "Shield" in item['name']:
                        shield4 += item['quantity']
                    if "12th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                        eweapon1 += item['quantity']
                    if "12th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                        eprotector1 += item['quantity']
                    if "12th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                        eaccessory1 += item['quantity']
                    if "12th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                        eshield1 += item['quantity']
                    if "13th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                        eweapon2 += item['quantity']
                    if "13th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                        eprotector2 += item['quantity']
                    if "13th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                        eaccessory2 += item['quantity']
                    if "13th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                        eshield2 += item['quantity']
                    if "14th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                        eweapon3 += item['quantity']
                    if "14th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                        eprotector3 += item['quantity']
                    if "14th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                        eaccessory3 += item['quantity']
                    if "14th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                        eshield3 += item['quantity']
                    if "15th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                        eweapon4 += item['quantity']
                    if "15th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                        eprotector4 += item['quantity']
                    if "15th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                        eaccessory4 += item['quantity']
                    if "15th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                        eshield4 += item['quantity']
                    if "16th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                        eweapon5 += item['quantity']
                    if "16th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                        eprotector5 += item['quantity']
                    if "16th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                        eaccessory5 += item['quantity']
                    if "16th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                        eshield5 += item['quantity']
                    if "17th Grade Enhancer" in item['name'] and "Weapon" in item['name']:
                        eweapon6 += item['quantity']
                    if "17th Grade Enhancer" in item['name'] and "Armor" in item['name']:
                        eprotector6 += item['quantity']
                    if "17th Grade Enhancer" in item['name'] and "Accessory" in item['name']:
                        eaccessory6 += item['quantity']
                    if "17th Grade Enhancer" in item['name'] and "Shield" in item['name']:
                        eshield6 += item['quantity']
                    if "Flower" in item['name'] and "Evil" in item['name']:
                        flowerevil += item['quantity']
                    if "Flower" in item['name'] and "Illusion" in item['name']:
                        flowerillusion += item['quantity']
                    if "Flower" in item['name'] and "Life" in item['name']:
                        flowerlife += item['quantity']
                    if "Flower" in item['name'] and "Energy" in item['name']:
                        flowerenergy += item['quantity']
                    if "Flower" in item['name'] and "Whirling" in item['name']:
                        flowerwhirling += item['quantity']
                    if "ITEM_ETC_ARENA_COIN" in item['servername']:
                        arena += item['quantity']
                    if "ITEM_ETC_SD_TOKEN_04" in item['servername']:
                        qgold += item['quantity']
                    if "ITEM_ETC_SD_TOKEN_03" in item['servername']:
                        silver += item['quantity']
                    if "ITEM_ETC_SD_TOKEN_02" in item['servername']:
                        iron += item['quantity']
                    if "ITEM_ETC_SD_TOKEN_01" in item['servername']:
                        copper += item['quantity']
                    if "ITEM_ETC_SURVIVAL_ARENA_PARTY_COIN" in item['servername']:
                        combativeness1 += item['quantity']
                    if "ITEM_ETC_SURVIVAL_ARENA_SOLO_COIN" in item['servername']:
                        combativeness2 += item['quantity']
                    if "Alchemy catalyst" in item['name']:
                        catalyst += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_STR_11" in item['servername']:
                        str11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_STR_10" in item['servername']:
                        str10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_STR_09" in item['servername']:
                        str9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_STR_08" in item['servername']:
                        str8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_INT_11" in item['servername']:
                        int11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_INT_10" in item['servername']:
                        int10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_INT_09" in item['servername']:
                        int9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_INT_08" in item['servername']:
                        int8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_DUR_11" in item['servername']:
                        master11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_DUR_10" in item['servername']:
                        master10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_DUR_09" in item['servername']:
                        master9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_DUR_08" in item['servername']:
                        master8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_HR_11" in item['servername']:
                        strikes11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_HR_10" in item['servername']:
                        strikes10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_HR_09" in item['servername']:
                        strikes9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_HR_08" in item['servername']:
                        strikes8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_BLOCK_11" in item['servername']:
                        discipline11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_BLOCK_10" in item['servername']:
                        discipline10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_BLOCK_09" in item['servername']:
                        discipline9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_BLOCK_08" in item['servername']:
                        discipline8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_CRITICAL_11" in item['servername']:
                        penetration11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_CRITICAL_10" in item['servername']:
                        penetration10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_CRITICAL_09" in item['servername']:
                        penetration9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_EVADE_CRITICAL_08" in item['servername']:
                        penetration8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ER_11" in item['servername']:
                        dodging11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ER_10" in item['servername']:
                        dodging10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ER_09" in item['servername']:
                        dodging9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ER_08" in item['servername']:
                        dodging8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_HP_11" in item['servername']:
                        stamina11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_HP_10" in item['servername']:
                        stamina10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_HP_09" in item['servername']:
                        stamina9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_HP_08" in item['servername']:
                        stamina8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_MP_11" in item['servername']:
                        magic11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_MP_10" in item['servername']:
                        magic10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_MP_09" in item['servername']:
                        magic9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_MP_08" in item['servername']:
                        magic8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_FROSTBITE_11" in item['servername']:
                        fogs11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_FROSTBITE_10" in item['servername']:
                        fogs10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_FROSTBITE_09" in item['servername']:
                        fogs9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_FROSTBITE_08" in item['servername']:
                        fogs8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ESHOCK_11" in item['servername']:
                        air11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ESHOCK_10" in item['servername']:
                        air10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ESHOCK_09" in item['servername']:
                        air9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ESHOCK_08" in item['servername']:
                        air8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_BURN_11" in item['servername']:
                        fire11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_BURN_10" in item['servername']:
                        fire10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_BURN_09" in item['servername']:
                        fire9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_BURN_08" in item['servername']:
                        fire8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_POISON_11" in item['servername']:
                        immunity11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_POISON_10" in item['servername']:
                        immunity10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_POISON_09" in item['servername']:
                        immunity9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_POISON_08" in item['servername']:
                        immunity8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ZOMBIE_11" in item['servername']:
                        revival11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ZOMBIE_10" in item['servername']:
                        revival10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ZOMBIE_09" in item['servername']:
                        revival9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_ZOMBIE_08" in item['servername']:
                        revival8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PA_11" in item['servername']:
                        courage11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PA_10" in item['servername']:
                        courage10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PA_09" in item['servername']:
                        courage9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PA_08" in item['servername']:
                        courage8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PASTR_11" in item['servername']:
                        warriors11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PASTR_10" in item['servername']:
                        warriors10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PASTR_09" in item['servername']:
                        warriors9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PASTR_08" in item['servername']:
                        warriors8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MA_11" in item['servername']:
                        philosophy11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MA_10" in item['servername']:
                        philosophy10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MA_09" in item['servername']:
                        philosophy9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MA_08" in item['servername']:
                        philosophy8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAINT_11" in item['servername']:
                        meditation11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAINT_10" in item['servername']:
                        meditation10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAINT_09" in item['servername']:
                        meditation9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAINT_08" in item['servername']:
                        meditation8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_CRITICAL_11" in item['servername']:
                        challenge11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_CRITICAL_10" in item['servername']:
                        challenge10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_CRITICAL_09" in item['servername']:
                        challenge9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_CRITICAL_08" in item['servername']:
                        challenge8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_HR_11" in item['servername']:
                        focus11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_HR_10" in item['servername']:
                        focus10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_HR_09" in item['servername']:
                        focus9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_HR_08" in item['servername']:
                        focus8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PD_11" in item['servername']:
                        flesh11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PD_10" in item['servername']:
                        flesh10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PD_09" in item['servername']:
                        flesh9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PD_08" in item['servername']:
                        flesh8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PDSTR_11" in item['servername']:
                        life11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PDSTR_10" in item['servername']:
                        life10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PDSTR_09" in item['servername']:
                        life9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PDSTR_08" in item['servername']:
                        life8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MD_11" in item['servername']:
                        mind11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MD_10" in item['servername']:
                        mind10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MD_09" in item['servername']:
                        mind9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MD_08" in item['servername']:
                        mind8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MDINT_11" in item['servername']:
                        spirit11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MDINT_10" in item['servername']:
                        spirit10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MDINT_09" in item['servername']:
                        spirit9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MDINT_08" in item['servername']:
                        spirit8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_ER_11" in item['servername']:
                        dodgings11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_ER_10" in item['servername']:
                        dodgings10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_ER_09" in item['servername']:
                        dodgings9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_ER_08" in item['servername']:
                        dodgings8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_BR_11" in item['servername']:
                        agility11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_BR_10" in item['servername']:
                        agility10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_BR_09" in item['servername']:
                        agility9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_BR_08" in item['servername']:
                        agility8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PAR_11" in item['servername']:
                        training11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PAR_10" in item['servername']:
                        training10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PAR_09" in item['servername']:
                        training9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_PAR_08" in item['servername']:
                        training8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAR_11" in item['servername']:
                        prayer11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAR_10" in item['servername']:
                        prayer10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAR_09" in item['servername']:
                        prayer9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_ATTRSTONE_MAR_08" in item['servername']:
                        prayer8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_LUCK_08" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_LUCK_08" in item['servername']:
                        luckst8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_SOLID_08" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_SOLID_08" in item['servername']:
                        steadyst8 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_LUCK_09" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_LUCK_09" in item['servername']:
                        luckst9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_SOLID_09" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_SOLID_09" in item['servername']:
                        steadyst9 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_LUCK_10" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_LUCK_10" in item['servername']:
                        luckst10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_SOLID_10" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_SOLID_10" in item['servername']:
                        steadyst10 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_LUCK_11" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_LUCK_11" in item['servername']:
                        luckst11 += item['quantity']
                    if "ITEM_ETC_ARCHEMY_MAGICSTONE_SOLID_11" in item['servername'] or "ITEM_EVENT_ARCHEMY_MAGICSTONE_SOLID_11" in item['servername']:
                        steadyst11 += item['quantity']
                    if "ITEM_ETC_E060517_MON_GENERATION_BOX" in item['servername'] or "ITEM_EVENT_GENERATION_BOX" in item['servername'] or "ITEM_EVENT_RENT_E100222_MON_GENERATION_BOX" in item['servername']:
                        pandora += item['quantity']
                    if "ITEM_ETC_E060517_SUMMON_PARTY_SCROLL" in item['servername'] or "ITEM_ETC_E060526_SUMMON_PARTY_SCROLL_A" in item['servername'] or "ITEM_EVENT_RENT_E100222_SUMMON_SCROLL" in item['servername']:
                        ms += item['quantity']
                    if "ITEM_ETC_E090121_LUCKYBOX" in item['servername'] or "ITEM_ETC_E120118_LUCKYBOX" in item['servername']:
                        luckybox += item['quantity']
                    if "ITEM_ETC_E070523_LEFT_HEART" in item['servername']:
                        pledge1 += item['quantity']
                    if "ITEM_ETC_E070523_RIGHT_HEART" in item['servername']:
                        pledge2 += item['quantity']
                    if "AliBaba Seal" in item['name']:
                        alibabaseal += item['quantity']
                    if "Rubber Piece" in item['name']:
                        rubber += item['quantity']
                    if "T (Event Item)" in item['name']:
                        T1 += item['quantity']
                    if "H (Event Item)" in item['name']:
                        T2 += item['quantity']
                    if "A (Event Item)" in item['name']:
                        T3 += item['quantity']
                    if "N (Event Item)" in item['name']:
                        T4 += item['quantity']
                    if "K (Event Item)" in item['name']:
                        T5 += item['quantity']
                    if "S (Event Item)" in item['name']:
                        T6 += item['quantity']
                    if "Snow flake" in item['name']:
                        snowflake += item['quantity']
                    if "Halloween Candy" in item['name']:
                        halloweencandy += item['quantity']
                    if "Berserker Regeneration Potion" in item['name']:
                        berserker += item['quantity']
                    if "ITEM_ETC_E090722_" in item['servername'] and "ICECREAM" in item['servername']:
                        cream += item['quantity']
                    if "Genie’s Lamp" in item['name']:
                        lamp += item['quantity']
                    if "Dirty Lamp" in item['name']:
                        dLamp += item['quantity']
                    if "ITEM_TALISMAN_TOGUI_RED_TEARS" in item['servername']:
                        card1 += item['quantity']
                    if "ITEM_TALISMAN_TOGUI_WESTERN_SCRIPTURES" in item['servername']:
                        card2 += item['quantity']
                    if "ITEM_TALISMAN_TOGUI_TOGUI_MASK" in item['servername']:
                        card3 += item['quantity']
                    if "ITEM_TALISMAN_TOGUI_RED_TALISMAN" in item['servername']:
                        card4 += item['quantity']
                    if "ITEM_TALISMAN_TOGUI_PUPPETS" in item['servername']:
                        card5 += item['quantity']
                    if "ITEM_TALISMAN_TOGUI_KITCHEN_KNIFE" in item['servername']:
                        card6 += item['quantity']
                    if "ITEM_TALISMAN_TOGUI_ELDER_STAFF" in item['servername']:
                        card7 += item['quantity']
                    if "ITEM_TALISMAN_TOGUI_SPELL_PAPERS" in item['servername']:
                        card8 += item['quantity']
                    if "ITEM_TALISMAN_FLAME_FIRE_FLOWER" in item['servername']:
                        card9 += item['quantity']
                    if "ITEM_TALISMAN_FLAME_HORNED_CATTLE" in item['servername']:
                        card10 += item['quantity']
                    if "ITEM_TALISMAN_FLAME_FLAME_OF_OBLIVION" in item['servername']:
                        card11 += item['quantity']
                    if "ITEM_TALISMAN_FLAME_FLAME_PAPERS" in item['servername']:
                        card12 += item['quantity']
                    if "ITEM_TALISMAN_FLAME_HEARTHSTONE_FLAME" in item['servername']:
                        card13 += item['quantity']
                    if "ITEM_TALISMAN_FLAME_ENCHANTRESS_NECKLACE" in item['servername']:
                        card14 += item['quantity']
                    if "ITEM_TALISMAN_FLAME_HONGHAEAH_ARMOR" in item['servername']:
                        card15 += item['quantity']
                    if "ITEM_TALISMAN_FLAME_FIRE_DRAGON_SWORD" in item['servername']:
                        card16 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_A_SILVER_PENDANT" in item['servername']:
                        card17 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_A_COBALT_EMERALD" in item['servername']:
                        card18 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_A_LOGBOOK" in item['servername']:
                        card19 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_A_LOVE_LETTER" in item['servername']:
                        card20 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_A_PORTRAIT_WOMAN" in item['servername']:
                        card21 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_A_JEWELRY_BOX" in item['servername']:
                        card22 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_A_DIAMOND_WATCHES" in item['servername']:
                        card23 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_A_MERMAID_TEARS" in item['servername']:
                        card24 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_B_BROKEN_KEY" in item['servername']:
                        card25 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_B_LARGE_TONGS" in item['servername']:
                        card26 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_B_PHANTOM_HALF" in item['servername']:
                        card27 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_B_EVIL_HEART" in item['servername']:
                        card28 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_B_REVENGEFUL_SPIRIT_BEADS" in item['servername']:
                        card29 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_B_HOOK_HAND" in item['servername']:
                        card30 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_B_SERENITY_TEARS" in item['servername']:
                        card31 += item['quantity']
                    if "ITEM_TALISMAN_WRECK_B_COMMANDER_PATCH" in item['servername']:
                        card32 += item['quantity']
                    if "ITEM_ETC_SKILLPOINT_STONE" in item['servername']:
                        faded += item['quantity']
                    if 'SET_A_RARE' in item['servername']:
                        aGrade += 1
                    if 'SET_B_RARE' in item['servername']:
                        bGrade += 1
                    if "ITEM_MALL_GLOBAL_CHATTING" in item['servername'] or "ITEM_ETC_GLOBAL_CHATTING_BASIC" in item['servername'] or "ITEM_EVENT_RENT_GLOBAL_CHATTING" in item['servername'] or "ITEM_EVENT_GLOBAL_CHATTING" in item['servername'] or "ITEM_EVENT_GLOBAL_CHATTING_SUPPORT" in item['servername']:
                        chatglobal += item['quantity']
                    if "ITEM_MALL_GLOBAL_CHATTING_2" in item['servername'] or "ITEM_EVENT_GLOBAL_CHATTING_2" in item['servername']:
                        chatglobalvip += item['quantity']
                    if "ITEM_MALL_REVERSE_RETURN_SCROLL" in item['servername'] or "ITEM_EVENT_REVERSE_RETURN_SCROLL" in item['servername'] or "ITEM_EVENT_RENT_REVERSE_RETURN_SCROLL" in item['servername'] or "ITEM_EVENT_REVERSE_RETURN_SCROLL_BASIC" in item['servername'] or "ITEM_EVENT_REVERSE_RETURN_SCROLL_SUPPORT" in item['servername']:
                        reversesc += item['quantity']
                    if "ITEM_COS_P_EXTENSION" in item['servername'] or "ITEM_EVENT_RENT_COS_P_EXTENSION" in item['servername'] or "ITEM_COS_P_EXTENSION_1D" in item['servername'] or "ITEM_EVENT_COS_P_EXTENSION_3D" in item['servername'] or "ITEM_EVENT_COS_P_EXTENSION_7D" in item['servername']:
                        clocksc += item['quantity']
                    if "ITEM_MALL_NASRUN_EXTENSION" in item['servername'] or "ITEM_EVENT_NASRUN_EXTENSION" in item['servername'] or "ITEM_EVENT_RENT_NASRUN_EXTENSION" in item['servername'] or "ITEM_EVENT_NASRUN_EXTENSION_3DAY" in item['servername'] or "ITEM_EVENT_NASRUN_EXTENSION_7DAY" in item['servername'] or "ITEM_EVENT_NASRUN_EXTENSION_28DAY" in item['servername']:
                        devilres += item['quantity']
                    if "ITEM_MALL_PREMIUM_GOLDTIME" in item['servername'] or "ITEM_MALL_PREMIUM_GLOBAL_GOLDTIME" in item['servername'] or "ITEM_MALL_PREMIUM_GLOBAL_GOLDTIME_PLUS" in item['servername'] or "ITEM_EVENT_PREMIUM_GOLDTIME" in item['servername'] or "ITEM_EVENT_PREMIUM_GLOBAL_GOLDTIME_PLUS" in item['servername'] or "ITEM_ETC_PREMIUM_GLOBAL_GOLDTIME_PLUS_SUPPORT" in item['servername'] or "ITEM_MALL_PREMIUM_GLOBAL_GOLDTIME_PLUS_2" in item['servername']:
                        preplus += item['quantity']
                    if "ITEM_MALL_REPAIR_HAMMER" in item['servername'] or "ITEM_EVENT_REPAIR_HAMMER" in item['servername'] or "ITEM_EVENT_REPAIR_HAMMER_SUPPORT" in item['servername']:
                        repairhammer += item['quantity']
                    if "Magic stone of Astral" in item['name'] and "(Lvl.08)" in item['name']:
                        astral8 += item['quantity']
                    if "Magic stone of Astral" in item['name'] and "(Lvl.09)" in item['name']:
                        astral9 += item['quantity']
                    if "Magic stone of Astral" in item['name'] and "(Lvl.10)" in item['name']:
                        astral10 += item['quantity']
                    if "Magic stone of Astral" in item['name'] and "(Lvl.11)" in item['name']:
                        astral11 += item['quantity']
                    if "Magic stone of immortal" in item['name'] and "(Lvl.08)" in item['name']:
                        immortal8 += item['quantity']
                    if "Magic stone of immortal" in item['name'] and "(Lvl.09)" in item['name']:
                        immortal9 += item['quantity']
                    if "Magic stone of immortal" in item['name'] and "(Lvl.10)" in item['name']:
                        immortal10 += item['quantity']
                    if "Magic stone of immortal" in item['name'] and "(Lvl.11)" in item['name']:
                        immortal11 += item['quantity']
                    if "ITEM_MALL_INVENTORY_ADDITION" in item['servername'] or "ITEM_EVENT_INVENTORY_ADDITION" in item['servername']:
                        inventorysc += item['quantity']
                    if "ITEM_MALL_WAREHOUSE_ADDITION" in item['servername'] or "ITEM_EVENT_WAREHOUSE_ADDITION" in item['servername']:
                        storagesc += item['quantity']
                    if "ITEM_MALL_TRADE_MAGICRUNE_SEAL" in item['servername'] or "ITEM_EVENT_TRADE_MAGICRUNE_SEAL" in item['servername']:
                        jobblue += item['quantity']
                    if "ITEM_MALL_TRADE_STRENTHRUNE_SEAL" in item['servername'] or "ITEM_EVENT_TRADE_STRENTHRUNE_SEAL" in item['servername']:
                        jobartı += item['quantity']
                    if "ITEM_ETC_LEVEL_TOKEN_01" in item['servername']:
                        token1 += item['quantity']
                    if "ITEM_ETC_LEVEL_TOKEN_02" in item['servername']:
                        token2 += item['quantity']
                    if "ITEM_ETC_LEVEL_TOKEN_03" in item['servername']:
                        token3 += item['quantity']
                    if "Increase Strength" in item['name'] or "Gücü Arttır" in item['name']:
                        petstr += item['quantity']
                    if "Increase Intelligence" in item['name'] or "Zekayı Arttır" in item['name']:
                        petint += item['quantity']

    if arg == "ElixirInc":
        send_response(player,f"Incomplete Weapon {weapon5} , Incomplete Armor {protector5} , Incomplete Shield {shield5} , Incomplete Accessory {accessory5}")
    if arg == "Elixir8":
        send_response(player,f"8DG Elixir; Weapon {weapon1} , Armor {protector1} , Shield {shield1} , Accessory {accessory1}")
    if arg == "Elixir9":
        send_response(player,f"9DG Elixir; Weapon {weapon2} , Armor {protector2} , Shield {shield2} , Accessory {accessory2}")
    if arg == "Elixir10":
        send_response(player,f"10DG Elixir; Weapon {weapon3} , Armor {protector3} , Shield {shield3} , Accessory {accessory3}")
    if arg == "Elixir11":
        send_response(player,f"11DG Elixir; Weapon {weapon4} , Armor {protector4} , Shield {shield4} , Accessory {accessory4}")
    if arg == "Enhancer12":
        send_response(player,f"12DG ENHANCER; Weapon {eweapon1} , Armor {eprotector1} , Shield {eshield1} , Accessory {eaccessory1}")
    if arg == "Enhancer13":
        send_response(player,f"13DG ENHANCER; Weapon {eweapon2} , Armor {eprotector2} , Shield {eshield2} , Accessory {eaccessory2}")
    if arg == "Enhancer14":
        send_response(player,f"14DG ENHANCER; Weapon {eweapon3} , Armor {eprotector3} , Shield {eshield3} , Accessory {eaccessory3}")
    if arg == "Enhancer15":
        send_response(player,f"15DG ENHANCER; Weapon {eweapon4} , Armor {eprotector4} , Shield {eshield4} , Accessory {eaccessory4}")
    if arg == "Enhancer16":
        send_response(player,f"16DG ENHANCER; Weapon {eweapon5} , Armor {eprotector5} , Shield {eshield5} , Accessory {eaccessory5}")
    if arg == "Enhancer17":
        send_response(player,f"17DG ENHANCER; Weapon {eweapon6} , Armor {eprotector6} , Shield {eshield6} , Accessory {eaccessory6}")
    if arg == "Flowerall":
        send_response(player,f"Flower; Life {flowerlife} , Energy {flowerenergy} , Evil {flowerevil} , Illusion {flowerillusion} , Whirling {flowerwhirling}")
    if arg == "Combatii":
        send_response(player,f"Coin of Combativeness (Party) {combativeness1} , Coin of Combativeness (Individual) {combativeness2}")
    if arg == "8Blue":
        send_response(player,f"8DG STR {str8} , INT {int8} , MASTER {master8} , STRIKES {strikes8} , DSCPLNE {discipline8} , PNTRTON {penetration8} , DODGING {dodging8} , STAMINA {stamina8}")
    if arg == "9Blue":
        send_response(player,f"9DG STR {str9} , INT {int9} , MASTER {master9} , STRIKES {strikes9} , DSCPLNE {discipline9} , PNTRTON {penetration9} , DODGING {dodging9} , STAMINA {stamina9}")
    if arg == "10Blue":
        send_response(player,f"10DG STR {str10} , INT {int10} , MASTER {master10} , STRIKES {strikes10} , DSCPLNE {discipline10} , PNTRTON {penetration10} , DODGING {dodging10} , STAMINA {stamina10}")
    if arg == "11Blue":
        send_response(player,f"11DG STR {str11} , INT {int11} , MASTER {master11} , STRIKES {strikes11} , DSCPLNE {discipline11} , PNTRTON {penetration11} , DODGING {dodging11} , STAMINA {stamina11}")
    if arg == "8Blue2":
        send_response(player,f"8DG MAGIC {magic8} , FOGS {fogs8} , AIR {air8} , FIRE {fire8} , IMMUNITY {immunity8} , REVIVAL {revival8}")
    if arg == "9Blue2":
        send_response(player,f"9DG MAGIC {magic9} , FOGS {fogs9} , AIR {air9} , FIRE {fire9} , IMMUNITY {immunity9} , REVIVAL {revival9}")
    if arg == "10Blue2":
        send_response(player,f"10DG MAGIC {magic10} , FOGS {fogs10} , AIR {air10} , FIRE {fire10} , IMMUNITY {immunity10} , REVIVAL {revival10}")
    if arg == "11Blue2":
        send_response(player,f"11DG MAGIC {magic11} , FOGS {fogs11} , AIR {air11} , FIRE {fire11} , IMMUNITY {immunity11} , REVIVAL {revival11}")
    if arg == "8Stat":
        send_response(player,f"8DG COURAGE {courage8} , WARRIORS {warriors8} , PHILOSOPHY {philosophy8} , MEDITATION {meditation8} , CHALLENGE {challenge8} , FOCUS {focus8} , FLESH {flesh8}")
    if arg == "9Stat":
        send_response(player,f"9DG COURAGE {courage9} , WARRIORS {warriors9} , PHILOSOPHY {philosophy9} , MEDITATION {meditation9} , CHALLENGE {challenge9} , FOCUS {focus9} , FLESH {flesh9}")
    if arg == "10Stat":
        send_response(player,f"10DG COURAGE {courage10} , WARRIORS {warriors10} , PHILOSOPHY {philosophy10} , MEDITATION {meditation10} , CHALLENGE {challenge10} , FOCUS {focus10} , FLESH {flesh10}")
    if arg == "11Stat":
        send_response(player,f"11DG COURAGE {courage11} , WARRIORS {warriors11} , PHILOSOPHY {philosophy11} , MEDITATION {meditation11} , CHALLENGE {challenge11} , FOCUS {focus11} , FLESH {flesh11}")
    if arg == "8Stat2":
        send_response(player,f"8DG LIFE {life8} , MIND {mind8} , SPIRIT {spirit8} , DODGING {dodgings8} , AGILITY {agility8} , TRAINING {training8} , PRAYER {prayer8}")
    if arg == "9Stat2":
        send_response(player,f"9DG LIFE {life9} , MIND {mind9} , SPIRIT {spirit9} , DODGING {dodgings9} , AGILITY {agility9} , TRAINING {training9} , PRAYER {prayer9}")
    if arg == "10Stat2":
        send_response(player,f"10DG LIFE {life10} , MIND {mind10} , SPIRIT {spirit10} , DODGING {dodgings10} , AGILITY {agility10} , TRAINING {training10} , PRAYER {prayer10}")
    if arg == "11Stat2":
        send_response(player,f"11DG LIFE {life11} , MIND {mind11} , SPIRIT {spirit11} , DODGING {dodgings11} , AGILITY {agility11} , TRAINING {training11} , PRAYER {prayer11}")
    if arg == "Coin":
        send_response(player,f"Gold Coin {qgold} , Silver Coin {silver} , Iron Coin {iron} , Copper Coin {copper} , Arena Coin {arena}")
    if arg == "Catalyst":
        send_response(player,f"Alchemy Catalyst {catalyst}")
    if arg == "Cream":
        send_response(player,f"Ice Cream {cream}")
    if arg == "luckyboxx":
        send_response(player,f"Lucky Box {luckybox}")
    if arg == "Pledges":
        send_response(player,f"Pledge of Love(Left) {pledge1} , Pledge of Love(Right) {pledge2}")
    if arg == "Pandora":
        send_response(player,f"Pandora {pandora}")
    if arg == "alibabaseall":
        send_response(player,f"AliBaba Seal {alibabaseal}")
    if arg == "Rubberr":
        send_response(player,f"Rubber Piece {rubber}")
    if arg == "Thanks":
        send_response(player,f"T > {T1} , H > {T2} , A > {T3} , N > {T4} , K > {T5} , S > {T6}")
    if arg == "Snoww":
        send_response(player,f"Snow flake {snowflake}")
    if arg == "halloweencandyy":
        send_response(player,f"Halloween Candy {halloweencandy}")
    if arg == "Zerk":
        send_response(player,f"Berserker Regeneration Potion {berserker}")
    if arg == "Ms":
        send_response(player,f"Monster Summon Scroll {ms}")
    if arg == "luck8":
        send_response(player,f"Magic stone of luck {luckst8}")
    if arg == "steady8":
        send_response(player,f"Magic stone of steady {steadyst8}")
    if arg == "luck9":
        send_response(player,f"Magic stone of luck {luckst9}")
    if arg == "steady9":
        send_response(player,f"Magic stone of steady {steadyst9}")
    if arg == "luck10":
        send_response(player,f"Magic stone of luck {luckst10}")
    if arg == "steady10":
        send_response(player,f"Magic stone of steady {steadyst10}")
    if arg == "luck11":
        send_response(player,f"Magic stone of luck {luckst11}")
    if arg == "steady11":
        send_response(player,f"Magic stone of steady {steadyst11}")
    if arg == "Lamp":
        send_response(player,f"Genie’s Lamp {lamp} -- Dirty Lamp {dLamp}")
    if arg == "fgw8dgeasy":
        send_response(player,f"Red tears{card1} , Western scriptures {card2} , Togui mask {card3} , Red talisman {card4} , Puppet {card5} , Dull kitchen knife {card6}")
    if arg == "fgw8dghard":
        send_response(player,f"Elder staff {card7} , Spell paper {card8}")
    if arg == "fgw9dgeasy":
        send_response(player,f"Fire flower {card9} , Horned cattle {card10} , Flame of oblivion {card11} , Flame paper {card12} , Hearthstone flame {card13} , Enchantress necklace {card14}")
    if arg == "fgw9dghard":
        send_response(player,f"Honghaeah armor {card15} , Fire dragon sword {card16}")
    if arg == "fgw10dgeasy":
        send_response(player,f"Silver pendant {card17} , Cobalt emerald {card18} , Logbook {card19} , Love letter {card20} , Portrait of a woman {card21} , Jewelry box {card22}")
    if arg == "fgw10dghard":
        send_response(player,f"Diamond watch {card23} , Mermaid’s tears {card24}")
    if arg == "fgw11dgeasy":
        send_response(player,f"Broken Key {card25} , Large tong {card26} , Phantom harp {card27} , Evil’s heart {card28} , Vindictive sprit’s bead {card29} , Hook hand {card30}")
    if arg == "fgw11dghard":
        send_response(player,f"Sereness’s tears {card31} , Commander’s patch {card32}")
    if arg == "faded":
        send_response(player,f"Faded Bead {faded}")
    if arg == "SetA":
        send_response(player, f"{aGrade} Parca Egpty A Esyasi")
    if arg == "SetB":
        send_response(player, f"{bGrade} Parca Egpty B Esyasi")
    if arg == "chatglobal":
        send_response(player,f"Global Chat {chatglobal}")
    if arg == "chatglobalvip":
        send_response(player,f"Global Chat VIP {chatglobalvip}")
    if arg == "reversesc":
        send_response(player,f"Reverse Return Scroll {reversesc}")
    if arg == "clocksc":
        send_response(player,f"Clock of Reincarnation {clocksc}")
    if arg == "devilres":
        send_response(player,f"Extension gear {devilres}")
    if arg == "preplus":
        send_response(player,f"Premium Gold Time PLUS {preplus}")
    if arg == "repairhammer":
        send_response(player,f"Repair hammer {repairhammer}")
    if arg == "astral":
        send_response(player,f"Astral (Lvl.8)= {astral8} , (Lvl.9)= {astral9} , (Lvl.10)= {astral10} , (Lvl.11)= {astral11}")
    if arg == "immortal":
        send_response(player,f"Immortal (Lvl.8)= {immortal8} , (Lvl.9)= {immortal9} , (Lvl.10)= {immortal10} , (Lvl.11)= {immortal11}")
    if arg == "inventorysc":
        send_response(player,f"Inventory expansion item {inventorysc}")
    if arg == "storagesc":
        send_response(player,f"Storage expansion item {storagesc}")
    if arg == "jobblue":
        send_response(player,f"Sealed Magic Rune {jobblue}")
    if arg == "jobartı":
        send_response(player,f"Sealed Reinforcement Rune {jobartı}")
    if arg == "token1":
        send_response(player,f"Monk's Token {token1}")
    if arg == "token2":
        send_response(player,f"Soldier's Token {token2}")
    if arg == "token3":
        send_response(player,f"General's Token {token3}")
    if arg == "petstr":
        send_response(player,f"Increase Strength {petstr}")
    if arg == "petint":
        send_response(player,f"Increase Intelligence {petint}")

def get_sox_counts():
    sox_inventory = 0
    sox_pet = 0
    sox_storage = 0

    def is_sox(item):
        if item and 'servername' in item:
            sn = item['servername']
            return 'RARE' in sn and 'EVENT' not in sn and 'ARCHEMY' not in sn and 'ITEM_TRADE' not in sn
        return False

    inventory = get_inventory()
    if inventory and 'items' in inventory:
        inventory_items = inventory['items'][13:]
        for item in inventory_items:
            if is_sox(item):
                sox_inventory += 1

    pets = get_pets()
    if pets:
        for p_info in pets.values():
            if p_info.get('type') == 'pick' and 'items' in p_info:
                 for item in p_info['items']:
                     if is_sox(item):
                         sox_pet += 1

    storage = get_storage()
    if storage and 'items' in storage:
        storage_items = storage['items']
        for item in storage_items:
            if is_sox(item):
                sox_storage += 1

    return sox_inventory, sox_pet, sox_storage

def handle_chat(t, player, msg):
    if player and lstLeaders_exist(player) or t == 100:
        if msg == "ENV":
            try:
                inventory_data = get_inventory()
                if inventory_data and 'items' in inventory_data and 'size' in inventory_data and isinstance(inventory_data['items'], list) and isinstance(inventory_data['size'], int):
                    total_slots = inventory_data['size']
                    equipment_slots_count = 13
                    inventory_slots_count = total_slots - equipment_slots_count
                    free_slots = 0
                    if inventory_slots_count > 0 and len(inventory_data['items']) >= total_slots:
                        inventory_items_slice = inventory_data['items'][equipment_slots_count:total_slots]
                        for item_in_slot in inventory_items_slice:
                            if item_in_slot == {}:
                                free_slots += 1
                        occupied_slots = inventory_slots_count - free_slots
                        send_response(player, f"Bos Alan: {free_slots} ----> Dolu: {occupied_slots}/{inventory_slots_count} (Toplam Yuva: {total_slots})")
                    elif inventory_slots_count <= 0:
                         log(f"Hata (ENV): Hesaplanan envanter slot sayisi ({inventory_slots_count}) gecerli değil.")
                         send_response(player, "Envanter slot sayisi hesaplanamadi.")
                    else:
                         log(f"Hata (ENV): Items listesi ({len(inventory_data['items'])}) raporlanan boyuttan ({total_slots}) kısa.")
                         send_response(player, "Envanter verisi tutarsız.")
                else:
                    log("Hata (ENV): Envanter bilgisi alinamadi veya format hatali.")
                    send_response(player, "Envanter bilgisi alinamadi.")
            except Exception as e:
                log(f"Hata (ENV): Komut islenirken bir istisna olustu: {e}\n{traceback.format_exc()}")
                send_response(player, "ENV komutu islenirken bir hata olustu.")

        elif msg == "DEPO":
            try:
                storage_data = get_storage()
                if storage_data and 'items' in storage_data and isinstance(storage_data['items'], list) and 'size' in storage_data and isinstance(storage_data['size'], int):

                    reported_size = storage_data['size']
                    storage_items = storage_data['items']
                    actual_items_length = len(storage_items)
                    effective_size = reported_size
                    if actual_items_length != reported_size:
                        log(f"UYARI (DEPO): Depo items listesi uzunlugu ({actual_items_length}) raporlanan boyutla ({reported_size}) eslesmiyor! Gerçek liste uzunlugu ({actual_items_length}) kullaniliyor.")
                        effective_size = actual_items_length 
                    free_slots = 0
                    if effective_size > 0 :
                         free_slots = storage_items[:effective_size].count({})
                         occupied_slots = effective_size - free_slots
                         send_response(player, f"Depo Bos Alan: {free_slots} ----> Dolu: {occupied_slots}/{effective_size}")
                    else:
                         send_response(player, f"Depo Bos Alan: 0 ----> Dolu: 0/0")
                else:
                    log("Hata (DEPO): Depo bilgisi alinamadi veya format hatali.")
                    send_response(player, "Depo bilgisi alinamadi.")
            except Exception as e:
                log(f"Hata (DEPO): Komut islenirken bir istisna olustu: {e}\n{traceback.format_exc()}")
                send_response(player, "DEPO komutu islenirken bir hata olustu.")

        elif msg == "EXP":
            try:
                data = get_character_data()
                if data and 'current_exp' in data and 'level' in data and 'max_exp' in data and data['max_exp'] > 0:
                    currentExp = data['current_exp']
                    level = data['level']
                    maxExp = data['max_exp']
                    exp_percentage = (100.0 * currentExp) / maxExp
                    send_response(player, f"Seviye: {level} - EXP: %{exp_percentage:.2f}")
                else:
                    send_response(player, "Karakter EXP bilgisi alinamadi.")
            except Exception as e:
                log(f"Hata (EXP): {e}")
                send_response(player, "EXP komutu islenirken hata olustu.")

        elif msg == "JOBINFO":
            char_data = get_character_data()
            if char_data:
                try:
                    job_name = char_data.get('job_name', 'N/A')
                    job_level = char_data.get('job_level', 0)
                    job_type = char_data.get('job_type', 'N/A')
                    job_current_exp = char_data.get('job_current_exp', 0)
                    job_max_exp = char_data.get('job_max_exp', 1)
                    if job_max_exp > 0:
                        currentJobExp = (job_current_exp / job_max_exp) * 100
                    else:
                        currentJobExp = 100 if job_current_exp > 0 else 0
                    message = f"JOB Nick: {job_name}, JOB Seviye: {job_level}, JOB Tipi: {job_type}, JOB Exp: {currentJobExp:.2f}%"
                    send_response(player, message)

                except KeyError as e:
                    log(f"Hata: Karakter verisinde eksik anahtar: {e}")
                    send_response(player, f"JOB bilgileri alinirken bir sorun olustu (Eksik veri: {e}).")
                except Exception as e:
                    log(f"Hata (JOBINFO): {e}\n{traceback.format_exc()}")
                    send_response(player, "JOB bilgileri islenirken beklenmedik bir hata olustu.")
            else:
                log("Hata (JOBINFO): Karakter verisi alinamadı.")
                send_response(player, "Karakter verileri alınamadı.")

        elif msg == "GOLD":
            try:
                chars = get_character_data()
                if chars and 'gold' in chars:
                    gold = chars['gold']
                    goldS = f"{gold:,}"
                    send_response(player, f"Envanterde {goldS} Altin var.") # Açıklama güncellendi
                else:
                    send_response(player, "Envanter Altin bilgisi alinamadi.")
            except Exception as e:
                log(f"Hata (GOLD): {e}")
                send_response(player, "GOLD komutu islenirken hata olustu.")
        
        elif msg == "GOLDGUILD":
            try:
                guild_storage_data = get_guild_storage()
                if guild_storage_data and 'gold' in guild_storage_data:
                    gold = guild_storage_data['gold']
                    goldS = f"{gold:,}"
                    send_response(player, f"Guild Deposunda {goldS} Altin var.")
                elif guild_storage_data is None:
                     send_response(player, "Guild Deposu bilgisi alinamadi (Muhtemelen depoya henüz erisilmedi).")
                else:
                    send_response(player, "Guild Deposu Altin bilgisi alinamadi (Veri formatı beklenenden farklı olabilir).")
            except Exception as e:
                log(f"Hata (GOLDG): Komut islenirken bir istisna olustu: {e}\n{traceback.format_exc()}")
                send_response(player, "GOLDGUILD komutu islenirken bir hata olustu.")

        elif msg == "GOLDDEPO":
            try:
                storage_data = get_storage()
                if storage_data and 'gold' in storage_data:
                    gold = storage_data['gold']
                    goldS = f"{gold:,}"
                    send_response(player, f"Depoda {goldS} Altin var.")
                elif storage_data is None:
                     send_response(player, "Depo bilgisi alinamadi (Muhtemelen depoya henüz erisilmedi).")
                else:
                    send_response(player, "Depo Altin bilgisi alinamadi (Veri formatı beklenenden farklı olabilir).")
            except Exception as e:
                log(f"Hata (GOLDD): Komut islenirken bir istisna olustu: {e}\n{traceback.format_exc()}")
                send_response(player, "GOLDDEPO komutu islenirken bir hata olustu.")

        elif msg == "JOBBOX":
            try:
                pouch = get_job_pouch()
                if pouch and "items" in pouch:
                    items = pouch["items"]
                    total_quantity = 0
                    total_slots = len(items)
                    max_capacity_per_slot = 5

                    for item in items:
                        if item is not None and "quantity" in item:
                            total_quantity += item["quantity"]

                    max_total_capacity = total_slots * max_capacity_per_slot
                    send_response(player, f"Specialty -> {total_quantity} / {max_total_capacity} ({total_slots} slot)")
                else:
                    send_response(player, "Meslek cantasi bilgisi alinamadi.")
            except Exception as e:
                log(f"Hata (JOBBOX): {e}")
                send_response(player, "JOBBOX komutu islenirken hata olustu.")

        elif msg == "SP":
            try:
                chars = get_character_data()
                if chars and 'sp' in chars:
                    sp = chars['sp']
                    spS = f"{sp:,}"
                    send_response(player, f"Su an {spS} Skill Point var.")
                else:
                    send_response(player, "SP bilgisi alinamadi.")
            except Exception as e:
                log(f"Hata (SP): {e}")
                send_response(player, "SP komutu islenirken hata olustu.")

        elif msg == "SOX":
            try:
                inv_count, pet_count, storage_count = get_sox_counts()
                response_message = f"Envanter > ( {inv_count} ) , Pet > ( {pet_count} ) , Depo > ( {storage_count} )"
                send_response(player, response_message)
            except Exception as e:
                log(f"Hata (SOX): Komut islenirken bir istisna olustu: {e}\n{traceback.format_exc()}")
                send_response(player, "SOX komutu islenirken bir hata olustu.")

        elif msg == "INCELX": checkInv("ElixirInc", player)
        elif msg == "8ELX": checkInv("Elixir8", player)
        elif msg == "9ELX": checkInv("Elixir9", player)
        elif msg == "10ELX": checkInv("Elixir10", player)
        elif msg == "11ELX": checkInv("Elixir11", player)
        elif msg == "ENH12": checkInv("Enhancer12", player)
        elif msg == "ENH13": checkInv("Enhancer13", player)
        elif msg == "ENH14": checkInv("Enhancer14", player)
        elif msg == "ENH15": checkInv("Enhancer15", player)
        elif msg == "ENH16": checkInv("Enhancer16", player)
        elif msg == "ENH17": checkInv("Enhancer17", player)
        elif msg == "8BLUE": checkInv("8Blue", player)
        elif msg == "9BLUE": checkInv("9Blue", player)
        elif msg == "10BLUE": checkInv("10Blue", player)
        elif msg == "11BLUE": checkInv("11Blue", player)
        elif msg == "8BLUE2": checkInv("8Blue2", player)
        elif msg == "9BLUE2": checkInv("9Blue2", player)
        elif msg == "10BLUE2": checkInv("10Blue2", player)
        elif msg == "11BLUE2": checkInv("11Blue2", player)
        elif msg == "8STAT": checkInv("8Stat", player)
        elif msg == "9STAT": checkInv("9Stat", player)
        elif msg == "10STAT": checkInv("10Stat", player)
        elif msg == "11STAT": checkInv("11Stat", player)
        elif msg == "8STAT2": checkInv("8Stat2", player)
        elif msg == "9STAT2": checkInv("9Stat2", player)
        elif msg == "10STAT2": checkInv("10Stat2", player)
        elif msg == "11STAT2": checkInv("11Stat2", player)
        elif msg == "FLOWER": checkInv("Flowerall", player)
        elif msg == "PANDORA": checkInv("Pandora", player)
        elif msg == "8LUCK": checkInv("luck8", player)
        elif msg == "9LUCK": checkInv("luck9", player)
        elif msg == "10LUCK": checkInv("luck10", player)
        elif msg == "11LUCK": checkInv("luck11", player)
        elif msg == "8STEADY": checkInv("steady8", player)
        elif msg == "9STEADY": checkInv("steady9", player)
        elif msg == "10STEADY": checkInv("steady10", player)
        elif msg == "11STEADY": checkInv("steady11", player)
        elif msg == "MONSTER": checkInv("Ms", player)
        elif msg == "ICE": checkInv("Cream", player)
        elif msg == "LUCKYBOX": checkInv("luckyboxx", player)
        elif msg == "PLEDGE": checkInv("Pledges", player)
        elif msg == "ALIBABA": checkInv("alibabaseall", player)
        elif msg == "RUBBER": checkInv("Rubberr", player)
        elif msg == "THANKS": checkInv("Thanks", player)
        elif msg == "FLAKE": checkInv("Snoww", player)
        elif msg == "HALLOWEN": checkInv("halloweencandyy", player)
        elif msg == "ZERK": checkInv("Zerk", player)
        elif msg == "LAMP": checkInv("Lamp", player)
        elif msg == "COIN": checkInv("Coin", player)
        elif msg == "COMBATI": checkInv("Combatii", player)
        elif msg == "CATA": checkInv("Catalyst", player)
        elif msg == "8FGW1": checkInv("fgw8dgeasy", player)
        elif msg == "8FGW2": checkInv("fgw8dghard", player)
        elif msg == "9FGW1": checkInv("fgw9dgeasy", player)
        elif msg == "9FGW2": checkInv("fgw9dghard", player)
        elif msg == "10FGW1": checkInv("fgw10dgeasy", player)
        elif msg == "10FGW2": checkInv("fgw10dghard", player)
        elif msg == "11FGW1": checkInv("fgw11dgeasy", player)
        elif msg == "11FGW2": checkInv("fgw11dghard", player)
        elif msg == "FADED": checkInv("faded", player)
        elif msg == "SETA": checkInv("SetA", player)
        elif msg == "SETB": checkInv("SetB", player)
        elif msg == "GLOBALSC": checkInv("chatglobal", player)
        elif msg == "VIPGLOBAL": checkInv("chatglobalvip", player)
        elif msg == "REVSC": checkInv("reversesc", player)
        elif msg == "CLOCKSC": checkInv("clocksc", player)
        elif msg == "DEVILSC": checkInv("devilres", player)
        elif msg == "PREPLUS": checkInv("preplus", player)
        elif msg == "HAMMER": checkInv("repairhammer", player)
        elif msg == "ASTRAL": checkInv("astral", player)
        elif msg == "IMMORTAL": checkInv("immortal", player)
        elif msg == "ENVANTERSC": checkInv("inventorysc", player)
        elif msg == "STORAGESC": checkInv("storagesc", player)
        elif msg == "JOBBLUE": checkInv("jobblue", player)
        elif msg == "JOBARTI": checkInv("jobartı", player)
        elif msg == "TOKEN1": checkInv("token1", player)
        elif msg == "TOKEN2": checkInv("token2", player)
        elif msg == "TOKEN3": checkInv("token3", player)
        elif msg == "PETSTR": checkInv("petstr", player)
        elif msg == "PETINT": checkInv("petint", player)

def GetPluginsFolder():
    return os.path.dirname(os.path.realpath(__file__))

log(f'Eklenti: {name} başarıyla yüklendi.')

config_path = getPath()
if os.path.exists(config_path):
    loadConfigs()
else:
    try:
        os.makedirs(config_path)
        log(f'TR_InventoryCounter: Klasör oluşturuldu: phBot/Config/TR_InventoryCounter')
    except Exception as e:
        log(f'Hata: {name} klasörü oluşturulamadı: {e}')
