from phBot import *
import QtBind

gui = QtBind.init(__name__,'xDropSayac')
metaby = QtBind.createLabel(gui,'edited by hakankahya',15,295)
lLIST = QtBind.createLabel(gui,'________________________',9,14)
Etkinlik = QtBind.createLabel(gui,'ETKİNLIK ESYALARI',20,9)
lSTRScroll = QtBind.createLabel(gui,'STR Scroll',16,30)
lINTScroll = QtBind.createLabel(gui,'INT Scroll',16,45)
lHPScroll = QtBind.createLabel(gui,'HP Scroll',16,60)
lMPScroll = QtBind.createLabel(gui,'MP Scroll',16,75)
lHitScroll = QtBind.createLabel(gui,'Hit Scroll',16,90)
lDodgingScroll = QtBind.createLabel(gui,'Dodging Scroll',16,105)
lTriggerScroll = QtBind.createLabel(gui,'Trigger Scroll',16,120)
lsceva = QtBind.createLabel(gui,'Scroll of Evasion',16,135)
lscacc = QtBind.createLabel(gui,'Scroll of Accuracy',16,150)
pandora = QtBind.createLabel(gui,'Pandora Box',16,165)
monster = QtBind.createLabel(gui,'Monster Scroll',16,180)
bluestone = QtBind.createLabel(gui,'Blue Stone',16,200)
blackstone = QtBind.createLabel(gui,'Black Stone',16,215)
ticketstone = QtBind.createLabel(gui,'Ticket',16,230)
qSTRScroll = QtBind.createLabel(gui,'0',110,30)
qINTScroll = QtBind.createLabel(gui,'0',110,45)
qHPScroll = QtBind.createLabel(gui,'0',110,60)
qMPScroll = QtBind.createLabel(gui,'0',110,75)
qHitScroll = QtBind.createLabel(gui,'0',110,90)
qDodgingScroll = QtBind.createLabel(gui,'0',110,105)
qTriggerScroll = QtBind.createLabel(gui,'0',110,120)
qsceva = QtBind.createLabel(gui,'0',110,135)
qscacc = QtBind.createLabel(gui,'0',110,150)
qpandora = QtBind.createLabel(gui,'0',110,165)
qmonster = QtBind.createLabel(gui,'0',110,180)
qbluestone = QtBind.createLabel(gui,'0',110,200)
qblackstone = QtBind.createLabel(gui,'0',110,215)
qticketstone = QtBind.createLabel(gui,'0',110,230)

lLIST = QtBind.createLabel(gui,'_______________________',153,14)
lAttStones = QtBind.createLabel(gui,'STAT STONELERI',148,9)
lCourage = QtBind.createLabel(gui,'Courage',140,30)
lPhilosophy = QtBind.createLabel(gui,'Philosophy',140,45)
lFocus = QtBind.createLabel(gui,'Focus',140,60)
lChallenge = QtBind.createLabel(gui,'Challenge',140,75)
lAgility = QtBind.createLabel(gui,'Agility',140,90)
lWarriors = QtBind.createLabel(gui,'Warriors',140,105)
lMeditation = QtBind.createLabel(gui,'Meditation',140,120)
lFlesh = QtBind.createLabel(gui,'Flesh',140,135)
lMind = QtBind.createLabel(gui,'Mind',140,150)
lDodging = QtBind.createLabel(gui,'Dodging',140,165)
lLife = QtBind.createLabel(gui,'Life',140,180)
lSpirit = QtBind.createLabel(gui,'Spirit',140,195)
lTraining = QtBind.createLabel(gui,'Training',140,210)
lPrayer = QtBind.createLabel(gui,'Prayer',140,225)
qcourage = QtBind.createLabel(gui,'0',225,30)
qphilosophy = QtBind.createLabel(gui,'0',225,45)
qfocus = QtBind.createLabel(gui,'0',225,60)
qchallenge = QtBind.createLabel(gui,'0',225,75)
qagility = QtBind.createLabel(gui,'0',225,90)
qwarriors = QtBind.createLabel(gui,'0',225,105)
qmeditation = QtBind.createLabel(gui,'0',225,120)
qflesh = QtBind.createLabel(gui,'0',225,135)
qmind = QtBind.createLabel(gui,'0',225,150)
qdodging = QtBind.createLabel(gui,'0',225,165)
qlife = QtBind.createLabel(gui,'0',225,180)
qspirit = QtBind.createLabel(gui,'0',225,195)
qtraining = QtBind.createLabel(gui,'0',225,210)
qprayer = QtBind.createLabel(gui,'0',225,225)

