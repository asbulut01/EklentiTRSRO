from phBot import *
from threading import Timer
import QtBind
import struct

name = "TR_SpawnTimer"
version = "1.1"

is_running_timers = {"pandora": False, "mss": False}
timers = {"pandora": None, "mss": None}
intervals = {"pandora": 1, "mss": 1}
remaining_times = {"pandora": 1, "mss": 1}

gui = QtBind.init(__name__, name)

lblPandoraFrame = QtBind.createList(gui, 50, 5, 300, 200)
lblPandoraHeader = QtBind.createLabel(gui, "<b>Otomatik Pandora Box</b>", 75, 10)
lblMSSFrame = QtBind.createList(gui, 375, 5, 300, 200)
lblMSSHeader = QtBind.createLabel(gui, "<b>Otomatik Monster Summon Scroll</b>", 400, 10)

lblPandoraTimer = QtBind.createLabel(gui, "Pandora Kalan Süre: 00:00", 75, 40)
lblPandoraInterval = QtBind.createLabel(gui, "Pandora Süresi (dk):", 75, 80)
txtPandoraInterval = QtBind.createLineEdit(gui, str(intervals["pandora"]), 185, 77, 40, 20)
btnSetPandoraInterval = QtBind.createButton(gui, 'set_pandora_interval', " Pandora Süresini Ayarla ", 75, 120)
btnTogglePandora = QtBind.createButton(gui, 'toggle_pandora_timer', " Başlat ", 75, 160)
btnUsePandoraNow = QtBind.createButton(gui, 'use_pandora_now', " Şimdi Kullan ", 250, 38)

btnUseMSSNow = QtBind.createButton(gui, 'use_mss_now', " Şimdi Kullan ", 575, 38)
lblMSSTimer = QtBind.createLabel(gui, "MSS Kalan Süre: 00:00", 400, 40)
lblMSSInterval = QtBind.createLabel(gui, "MSS Süresi (dk):", 400, 80)
txtMSSInterval = QtBind.createLineEdit(gui, str(intervals["mss"]), 500, 77, 40, 20)
btnSetMSSInterval = QtBind.createButton(gui, 'set_mss_interval', " MSS Süresini Ayarla ", 400, 120)
btnToggleMSS = QtBind.createButton(gui, 'toggle_mss_timer', " Başlat ", 400, 160)

def pandora():
    items = get_inventory()['items']
    for slot, item in enumerate(items):
        if item:
            if "ITEM_ETC_E060517_MON_GENERATION_BOX" in item['servername'] or \
               "ITEM_EVENT_GENERATION_BOX" in item['servername'] or \
               "ITEM_EVENT_RENT_E100222_MON_GENERATION_BOX" in item['servername']:
                p = struct.pack('B', slot)
                p += b'\x30\x0c\x0f\x01'
                log("Plugin: Kullanildi 1x Pandora's Box")
                inject_joymax(0x704C, p, True)
                return True

    log(r'Plugin: Pandora Box Envanterde bulunamadı.')
    return False

def monstersc():
    items = get_inventory()['items']
    for slot, item in enumerate(items):
        if item:
            if "ITEM_ETC_E060517_SUMMON_PARTY_SCROLL" in item['servername'] or \
               "ITEM_ETC_E060526_SUMMON_PARTY_SCROLL_A" in item['servername'] or \
               "ITEM_EVENT_RENT_E100222_SUMMON_SCROLL" in item['servername']:
                p = struct.pack('B', slot)
                p += b'\x30\x0c\x0f\x02'
                log('Plugin: Kullanildi 1x Monster Summon Scroll')
                inject_joymax(0x704C, p, True)
                return True

    log(r'Plugin: Monster Summon Scroll Envanterde bulunamadı.')
    return False

def use_pandora_now():
    pandora()

def use_mss_now():
    monstersc()

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
    remaining_times[timer_type] = intervals[timer_type] * 60
    log(f"Plugin: {timer_type.capitalize()} zamanlayıcı başlatıldı.")
    reset_timer(timer_type)

def reset_timer(timer_type):
    global timers, remaining_times
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
        used = False
        if timer_type == "pandora":
            used = pandora()
        elif timer_type == "mss":
            used = monstersc()

        if used:
            remaining_times[timer_type] = intervals[timer_type] * 60
        else:
            stop_timer(timer_type)
        update_labels()
        if is_running_timers[timer_type]:
            timers[timer_type] = Timer(1.0, countdown_timer, args=[timer_type])
            timers[timer_type].start()

def set_pandora_interval():
    global intervals
    try:
        pandora_interval = int(QtBind.text(gui, txtPandoraInterval))
        if pandora_interval > 0:
            intervals["pandora"] = pandora_interval
            log(f"Plugin: Pandora süresi {pandora_interval} dk olarak ayarlandı.")
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
            log(f"Plugin: MSS süresi {mss_interval} dk olarak ayarlandı.")
        else:
            log("Plugin: MSS süresi pozitif bir değer olmalıdır.")
    except ValueError:
        log("Plugin: Geçerli bir sayı giriniz.")

def update_labels():
    def format_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    QtBind.setText(gui, lblPandoraTimer, f"Pandora Kalan Süre: {format_time(remaining_times['pandora'])}")
    QtBind.setText(gui, lblMSSTimer, f"MSS Kalan Süre: {format_time(remaining_times['mss'])}")

log('Eklenti: [%s] Sürüm %s Yüklendi. // edit by hakankahya' % (name, version))
