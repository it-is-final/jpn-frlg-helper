from jpn_frlg_helper.constants import (
    AdjustmentType,
    GameVersion,
    ECSEntry,
    GlitchPokemonEntry,
    )
from jpn_frlg_helper.resources.getter import (
    easy_chat_system,
    firered_data,
    leafgreen_data,
    )


def get_adjustment_type(pid: int):
    pid_substructure = pid % 24
    if pid_substructure in (8, 22):
        return AdjustmentType.EV
    if pid_substructure in (6, 7, 12, 13, 18, 19):
        return AdjustmentType.EXP
    return None


def calc_mon_word(
        pid: int,
        tid: int,
        game_version: GameVersion
):
    available: list[tuple[GlitchPokemonEntry, ECSEntry]] = []
    encryption_key = (tid ^ pid) & 0xFFFF
    match game_version:
        case GameVersion.FIRERED:
            glitch_mon_list = firered_data
        case GameVersion.LEAFGREEN:
            glitch_mon_list = leafgreen_data
    for glitch_mon in glitch_mon_list:
        word_index = glitch_mon['Index'] ^ encryption_key
        if word_index in easy_chat_system:
            available.append((glitch_mon, ECSEntry(
                Index=word_index,
                Group=easy_chat_system[word_index]['Group'],
                Word=easy_chat_system[word_index]['Word']
            )))
    return available


def calc_adjustment(
        word_index: int,
        glitch_mon_index: int,
        base_mon_index: int,
        encryption_key: int
):
    mon_difference = glitch_mon_index - base_mon_index
    decrypted_value = word_index ^ encryption_key
    return (mon_difference + decrypted_value) & 0xFFFF


def calc_exp_adjustment(
        base_adjustment: int,
        exp: int | None
):
    experience = exp if exp is not None else 0 
    adjustment = base_adjustment
    while adjustment < experience:
        adjustment += 0x10000
    return adjustment


def calc_ev_adjustment(
        base_adjustment: int
):
    ev_1 = base_adjustment & 0xFF
    ev_2 = (base_adjustment >> 8) & 0xFF
    return ev_1, ev_2