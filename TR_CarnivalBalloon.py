from phBot import *
from threading import Timer
import QtBind
import struct
import urllib.request
import os
import json

name = 'TR_CarnivalBalloon'
version = '2.1'

INFLATE_BALLOON_LEVEL_STOP = 6
INFLATE_BALLOON_LEVELUP_DELAY = 5.0

isInflating = False
inflatingLevel = 0

gui = QtBind.init(__name__, name)

txtOpcode = QtBind.createLineEdit(gui, "6", 85, 45, 40, 20)
btnSetLevel = QtBind.createButton(gui, 'btnSetLevel_clicked', " Seviyeyi Ayarla ", 135, 45)
lblLevel = QtBind.createLabel(gui, ' Mevcut Seviye: ' + str(INFLATE_BALLOON_LEVEL_STOP), 75, 85)
btnBaslat = QtBind.createButton(gui, 'InflateBalloons', " Balonları Uçurmaya Başla ", 75, 120)
lblSpeed = QtBind.createLabel(gui, 'Balon Uçurma Hızı (sn):', 75, 160)
txtSpeed = QtBind.createLineEdit(gui, str(INFLATE_BALLOON_LEVELUP_DELAY), 220, 160, 40, 20)
btnSetSpeed = QtBind.createButton(gui, 'btnSetSpeed_clicked', ' Hızı Ayarla ', 270, 160)
chkReturn = QtBind.createCheckBox(gui, 'return_scroll_changed', 'Return Çekilsin mi?', 75, 200)
QtBind.setChecked(gui, chkReturn, True)

def get_config_dir():
    base_path = os.path.join(os.getcwd(), 'Config')
    plugin_path = os.path.join(base_path, name)
    if not os.path.exists(plugin_path):
        os.makedirs(plugin_path)
        log(f'[{name}] Yedek klasörü oluşturuldu.')
    return plugin_path + os.sep

def get_config_file():
    character_data = get_character_data()
    if not character_data['name'] or not character_data['server']:
        return None
    path = get_config_dir()
    return os.path.join(path, f"{character_data['server']}_{character_data['name']}.json")

def save_config():
    config_file = get_config_file()
    if not config_file:
        log('Karakter bilgisi alınamadı. Lütfen giriş yapın.')
        return

    data = {
        "INFLATE_BALLOON_LEVEL_STOP": INFLATE_BALLOON_LEVEL_STOP,
        "INFLATE_BALLOON_LEVELUP_DELAY": INFLATE_BALLOON_LEVELUP_DELAY,
        "ReturnScroll": QtBind.isChecked(gui, chkReturn)
    }

    try:
        with open(config_file, 'w') as f:
            json.dump(data, f, indent=4)
        log('Ayarlar başarıyla kaydedildi.')
    except Exception as e:
        log(f'Ayarlar kaydedilirken bir hata oluştu: {e}')

def load_config():
    config_file = get_config_file()
    if not config_file or not os.path.exists(config_file):
        log('Ayar dosyası bulunamadı.')
        return

    try:
        with open(config_file, 'r') as f:
            data = json.load(f)

        global INFLATE_BALLOON_LEVEL_STOP, INFLATE_BALLOON_LEVELUP_DELAY
        if "INFLATE_BALLOON_LEVEL_STOP" in data:
            INFLATE_BALLOON_LEVEL_STOP = data["INFLATE_BALLOON_LEVEL_STOP"]
            QtBind.setText(gui, lblLevel, ' Mevcut Seviye: ' + str(INFLATE_BALLOON_LEVEL_STOP))
        if "INFLATE_BALLOON_LEVELUP_DELAY" in data:
            INFLATE_BALLOON_LEVELUP_DELAY = data["INFLATE_BALLOON_LEVELUP_DELAY"]
            QtBind.setText(gui, txtSpeed, str(INFLATE_BALLOON_LEVELUP_DELAY))
        if "ReturnScroll" in data:
            QtBind.setChecked(gui, chkReturn, data["ReturnScroll"])

        log('Ayarlar başarıyla yüklendi.')
    except Exception as e:
        log(f'Ayarlar yüklenirken bir hata oluştu: {e}')

def return_scroll_changed(checked):
    state = 'Evet' if checked else 'Hayır'
    log(f'Eklenti: Return Çekme Durumu -> {state}')
    save_config()

