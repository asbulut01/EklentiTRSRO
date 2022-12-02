from phBot import *
import QtBind
import struct
import json
import os

pName = 'xTakasKabul'

# ______________________________ Initializing ______________________________ #

# globals
character_data = None
ExchangeStatus = ''

# opcodes
CLIENT_GAME_PETITION_RESPONSE = 0x3080
SERVER_GAME_PETITION_REQUEST = 0x3080
SERVER_EXCHANGE_STARTED = 0x3085
SERVER_EXCHANGE_PLAYER_CONFIRMED = 0x3086
SERVER_EXCHANGE_COMPLETED = 0x3087
SERVER_EXCHANGE_CANCELED = 0x3088
CLIENT_EXCHANGE_CONFIRM_REQUEST = 0x7082
SERVER_EXCHANGE_CONFIRM_RESPONSE = 0xB082
CLIENT_EXCHANGE_APPROVE_REQUEST = 0x7083
SERVER_EXCHANGE_INVITATION_RESPONSE = 0xB081
SERVER_EXCHANGE_APPROVE_RESPONSE = 0xB083
SERVER_EXCHANGE_EXIT_RESPONSE = 0xB084

# Initializing GUI
gui = QtBind.init(__name__,pName)

QtBind.createLabel(gui,"↓ Takas Listesi (Parti Gereklidir.) ↓",15,30)
tbxExchangerName = QtBind.createLineEdit(gui,"",30,60,120,20)
lvwExchangers = QtBind.createList(gui,30,82,120,100)
QtBind.createButton(gui,'btnAddExchanger_clicked',"    Ekle   ",150,59)
QtBind.createButton(gui,'btnRemExchanger_clicked',"     Sil     ",150,82)
cbxReplyAccept = QtBind.createCheckBox(gui,'checkbox_changed','Otomatik Takas kabul et',260,30)
cbxReplyApprove = QtBind.createCheckBox(gui,'checkbox_changed','Cevabı otomatik onayla',260,60)
cbxAcceptAll = QtBind.createCheckBox(gui,'checkbox_changed','Tüm Takas davetlerini kabul et',260,90)
QtBind.createLabel(gui,"Not : Eklenti ilk yüklemede Otomatik takas ve onaylama aktif olacaktır.",170,145)
metaby = QtBind.createLabel(gui,'edited by hakankahya',400,165)

# ______________________________ Methods ______________________________ #

# Return folder path
def get_path():
	return get_config_dir()+pName+"\\"

# Return character configs path (JSON)
def get_config():
	return get_path()+character_data['server'] + "_" + character_data['name'] + ".json"

# Check if character is ingame
def is_joined():
	global character_data
	character_data = get_character_data()
	if not (character_data and "name" in character_data and character_data["name"]):
		character_data = None
	return character_data

# Load default configs
def load_default_config():
	# Clear data
	QtBind.setChecked(gui,cbxAcceptAll,False)
	QtBind.setChecked(gui,cbxReplyAccept,True)
	QtBind.setChecked(gui,cbxReplyApprove,True)
	QtBind.clear(gui,lvwExchangers)

# Save all config
def save_configs():
	# Save if data has been loaded
	if is_joined():
		# Save all data
		data = {}
		data["AcceptAll"] = QtBind.isChecked(gui,cbxAcceptAll)
		data["ReplyAccept"] = QtBind.isChecked(gui,cbxReplyAccept)
		data["ReplyApprove"] = QtBind.isChecked(gui,cbxReplyApprove)
		data["Exchangers"] = QtBind.getItems(gui,lvwExchangers)

		# Overrides
		with open(get_config(),"w") as f:
			f.write(json.dumps(data, indent=4, sort_keys=True))
		log("Plugin: "+pName+" yapılandırmalar kaydedildi.")

# Loads all config previously saved
def load_configs():
	load_default_config()
	if is_joined():
		# Check config exists to load
		if os.path.exists(get_config()):
			data = {}
			with open(get_config(),"r") as f:
				data = json.load(f)
			# Load data
			if "AcceptAll" in data and data['AcceptAll']:
				QtBind.setChecked(gui,cbxAcceptAll,True)
			if "ReplyAccept" in data and not data['ReplyAccept']:
				QtBind.setChecked(gui,cbxReplyAccept,False)
			if "ReplyApprove" in data and not data['ReplyApprove']:
				QtBind.setChecked(gui,cbxReplyApprove,False)
			if "Exchangers" in data:
				for charName in data["Exchangers"]:
					QtBind.append(gui,lvwExchangers,charName)

# Called when any checkbox value changed
def checkbox_changed(newValue):
	save_configs()

