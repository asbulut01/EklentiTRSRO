from phBot import *
from threading import Thread
from time import sleep
from binascii import hexlify
import QtBind
import struct
import copy
import re

pName = 'TR_ItemManager'

gui = QtBind.init(__name__, pName)
lblCizgi1 = QtBind.createList(gui,10,10,200,250)
lblSırala = QtBind.createLabel(gui,' Eşyaları Sırala: ', 80, 20)
btnSıralaEnvanter = QtBind.createButton(gui,'sort_items_inventory', ' Envanter ', 75, 50)
btnSıralaDepo = QtBind.createButton(gui,'sort_items_storage', ' Depo ', 75, 80)
btnSıralaGuild = QtBind.createButton(gui,'sort_items_guild_storage', ' Guild Deposu ', 75, 110)
lblDurdur = QtBind.createLabel(gui,'Devam Eden Sıralamayı Durdur:', 35, 160)
btnDurdur = QtBind.createButton(gui,'stop_processing',"  Durdur  ", 75, 190)
lblCizgi2 = QtBind.createList(gui, 211, 10, 200, 250)
lblAltınAlDepola = QtBind.createLabel(gui,'Altın Depola/Altın Al:', 260, 20)
lblDepo = QtBind.createLabel(gui,'Depo', 235, 40)
store_take_gold_storage_amount_widget_widget = QtBind.createLineEdit(gui,"0", 235, 60, 145, 20)
btnDepolaGold = QtBind.createButton(gui,'store_gold_storage', 'Depola ', 310, 90)
btnAlGold = QtBind.createButton(gui,'take_gold_storage', 'Al', 230, 90)
lblGuildDepo = QtBind.createLabel(gui,'Guild Deposu', 235, 130)
store_take_gold_guild_storage_amount_widget = QtBind.createLineEdit(gui,"0", 235, 150, 145, 20)
btnGDepolaGold = QtBind.createButton(gui,'store_gold_guild_storage', ' Depola ', 310, 180)
btnGAlGold = QtBind.createButton(gui,'take_gold_guild_storage', ' Al ', 230, 180)
lblCizgi3 = QtBind.createList(gui, 412, 10, 200, 250)
lblDebugMod = QtBind.createLabel(gui,'Debug Modu:', 475, 20)
debug_list_widget = QtBind.createList(gui, 460, 60, 100, 80)
QtBind.append(gui, debug_list_widget, '0 (Varsayılan)')
QtBind.append(gui, debug_list_widget, '1')
QtBind.append(gui, debug_list_widget, '2')
QtBind.append(gui, debug_list_widget, '3 (Maksimum)')
btnDegistir = QtBind.createButton(gui,'set_debug_mode', ' Değiştir ', 470, 160)

debug = 0
running = False
thread = False

npc_servernames = {
    'storage': [
        'NPC_CH_WAREHOUSE_M',  # jangan #1
        'NPC_CH_WAREHOUSE_W',  # jangan #2
        'NPC_EU_WAREHOUSE',  # constantinople
        'NPC_WC_WAREHOUSE_M',  # donwhang #1
        'NPC_WC_WAREHOUSE_W',  # donwhang #2
        'NPC_CA_WAREHOUSE',  # samarkand
        'NPC_KT_WAREHOUSE',  # hotan
        'NPC_AR_WAREHOUSE',  # bagdad
        'NPC_SD_M_AREA_WAREHOUSE',  # alexandria south
        'NPC_SD_T_AREA_WAREHOUSE2'  # alexandria north
    ],
    'guild_storage': [
        'NPC_CH_GENARAL_SP',  # jangan
        'NPC_WC_GUILD',  # donwhang
        'NPC_CA_GUILD',  # samarkand
        'NPC_SD_M_AREA_GUILD',  # alexandria south
        'NPC_SD_T_AREA_GUILD2'  # alexandria north
    ]
}

store_take_gold_storage_amount_widget_widget_default = '0'
store_take_gold_guild_storage_amount_widget_default = '0'

def inject_client(opcode, data, encrypted):
    global debug
    if debug >= 3:
        log('[%s] DEBUG3: Bottan Cliente' % (__name__))
        log('[%s] DEBUG3:  └ OPCODE: 0x%02X' % (__name__, opcode))
        if data is not None:
            log('[%s] DEBUG3:  └ Data: %s' % (__name__, hexlify(data)))
    return inject_silkroad(opcode, data, encrypted)

