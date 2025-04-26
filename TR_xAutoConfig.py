from phBot import *
from threading import Timer
import shutil
import time
import os
import re

pName = 'TR_xAutoConfig'

DATABASE_LOADING_TIME = 90.0

def getConfigFilename():
    data = get_character_data()
    return data['server'] + "_" + data['name']

def FindFiles(pattern, dir=''):
    return [x for x in os.listdir(dir) if re.search(pattern, x)]

def ReplaceFile(newPath, oldPath, message):
    shutil.copyfile(newPath, oldPath)
    log(message)

def joined_game():
    configDir = get_config_dir()
    configFilename = getConfigFilename()

    if not os.path.exists(configDir + configFilename + ".json"):
        defaultConfigs = FindFiles(r'[Dd]efault\.json|[Dd]efault\.[\s\S]*\.json', configDir)
        for cfg in defaultConfigs:
            ReplaceFile(configDir + cfg, configDir + configFilename + cfg[7:], 'TR_xAutoConfig: "' + str(cfg) + '" yüklendi')

    defaultFilter = FindFiles(r'[Dd]efault\.db3', configDir)
    if not defaultFilter:
        return
    defaultFilter = configDir + defaultFilter[0]
    configFilter = configDir + configFilename + ".db3"

    if os.path.exists(configFilter):
        lastModification = time.time() - os.path.getmtime(configFilter)
        if lastModification <= 2:
            log("TR_xAutoConfig: Filtre birkaç saniye önce oluşturuldu! Varsayılan filtre " + str(DATABASE_LOADING_TIME) + " saniye içinde yüklenecek...")
            Timer(DATABASE_LOADING_TIME, ReplaceFile, [defaultFilter, configFilter, "TR_xAutoConfig: Varsayılan filtre yüklendi"]).start()
    else:
        log("TR_xAutoConfig: Filtre bulunamadı. Varsayılan filtre " + str(DATABASE_LOADING_TIME) + " saniye içinde yüklenecek...")
        Timer(DATABASE_LOADING_TIME, ReplaceFile, [defaultFilter, configFilter, "TR_xAutoConfig: Varsayılan filtre yüklendi"]).start()

log('Eklenti: ' + pName + ' başarıyla yüklendi')