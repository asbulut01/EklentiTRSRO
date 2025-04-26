from phBot import *
from threading import Timer
import QtBind
import struct
import time

name = "TR_SpawnTimer"

is_running_timers = {"pandora": False, "mss": False}
timers = {"pandora": None, "mss": None}
intervals = {"pandora": 1, "mss": 1}
quantities = {"pandora": 1, "mss": 1}
remaining_times = {"pandora": 1, "mss": 1}
sequence_timers = {"pandora": None, "mss": None}

gui = QtBind.init(__name__, name)

lblPandoraFrame = QtBind.createList(gui, 50, 5, 300, 230)
lblPandoraHeader = QtBind.createLabel(gui, "<b>Otomatik Pandora Box</b>", 75, 10)
lblPandoraTimer = QtBind.createLabel(gui, "Pandora Kalan Süre: 00:00", 75, 40)
btnUsePandoraNow = QtBind.createButton(gui, 'use_pandora_now', " Şimdi Kullan ", 250, 38)
lblPandoraInterval = QtBind.createLabel(gui, "Pandora Süresi (dk):", 75, 80)
txtPandoraInterval = QtBind.createLineEdit(gui, str(intervals["pandora"]), 210, 77, 40, 20)
btnSetPandoraInterval = QtBind.createButton(gui, 'set_pandora_interval', " Süreyi Ayarla ", 75, 110)
lblPandoraQuantity = QtBind.createLabel(gui, "Adet (1-5):", 75, 150)
txtPandoraQuantity = QtBind.createLineEdit(gui, str(quantities["pandora"]), 210, 147, 40, 20)
btnSetPandoraQuantity = QtBind.createButton(gui, 'set_pandora_quantity', " Adet Ayarla ", 75, 180)
btnTogglePandora = QtBind.createButton(gui, 'toggle_pandora_timer', " Başlat ", 75, 210)

lblMSSFrame = QtBind.createList(gui, 375, 5, 300, 230)
lblMSSHeader = QtBind.createLabel(gui, "<b>Otomatik Monster Summon Scroll</b>", 400, 10)
lblMSSTimer = QtBind.createLabel(gui, "MSS Kalan Süre: 00:00", 400, 40)
btnUseMSSNow = QtBind.createButton(gui, 'use_mss_now', " Şimdi Kullan ", 575, 38)
lblMSSInterval = QtBind.createLabel(gui, "MSS Süresi (dk):", 400, 80)
txtMSSInterval = QtBind.createLineEdit(gui, str(intervals["mss"]), 535, 77, 40, 20)
btnSetMSSInterval = QtBind.createButton(gui, 'set_mss_interval', " Süreyi Ayarla ", 400, 110)
lblMSSQuantity = QtBind.createLabel(gui, "Adet (1-5):", 400, 150)
txtMSSQuantity = QtBind.createLineEdit(gui, str(quantities["mss"]), 535, 147, 40, 20)
btnSetMSSQuantity = QtBind.createButton(gui, 'set_mss_quantity', " Adet Ayarla ", 400, 180)
btnToggleMSS = QtBind.createButton(gui, 'toggle_mss_timer', " Başlat ", 400, 210)

def find_pandora():
    items = get_inventory()['items']
    for slot, item in enumerate(items):
        if item:
            if "ITEM_ETC_E060517_MON_GENERATION_BOX" in item['servername'] or \
               "ITEM_EVENT_GENERATION_BOX" in item['servername'] or \
               "ITEM_EVENT_RENT_E100222_MON_GENERATION_BOX" in item['servername']:
                return slot, item['servername']
    return None, None

def find_monstersc():
    items = get_inventory()['items']
    for slot, item in enumerate(items):
        if item:
            if "ITEM_ETC_E060517_SUMMON_PARTY_SCROLL" in item['servername'] or \
               "ITEM_ETC_E060526_SUMMON_PARTY_SCROLL_A" in item['servername'] or \
               "ITEM_EVENT_RENT_E100222_SUMMON_SCROLL" in item['servername']:
                return slot, item['servername']
    return None, None