def btnSetSpeed_clicked():
    global INFLATE_BALLOON_LEVELUP_DELAY
    try:
        new_speed = float(QtBind.text(gui, txtSpeed))
        if new_speed > 0:
            INFLATE_BALLOON_LEVELUP_DELAY = new_speed
            log(f'Eklenti: Balon uçurma hızı {new_speed} saniye olarak ayarlandı.')
            save_config()
        else:
            log('Eklenti: Hız 0\'dan büyük olmalıdır.')
    except ValueError:
        log('Eklenti: Geçerli bir hız değeri giriniz.')

def btnSetLevel_clicked():
    global INFLATE_BALLOON_LEVEL_STOP
    try:
        new_level = int(QtBind.text(gui, txtOpcode))
        
        if 1 <= new_level <= 6:
            INFLATE_BALLOON_LEVEL_STOP = new_level
            QtBind.setText(gui, lblLevel, ' Mevcut Seviye: ' + str(INFLATE_BALLOON_LEVEL_STOP))
            log(f'Eklenti: Seviyeyi {INFLATE_BALLOON_LEVEL_STOP} olarak ayarladınız.')
            save_config()
        else:
            log('Eklenti: Seviye 1 ile 6 arasında olmalıdır.')
    except ValueError:
        log('Eklenti: Geçerli bir seviye değeri giriniz.')

def joined_game():
    Timer(2.0, load_config).start()

# Diğer mevcut fonksiyonlar ve eklenti işlevleri burada korunuyor.

def GetItemByExpression(_lambda):
    items = get_inventory()['items']
    for slot, item in enumerate(items):
        if item:
            if _lambda(item['name'], item['servername']):
                item['slot'] = slot
                return item
    return None

def InflateNewBalloon():
    item = GetItemByExpression(lambda n, s: s.startswith('ITEM_ETC_E101216_BALLOON_'))
    if item:
        global inflatingLevel
        inflatingLevel = 1
        p = struct.pack('B', item['slot'])
        p += b'\x30\x0C\x09\x00'
        log('Eklenti: Using "' + item['name'] + '"...')
        inject_joymax(0x704C, p, True)
        Timer(INFLATE_BALLOON_LEVELUP_DELAY, LevelUpBalloon).start()
    else:
        global isInflating
        isInflating = False
        log('Eklenti: Balon Bulunamadı, Return Çekiliyor...')
        if QtBind.isChecked(gui, chkReturn):
            use_return_scroll()
        else:
            log('Eklenti: Return Çekme devre dışı bırakıldı.')
        start_bot()

def LevelUpBalloon():
    global inflatingLevel
    if inflatingLevel >= INFLATE_BALLOON_LEVEL_STOP:
        log('Eklenti: Balon Ödülünü Alındı. (Lv.' + str(inflatingLevel) + ')')
        inject_joymax(0x7574, b'\x02', False)
        inflatingLevel = 0
        Timer(INFLATE_BALLOON_LEVELUP_DELAY, LevelUpBalloon).start()
    elif inflatingLevel:
        log('Eklenti: Balon Şişiriliyor...')
        inject_joymax(0x7574, b'\x01', False)
        Timer(INFLATE_BALLOON_LEVELUP_DELAY, LevelUpBalloon).start()
    else:
        InflateNewBalloon()

def InflateBalloons():
    global isInflating
    if not isInflating:
        inflate_balloons([])

def inflate_balloons(args):
    item = GetItemByExpression(lambda n, s: s.startswith('ITEM_ETC_E101216_BALLOON_'))
    if item:
        stop_bot()
        global isInflating
        isInflating = True
        log('Eklenti: Balonlar Şişirilmeye Başlandı...')
        Timer(0.001, InflateNewBalloon).start()
    else:
        log('Eklenti: Envanterinizde Balon Bulunmuyor.')
    return 0

def handle_joymax(opcode, data):
    global inflatingLevel
    if opcode == 0xB574 and isInflating:
        if data[0] == 1:
            if data[1] == 1:
                inflatingLevel += 1
            elif data[1] == 2:
                inflatingLevel = 0
    return True

log('Eklenti: %s v%s Yuklendi. // edit by hakankahya' % (name, version))
