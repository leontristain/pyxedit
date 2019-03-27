from xelib.xedit.attribute import XEditAttribute
from xelib.xedit.generic import XEditGenericObject


class XEditNPC(XEditGenericObject):
    SIGNATURE = 'NPC_'

    vmad = script_info = XEditAttribute('VMAD', read_only=True)
    obnd = object_bounds = XEditAttribute('OBND', read_only=True)

    acbs = base_stats = XEditAttribute('ACBS', read_only=True)
    snam = factions = XEditAttribute('SNAM', read_only=True)
    inam = death_item = XEditAttribute('INAM')
    vtck = voice_type = XEditAttribute('VTCK')
    tplt = template = XEditAttribute('TPLT')
    rnam = race = XEditAttribute('RNAM')

    spct = spell_count = XEditAttribute('SPCT')
    splo = spell = actor_effects = XEditAttribute('SPLO')

    dest = destructible = destruction_data = XEditAttribute('DEST')
    wnam = worn_armor = XEditAttribute('WNAM')
    anam = faraway_model = XEditAttribute('ANAM')

    atkr = attack_race = XEditAttribute('ATKR')
    atkd = attacks = attack_data = XEditAttribute('ATKD', read_only=True)

    spor = ai_spectator_override = XEditAttribute('SPOR')
    ocor = ai_observe_corpse = XEditAttribute('OCOR')
    gwor = ai_guard_warn_override = XEditAttribute('GWOR')
    ecor = ai_combat_override = XEditAttribute('ECOR')

    prkz = perk_count = XEditAttribute('PRKZ')
    prkr = perk_record = XEditAttribute('PRKR', read_only=True)

    coct = container_count = items_count = XEditAttribute('COCT')
    cnto = container = items = XEditAttribute('CNTO', read_only=True)

    aidt = ai_data = XEditAttribute('AIDT', read_only=True)
    pkid = ai_package = XEditAttribute('PKID', read_only=True)

    ksiz = keyword_count = XEditAttribute('KSIZ')
    kwda = keywords = XEditAttribute('KWDA')

    cnam = class_ = XEditAttribute('CNAM')
    full = full_name = XEditAttribute('FULL')
    shrt = short_name = XEditAttribute('SHRT')
    data = marker = XEditAttribute('DATA')
    dnam = skills_and_stats = XEditAttribute('DNAM', read_only=True)

    pnam = head_parts = XEditAttribute('PNAM', read_only=True)
    hclf = hair_color = XEditAttribute('HCLF')

    znam = combat_style = XEditAttribute('ZNAM')
    gnam = gift_filter = XEditAttribute('GNAM')
    # nam5 = XEditAttribute('NAM5')  # this one is unknown, let's not touch it

    nam6 = height = XEditAttribute('NAM6')
    nam7 = weight = XEditAttribute('NAM7')

    nam8 = sound_level = XEditAttribute('NAM8')
    csdt = sound_types = XEditAttribute('CSDT')
    cscr = inherits_sounds_from = audio_template = XEditAttribute('CSCR')

    doft = default_outfit = XEditAttribute('DOFT')
    soft = sleep_outfit = XEditAttribute('SOFT')

    dplt = default_package_list = XEditAttribute('DPLT')
    crif = crime_faction = XEditAttribute('CRIF')

    ftst = head_texture = face_texture_set = XEditAttribute('FTST')
    qnam = skin_tone = texture_lighting = XEditAttribute('QNAM', read_only=True)
    nam9 = face_morphs = XEditAttribute('NAM9', read_only=True)
    nama = face_parts = XEditAttribute('NAMA', read_only=True)
    tini = tint_layers = XEditAttribute('TINI', read_only=True)