def use_item(slot, item_type):
    if slot is None:
        log(f'TR_SpawnTimer: Kullanılacak {item_type} bulunamadı.')
        return False

    p = struct.pack('B', slot)
    if item_type == "pandora":
         p += b'\x30\x0c\x0f\x01'
         log(f"TR_SpawnTimer: Kullanildi 1x Pandora's Box (Slot: {slot})")
    elif item_type == "mss":
         p += b'\x30\x0c\x0f\x02'
         log(f'TR_SpawnTimer: Kullanildi 1x Monster Summon Scroll (Slot: {slot})')
    else:
        log(f'TR_SpawnTimer: Bilinmeyen eşya tipi: {item_type}')
        return False

    inject_joymax(0x704C, p, True)
    return True

def use_pandora_now():
    slot, servername = find_pandora()
    if slot is not None:
        use_item(slot, "pandora")
    else:
        log(r'TR_SpawnTimer: Pandora Box Envanterde bulunamadı.')

def use_mss_now():
    slot, servername = find_monstersc()
    if slot is not None:
        use_item(slot, "mss")
    else:
        log(r'TR_SpawnTimer: Monster Summon Scroll Envanterde bulunamadı.')

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
    log(f"TR_SpawnTimer: {timer_type.capitalize()} zamanlayıcı {intervals[timer_type]} dakika, {quantities[timer_type]} adet ile başlatıldı.")
    reset_timer(timer_type)

def reset_timer(timer_type):
    global timers, remaining_times
    update_labels()
    if is_running_timers[timer_type]:
        if timers.get(timer_type):
             timers[timer_type].cancel()
        timers[timer_type] = Timer(1.0, countdown_timer, args=[timer_type])
        timers[timer_type].start()

def stop_timer(timer_type):
    global is_running_timers, timers, sequence_timers
    is_running_timers[timer_type] = False
    if timers.get(timer_type):
        timers[timer_type].cancel()
        timers[timer_type] = None
    if sequence_timers.get(timer_type):
        sequence_timers[timer_type].cancel()
        sequence_timers[timer_type] = None
    log(f"TR_SpawnTimer: {timer_type.capitalize()} zamanlayıcı durduruldu.")
    remaining_times[timer_type] = intervals[timer_type] * 60
    update_labels()
    QtBind.setText(gui, btnTogglePandora if timer_type == 'pandora' else btnToggleMSS, " Başlat ")

def countdown_timer(timer_type):
    global timers, remaining_times, is_running_timers
    if not is_running_timers[timer_type]:
        return

    if remaining_times[timer_type] > 0:
        remaining_times[timer_type] -= 1
        update_labels()
        timers[timer_type] = Timer(1.0, countdown_timer, args=[timer_type])
        timers[timer_type].start()
    else:
        log(f"TR_SpawnTimer: {timer_type.capitalize()} süresi doldu. Kullanım sırası başlıyor...")
        use_item_sequence(timer_type, quantities[timer_type])

def use_item_sequence(timer_type, count):
    global sequence_timers, is_running_timers

    if not is_running_timers[timer_type]:
        log(f"TR_SpawnTimer: {timer_type.capitalize()} zamanlayıcı durdurulduğu için kullanım sırası iptal edildi.")
        return

    if count <= 0:
        log(f"TR_SpawnTimer: {timer_type.capitalize()} kullanım sırası tamamlandı.")
        slot, _ = find_pandora() if timer_type == "pandora" else find_monstersc()
        if slot is None:
             log(f"TR_SpawnTimer: {timer_type.capitalize()} envanterde kalmadı, zamanlayıcı durduruluyor.")
             stop_timer(timer_type)
             return

        remaining_times[timer_type] = intervals[timer_type] * 60
        reset_timer(timer_type)
        return

    slot, servername = find_pandora() if timer_type == "pandora" else find_monstersc()

    if slot is not None:
        log(f"TR_SpawnTimer: {timer_type.capitalize()} kullanılıyor... Kalan: {count-1}")
        used = use_item(slot, timer_type)
        if used:
            if count > 1:
                if sequence_timers.get(timer_type):
                    sequence_timers[timer_type].cancel()
                sequence_timers[timer_type] = Timer(2.0, use_item_sequence, args=[timer_type, count - 1])
                sequence_timers[timer_type].start()
            else:
                log(f"TR_SpawnTimer: {timer_type.capitalize()} son kullanım tamamlandı.")
                remaining_times[timer_type] = intervals[timer_type] * 60
                reset_timer(timer_type)
        else:
             log(f"TR_SpawnTimer: {timer_type.capitalize()} kullanılamadı (Inject başarısız?). Zamanlayıcı durduruluyor.")
             stop_timer(timer_type)
    else:
        log(f"TR_SpawnTimer: {timer_type.capitalize()} kullanım sırasında envanterde bulunamadı. Zamanlayıcı durduruluyor.")
        stop_timer(timer_type)