def inject_server(opcode, data, encrypted):
    global debug
    if debug >= 3:
        log('[%s] DEBUG3: Bottan Servere' % (__name__))
        log('[%s] DEBUG3:  └ OPCODE: 0x%02X' % (__name__, opcode))
        if data is not None:
            log('[%s] DEBUG3:  └ Data: %s' % (__name__, hexlify(data)))
    return inject_joymax(opcode, data, encrypted)

def handle_silkroad(opcode, data):
    global running
    if running == 'guild_storage':
        if opcode in [0x7250, 0x7251, 0x7252]:
            return False
    return True

def get_running_job():
    global running
    if running == 'sort_items_inventory':
        return 'Envanterdeki Eşyalar'
    elif running == 'sort_items_storage':
        return 'Depodaki Eşyalar'
    elif running == 'sort_items_guild_storage':
        return 'Guild Deposundaki Eşyalar'
    elif running == 'store_gold_storage':
        return 'Depoya Depolanan Gold'
    elif running == 'store_gold_guild_storage':
        return 'Guild Deposuna Depolanan Gold'
    elif running == 'take_gold_storage':
        return 'Depodan Alınan Gold'
    elif running == 'take_gold_guild_storage':
        return 'Guild Deposundan Alınan Gold'

def wait_for_thread_end(clean_end, job):
    global thread
    if clean_end != True:
        thread.join()
    thread = False
    log('[%s] %s: Tamamlandı.' % (__name__, job))

def stop_processing(clean_end=False):
    global running
    global thread
    if running == False or thread == False:
        return
    job = get_running_job()
    running = False
    Thread(target=wait_for_thread_end, args=(clean_end, job)).start()

def set_debug_mode():
    global gui
    global debug
    global debug_list_widget
    mode = QtBind.currentIndex(gui, debug_list_widget)
    if mode < 0 or mode > 3:
        mode = 0
    if debug == mode:
        return
    prev_mode = debug
    debug = mode
    log('[%s] %s:  %i > %i  Değiştirildi.' % (__name__, 'DEBUG-MODU', prev_mode, mode))
    pass

def sort_items_inventory():
    global running
    global thread
    if running != False:
        return
    running = 'sort_items_inventory'
    job = get_running_job()
    log('[%s] %s: Başlıyor...' % (__name__, get_running_job()))
    thread = Thread(target=sort_items, args=('inventory',))
    thread.start()

def sort_items_storage():
    global running
    global thread
    if running != False:
        return
    running = 'sort_items_storage'
    log('[%s] %s: Başlıyor...' % (__name__, get_running_job()))
    thread = Thread(target=sort_items, args=('storage',))
    thread.start()

def sort_items_guild_storage():
    global running
    global thread
    if running != False:
        return
    running = 'sort_items_guild_storage'
    log('[%s] %s: Başlıyor...' % (__name__, get_running_job()))
    thread = Thread(target=sort_items, args=('guild_storage',))
    thread.start()

def store_gold_storage():
    global gui
    global running
    global thread
    global store_take_gold_storage_amount_widget_widget
    global store_take_gold_storage_amount_widget_widget_default
    if running != False:
        return
    running = 'store_gold_storage'
    log('[%s] %s: Başlıyor....' % (__name__, get_running_job()))
    amount = fetch_amount(QtBind.text(gui, store_take_gold_storage_amount_widget_widget))
    QtBind.setText(gui, store_take_gold_storage_amount_widget_widget,
                   store_take_gold_storage_amount_widget_widget_default)
    thread = Thread(target=store_gold, args=('storage', amount,))
    thread.start()

def store_gold_guild_storage():
    global gui
    global running
    global thread
    global store_take_gold_guild_storage_amount_widget
    global store_take_gold_guild_storage_amount_widget_default
    if running != False:
        return
    running = 'store_gold_guild_storage'
    log('[%s] %s: Başlıyor...' % (__name__, get_running_job()))
    amount = fetch_amount(QtBind.text(gui, store_take_gold_guild_storage_amount_widget))
    QtBind.setText(gui, store_take_gold_guild_storage_amount_widget,
                   store_take_gold_guild_storage_amount_widget_default)
    thread = Thread(target=store_gold, args=('guild_storage', amount,))
    thread.start()

