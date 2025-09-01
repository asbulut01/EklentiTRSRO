from phBot import *
import QtBind
import json
import time
import os

pName = 'DimensionalManuel'
pVersion = '1.3'

# ----------------- GUI ----------------- #
gui = QtBind.init(__name__, pName)
QtBind.createLabel(gui, "Dimensional Gate NPC Tarayýcý", 10, 10)

lstNPCs = QtBind.createList(gui, 10, 40, 200, 200)
lstOptions = QtBind.createList(gui, 220, 40, 200, 200)
lstPackets = QtBind.createList(gui, 440, 40, 400, 200)

QtBind.createButton(gui, 'scan_npcs', "Refresh NPCs", 10, 250)
QtBind.createButton(gui, 'show_packets', "Show Packets", 220, 250)
QtBind.createButton(gui, 'save_json', "Save JSON", 440, 250)

lblLastUpdate = QtBind.createLabel(gui, "", 10, 280)

# ----------------- Global ----------------- #
npc_data = {}
current_json = {}
saved_npcs = {}
file_path = os.path.join(get_config_dir(), "CustomNPC.json")

# Önceki kayýtlarý yükle
if os.path.exists(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            saved_npcs = json.load(f)
    except:
        saved_npcs = {}

# ----------------- Fonksiyonlar ----------------- #
def format_uid_bytes(uid):
    b1 = uid & 0xFF
    b2 = (uid >> 8) & 0xFF
    b3 = (uid >> 16) & 0xFF
    b4 = (uid >> 24) & 0xFF
    return f"{b1:02X} {b2:02X} {b3:02X} {b4:02X}"

def update_json_file(uid, name, packets):
    """JSON kaydýný ayrý fonksiyon ile yap"""
    global saved_npcs
    uid_str = str(uid)

    # Önceki kayýt ile karþýlaþtýr
    existing = saved_npcs.get(uid_str)
    if existing is None or existing.get("Packets") != packets:
        saved_npcs[uid_str] = {"Name": name, "Packets": packets}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(saved_npcs, f, indent=4, ensure_ascii=False)
        log(f"{pName}: NPC kaydedildi/güncellendi -> {name} (UID: {uid})")
    else:
        log(f"{pName}: NPC zaten güncel -> {name} (UID: {uid})")

def scan_npcs():
    global npc_data
    QtBind.clear(gui, lstNPCs)
    QtBind.clear(gui, lstOptions)
    QtBind.clear(gui, lstPackets)

    npcs = get_npcs()
    if not npcs:
        QtBind.append(gui, lstNPCs, "NPC yok")
        QtBind.setText(gui, lblLastUpdate, time.strftime("%H:%M:%S"))
        log(f"{pName}: NPC bulunamadý ({time.strftime('%H:%M:%S')})")
        return

    npc_data = {uid: npc for uid, npc in npcs.items()}
    for uid, npc in npc_data.items():
        name = npc.get('name', "Unknown")
        QtBind.append(gui, lstNPCs, f"{uid} - {name}")

    QtBind.setText(gui, lblLastUpdate, time.strftime("%H:%M:%S"))
    log(f"{pName}: NPC listesi güncellendi ({time.strftime('%H:%M:%S')})")

def show_packets():
    global current_json
    QtBind.clear(gui, lstOptions)
    QtBind.clear(gui, lstPackets)

    selected_index = QtBind.currentIndex(gui, lstNPCs)
    if selected_index == -1 or not npc_data:
        return

    uid_list = list(npc_data.keys())
    selected_uid = uid_list[selected_index]
    npc_info = npc_data[selected_uid]
    name = npc_info.get('name', "Unknown")

    hex_uid = format_uid_bytes(selected_uid)
    packet_list = [
        f"0x7045:{hex_uid}",
        f"0x704B:{hex_uid}",
        f"0x705A:{hex_uid} 03 00"
    ]

    for p in packet_list:
        QtBind.append(gui, lstOptions, p)

    current_json = {str(selected_uid): {"Name": name, "Packets": packet_list}}
    QtBind.append(gui, lstPackets, json.dumps(current_json, indent=4, ensure_ascii=False))
    log(f"{pName}: Paketler görüntülendi -> {name}")

def save_json():
    if not current_json:
        return
    uid_str = list(current_json.keys())[0]
    name = current_json[uid_str]["Name"]
    packets = current_json[uid_str]["Packets"]
    update_json_file(uid_str, name, packets)
    QtBind.append(gui, lstPackets, f"JSON kaydedildi: {file_path}")