def set_pandora_interval():
    global intervals
    try:
        pandora_interval = int(QtBind.text(gui, txtPandoraInterval))
        if pandora_interval > 0:
            intervals["pandora"] = pandora_interval
            log(f"TR_SpawnTimer: Pandora süresi {pandora_interval} dk olarak ayarlandı.")
            if is_running_timers["pandora"]:
               remaining_times["pandora"] = intervals["pandora"] * 60
               update_labels()
        else:
            log("TR_SpawnTimer: Pandora süresi pozitif bir değer olmalıdır.")
    except ValueError:
        log("TR_SpawnTimer: Pandora süresi için geçerli bir sayı giriniz.")

def set_mss_interval():
    global intervals
    try:
        mss_interval = int(QtBind.text(gui, txtMSSInterval))
        if mss_interval > 0:
            intervals["mss"] = mss_interval
            log(f"TR_SpawnTimer: MSS süresi {mss_interval} dk olarak ayarlandı.")
            if is_running_timers["mss"]:
               remaining_times["mss"] = intervals["mss"] * 60
               update_labels()
        else:
            log("TR_SpawnTimer: MSS süresi pozitif bir değer olmalıdır.")
    except ValueError:
        log("TR_SpawnTimer: MSS süresi için geçerli bir sayı giriniz.")

def set_pandora_quantity():
    global quantities
    try:
        pandora_quantity = int(QtBind.text(gui, txtPandoraQuantity))
        if 1 <= pandora_quantity <= 5:
            quantities["pandora"] = pandora_quantity
            log(f"TR_SpawnTimer: Pandora adedi {pandora_quantity} olarak ayarlandı.")
        else:
            log("TR_SpawnTimer: Pandora adedi 1 ile 5 arasında olmalıdır.")
            QtBind.setText(gui, txtPandoraQuantity, str(quantities["pandora"]))
    except ValueError:
        log("TR_SpawnTimer: Pandora adedi için geçerli bir sayı giriniz.")
        QtBind.setText(gui, txtPandoraQuantity, str(quantities["pandora"]))

def set_mss_quantity():
    global quantities
    try:
        mss_quantity = int(QtBind.text(gui, txtMSSQuantity))
        if 1 <= mss_quantity <= 5:
            quantities["mss"] = mss_quantity
            log(f"TR_SpawnTimer: MSS adedi {mss_quantity} olarak ayarlandı.")
        else:
            log("TR_SpawnTimer: MSS adedi 1 ile 5 arasında olmalıdır.")
            QtBind.setText(gui, txtMSSQuantity, str(quantities["mss"]))
    except ValueError:
        log("TR_SpawnTimer: MSS adedi için geçerli bir sayı giriniz.")
        QtBind.setText(gui, txtMSSQuantity, str(quantities["mss"]))

def update_labels():
    def format_time(seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    QtBind.setText(gui, lblPandoraTimer, f"Pandora Kalan Süre: {format_time(remaining_times['pandora'])}")
    QtBind.setText(gui, lblMSSTimer, f"MSS Kalan Süre: {format_time(remaining_times['mss'])}")

log(f'Eklenti: {name} başarıyla yüklendi.')
update_labels()