from phBot import *
import QtBind

name = 'TR_CountDrop'
version = 2.0
NewestVersion = 0
gui = QtBind.init(__name__, name)

lblCizgi1 = QtBind.createList(gui,6,8,147,280)
lblCizgi2 = QtBind.createLabel(gui,'________________________',6,18)
lTITAN = QtBind.createLabel(gui,'TITAN DROPS',40,10)
lBRP = QtBind.createLabel(gui,'Berserker R. Potion',11,40)
lSTRScroll = QtBind.createLabel(gui,'STR Increase Scroll',11,55)
lINTScroll = QtBind.createLabel(gui,'INT Increase Scroll',11,70)
lHPScroll = QtBind.createLabel(gui,'HP Increase Scroll',11,85)
lMPScroll = QtBind.createLabel(gui,'MP Increase Scroll',11,100)
lHitScroll = QtBind.createLabel(gui,'Hit Scroll',11,115)
lDodgingScroll = QtBind.createLabel(gui,'Dodging Scroll',11,130)
lTriggerScroll = QtBind.createLabel(gui,'Trigger Scroll',11,145)
lsceva = QtBind.createLabel(gui,'Scroll of Evasion',11,160)
lscacc = QtBind.createLabel(gui,'Scroll of Accuracy',11,175)
lPandoraBox = QtBind.createLabel(gui,'Pandora Box',11,190)
lMonsterSc = QtBind.createLabel(gui,'Monster Summon Scroll',11,205)
lCatalyst = QtBind.createLabel(gui,'Alchemy catalyst',11,220)
lTicketSt = QtBind.createLabel(gui,'Ticket',11,235)
lBlueSt = QtBind.createLabel(gui,'Blue Stone',11,250)
lBlackSt = QtBind.createLabel(gui,'Black Stone',11,265)
qBRP = QtBind.createLabel(gui,'0',130,40)
qSTRScroll = QtBind.createLabel(gui,'0',130,55)
qINTScroll = QtBind.createLabel(gui,'0',130,70)
qHPScroll = QtBind.createLabel(gui,'0',130,85)
qMPScroll = QtBind.createLabel(gui,'0',130,100)
qHitScroll = QtBind.createLabel(gui,'0',130,115)
qDodgingScroll = QtBind.createLabel(gui,'0',130,130)
qTriggerScroll = QtBind.createLabel(gui,'0',130,145)
qsceva = QtBind.createLabel(gui,'0',130,160)
qscacc = QtBind.createLabel(gui,'0',130,175)
qPandoraBox = QtBind.createLabel(gui,'0',130,190)
qMonsterSc = QtBind.createLabel(gui,'0',130,205)
qCatalyst = QtBind.createLabel(gui,'0',130,220)
qTicketSt = QtBind.createLabel(gui,'0',130,235)
qBlueSt = QtBind.createLabel(gui,'0',130,250)
qBlackSt = QtBind.createLabel(gui,'0',130,265)

lblCizgi3 = QtBind.createList(gui,158,8,147,280)
lblCizgi4 = QtBind.createLabel(gui,'________________________',158,18)
lAttStones = QtBind.createLabel(gui,'ATTRIBUTE STONES',180,10)
lCourage = QtBind.createLabel(gui,'Courage',164,40)
lPhilosophy = QtBind.createLabel(gui,'Philosophy',164,55)
lFocus = QtBind.createLabel(gui,'Focus',164,70)
lChallenge = QtBind.createLabel(gui,'Challenge',164,85)
lAgility = QtBind.createLabel(gui,'Agility',164,100)
lWarriors = QtBind.createLabel(gui,'Warriors',164,115)
lMeditation = QtBind.createLabel(gui,'Meditation',164,130)
lFlesh = QtBind.createLabel(gui,'Flesh',164,145)
lMind = QtBind.createLabel(gui,'Mind',164,160)
lDodging = QtBind.createLabel(gui,'Dodging',164,175)
lLife = QtBind.createLabel(gui,'Life',164,190)
lSpirit = QtBind.createLabel(gui,'Spirit',164,205)
lTraining = QtBind.createLabel(gui,'Training',164,220)
lPrayer = QtBind.createLabel(gui,'Prayer',164,235)
qcourage = QtBind.createLabel(gui,'0',265,40)
qphilosophy = QtBind.createLabel(gui,'0',265,55)
qfocus = QtBind.createLabel(gui,'0',265,70)
qchallenge = QtBind.createLabel(gui,'0',265,85)
qagility = QtBind.createLabel(gui,'0',265,100)
qwarriors = QtBind.createLabel(gui,'0',265,115)
qmeditation = QtBind.createLabel(gui,'0',265,130)
qflesh = QtBind.createLabel(gui,'0',265,145)
qmind = QtBind.createLabel(gui,'0',265,160)
qdodging = QtBind.createLabel(gui,'0',265,175)
qlife = QtBind.createLabel(gui,'0',265,190)
qspirit = QtBind.createLabel(gui,'0',265,205)
qtraining = QtBind.createLabel(gui,'0',265,220)
qprayer = QtBind.createLabel(gui,'0',265,235)

