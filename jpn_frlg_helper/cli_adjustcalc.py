import csv
from pathlib import Path
from jpn_frlg_helper.constants import AdjustmentType, ECSEntry
from jpn_frlg_helper.resources.getter import easy_chat_system
from jpn_frlg_helper.wordcalc import calc_ev_adjustment, calc_exp_adjustment, calc_adjustment


def get_params():
    while True:
        try:
            user_input = input("Base Pokemon Index: ")
            base_pokemon = int(user_input, 16)
            if not (0 <= base_pokemon <= 0xFFFF):
                print("Not a valid index")
                continue
            break
        except ValueError as err:
            print(err)
    while True:
        try:
            user_input = input("Glitch Pokemon Index: ")
            glitch_pokemon = int(user_input, 16)
            if not (0 <= glitch_pokemon <= 0xFFFF):
                print("Not a valid index")
                continue
            break
        except ValueError as err:
            print(err)
    while True:
        try:
            user_input = input("Encryption Key: ")
            encryption_key = int(user_input, 16)
            if not (0 <= encryption_key <= 0xFFFF):
                print("Not a valid encryption key")
                continue
            break
        except ValueError as err:
            print(err)
    while True:
        try:
            user_input = input("Word Index: ")
            word_index = int(user_input, 16) if user_input != "" else None
            if word_index is not None and not (0x0 <= word_index <= 0xFFFF):
                print("Invalid word index")
                continue
            break
        except ValueError as err:
            print(err)
    while True:
        user_input = input("EV Adjustment (0) or Exp Adjustment (1): ")
        match user_input:
            case "0":
                adjustment_type = AdjustmentType.EV
            case "1":
                adjustment_type = AdjustmentType.EXP
            case _:
                continue
        break
    if adjustment_type is AdjustmentType.EXP:
        while True:
            try:
                user_input = input("Pokemon's experience: ")
                exp = int(user_input) if user_input != "" else None
                if exp is not None and not (0x0 <= exp <= (2**32 - 1)):
                    print("Invalid experience")
                    continue
                break
            except ValueError as err:
                print(err)
    else:
        exp = None
    return (
        base_pokemon,
        glitch_pokemon,
        encryption_key,
        word_index,
        exp,
        adjustment_type
    )


def main():
    (
        base_pokemon,
        glitch_pokemon,
        encryption_key,
        word_index,
        exp,
        adjustment_type
    ) = get_params()
    results: list[tuple[int, int]] = []
    if word_index is None:
        for ecs_word_index in sorted(easy_chat_system.keys()):
            results.append((ecs_word_index, calc_adjustment(ecs_word_index, glitch_pokemon, base_pokemon, encryption_key)))
    else:
        results.append((word_index, calc_adjustment(word_index, glitch_pokemon, base_pokemon, encryption_key)))
    if len(results) > 1:
        user_input = input("Enter a file path: ")
        output_path = Path(user_input)
        with output_path.open("w", encoding="utf-8", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(["Index", "Group", "Word", "Experience", "EV 1", "EV 2"])
            for result in results:
                exp_adjust = (
                    calc_exp_adjustment(result[1], exp)
                    if adjustment_type is AdjustmentType.EXP else None
                )
                ev_adjust = (
                    calc_ev_adjustment(result[1])
                    if adjustment_type is AdjustmentType.EV else (None, None)
                )
                row = (
                    f"{result[0]:04X}",
                    easy_chat_system[result[0]]["Group"],
                    easy_chat_system[result[0]]["Word"],
                    exp_adjust,
                    ev_adjust[0],
                    ev_adjust[1]
                )
                csv_writer.writerow(row)
    else:
        result = results[0]
        exp_adjust = (
            calc_exp_adjustment(result[1], exp)
        )
        ev_adjust = (
            calc_ev_adjustment(result[1])
        )
        word = ECSEntry(
            Index=result[0],
            Group=easy_chat_system[result[0]]["Group"],
            Word=easy_chat_system[result[0]]["Word"]
        )
        if adjustment_type is AdjustmentType.EXP:
            adjust_string = str(exp_adjust)
        if adjustment_type is AdjustmentType.EV:
            adjust_string = f"{ev_adjust[0]}/{ev_adjust[1]}"
        print(f"{word["Index"]:04X} | {word["Group"]} | {word["Word"]} | {adjust_string}")
