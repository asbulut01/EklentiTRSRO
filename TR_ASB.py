from phBot import *
import QtBind
import traceback

name = 'ASB'

gui = QtBind.init(__name__, name)

# Sol panel başlığı
lblPanel1 = QtBind.createLabel(gui, "Sol Panel", 20, 40)
# Sol panel (liste)
lstPanel1 = QtBind.createList(gui, 20, 60, 200, 200)
# Sol panel butonu (fonksiyon adı: button_panel1)
btnPanel1 = QtBind.createButton(gui, 'button_panel1', 'NPC Tara', 20, 270)
# Manual button (below NPC Tara)
btnManualTeleport = QtBind.createButton(gui, 'button_manual_teleport', 'Manuel Teleport', 20, 300)

# Sağ panel başlığı
lblPanel2 = QtBind.createLabel(gui, "Sağ Panel", 240, 40)
# Sağ panel (liste)
lstPanel2 = QtBind.createList(gui, 240, 60, 200, 200)


def scan_npcs():
    """Scan nearby NPCs and return a list of 4-byte hex UID strings. Logs results instead of using GUI panels.

    Returns: list of hex strings like ['AA BB CC DD', ...]
    """
    hex_list = []
    try:
        npcs = get_npcs()
        if not npcs:
            log("TR_ASB: Yakında NPC yok.")
            return hex_list

        # If get_npcs returns a dict (uid -> npc)
        if isinstance(npcs, dict):
            for uid, npc in npcs.items():
                npc_name = npc.get('name', 'Bilinmeyen') if isinstance(npc, dict) else str(npc)
                distance = npc.get('distance', 0) if isinstance(npc, dict) else 0
                log(f"TR_ASB: {uid} - {npc_name} ({distance}m)")

                pack_str = format_npc_pack(npc)
                if pack_str and pack_str != 'Paket yok veya erişilemez':
                    log(f"TR_ASB: {uid} - {npc_name}: {pack_str}")
                else:
                    hex_uid = format_uid_bytes(uid)
                    log(f"TR_ASB: {uid} - UID_HEX: {hex_uid}")
                    hex_list.append(hex_uid)

            log(f"TR_ASB: {len(npcs)} adet NPC bulundu.")
            return hex_list

        # Fallback: iterable/list handling
        for npc in npcs:
            if isinstance(npc, dict):
                npc_name = npc.get('name', 'Bilinmeyen')
                distance = npc.get('distance', 0)
                uid = npc.get('id') if 'id' in npc else None
            elif isinstance(npc, (list, tuple)):
                npc_name = str(npc[0]) if len(npc) >= 1 else 'Bilinmeyen'
                distance = npc[1] if len(npc) >= 2 and isinstance(npc[1], (int, float)) else 0
                uid = npc[2] if len(npc) >= 3 else None
            elif isinstance(npc, int):
                npc_name = f"NPC_ID_{npc}"
                distance = 0
                uid = npc
            else:
                npc_name = str(npc)
                distance = 0
                uid = None

            log(f"TR_ASB: {npc_name} ({distance}m)")
            pack_str = format_npc_pack(npc)
            log(f"TR_ASB: {npc_name}: {pack_str}")
            if uid is not None:
                hex_uid = format_uid_bytes(uid)
                log(f"TR_ASB: UID_HEX: {hex_uid}")
                hex_list.append(hex_uid)

        log("TR_ASB: NPC tarama tamamlandı.")
        return hex_list
    except Exception:
        log("TR_ASB: NPC taraması sırasında hata oluştu. Hata ayrıntıları eklendi.")
        for line in traceback.format_exc().splitlines():
            log(line)
        return hex_list


def format_npc_pack(npc):
    """Try to extract package contents from npc object in several common formats and return a short string."""
    items = None
    info = None

    if isinstance(npc, int):
        npc_id = npc
        for fn in ('get_npc', 'get_entity', 'get_npc_by_id', 'get_mob'):
            try:
                if fn in globals() and callable(globals()[fn]):
                    info = globals()[fn](npc_id)
                    break
            except Exception:
                info = None

    if isinstance(npc, dict):
        info = npc

    if isinstance(info, dict):
        for key in ('items', 'pack', 'package', 'inventory', 'loot'):
            if key in info and info[key]:
                items = info[key]
                break

    if items is None and isinstance(npc, dict) and 'id' in npc:
        try:
            for fn in ('get_npc_by_id', 'get_npc', 'get_entity'):
                if fn in globals() and callable(globals()[fn]):
                    info2 = globals()[fn](npc['id'])
                    if isinstance(info2, dict):
                        for key in ('items', 'inventory', 'pack', 'package', 'loot'):
                            if key in info2 and info2[key]:
                                items = info2[key]
                                break
                    if items:
                        break
        except Exception:
            items = None

    if not items:
        return 'Paket yok veya erişilemez'

    parts = []
    for it in items:
        if isinstance(it, dict):
            it_name = it.get('name') or str(it.get('id', 'bilinmeyen'))
            qty = it.get('count') or it.get('quantity') or it.get('qty') or 1
            parts.append(f"{it_name} x{qty}")
        elif isinstance(it, (list, tuple)):
            it_name = str(it[0]) if len(it) > 0 else 'bilinmeyen'
            qty = it[1] if len(it) > 1 else 1
            parts.append(f"{it_name} x{qty}")
        else:
            parts.append(str(it))

    return ', '.join(parts) if parts else 'Boş paket'


def format_uid_bytes(uid):
    try:
        uid_int = int(uid)
    except Exception:
        return '00 00 00 00'
    b1 = uid_int & 0xFF
    b2 = (uid_int >> 8) & 0xFF
    b3 = (uid_int >> 16) & 0xFF
    b4 = (uid_int >> 24) & 0xFF
    return f"{b1:02X} {b2:02X} {b3:02X} {b4:02X}"


def get_first_npc_hex():
    """Return first found NPC 4-byte hex string (e.g. 'AA BB CC DD') or None."""
    try:
        hex_list = scan_npcs()
        if hex_list and len(hex_list) > 0:
            return hex_list[0]
    except Exception:
        for line in traceback.format_exc().splitlines():
            log(line)
    return None


def button_manual_teleport():
    """Manual button: scan NPCs and log the first NPC hex (no teleport performed)."""
    try:
        first_hex = get_first_npc_hex()
        if first_hex:
            log(f"TR_ASB: İlk bulunan NPC hex: {first_hex}")
            return first_hex
        else:
            log('TR_ASB: Yakında NPC yok veya hex alınamadı.')
            return None
    except Exception:
        log('TR_ASB: Manuel işlem sırasında hata oluştu.')
        for line in traceback.format_exc().splitlines():
            log(line)
        return None


log(f'Eklenti: {name} başarıyla yüklendi.')