lblCizgi5 = QtBind.createList(gui,310,8,150,280)
lblCizgi6 = QtBind.createLabel(gui,'_________________________',310,18)
lMagStones = QtBind.createLabel(gui,'MAGIC STONES',344,10)
lSTR = QtBind.createLabel(gui,'Str',317,40)
lINT = QtBind.createLabel(gui,'Int',317,55)
lMaster = QtBind.createLabel(gui,'Master',317,70)
lStrikes = QtBind.createLabel(gui,'Strikes',317,85)
lDiscipline = QtBind.createLabel(gui,'Discipline',317,100)
lPenetration = QtBind.createLabel(gui,'Penetration',317,115)
lDodging2 = QtBind.createLabel(gui,'Dodging',317,130)
lStamina = QtBind.createLabel(gui,'Stamina',317,145)
lMagic = QtBind.createLabel(gui,'Magic',317,160)
lFogs = QtBind.createLabel(gui,'Fogs',317,175)
lAir = QtBind.createLabel(gui,'Air',317,190)
lFire = QtBind.createLabel(gui,'Fire',317,205)
lImmunity = QtBind.createLabel(gui,'Immunity',317,220)
lRevival = QtBind.createLabel(gui,'Revival',317,235)
lLuck = QtBind.createLabel(gui,'Luck',317,250)
lSteady = QtBind.createLabel(gui,'Steady',317,265)
qstr = QtBind.createLabel(gui,'0',418,40)
qint = QtBind.createLabel(gui,'0',418,55)
qmaster = QtBind.createLabel(gui,'0',418,70)
qstrikes = QtBind.createLabel(gui,'0',418,85)
qdiscipline = QtBind.createLabel(gui,'0',418,100)
qpenetration = QtBind.createLabel(gui,'0',418,115)
qdodging2 = QtBind.createLabel(gui,'0',418,130)
qstamina = QtBind.createLabel(gui,'0',418,145)
qmagic = QtBind.createLabel(gui,'0',418,160)
qfogs = QtBind.createLabel(gui,'0',418,175)
qair = QtBind.createLabel(gui,'0',418,190)
qfire = QtBind.createLabel(gui,'0',418,205)
qimmunity = QtBind.createLabel(gui,'0',418,220)
qrevival = QtBind.createLabel(gui,'0',418,235)
qluck = QtBind.createLabel(gui,'0',418,250)
qsteady = QtBind.createLabel(gui,'0',418,265)

lblCizgi7 = QtBind.createList(gui,555,100,150,190)
lblCizgi8 = QtBind.createLabel(gui,'_________________________',555,110)
lElixirs = QtBind.createLabel(gui,'ELIXIRS',610,105)
lWeapon = QtBind.createLabel(gui,'Weapon',565,125)
lProtector = QtBind.createLabel(gui,'Protector',565,140)
lAccessory = QtBind.createLabel(gui,'Accessory',565,155)
lShield = QtBind.createLabel(gui,'Shield',565,170)
qweapon = QtBind.createLabel(gui,'0',684,125)
qprotector = QtBind.createLabel(gui,'0',684,140)
qaccessory = QtBind.createLabel(gui,'0',684,155)
qshield = QtBind.createLabel(gui,'0',684,170)

lblCizgi9 = QtBind.createLabel(gui,'_________________________',555,175)
lblCizgi10 = QtBind.createLabel(gui,'_________________________',555,195)
lCoins = QtBind.createLabel(gui,'COINS',610,190)
lArenaC = QtBind.createLabel(gui,'Arena Coin',565,210)
lGoldC = QtBind.createLabel(gui,'Gold Coin',565,225)
lSilverC = QtBind.createLabel(gui,'Silver Coin',565,240)
lCopperC = QtBind.createLabel(gui,'Copper Coin',565,255)
lIronC = QtBind.createLabel(gui,'Iron Coin',565,270)
qarena = QtBind.createLabel(gui,'0',684,210)
qgold = QtBind.createLabel(gui,'0',684,225)
qsilver = QtBind.createLabel(gui,'0',684,240)
qcopper = QtBind.createLabel(gui,'0',684,255)
qiron = QtBind.createLabel(gui,'0',684,270)

