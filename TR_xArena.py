from phBot import *
from threading import Timer
import random
import struct

pName = 'TR_xArena'

InBattleArena = False
InCTF = False
isPluginRegistering = False

def GetNPCUniqueID(name):
    NPCs = get_npcs()
    if NPCs:
        name = name.lower()
        for UniqueID, NPC in NPCs.items():
            NPCName = NPC['name'].lower()
            if name in NPCName:
                return UniqueID
    return 0

def InjectRandomMovement(radiusMax=10):
    pX = 0
    pY = 0
    while pX == 0 and pY == 0:
        pX = random.uniform(-radiusMax, radiusMax)
        pY = random.uniform(-radiusMax, radiusMax)
    p = get_position()
    pX = pX + p["x"]
    pY = pY + p["y"]
    move_to(pX, pY, p["z"])
    log("TR_xArena: Rastgele hareket (X:%.1f,Y:%.1f)" % (pX, pY))

def AntiAFK():
    if InBattleArena or InCTF:
        InjectRandomMovement(1)
        Timer(random.uniform(2.5, 5), AntiAFK).start()

def arena(args):
    if len(args) < 2:
        log('TR_xArena: Scriptte arena tipi eksik')
        return 0

    NPCID = GetNPCUniqueID('Arena Manager')

    if NPCID == 0:
        log('TR_xArena: "Arena Manager" yakınlarda değil. Komutu NPC\'nin yakınında kullandığınızdan emin olun')
    else:
        t1 = args[1].lower()
        t2 = ''
        if len(args) >= 3:
            t2 = args[2].lower()

        p = b'\x01'

        if t1 == 'random':
            p += struct.pack('B', 0)
        elif t1 == 'party':
            p += struct.pack('B', 1)
        elif t1 == 'guild':
            p += struct.pack('B', 2)
        elif t1 == 'job':
            p += struct.pack('B', 3)
        else:
            log('TR_xArena: Yanlış Savaş Arenası tipi. Lütfen şunlardan birini seçtiğinizden emin olun: Random, Party, Guild veya Job')
            return 0

        if t2 == '':
            pass
        elif t2 == 'score':
            p += struct.pack('B', 1)
        elif t2 == 'flag':
            p += struct.pack('B', 2)
        else:
            log('TR_xArena: Yanlış Savaş Arenası tipi. Lütfen şunlardan birini seçtiğinizden emin olun: Score veya Flag')
            return 0

        global isPluginRegistering
        isPluginRegistering = True

        log('TR_xArena: Savaş Arenasına kayıt olunmaya çalışılıyor')
        inject_joymax(0x74D3, p, False)
        return 500
    return 0

def capturetheflag(args):
    NPCID = GetNPCUniqueID('So-Ok')
    if NPCID == 0:
        log('TR_xArena: "So-Ok" NPC\'si yakınlarda değil. Komutu NPC\'nin yakınında kullandığınızdan emin olun')
    else:
        p = bytearray()

        global isPluginRegistering
        isPluginRegistering = True

        log('TR_xArena: Bayrak Kapmaca\'ya kayıt olunmaya çalışılıyor')
        inject_joymax(0x74B2, p, False)
        return 500
    return 0

def handle_joymax(opcode, data):
    global isPluginRegistering
    if opcode == 0x34D2:
        global InBattleArena
        if data[0] == 0xFF:
            result = data[1]
            if result == 0:
                log('TR_xArena: Arenaya başarıyla kayıt olundu')
                if isPluginRegistering:
                    stop_bot()
            elif result == 2:
                log('TR_xArena: Zaten kayıt oldunuz!')
            else:
                if result == 4:
                    log('TR_xArena: Şu anda kayıt olamazsınız')
                elif result == 6:
                    log('TR_xArena: Yeterli oyuncu yok, maç iptal edildi!')
                elif result == 0x0B:
                    log("TR_xArena: Kayıt olamazsınız, partide değilsiniz")
                elif result == 0x0D:
                    log("TR_xArena: Kayıt olmak için uygun kıyafeti giymiyorsunuz!")
                isPluginRegistering = False
        elif data[0] == 8:
            InBattleArena = True
            if isPluginRegistering:
                log("TR_xArena: Anti-AFK etkinleştiriliyor...")
                AntiAFK()
        elif data[0] == 9:
            result = data[2]
            coins = data[3]
            log('TR_xArena: ' + ('kaybettiniz' if result == 2 else 'kazandınız') + ', ' + str(coins) + ' coin kazandınız!')
            if InBattleArena:
                InBattleArena = False
                if isPluginRegistering:
                    isPluginRegistering = False
                    log("TR_xArena: Anti-AFK devre dışı bırakılıyor. Bot başlatılıyor...")
                    start_bot()
    elif opcode == 0x34B1:
        global InCTF
        if data[0] == 0xFF:
            result = data[1]
            if result == 0:
                log('TR_xArena: CTF\'ye başarıyla kayıt olundu')
                if isPluginRegistering:
                    stop_bot()
            else:
                if result == 0x11:
                    log('TR_xArena: Maçı kazandınız!')
                elif result == 0x16:
                    log('TR_xArena: Maçı kaybettiniz!')
                elif result == 0x17:
                    log('TR_xArena: Maç berabere bitti!')
                elif result == 0x06:
                    log('TR_xArena: Yeterli oyuncu yok, maç iptal edildi!')
                elif result == 0x15:
                    log('TR_xArena: Kasabanın dışındasınız!')
                isPluginRegistering = False
        elif data[0] == 8:
            InCTF = True
            if isPluginRegistering:
                log("TR_xArena: Anti-AFK etkinleştiriliyor...")
                AntiAFK()
        elif data[0] == 9:
            result = data[2]
            if InCTF:
                InCTF = False
                log('TR_xArena: Bayrak Kapmaca etkinliği sona erdi')
                if isPluginRegistering:
                    isPluginRegistering = False
                    log("TR_xArena: Anti-AFK devre dışı bırakılıyor. Bot başlatılıyor...")
                    start_bot()
    return True

log('Eklenti: ' + pName + ' başarıyla yüklendi')