def take_gold_storage():
    global gui
    global running
    global thread
    global store_take_gold_storage_amount_widget_widget
    global store_take_gold_storage_amount_widget_widget_default
    if running != False:
        return
    running = 'take_gold_storage'
    log('[%s] %s: Başlıyor...' % (__name__, get_running_job()))
    amount = fetch_amount(QtBind.text(gui, store_take_gold_storage_amount_widget_widget))
    QtBind.setText(gui, store_take_gold_storage_amount_widget_widget,
                   store_take_gold_storage_amount_widget_widget_default)
    thread = Thread(target=take_gold, args=('storage', amount,))
    thread.start()

def take_gold_guild_storage():
    global gui
    global running
    global thread
    global store_take_gold_guild_storage_amount_widget
    global store_take_gold_guild_storage_amount_widget_default
    if running != False:
        return
    running = 'take_gold_guild_storage'
    log('[%s] %s: Başlıyor...' % (__name__, get_running_job()))
    amount = fetch_amount(QtBind.text(gui, store_take_gold_guild_storage_amount_widget))
    QtBind.setText(gui, store_take_gold_guild_storage_amount_widget,
                   store_take_gold_guild_storage_amount_widget_default)
    thread = Thread(target=take_gold, args=('guild_storage', amount,))
    thread.start()

def fetch_amount(amount):
    amount = re.sub('[kK]', '000', amount)
    amount = re.sub('[mM]', '000000', amount)
    amount = re.sub('[bB]', '000000000', amount)
    if amount == 'all' or re.match('^0+$', amount):
        return 0
    elif re.match('^\d+$', amount):
        return int(amount)
    return -1

def npc_get_id(type):
    global npc_servernames
    npc_keys = array_get_subkey_filterd_keys(get_npcs(), 'servername', npc_servernames[type])
    if len(npc_keys) == 0:
        return False
    return struct.pack('<H', npc_keys[0])

def send_npc_select(type, timeout=1.0):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: NPC Seçimi' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Cins: %s' % (__name__, type))
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    npc_id = npc_get_id(type)
    if npc_id == False:
        return False
    if debug >= 2:
        log('[%s] DEBUG2:  └ npc_id: %s' % (__name__, hexlify(npc_id)))
    opcode = 0x7045
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray(npc_id)
    packet += b'\x00\x00'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor...' % (__name__))
    sleep(timeout)