lblCizgi11 = QtBind.createList(gui,540,20,180,75)
lKontrol = QtBind.createLabel(gui,'Nereye bakmak istersin?',570,4)

btnStorage = QtBind.createButton(gui,'btnStorage_clicked'," Depo! ",550,60)
btnGuildStorage = QtBind.createButton(gui,'btnGuildStorage_clicked'," Guild Depo!",630,60,)

btnInventory = QtBind.createButton(gui,'btnInventory_clicked'," Envanter! ",550,29)
btnPet = QtBind.createButton(gui,'btnPet_clicked'," Toplama Pet! ",630,29)

leDegree = QtBind.createLineEdit(gui,"11",470,150,19,19)
lDegree = QtBind.createLabel(gui,'Degree',494,153)

def btnPet_clicked():
	countIn = 'pet'
	countItems(countIn)
def btnStorage_clicked():
	countIn = 'Storage'
	countItems(countIn)

def btnGuildStorage_clicked():
	countIn = 'GuildStorage'
	countItems(countIn)

def btnInventory_clicked():
	countIn = 'Inventory'
	countItems(countIn)

def countItems(countIn):
    BRP = 0
    STRScroll = 0
    INTScroll = 0
    PandoraBox = 0
    MonsterSc = 0
    Catalyst = 0
    HPScroll = 0
    MPScroll = 0
    HitScroll = 0
    DodgingScroll = 0
    TriggerScroll = 0
    sceva = 0
    scacc = 0
    courage = 0
    philosophy = 0
    focus = 0
    challenge = 0
    agility = 0
    warriors = 0
    meditation = 0
    flesh = 0
    mind = 0
    pdodging = 0
    life = 0
    spirit = 0
    training = 0
    prayer = 0
    Str = 0
    Int = 0
    master = 0
    strikes = 0
    discipline = 0
    penetration = 0
    gdodging = 0
    stamina = 0
    magic = 0
    fogs = 0
    air = 0
    fire = 0
    immunity = 0
    revival = 0
    luck = 0
    steady = 0
    weapon = 0
    protector = 0
    accessory = 0
    shield = 0
    gold = 0
    silver = 0
    arena = 0
    copper = 0
    iron = 0
    TicketSt = 0
    BlueSt = 0
    BlackSt = 0
    items = []
    
    if countIn == 'Storage':
        items = get_storage()['items']
    elif countIn == 'GuildStorage':
        items = get_guild_storage()['items']
    elif countIn == 'Inventory':
        items = get_inventory()['items']
    elif countIn == 'pet':
        items = get_pets()
        for key in items:
            if items[key]['type'] == 'pick':
                items = items[key]['items']
    degree = str(QtBind.text(gui, leDegree))
    if items != []:
        for item in items:
            if item != None and degree in item['name'] and 'tablet' not in item['name'] and 'stone' in item['name']:
                if "courage" in item['name']:
                    courage += item['quantity']
                elif "philosophy" in item['name']:
                    philosophy += item['quantity']
                elif "focus" in item['name']:
                    focus += item['quantity']
                elif "challenge" in item['name']:
                    challenge += item['quantity']
                elif "agility" in item['name']:
                    agility += item['quantity']
                elif "warriors" in item['name']:
                    warriors += item['quantity']
                elif "meditation" in item['name']:
                    meditation += item['quantity']
                elif "flesh" in item['name']:
                    flesh += item['quantity']
                elif "mind" in item['name']:
                    mind += item['quantity']
                elif "Attribute stone of dodging" in item['name']:
                    pdodging += item['quantity']
                elif "life" in item['name']:
                    life += item['quantity']
                elif "spirit" in item['name']:
                    spirit += item['quantity']
                elif "training" in item['name']:
                    training += item['quantity']
                elif "prayer" in item['name']:
                    prayer += item['quantity']
                elif "Str" in item['name']:
                    Str += item['quantity']
                elif "Int" in item['name']:
                    Int += item['quantity']
                elif "master" in item['name']:
                    master += item['quantity']
                elif "strikes" in item['name']:
                    strikes += item['quantity']
                elif "discipline" in item['name']:
                    discipline += item['quantity']
                elif "penetration" in item['name']:
                    penetration += item['quantity']
                elif "Magic stone of dodging" in item['name']:
                    gdodging += item['quantity']
                elif "stamina" in item['name']:
                    stamina += item['quantity']
                elif "magic" in item['name']:
                    magic += item['quantity']
                elif "fogs" in item['name']:
                    fogs += item['quantity']
                elif "air" in item['name']:
                    air += item['quantity']
                elif "immunity" in item['name']:
                    immunity += item['quantity']
                elif "revival" in item['name']:
                    revival += item['quantity']
                elif "fire" in item['name']:
                    fire += item['quantity']
                elif "steady" in item['name']:
                    steady += item['quantity']
                elif "luck" in item['name']:
                    luck += item['quantity']
            if item != None and "Berserker" in item['name'] and "Potion" in item['name']:
                BRP += item['quantity']
            if item != None and "Strength" in item['name'] and "Scroll" in item['name']:
                STRScroll += item['quantity']
            if item != None and "Intelligence" in item['name'] and "Scroll" in item['name']:
                INTScroll += item['quantity']
            if item != None and "Pandora's Box" in item['name']:
                PandoraBox += item['quantity']
            if item != None and "Monster Summon Scroll" in item['name']:
                MonsterSc += item['quantity']
            if item != None and "Alchemy" in item['name'] and "catalyst" in item['name']:
                Catalyst += item['quantity']
            if item != None and "HP" in item['name'] and "Scroll" in item['name']:
                HPScroll += item['quantity']
            if item != None and "MP" in item['name'] and "Scroll" in item['name']:
                MPScroll += item['quantity']
            if item != None and "Hit" in item['name'] and "Scroll" in item['name']:
                HitScroll += item['quantity']
            if item != None and "Dodging" in item['name'] and "Scroll" in item['name']:
                DodgingScroll += item['quantity']
            if item != None and "Trigger" in item['name'] and "Scroll" in item['name']:
                TriggerScroll += item['quantity']
            if item != None and "Scroll" in item['name'] and "Evasion" in item['name']:
                sceva += item['quantity']
            if item != None and "Scroll" in item['name'] and "Accuracy" in item['name']:
                scacc += item['quantity']
            if item != None and "Intensifing" in item['name'] and "(Weapon)" in item['name']:
                weapon += item['quantity']
            if item != None and "Intensifing" in item['name'] and "(Protector)" in item['name']:
                protector += item['quantity']
            if item != None and "Intensifing" in item['name'] and "(Accessory)" in item['name']:
                accessory += item['quantity']
            if item != None and "Intensifing" in item['name'] and "(Shield)" in item['name']:
                shield += item['quantity']
            if item != None and "Coin" in item['name'] and "Gold" in item['name']:
                gold += item['quantity']
            if item != None and "Coin" in item['name'] and "Silver" in item['name']:
                silver += item['quantity']
            if item != None and "Coin" in item['name'] and "Copper" in item['name']:
                copper += item['quantity']
            if item != None and "Coin" in item['name'] and "Iron" in item['name']:
                iron += item['quantity']
            if item != None and "Ticket" in item['name']:
                TicketSt += item['quantity']
            if item != None and "Blue" in item['name'] and "Stone" in item['name']:
                BlueSt += item['quantity']
            if item != None and "Black" in item['name'] and "Stone" in item['name']:
                BlackSt += item['quantity']
    QtBind.setText(gui, qBRP, str(BRP))
    QtBind.setText(gui, qSTRScroll, str(STRScroll))
    QtBind.setText(gui, qINTScroll, str(INTScroll))
    QtBind.setText(gui, qPandoraBox, str(PandoraBox))
    QtBind.setText(gui, qMonsterSc, str(MonsterSc))
    QtBind.setText(gui, qCatalyst, str(Catalyst))
    QtBind.setText(gui, qHPScroll, str(HPScroll))
    QtBind.setText(gui, qMPScroll, str(MPScroll))
    QtBind.setText(gui, qHitScroll, str(HitScroll))
    QtBind.setText(gui, qDodgingScroll, str(DodgingScroll))
    QtBind.setText(gui, qTriggerScroll, str(TriggerScroll))
    QtBind.setText(gui, qsceva, str(sceva))
    QtBind.setText(gui, qscacc, str(scacc))
    QtBind.setText(gui, qcourage, str(courage))
    QtBind.setText(gui, qphilosophy, str(philosophy))
    QtBind.setText(gui, qfocus, str(focus))
    QtBind.setText(gui, qchallenge, str(challenge))
    QtBind.setText(gui, qagility, str(agility))
    QtBind.setText(gui, qwarriors, str(warriors))
    QtBind.setText(gui, qmeditation, str(meditation))
    QtBind.setText(gui, qflesh, str(flesh))
    QtBind.setText(gui, qmind, str(mind))
    QtBind.setText(gui, qdodging, str(pdodging))
    QtBind.setText(gui, qlife, str(life))
    QtBind.setText(gui, qspirit, str(spirit))
    QtBind.setText(gui, qtraining, str(training))
    QtBind.setText(gui, qprayer, str(prayer))
    QtBind.setText(gui, qstr, str(Str))
    QtBind.setText(gui, qint, str(Int))
    QtBind.setText(gui, qmaster, str(master))
    QtBind.setText(gui, qstrikes, str(strikes))
    QtBind.setText(gui, qdiscipline, str(discipline))
    QtBind.setText(gui, qpenetration, str(penetration))
    QtBind.setText(gui, qdodging2, str(gdodging))
    QtBind.setText(gui, qstamina, str(stamina))
    QtBind.setText(gui, qmagic, str(magic))
    QtBind.setText(gui, qfire, str(fire))
    QtBind.setText(gui, qair, str(air))
    QtBind.setText(gui, qfogs, str(fogs))
    QtBind.setText(gui, qrevival, str(revival))
    QtBind.setText(gui, qimmunity, str(immunity))
    QtBind.setText(gui, qluck, str(luck))
    QtBind.setText(gui, qsteady, str(steady))
    QtBind.setText(gui, qweapon, str(weapon))
    QtBind.setText(gui, qprotector, str(protector))
    QtBind.setText(gui, qaccessory, str(accessory))
    QtBind.setText(gui, qshield, str(shield))
    QtBind.setText(gui, qgold, str(gold))
    QtBind.setText(gui, qsilver, str(silver))
    QtBind.setText(gui, qarena, str(arena))
    QtBind.setText(gui, qcopper, str(copper))
    QtBind.setText(gui, qiron, str(iron))
    QtBind.setText(gui, qTicketSt, str(TicketSt))
    QtBind.setText(gui, qBlueSt, str(BlueSt))
    QtBind.setText(gui, qBlackSt, str(BlackSt))

