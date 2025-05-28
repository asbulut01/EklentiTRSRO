from phBot import *
import QtBind
import traceback
import difflib

name = 'TR_CountDrop'

gui = QtBind.init(__name__, name)

btnInventory = QtBind.createButton(gui,'btnInventory_clicked',"Envanter",620,10)
btnStorage = QtBind.createButton(gui,'btnStorage_clicked',"Depo",620,40)
btnGuildStorage = QtBind.createButton(gui,'btnGuildStorage_clicked',"Guild Depo",620,70,)
btnPet = QtBind.createButton(gui,'btnPet_clicked',"Pet",620,100)
leDegree = QtBind.createLineEdit(gui,"11",620,130,19,19)
lDegree = QtBind.createLabel(gui,'Degree',643,132)
lCizgi1_1 = QtBind.createList(gui,6,4,147,300)
lCizgi1_2 = QtBind.createLabel(gui,'________________________',6,12)
lEtkinlik = QtBind.createLabel(gui,'Etkinlik Eşyaları',40,7)
lBRP = QtBind.createLabel(gui,'Berserker Potion',11,30)
lSTRScroll = QtBind.createLabel(gui,'STR Increase Scroll',11,45)
lINTScroll = QtBind.createLabel(gui,'INT Increase Scroll',11,60)
lHPScroll = QtBind.createLabel(gui,'HP Increase Scroll',11,75)
lMPScroll = QtBind.createLabel(gui,'MP Increase Scroll',11,90)
lHitScroll = QtBind.createLabel(gui,'Hit Scroll',11,105)
lDodgingScroll = QtBind.createLabel(gui,'Dodging Scroll',11,120)
lTriggerScroll = QtBind.createLabel(gui,'Trigger Scroll',11,135)
lsceva = QtBind.createLabel(gui,'Scroll of Evasion',11,150)
lscacc = QtBind.createLabel(gui,'Scroll of Accuracy',11,165)
lPandoraBox = QtBind.createLabel(gui,'Pandora Box',11,180)
lMonsterSc = QtBind.createLabel(gui,'Monster S. Scroll',11,195)
lCatalyst = QtBind.createLabel(gui,'Alchemy catalyst',11,210)
qBRP = QtBind.createLabel(gui,'0',120,30)
qSTRScroll = QtBind.createLabel(gui,'0',120,45)
qINTScroll = QtBind.createLabel(gui,'0',120,60)
qHPScroll = QtBind.createLabel(gui,'0',120,75)
qMPScroll = QtBind.createLabel(gui,'0',120,90)
qHitScroll = QtBind.createLabel(gui,'0',120,105)
qDodgingScroll = QtBind.createLabel(gui,'0',120,120)
qTriggerScroll = QtBind.createLabel(gui,'0',120,135)
qsceva = QtBind.createLabel(gui,'0',120,150)
qscacc = QtBind.createLabel(gui,'0',120,165)
qPandoraBox = QtBind.createLabel(gui,'0',120,180)
qMonsterSc = QtBind.createLabel(gui,'0',120,195)
qCatalyst = QtBind.createLabel(gui,'0',120,210)
lCizgi2_1 = QtBind.createList(gui,155,4,147,90)
lCizgi2_2 = QtBind.createLabel(gui,'________________________',155,12)
lElixir = QtBind.createLabel(gui,'         Elixirler   ',177,7)
lWeapon = QtBind.createLabel(gui,'Weapon',160,30)
lProtector = QtBind.createLabel(gui,'Protector',160,45)
lAccessory = QtBind.createLabel(gui,'Accessory',160,60)
lShield = QtBind.createLabel(gui,'Shield',160,75)
qweapon = QtBind.createLabel(gui,'0',265,30)
qprotector = QtBind.createLabel(gui,'0',265,45)
qaccessory = QtBind.createLabel(gui,'0',265,60)
qshield = QtBind.createLabel(gui,'0',265,75)
lCizgi3_1 = QtBind.createList(gui,155,97,147,114)
lCizgi3_2 = QtBind.createLabel(gui,'________________________',155,102)
lCoinler = QtBind.createLabel(gui,'           Coinler  ',177,99)
lArenaC = QtBind.createLabel(gui,'Arena Coin',160,120)
lGoldC = QtBind.createLabel(gui,'Gold Coin',160,135)
lSilverC = QtBind.createLabel(gui,'Silver Coin',160,150)
lCopperC = QtBind.createLabel(gui,'Copper Coin',160,165)
lIronC = QtBind.createLabel(gui,'Iron Coin',160,180)
lSurvivalC = QtBind.createLabel(gui,'Survival Coin',160,195)
qarena = QtBind.createLabel(gui,'0',265,120)
qgold = QtBind.createLabel(gui,'0',265,135)
qsilver = QtBind.createLabel(gui,'0',265,150)
qcopper = QtBind.createLabel(gui,'0',265,165)
qiron = QtBind.createLabel(gui,'0',265,180)
qsurvival = QtBind.createLabel(gui,'0',265,195)
lCizgi4_1 = QtBind.createList(gui,155,215,147,90)
lCizgi4_2 = QtBind.createLabel(gui,'________________________',155,219)
lJob = QtBind.createLabel(gui,'       Job Eşyaları     ',177,217)
lTicketSt = QtBind.createLabel(gui,'Ticket',160,235)
lBlueSt = QtBind.createLabel(gui,'Blue Stone',160,250)
lBlackSt = QtBind.createLabel(gui,'Black Stone',160,265)
qTicketSt = QtBind.createLabel(gui,'0',265,235)
qBlueSt = QtBind.createLabel(gui,'0',265,250)
qBlackSt = QtBind.createLabel(gui,'0',265,265)
lCizgi5_1 = QtBind.createList(gui,304,4,147,300)
lCizgi5_2 = QtBind.createLabel(gui,'________________________',304,12)
lBlueStoneler = QtBind.createLabel(gui,'Blue Stoneler',338,7)
lSTR = QtBind.createLabel(gui,'Str',310,30)
lINT = QtBind.createLabel(gui,'Int',310,45)
lMaster = QtBind.createLabel(gui,'Master',310,60)
lStrikes = QtBind.createLabel(gui,'Strikes',310,75)
lDiscipline = QtBind.createLabel(gui,'Discipline',310,90)
lPenetration = QtBind.createLabel(gui,'Penetration',310,105)
lDodging2 = QtBind.createLabel(gui,'Dodging',310,120)
lStamina = QtBind.createLabel(gui,'Stamina',310,135)
lMagic = QtBind.createLabel(gui,'Magic',310,150)
lFogs = QtBind.createLabel(gui,'Fogs',310,165)
lAir = QtBind.createLabel(gui,'Air',310,180)
lFire = QtBind.createLabel(gui,'Fire',310,195)
lImmunity = QtBind.createLabel(gui,'Immunity',310,210)
lRevival = QtBind.createLabel(gui,'Revival',310,225)
lLuck = QtBind.createLabel(gui,'Luck',310,240)
lSteady = QtBind.createLabel(gui,'Steady',310,255)
lImmortal = QtBind.createLabel(gui,'Immortal',310,270)
lAstral = QtBind.createLabel(gui,'Astral',310,285)
qstr = QtBind.createLabel(gui,'0',415,30)
qint = QtBind.createLabel(gui,'0',415,45)
qmaster = QtBind.createLabel(gui,'0',415,60)
qstrikes = QtBind.createLabel(gui,'0',415,75)
qdiscipline = QtBind.createLabel(gui,'0',415,90)
qpenetration = QtBind.createLabel(gui,'0',415,105)
qdodging2 = QtBind.createLabel(gui,'0',415,120)
qstamina = QtBind.createLabel(gui,'0',415,135)
qmagic = QtBind.createLabel(gui,'0',415,150)
qfogs = QtBind.createLabel(gui,'0',415,165)
qair = QtBind.createLabel(gui,'0',415,180)
qfire = QtBind.createLabel(gui,'0',415,195)
qimmunity = QtBind.createLabel(gui,'0',415,210)
qrevival = QtBind.createLabel(gui,'0',415,225)
qluck = QtBind.createLabel(gui,'0',415,240)
qsteady = QtBind.createLabel(gui,'0',415,255)
qImmortal = QtBind.createLabel(gui,'0',415,270)
qAstral = QtBind.createLabel(gui,'0',415,285)
lCizgi6_1 = QtBind.createList(gui,453,4,147,240)
lCizgi6_2 = QtBind.createLabel(gui,'________________________',453,12)
lStatStoneler = QtBind.createLabel(gui,'   Stat Stoneler',482,7)
lCourage = QtBind.createLabel(gui,'Courage',460,30)
lPhilosophy = QtBind.createLabel(gui,'Philosophy',460,45)
lFocus = QtBind.createLabel(gui,'Focus',460,60)
lChallenge = QtBind.createLabel(gui,'Challenge',460,75)
lAgility = QtBind.createLabel(gui,'Agility',460,90)
lWarriors = QtBind.createLabel(gui,'Warriors',460,105)
lMeditation = QtBind.createLabel(gui,'Meditation',460,120)
lFlesh = QtBind.createLabel(gui,'Flesh',460,135)
lMind = QtBind.createLabel(gui,'Mind',460,150)
lDodging = QtBind.createLabel(gui,'Dodging',460,165)
lLife = QtBind.createLabel(gui,'Life',460,180)
lSpirit = QtBind.createLabel(gui,'Spirit',460,195)
lTraining = QtBind.createLabel(gui,'Training',460,210)
lPrayer = QtBind.createLabel(gui,'Prayer',460,225)
qcourage = QtBind.createLabel(gui,'0',565,30)
qphilosophy = QtBind.createLabel(gui,'0',565,45)
qfocus = QtBind.createLabel(gui,'0',565,60)
qchallenge = QtBind.createLabel(gui,'0',565,75)
qagility = QtBind.createLabel(gui,'0',565,90)
qwarriors = QtBind.createLabel(gui,'0',565,105)
qmeditation = QtBind.createLabel(gui,'0',565,120)
qflesh = QtBind.createLabel(gui,'0',565,135)
qmind = QtBind.createLabel(gui,'0',565,150)
qdodging = QtBind.createLabel(gui,'0',565,165)
qlife = QtBind.createLabel(gui,'0',565,180)
qspirit = QtBind.createLabel(gui,'0',565,195)
qtraining = QtBind.createLabel(gui,'0',565,210)
qprayer = QtBind.createLabel(gui,'0',565,225)
lblSearchTitlePrompt = QtBind.createLabel(gui, 'Ara:', 460, 250)
leSearchItemName = QtBind.createLineEdit(gui, "", 490, 250, 210, 20)
lblBestMatchResult = QtBind.createList(gui,460,275,240,25)