def send_npc_unselect(timeout=0.5):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: NPC Çıkışı.' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    opcode = 0xB04B
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray(b'\x01')
    inject_client(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def send_guild_storage_lock(timeout=0.5):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Guild Deposu Kilidi.' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    npc_id = npc_get_id('guild_storage')
    if npc_id == False:
        return False
    if debug >= 2:
        log('[%s] DEBUG2:  └ NPC ID: %s' % (__name__, hexlify(npc_id)))
    opcode = 0x7250
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray(npc_id)
    packet += b'\x00\x00'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def send_guild_storage_unlock(timeout=0.5):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Guild Deposu Kilidi Açma' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    npc_id = npc_get_id('guild_storage')
    if npc_id == False:
        return False
    if debug >= 2:
        log('[%s] DEBUG2:  └ NPC ID: %s' % (__name__, hexlify(npc_id)))
    opcode = 0x7251
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray(npc_id)
    packet += b'\x00\x00'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def send_storage_refresh(timeout=1.0):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Depo Yenileniyor...' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    npc_id = npc_get_id('storage')
    if npc_id == False:
        return False
    if debug >= 2:
        log('[%s] DEBUG2:  └ NPC ID: %s' % (__name__, hexlify(npc_id)))
    opcode = 0x703C
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray(npc_id)
    packet += b'\x00\x00\x00'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def send_guild_storage_refresh(timeout=1.0):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Guild Depo Yenileniyor...' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    npc_id = npc_get_id('guild_storage')
    if npc_id == False:
        return False
    if debug >= 2:
        log('[%s] DEBUG2:  └ NPC ID: %s' % (__name__, hexlify(npc_id)))
    opcode = 0x7252
    packet = bytearray(npc_id)
    packet += b'\x00\x00'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def send_storage_open(timeout=1.0):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Depo Açılışı.' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    npc_id = npc_get_id('storage')
    if npc_id == False:
        return False
    if debug >= 2:
        log('[%s] DEBUG2:  └ NPC ID: %s' % (__name__, hexlify(npc_id)))
    opcode = 0x7046
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray(npc_id)
    packet += b'\x00\x00\x03'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def send_guild_storage_open(timeout=1.0):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Guild Depo Açılışı.' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    npc_id = npc_get_id('guild_storage')
    if npc_id == False:
        return False
    if debug >= 2:
        log('[%s] DEBUG2:  └ NPC ID: %s' % (__name__, hexlify(npc_id)))
    opcode = 0x7046
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray(npc_id)
    packet += b'\x00\x00\x0f'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def send_storage_close(timeout=0.5):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Depo Kapanışı.' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    npc_id = npc_get_id('storage')
    if npc_id == False:
        return False
    if debug >= 2:
        log('[%s] DEBUG2:  └ NPC ID: %s' % (__name__, hexlify(npc_id)))
    opcode = 0x704B
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray(npc_id)
    packet += b'\x00\x00'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def send_guild_storage_close(timeout=0.5):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Guild Depo Kapanışı.' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    npc_id = npc_get_id('guild_storage')
    if npc_id == False:
        return False
    if debug >= 2:
        log('[%s] DEBUG2:  └ NPC ID: %s' % (__name__, hexlify(npc_id)))
    opcode = 0x704B
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray(npc_id)
    packet += b'\x00\x00'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def send_move_item(type, source_slot, destination_slot, timeout=1.0):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Item Taşıma.' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Mevcut Slot: %i' % (__name__, source_slot))
        log('[%s] DEBUG2:  └ Hedef Slot: %i' % (__name__, destination_slot))
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    if (
        get_items(type)['size'] == 0
        or source_slot > get_items(type)['size']
        or source_slot < 0
        or destination_slot > get_items(type)['size']
        or destination_slot < 0
        or (
        get_items(type)['items'][source_slot] is None
        and
        get_items(type)['items'][destination_slot] is None
    )
    ):
        return False
    opcode = 0x7034
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray()
    if type == 'inventory':
        packet += b'\x00'
    elif type == 'storage':
        packet += b'\x01'
    elif type == 'guild_storage':
        packet += b'\x1d'
    packet.append(source_slot)
    packet.append(destination_slot)
    packet += struct.pack('<H', get_items(type)['items'][source_slot]['quantity'])
    if type == 'storage' or type == 'guild_storage':
        npc_id = npc_get_id(type)
        if npc_id == False:
            return False
        if debug >= 2:
            log('[%s] DEBUG2:  └ NPC ID: %s' % (__name__, hexlify(npc_id)))
        packet += npc_id
        packet += b'\x00\x00'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor....' % (__name__))
    sleep(timeout)

def send_store_gold(type, amount, timeout=1.0):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Altın Depola' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    opcode = 0x7034
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray()
    if type == 'storage':
        packet += b'\x0c'
    else:  # type == 'guild_storage'
        packet += b'\x20'
    packet += struct.pack('<L', amount)
    packet += b'\x00\x00\x00\x00'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def send_take_gold(type, amount, timeout=1.0):
    global debug
    if debug >= 1:
        log('[%s] DEBUG1: Gönderiliyor: Altın Al' % (__name__))
    if debug >= 2:
        log('[%s] DEBUG2:  └ Zaman Aşımı: %.1f' % (__name__, timeout))
    opcode = 0x7034
    if debug >= 2:
        log('[%s] DEBUG2:  └ OPCODE: 0x%02X' % (__name__, opcode))
    packet = bytearray()
    if type == 'storage':
        packet += b'\x0b'
    else:  # type == 'guild_storage'
        packet += b'\x21'
    packet += struct.pack('<L', amount)
    packet += b'\x00\x00\x00\x00'
    inject_server(opcode, packet, False)
    if debug >= 1:
        log('[%s] DEBUG1:  └ Paket Gönderiliyor.....' % (__name__))
    sleep(timeout)

def array_sort_by_subkey(array, subkey):
    if not isinstance(array, (list, dict)):
        return False
    sorted_array = copy.deepcopy(array)
    for i, elem in enumerate(sorted_array):
        if not isinstance(elem, (list, dict)):
            sorted_array[i] = elem = {subkey: ''}
        if subkey not in elem:
            sorted_array[i] = elem = {subkey: ''}
        for o, subelem in elem.items():
            if not isinstance(subelem, (int, str)):
                sorted_array[i][o] = ''
    sorted_array = sorted(sorted_array, key=lambda subarray: subarray[subkey], reverse=True)
    return sorted_array