# Return True if text exist at the list
def string_in_list(vString,vList,ModeSensitive=False):
	if not ModeSensitive:
		vString = vString.lower()
	for i in range(len(vList)):
		if not ModeSensitive:
			vList[i] = vList[i].lower()
		if vList[i] == vString:
			return True
	return False

# Add leader to the list
def btnAddExchanger_clicked():
	# Check in game data
	if character_data:
		player = QtBind.text(gui,tbxExchangerName)
		# Player nickname it's not empty and not added
		if player and not string_in_list(player,QtBind.getItems(gui,lvwExchangers)):
			QtBind.append(gui,lvwExchangers,player)
			save_configs()
			# saved successfully
			QtBind.setText(gui,tbxExchangerName,"")
			log('Plugin: Takascı Eklendi. ['+player+']')

# Remove leader selected from list
def btnRemExchanger_clicked():
	# Check in game data
	if character_data:
		selectedItem = QtBind.text(gui,lvwExchangers)
		if selectedItem:
			QtBind.remove(gui,lvwExchangers,selectedItem)
			# saved successfully
			save_configs()
			log("Plugin: Takascı Silindi. ["+selectedItem+"]")

# Return character name from player ID but only if is in party
def get_charname(UniqueID):	
	# Checking if UID is mine
	if UniqueID == character_data['player_id']:
		return character_data['name']

	# Load players from party
	players = get_party()

	# Check UID existence
	if players:
		for key, player in players.items():
			if player['player_id'] == UniqueID:
				return player['name']
	return ""

# Send the response to the last game petition
def Inject_GamePetitionResponse(Accept,Type):
	if Accept:
		p = b'\x01\x01'
	else:
		# Party Invitation or Party Creation
		if Type == 2 or Type == 3:
			p = b'\x02\x0C\x2C'
		# Default
		else:
			p = b'\x01\x00'
	inject_joymax(CLIENT_GAME_PETITION_RESPONSE,p,False)

# ______________________________ Events ______________________________ #

# Called when the character enters the game world
def joined_game():
	load_configs()

# All packets received from game server will be passed to this function
# Returning True will keep the packet and False will not forward it to the game client
def handle_joymax(opcode, data):
	if opcode == SERVER_GAME_PETITION_REQUEST:
		t = data[0]
		# petition type
		if t == 1: # exchange
			# Accept everyone
			if QtBind.isChecked(gui,cbxAcceptAll):
				Inject_GamePetitionResponse(True,t)
				return True
			# Try to extract nickname
			entityID = struct.unpack_from('<I', data, 1)[0]
			charName = get_charname(entityID)
			# Accept if nickname is found in list
			if string_in_list(charName,QtBind.getItems(gui,lvwExchangers)):
				Inject_GamePetitionResponse(True,t)
		return True
	# Update depending exchange status
	global ExchangeStatus
	if opcode == SERVER_EXCHANGE_STARTED:
		ExchangeStatus = 'STARTED'
	elif opcode == SERVER_EXCHANGE_INVITATION_RESPONSE:
		if data[0] == 1: # success
			ExchangeStatus = 'STARTED'
	# apply confirmations
	elif opcode == SERVER_EXCHANGE_PLAYER_CONFIRMED:
		# check current status to reply
		if ExchangeStatus == 'STARTED':
			if QtBind.isChecked(gui,cbxReplyAccept):
				# confirm exchange
				inject_joymax(CLIENT_EXCHANGE_CONFIRM_REQUEST,b'',False)
		elif ExchangeStatus == 'CONFIRMED':
			if QtBind.isChecked(gui,cbxReplyApprove):
				# approve exchange
				inject_joymax(CLIENT_EXCHANGE_APPROVE_REQUEST,b'',False)
	elif opcode == SERVER_EXCHANGE_CONFIRM_RESPONSE:
		if data[0] == 1: # success
			ExchangeStatus = 'CONFIRMED'
			# reply if is required
			if QtBind.isChecked(gui,cbxReplyApprove):
				# approve exchange
				inject_joymax(CLIENT_EXCHANGE_APPROVE_REQUEST,b'',False)
	elif opcode == SERVER_EXCHANGE_APPROVE_RESPONSE:
		if data[0] == 1: # success
			ExchangeStatus = 'APPROVED'
	elif opcode == SERVER_EXCHANGE_COMPLETED or opcode == SERVER_EXCHANGE_CANCELED:
		ExchangeStatus = ''
	elif opcode == SERVER_EXCHANGE_EXIT_RESPONSE:
		if data[0] == 1: # success
			ExchangeStatus = ''
	return True

# Plugin loaded
log("Plugin: "+pName+" Yüklendi! Çalışıyor...")

# Check folder existence
if os.path.exists(get_path()):
	# RELOAD plugin support
	load_configs()
else:
	# Create configs folder
	os.makedirs(get_path())
	log('Plugin: '+pName+' Klasörü oluşturuldu.')
