from jpn_frlg_helper.constants import (
    GameVersion,
    PID_SUBSTRUCTURES,
    GlitchPokemonEntry,
    ECSEntry,
    )
from jpn_frlg_helper.wordcalc import calc_mon_word, get_adjustment_type


def get_params():
    while True:
        user_input = input("FireRed(0) or LeafGreen(1)? ")
        match user_input:
            case "0":
                game_version = GameVersion.FIRERED
                break
            case "1":
                game_version = GameVersion.LEAFGREEN
                break
            case _:
                continue
    while True:
        try:
            user_input = input("TID: ")
            tid = int(user_input)
            if not (0 <= tid <= 65535):
                print("Not a valid TID")
                continue
            break
        except ValueError as err:
            print(err)
    while True:
        try:
            user_input = input("PID: ")
            pid = int(user_input, 16)
            if not (0x0 <= pid <= 0xFFFFFFFF):
                print("Invalid PID")
                continue
            break
        except ValueError as err:
            print(err)
    return game_version, tid, pid


def main():
    game_version, tid, pid = get_params()
    adjustment_type = get_adjustment_type(pid)
    results: list[tuple[GlitchPokemonEntry, ECSEntry]] = []
    if adjustment_type is not None:
        results.extend(calc_mon_word(pid, tid, game_version))
    out_result_list: list[str] = []
    for entry in results:
        out_result_list.append(
            f"""{entry[0]['Index']:04X} \
| {entry[0]['Box Entrypoint']} \
| {entry[1]['Index']:04X} \
| {entry[1]['Group']} \
| {entry[1]['Word']}"""
        )
    results_output = "\n".join(out_result_list) if len(results) > 0 else "None"
    output = f"""PID Substructure: {pid % 24} {PID_SUBSTRUCTURES[pid % 24]}
Adjustment Type: {adjustment_type.name if adjustment_type is not None else "None"}
Encryption Key: {(tid ^ pid) & 0xFFFF:04X}
Glitch Pokemon Index | Entrypoint | Word Index | Word Group | Word:
{results_output}\
"""
    print(output)