def CheckForUpdate():
	global NewestVersion
	if NewestVersion == 0:
		try:
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_CountDrops.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8")).split()
				for num, line in enumerate(lines):
					if line == 'version':
						NewestVersion = int(lines[num+2].replace(".",""))
						CurrentVersion = int(str(version).replace(".",""))
						if NewestVersion > CurrentVersion:
							log('Eklenti : Yeni bir güncelleme var = [%s]!' % name)
							lblUpdate = QtBind.createLabel(gui,'Yeni Bir Güncelleme Mevcut. Yüklemek için Tıkla ->',100,290)
							button1 = QtBind.createButton(gui, 'button_update', ' Güncelle ', 350, 288)
		except:
			pass

def button_update():
	path = get_config_dir()[:-7]
	if os.path.exists(path + "Plugins/" + "TR_CountDrops.py"):
		try:
			os.rename(path + "Plugins/" + "TR_CountDrops.py", path + "Plugins/" + "TR_CountDropsBACKUP.py")
			req = urllib.request.Request('https://raw.githubusercontent.com/hakankahya48/EklentiTRSRO/main/TR_CountDrops.py', headers={'User-Agent': 'Mozilla/5.0'})
			with urllib.request.urlopen(req) as f:
				lines = str(f.read().decode("utf-8"))
				with open(path + "Plugins/" + "TR_CountDrops.py", "w+") as f:
					f.write(lines)
					os.remove(path + "Plugins/" + "TR_CountDropsBACKUP.py")
					log('Eklenti Başarıyla Güncellendi, Kullanmak için Eklentiyi Yeniden Yükleyin.')
		except Exception as ex:
			log('Güncelleme Hatası [%s] Lütfen Manuel Olarak Güncelleyin veya daha Sonra Tekrar Deneyin.' %ex)

CheckForUpdate()

log('Eklenti: %s v%s Yuklendi. // edit by hakankahya' % (name,version))
