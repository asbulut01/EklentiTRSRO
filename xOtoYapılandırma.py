from phBot import *
from threading import Timer
import shutil
import time
import os
import re

pName = 'xOtoYapılandırma'

# ______________________________ Initializing ______________________________ #

# Maximum time taken for filter database to be created
DATABASE_LOADING_TIME = 90.0
# ______________________________ Methods ______________________________ #

# Return character config filename (JSON)
def getConfigFilename():
	data = get_character_data()
	return data['server']+"_"+data['name']

# Returns a list of files existence by using regex
def FindFiles(pattern,dir=''):
	return [x for x in os.listdir(dir) if re.search(pattern,x)]

# Copy or replace a file while print an user message
def ReplaceFile(newPath,oldPath,message):
	shutil.copyfile(newPath,oldPath)
	log(message)

# ______________________________ Events ______________________________ #

# Called when the user successfully selects a character. No character data has been loaded yet.
def joined_game():
	# get for basic check
	configDir = get_config_dir()
	configFilename = getConfigFilename()

	# Check config (JSON) existence
	if not os.path.exists(configDir+configFilename+".json"):
		# Find JSON default configs and profile paths
		defaultConfigs = FindFiles(r'[Dd]efault\.json|[Dd]efault\.[\s\S]*\.json',configDir)
		for cfg in defaultConfigs:
			# Create character config/profile
			ReplaceFile(configDir+cfg,configDir+configFilename+cfg[7:],'Plugin: "'+str(cfg)+'" Yüklendi.')

	# Check Default filter existence
	defaultFilter = FindFiles(r'[Dd]efault\.db3',configDir)
	if not defaultFilter:
		return
	defaultFilter = configDir+defaultFilter[0]
	configFilter = configDir+configFilename+".db3"

	# Check Filter (db3) existence
	if os.path.exists(configFilter):
		# Check last modification time (seconds)
		lastModification = time.time() - os.path.getmtime(configFilter)
		# Replace filter if was created/edited a second ago
		if lastModification <= 2:
			log("Plugin: Filtre oluşturuldu! "+str(DATABASE_LOADING_TIME)+" saniye içerisinde yüklenecek...")
			Timer(DATABASE_LOADING_TIME,ReplaceFile,[defaultFilter,configFilter,"Plugin: Varsayılan filtre yüklendi."]).start()
	else:
		log("Plugin: Filtre bulunamadı! "+str(DATABASE_LOADING_TIME)+" saniye içerisinde yüklenecek...")
		Timer(DATABASE_LOADING_TIME,ReplaceFile,[defaultFilter,configFilter,"Plugin: Varsayılan filtre yüklendi."]).start()

# Plugin loaded
log("Plugin: "+pName+" Yüklendi! Çalışıyor...")