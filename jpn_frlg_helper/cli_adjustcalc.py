from jpn_frlg_helper.constants import AdjustmentType
from jpn_frlg_helper.resources.getter import easy_chat_system
from jpn_frlg_helper.wordcalc import calc_ev_adjustment, calc_exp_adjustment


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
    results: list[tuple[int, int | tuple[int, int]]] = []
    if word_index is None:
        for word in easy_chat_system:
            if adjustment_type is AdjustmentType.EV:
                results.append((
                    word["Index"],
                    calc_ev_adjustment(word["Index"], glitch_pokemon, base_pokemon, encryption_key)
                    ))
            if adjustment_type is AdjustmentType.EXP:
                results.append((
                    word["Index"],
                    calc_exp_adjustment(word["Index"], glitch_pokemon, base_pokemon, encryption_key, exp)
                    ))
    else:
        if adjustment_type is AdjustmentType.EV:
            results.append((
                word_index,
                calc_ev_adjustment(word_index, glitch_pokemon, base_pokemon, encryption_key),
            ))
        if adjustment_type is AdjustmentType.EXP:
            results.append((
                word_index,
                calc_exp_adjustment(word_index, glitch_pokemon, base_pokemon, encryption_key, exp)
            ))
    if adjustment_type is AdjustmentType.EV:
        print("The EV pairs to adjust can be either HP / Atk or Sp.Attack / Sp.Defense")
    for result in results:
        word_entry = next((word for word in easy_chat_system if word['Index'] == result[0]))
        word_temp = "{0:04X} : {1} : {2}".format(word_entry["Index"], word_entry["Group"], word_entry["Word"])
        print(f"""{word_temp} - {str(result[1])}""")
