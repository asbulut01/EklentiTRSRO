from phBot import *
from threading import Timer
import QtBind
import struct

name = "TR_SpawnTimer"
version = "1.0"

is_running_timers = {"pandora": False, "mss": False}
timers = {"pandora": None, "mss": None}
intervals = {"pandora": 60, "mss": 60}
remaining_times = {"pandora": 60, "mss": 60}

gui = QtBind.init(__name__, name)

lblPandoraFrame = QtBind.createList(gui, 50, 5, 300, 200)
lblPandoraHeader = QtBind.createLabel(gui, "<b>Otomatik Pandora Box</b>", 75, 10)
lblMSSFrame = QtBind.createList(gui, 375, 5, 300, 200)
lblMSSHeader = QtBind.createLabel(gui, "<b>Otomatik Monster Summon Scroll</b>", 400, 10)

lblPandoraTimer = QtBind.createLabel(gui, "Pandora Kalan Süre: 60 sn", 75, 40)
lblPandoraInterval = QtBind.createLabel(gui, "Pandora Süresi (sn):", 75, 80)
txtPandoraInterval = QtBind.createLineEdit(gui, str(intervals["pandora"]), 175, 80, 40, 20)
btnSetPandoraInterval = QtBind.createButton(gui, 'set_pandora_interval', " Pandora Süresini Ayarla ", 75, 120)
btnTogglePandora = QtBind.createButton(gui, 'toggle_pandora_timer', " Başlat ", 75, 160)
btnUsePandoraNow = QtBind.createButton(gui, 'use_pandora_now', " Şimdi Kullan ", 250, 38)

btnUseMSSNow = QtBind.createButton(gui, 'use_mss_now', " Şimdi Kullan ", 575, 38)
lblMSSTimer = QtBind.createLabel(gui, "MSS Kalan Süre: 60 sn", 400, 40)
lblMSSInterval = QtBind.createLabel(gui, "MSS Süresi (sn):", 400, 80)
txtMSSInterval = QtBind.createLineEdit(gui, str(intervals["mss"]), 500, 80, 40, 20)
btnSetMSSInterval = QtBind.createButton(gui, 'set_mss_interval', " MSS Süresini Ayarla ", 400, 120)
btnToggleMSS = QtBind.createButton(gui, 'toggle_mss_timer', " Başlat ", 400, 160)

def use_pandora_now():
    if use_item("Pandora's Box"):
        log("Plugin: Pandora's Box başarıyla kullanıldı.")
    else:
        log("Plugin: Pandora's Box envanterde bulunamadı.")

def use_mss_now():
    if use_item("Monster Summon Scroll (party use)"):
        log("Plugin: Monster Summon Scroll başarıyla kullanıldı.")
    else:
        log("Plugin: Monster Summon Scroll envanterde bulunamadı.")

def use_item(item_name):
    inventory = get_inventory()
    if not inventory or 'items' not in inventory:
        log("Plugin: Envanter verisi alınamadı.")
        return False

    items = inventory['items']
    for slot, item in enumerate(items):
        if item and item['name'] == item_name:
            p = struct.pack('B', slot)
            if item_name == "Pandora's Box":
                p += b'\x30\x0c\x0f\x01'
            elif item_name == "Monster Summon Scroll (party use)":
                p += b'\x30\x0c\x0f\x02'
            inject_joymax(0x704C, p, True)
            log(f"Plugin: Kullanıldı 1x {item['name']}.")
            return True

    log(f"Plugin: Envanterde {item_name} bulunamadı.")
    return False

def toggle_pandora_timer():
    if is_running_timers["pandora"]:
        stop_timer("pandora")
        QtBind.setText(gui, btnTogglePandora, " Başlat ")
    else:
        start_timer("pandora")
        QtBind.setText(gui, btnTogglePandora, " Durdur ")

def toggle_mss_timer():
    if is_running_timers["mss"]:
        stop_timer("mss")
        QtBind.setText(gui, btnToggleMSS, " Başlat ")
    else:
        start_timer("mss")
        QtBind.setText(gui, btnToggleMSS, " Durdur ")

def start_timer(timer_type):
    global is_running_timers, timers, remaining_times
    is_running_timers[timer_type] = True
    remaining_times[timer_type] = intervals[timer_type]
    log(f"Plugin: {timer_type.capitalize()} zamanlayıcı başlatıldı.")
    reset_timer(timer_type)

def reset_timer(timer_type):
    global timers, remaining_times
    remaining_times[timer_type] = intervals[timer_type]
    update_labels()
    if is_running_timers[timer_type]:
        timers[timer_type] = Timer(1.0, countdown_timer, args=[timer_type])
        timers[timer_type].start()

def stop_timer(timer_type):
    global is_running_timers, timers
    is_running_timers[timer_type] = False
    if timers[timer_type]:
        timers[timer_type].cancel()
        timers[timer_type] = None
    log(f"Plugin: {timer_type.capitalize()} zamanlayıcı durduruldu.")

def countdown_timer(timer_type):
    global timers, remaining_times, is_running_timers
    if remaining_times[timer_type] > 0:
        remaining_times[timer_type] -= 1
        update_labels()
        timers[timer_type] = Timer(1.0, countdown_timer, args=[timer_type])
        timers[timer_type].start()
    else:
        if timer_type == "pandora":
            used = use_item("Pandora's Box")
        elif timer_type == "mss":
            used = use_item("Monster Summon Scroll (party use)")

        if used:
            reset_timer(timer_type)
        else:
            stop_timer(timer_type)
            if timer_type == "pandora":
                QtBind.setText(gui, btnTogglePandora, " Başlat ")
            elif timer_type == "mss":
                QtBind.setText(gui, btnToggleMSS, " Başlat ")

def set_pandora_interval():
    global intervals
    try:
        pandora_interval = int(QtBind.text(gui, txtPandoraInterval))
        if pandora_interval > 0:
            intervals["pandora"] = pandora_interval
            log(f"Plugin: Pandora süresi {pandora_interval} sn olarak ayarlandı.")
        else:
            log("Plugin: Pandora süresi pozitif bir değer olmalıdır.")
    except ValueError:
        log("Plugin: Geçerli bir sayı giriniz.")

def set_mss_interval():
    global intervals
    try:
        mss_interval = int(QtBind.text(gui, txtMSSInterval))
        if mss_interval > 0:
            intervals["mss"] = mss_interval
            log(f"Plugin: MSS süresi {mss_interval} sn olarak ayarlandı.")
        else:
            log("Plugin: MSS süresi pozitif bir değer olmalıdır.")
    except ValueError:
        log("Plugin: Geçerli bir sayı giriniz.")

def update_labels():
    QtBind.setText(gui, lblPandoraTimer, f"Pandora Kalan Süre: {remaining_times['pandora']} sn")
    QtBind.setText(gui, lblMSSTimer, f"MSS Kalan Süre: {remaining_times['mss']} sn")

log('Eklenti: [%s] Sürüm %s Yüklendi. // edit by hakankahya' % (name,version))