LIST = QtBind.createLabel(gui,'______________',280,14)
lMagStones = QtBind.createLabel(gui,'BLUE STONELERI',265,9)
lSTR = QtBind.createLabel(gui,'Str',255,30)
lINT = QtBind.createLabel(gui,'Int',255,45)
lMaster = QtBind.createLabel(gui,'Master',255,60)
lStrikes = QtBind.createLabel(gui,'Strikes',255,75)
lDiscipline = QtBind.createLabel(gui,'Discipline',255,90)
lPenetration = QtBind.createLabel(gui,'Penetration',255,105)
lDodging2 = QtBind.createLabel(gui,'Dodging',255,120)
lStamina = QtBind.createLabel(gui,'Stamina',255,135)
lMagic = QtBind.createLabel(gui,'Magic',255,150)
lFogs = QtBind.createLabel(gui,'Fogs',255,165)
lAir = QtBind.createLabel(gui,'Air',255,180)
lFire = QtBind.createLabel(gui,'Fire',255,195)
lImmunity = QtBind.createLabel(gui,'Immunity',255,210)
lRevival = QtBind.createLabel(gui,'Revival',255,225)
lLuck = QtBind.createLabel(gui,'Luck',255,240)
lSteady = QtBind.createLabel(gui,'Steady',255,255)
qstr = QtBind.createLabel(gui,'0',340,30)
qint = QtBind.createLabel(gui,'0',340,45)
qmaster = QtBind.createLabel(gui,'0',340,60)
qstrikes = QtBind.createLabel(gui,'0',340,75)
qdiscipline = QtBind.createLabel(gui,'0',340,90)
qpenetration = QtBind.createLabel(gui,'0',340,105)
qdodging2 = QtBind.createLabel(gui,'0',340,120)
qstamina = QtBind.createLabel(gui,'0',340,135)
qmagic = QtBind.createLabel(gui,'0',340,150)
qfogs = QtBind.createLabel(gui,'0',340,165)
qair = QtBind.createLabel(gui,'0',340,180)
qfire = QtBind.createLabel(gui,'0',340,195)
qimmunity = QtBind.createLabel(gui,'0',340,210)
qrevival = QtBind.createLabel(gui,'0',340,225)
qluck = QtBind.createLabel(gui,'0',340,240)
qsteady = QtBind.createLabel(gui,'0',340,255)

lLIST = QtBind.createLabel(gui,'________________',363,14)
lElixirs = QtBind.createLabel(gui,'ELIXIRLER',382,9)
lWeapon = QtBind.createLabel(gui,'Weapon',370,30)
lProtector = QtBind.createLabel(gui,'Protector',370,45)
lAccessory = QtBind.createLabel(gui,'Accessory',370,60)
lShield = QtBind.createLabel(gui,'Shield',370,75)
qweapon = QtBind.createLabel(gui,'0',440,30)
qprotector = QtBind.createLabel(gui,'0',440,45)
qaccessory = QtBind.createLabel(gui,'0',440,60)
qshield = QtBind.createLabel(gui,'0',440,75)

lCoins = QtBind.createLabel(gui,'COINLER',385,105)
lLIST = QtBind.createLabel(gui,'_________________',360,110)
lArenaC = QtBind.createLabel(gui,'Arena Coin',370,130)
lGoldC = QtBind.createLabel(gui,'Gold Coin',370,145)
lSilverC = QtBind.createLabel(gui,'Silver Coin',370,160)
lCopperC = QtBind.createLabel(gui,'Copper Coin',370,175)
lIronC = QtBind.createLabel(gui,'Iron Coin',370,190)
qarena = QtBind.createLabel(gui,'0',440,130)
qgold = QtBind.createLabel(gui,'0',440,145)
qsilver = QtBind.createLabel(gui,'0',440,160)
qcopper = QtBind.createLabel(gui,'0',440,175)
qiron = QtBind.createLabel(gui,'0',440,190)