def btnPet_clicked():
    try:
        countItems('pet')
    except Exception as e:
        log(f"Hata (btnPet_clicked): {e}\n{traceback.format_exc()}")

def btnStorage_clicked():
    try:
        countItems('Storage')
    except Exception as e:
        log(f"Hata (btnStorage_clicked): {e}\n{traceback.format_exc()}")

def btnGuildStorage_clicked():
    try:
        countItems('GuildStorage')
    except Exception as e:
        log(f"Hata (btnGuildStorage_clicked): {e}\n{traceback.format_exc()}")

def btnInventory_clicked():
    try:
        countItems('Inventory')
    except Exception as e:
        log(f"Hata (btnInventory_clicked): {e}\n{traceback.format_exc()}")

def countItems(countIn):
    BRP, STRScroll, INTScroll, PandoraBox, MonsterSc, Catalyst, HPScroll, MPScroll = 0,0,0,0,0,0,0,0
    HitScroll, DodgingScroll, TriggerScroll, sceva, scacc = 0,0,0,0,0
    courage, philosophy, focus, challenge, agility, warriors, meditation, flesh, mind, pdodging = 0,0,0,0,0,0,0,0,0,0
    life, spirit, training, prayer = 0,0,0,0
    Str, Int, master, strikes, discipline, penetration, gdodging, stamina, magic = 0,0,0,0,0,0,0,0,0
    fogs, air, fire, immunity, revival, luck, steady, Immortal, Astral = 0,0,0,0,0,0,0,0,0
    weapon, protector, accessory, shield = 0,0,0,0
    gold, silver, arena, copper, iron, TicketSt, BlueSt, BlackSt, survival = 0,0,0,0,0,0,0,0,0
    
    items = []
    best_match_name_found = "Bulunamadı"
    best_match_quantity_found = 0

    try:
        if countIn == 'Storage':
            storage_data = get_storage()
            if storage_data and 'items' in storage_data: items = storage_data['items']
        elif countIn == 'GuildStorage':
            guild_storage_data = get_guild_storage()
            if guild_storage_data and 'items' in guild_storage_data: items = guild_storage_data['items']
        elif countIn == 'Inventory':
            inventory_data = get_inventory()
            if inventory_data and 'items' in inventory_data: items = inventory_data['items']
        elif countIn == 'pet':
            pets_data = get_pets()
            if pets_data:
                for pet_key in pets_data:
                    if isinstance(pets_data[pet_key], dict) and pets_data[pet_key].get('type') == 'pick' and 'items' in pets_data[pet_key]:
                        items = pets_data[pet_key]['items']
                        break
        
        degree_text = QtBind.text(gui, leDegree)
        degree = str(degree_text).lower().strip() if degree_text else ""
        search_input_text = QtBind.text(gui, leSearchItemName).strip()

        all_item_details = []
        if items is not None:
            for item_slot, item_data in enumerate(items):
                if item_data is not None:
                    item_name_full = item_data.get('name', '')
                    item_quantity = item_data.get('quantity', 0)
                    if item_name_full and item_quantity > 0:
                        all_item_details.append({'original': item_name_full, 'lower': item_name_full.lower(), 'quantity': item_quantity, 'slot': item_slot})
        
        if search_input_text and all_item_details:
            unique_lower_to_original_names = {details['lower']: details['original'] for details in all_item_details}
            possible_lower_names = list(unique_lower_to_original_names.keys())
            
            closest_lower_matches = difflib.get_close_matches(search_input_text.lower(), possible_lower_names, n=1, cutoff=0.5) # cutoff=0.5 iyi bir başlangıç
            
            if closest_lower_matches:
                matched_lower_name = closest_lower_matches[0]
                best_match_name_found = unique_lower_to_original_names[matched_lower_name]
                
                current_best_match_quantity = 0
                for item_detail in all_item_details:
                    if item_detail['original'] == best_match_name_found:
                        current_best_match_quantity += item_detail['quantity']
                best_match_quantity_found = min(current_best_match_quantity, 99999)

        if items is not None:
            for item_detail in all_item_details:
                item_name = item_detail['lower']
                item_quantity = item_detail['quantity']

                is_degree_item = False
                if degree:
                   is_degree_item = degree in item_name

                if is_degree_item:
                    if 'tablet' not in item_name and 'stone' in item_name:
                        if "courage" in item_name: courage += item_quantity
                        elif "philosophy" in item_name: philosophy += item_quantity
                        elif "focus" in item_name: focus += item_quantity
                        elif "challenge" in item_name: challenge += item_quantity
                        elif "agility" in item_name: agility += item_quantity
                        elif "warriors" in item_name: warriors += item_quantity
                        elif "meditation" in item_name: meditation += item_quantity
                        elif "flesh" in item_name: flesh += item_quantity
                        elif "mind" in item_name: mind += item_quantity
                        elif "attribute stone of dodging" in item_name: pdodging += item_quantity
                        elif "life" in item_name: life += item_quantity
                        elif "spirit" in item_name: spirit += item_quantity
                        elif "training" in item_name: training += item_quantity
                        elif "prayer" in item_name: prayer += item_quantity
                        elif "str" in item_name and "scroll" not in item_name: Str += item_quantity
                        elif "int" in item_name and "scroll" not in item_name: Int += item_quantity
                        elif "master" in item_name: master += item_quantity
                        elif "strikes" in item_name: strikes += item_quantity
                        elif "discipline" in item_name: discipline += item_quantity
                        elif "penetration" in item_name: penetration += item_quantity
                        elif "magic stone of dodging" in item_name: gdodging += item_quantity
                        elif "stamina" in item_name: stamina += item_quantity
                        elif "magic" in item_name and "magic stone" not in item_name and "potion" not in item_name: magic += item_quantity
                        elif "fogs" in item_name: fogs += item_quantity
                        elif "air" in item_name: air += item_quantity
                        elif "immunity" in item_name: immunity += item_quantity
                        elif "revival" in item_name: revival += item_quantity
                        elif "fire" in item_name: fire += item_quantity
                        elif "steady" in item_name: steady += item_quantity
                        elif "luck" in item_name: luck += item_quantity
                        elif "immortal" in item_name: Immortal += item_quantity
                        elif "astral" in item_name: Astral += item_quantity
                    
                    if "intensifying" in item_name and "elixir" in item_name:
                        if "(weapon)" in item_name: weapon += item_quantity
                        elif "(protector)" in item_name or "(armor)" in item_name: protector += item_quantity
                        elif "(accessory)" in item_name: accessory += item_quantity
                        elif "(shield)" in item_name: shield += item_quantity
                
                if "berserker" in item_name and "potion" in item_name: BRP += item_quantity
                if "strength scroll" in item_name or ("str" in item_name and "increase scroll" in item_name) : STRScroll += item_quantity
                if "intelligence scroll" in item_name or ("int" in item_name and "increase scroll" in item_name) : INTScroll += item_quantity
                if "pandora's box" in item_name: PandoraBox += item_quantity
                if "monster" in item_name and "summon scroll" in item_name: MonsterSc += item_quantity
                if "alchemy" in item_name and "catalyst" in item_name: Catalyst += item_quantity
                if "HP+430 potion" in item_name or "HP+800 Potion" in item_name or "HP+1300 Potion" in item_name or "HP+1900 potion" in item_name or "HP+2800 potion" in item_name or "HP+4100 potion" in item_name: HPScroll += item_quantity
                if "MP+430 potion" in item_name or "MP+800 potion" in item_name or "MP+1300 potion" in item_name or "MP+1900 potion" in item_name or "MP+2800 potion" in item_name or "MP+4100 potion" in item_name: MPScroll += item_quantity
                if "hit scroll" in item_name : HitScroll += item_quantity
                if "dodging scroll" in item_name and "attribute stone of dodging" not in item_name and "magic stone of dodging" not in item_name: DodgingScroll += item_quantity
                if "trigger scroll" in item_name: TriggerScroll += item_quantity
                if "scroll of evasion" in item_name: sceva += item_quantity
                if "scroll of accuracy" in item_name: scacc += item_quantity
                if "coin" in item_name and "gold" in item_name: gold += item_quantity
                if "coin" in item_name and "silver" in item_name: silver += item_quantity
                if "coin" in item_name and "copper" in item_name: copper += item_quantity
                if "coin" in item_name and "iron" in item_name: iron += item_quantity
                if "coin" in item_name and "arena" in item_name: arena += item_quantity
                if "coin" in item_name and ("combativeness" in item_name or "survival" in item_name) : survival += item_quantity
                if "ticket" in item_name: TicketSt += item_quantity
                if "blue stone" in item_name and "magic stone" not in item_name : BlueSt += item_quantity
                if "black stone" in item_name: BlackSt += item_quantity
    
    except AttributeError as ae:
        log(f"Hata (countItems - {countIn} - Nitelik Hatası): {ae}\n{traceback.format_exc()}")
    except TypeError as te:
        log(f"Hata (countItems - {countIn} - Tip Hatası): {te}\n{traceback.format_exc()}")
    except Exception as e:
        log(f"Hata (countItems - {countIn}): {e}\n{traceback.format_exc()}")
    finally:
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
        QtBind.setText(gui, qImmortal, str(Immortal))
        QtBind.setText(gui, qAstral, str(Astral))
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
        QtBind.setText(gui, qsurvival,str(survival))
        QtBind.clear(gui, lblBestMatchResult)
        if best_match_name_found != "Bulunamadı":
            result_text = f"{best_match_name_found} [{best_match_quantity_found}]"
            QtBind.append(gui, lblBestMatchResult, result_text)
        else:
            QtBind.append(gui, lblBestMatchResult, "Bulunamadı")

log(f'Eklenti: {name} başarıyla yüklendi.')