def array_get_subkey_filterd_keys(array, subkey, values):
    keys = []
    if isinstance(array, list):
        for i, subarray in enumerate(array):
            if not isinstance(subarray, (list, dict)):
                continue
            if isinstance(subarray, dict):
                if not subkey in subarray:
                    continue
            if not isinstance(values, list):
                values = [values]
            for value in values:
                if subarray[subkey] == value:
                    keys.append(i)
    elif isinstance(array, dict):
        for i, subarray in array.items():
            if not isinstance(subarray, (list, dict)):
                continue
            if isinstance(subarray, dict):
                if not subkey in subarray:
                    continue
            if not isinstance(values, list):
                values = [values]
            for value in values:
                if subarray[subkey] == value:
                    keys.append(i)
    else:
        return False
    return keys

def get_items(type):
    if type == 'inventory':
        return get_inventory()
    elif type == 'storage':
        return get_storage()
    elif type == 'guild_storage':
        return get_guild_storage()
    return False

def sort_items(type):
    global running
    if type == 'storage':
        send_npc_select(type)
        send_storage_open()
        send_storage_refresh()
        item_start_slot = 0
    elif type == 'guild_storage':
        send_npc_select(type)
        send_guild_storage_open()
        send_guild_storage_lock()
        send_guild_storage_refresh()
        item_start_slot = 0
    elif type == 'inventory':
        item_start_slot = 13
    else:
        return
    for i in range(item_start_slot, get_items(type)['size']):
        if running == False:
            break
        sorted_items = array_sort_by_subkey(get_items(type)['items'][i:], 'servername')
        if sorted_items == False or len(sorted_items) == 0:
            continue
        item_slots = array_get_subkey_filterd_keys(get_items(type)['items'][i:], 'servername',
                                                   sorted_items[0]['servername'])
        if item_slots == False or len(item_slots) == 0:
            break
        if i + item_slots[0] == i:
            continue
        log('[%s] %s: %i Nolu Slottan  %i Nolu Slota Taşınıyor.' % (__name__, get_running_job(), i + item_slots[0], i))
        send_move_item(type, i + item_slots[0], i)
    if type == 'storage':
        send_storage_close()
        send_npc_unselect()
    elif type == 'guild_storage':
        send_guild_storage_unlock()
        send_guild_storage_close()
    stop_processing(True)

def store_gold(type, amount):
    max_gold = get_character_data()['gold']
    if amount == 0 or amount > max_gold:
        amount = max_gold
    if amount > 0:
        if type == 'storage':
            send_npc_select(type)
            send_storage_open()
            send_storage_refresh()
        elif type == 'guild_storage':
            send_npc_select(type)
            send_guild_storage_open()
            send_guild_storage_lock()
            send_guild_storage_refresh()
        else:
            return
        while amount >= 10 ** 9:
            if running == False:
                break
            log('[%s] %s: %s Altın Depolanıyor.' % (__name__, get_running_job(), 10 ** 9))
            send_store_gold(type, 10 ** 9)
            amount -= 10 ** 9
        if running != False:
            if amount % 10 ** 9:
                log('[%s] %s: %s Altın Depolanıyor.' % (__name__, get_running_job(), amount))
                send_store_gold(type, amount)
    if type == 'storage':
        send_storage_close()
        send_npc_unselect()
    elif type == 'guild_storage':
        send_guild_storage_unlock()
        send_guild_storage_close()
    stop_processing(True)

def take_gold(type, amount):
    max_gold = 0
    if amount > 0:
        if type == 'storage':
            send_npc_select(type)
            send_storage_open()
            send_storage_refresh()
        elif type == 'guild_storage':
            send_npc_select(type)
            send_guild_storage_open()
            send_guild_storage_lock()
            send_guild_storage_refresh()
        else:
            return
        while amount >= 10 ** 9:
            if running == False:
                break
            log('[%s] %s:  %s Altın Alınıyor.' % (__name__, get_running_job(), 10 ** 9))
            send_take_gold(type, 10 ** 9)
            amount -= 10 ** 9
        if running != False:
            if amount % 10 ** 9:
                log('[%s] %s: %s Altın Alınıyor.' % (__name__, get_running_job(), amount))
                send_take_gold(type, amount)
    if type == 'storage':
        send_storage_close()
        send_npc_unselect()
    elif type == 'guild_storage':
        send_guild_storage_unlock()
        send_guild_storage_close()
    stop_processing(True)

log('Eklenti: '+ pName +' başarıyla yüklendi.')