lLIST = QtBind.createList(gui,130,10,1,275)
lLIST2 = QtBind.createList(gui,245,10,1,275)
lLIST3 = QtBind.createList(gui,360,10,1,275)
lLIST3 = QtBind.createList(gui,9,10,1,275)
lLIST4 = QtBind.createList(gui,460,10,1,275)

lNEREYAZI = QtBind.createLabel(gui,'Nereyi kontrol edelim?',520,25)
btnStorage = QtBind.createButton(gui,'btnStorage_clicked',"  Depo!  ",530,75)
btnGuildStorage = QtBind.createButton(gui,'btnGuildStorage_clicked',"  Guild Depo!",530,125,)
btnInventory = QtBind.createButton(gui,'btnInventory_clicked'," Envanter! ",530,50)
btnPet = QtBind.createButton(gui,'btnPet_clicked'," Toplama Pet! ",530,100)
lBILGIYAZI = QtBind.createLabel(gui,'Kac derece eşya arıyorsun?',500,170)
leDegree = QtBind.createLineEdit(gui,"11",540,190,19,19)
lDegree = QtBind.createLabel(gui,'Derece',565,193)
lBILGIYAZI2 = QtBind.createLabel(gui,'Not : Eşyaları görebilmek için 1 defa',500,250)
lBILGIYAZI3 = QtBind.createLabel(gui,'depolara girmeniz gerekmektedir.',525,270)
lBILGIYAZI3 = QtBind.createLabel(gui,'Sadece Stoneler için geçerlidir.',500,210)

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
	STRScroll = 0
	INTScroll = 0
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
	bluestone = 0
	blackstone = 0
	ticketstone = 0
	monster = 0
	pandora = 0
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
			if item != None and "Strength" in item['name'] and "Scroll" in item['name']:
				STRScroll += item['quantity']
			if item != None and "Intelligence" in item['name'] and "Scroll" in item['name']:
				INTScroll += item['quantity']
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
			if item != None and "Elixir" in item['name'] and "(Weapon)" in item['name']:
				weapon += item['quantity']
			if item != None and "Elixir" in item['name'] and "(Protector)" in item['name']:
				protector += item['quantity']
			if item != None and "Elixir" in item['name'] and "(Accessory)" in item['name']:
				accessory += item['quantity']
			if item != None and "Elixir" in item['name'] and "(Shield)" in item['name']:
				scacc += item['quantity']
			if item != None and "Coin" in item['name'] and "Gold" in item['name']:
				gold += item['quantity']
			if item != None and "Coin" in item['name'] and "Silver" in item['name']:
				silver += item['quantity']
			if item != None and "Coin" in item['name'] and "Copper" in item['name']:
				copper += item['quantity']
			if item != None and "Coin" in item['name'] and "Iron" in item['name']:
				iron += item['quantity']
			if item != None and "Coin" in item['name'] and "Arena" in item['name']:
				arena += item['quantity']
			if item != None and "Stone" in item['name'] and "Blue" in item['name']:
				bluestone += item['quantity']
			if item != None and "Stone" in item['name'] and "Black" in item['name']:
				blackstone += item['quantity']
			if item != None and "Ticket" in item['name'] and "Ticket" in item['name']:
				ticketstone += item['quantity']
			if item != None and "Pandora's Box" in item['name'] and "Pandora's Box" in item['name']:
				pandora += item['quantity']
			if item != None and "Monster Summon Scroll)" in item['name'] and "Monster Summon Scroll" in item['name']:
				monster += item['quantity']
	QtBind.setText(gui, qSTRScroll, str(STRScroll))
	QtBind.setText(gui, qINTScroll, str(INTScroll))
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
	QtBind.setText(gui, qblackstone, str(blackstone))
	QtBind.setText(gui, qbluestone, str(bluestone))
	QtBind.setText(gui, qticketstone, str(ticketstone))
	QtBind.setText(gui, qpandora, str(pandora))
	QtBind.setText(gui, qmonster, str(monster))


log('Plugin: xDropSayac Çalışıyor...')