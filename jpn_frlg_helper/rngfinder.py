from typing import Any, Generator
from jpn_frlg_helper.constants import (
    GameVersion,
    EncounterType,
    AdvanceEntry
    )
from jpn_frlg_helper.wordcalc import calc_mon_word, get_adjustment_type


class PokeRNG:
    def __init__(self, seed: int):
        self.state = seed
    
    def _next(this, advances: int = 1):
        for _ in range(advances):
            this.state = (0x41C64E6D * this.state + 0x00006073) & 0xFFFFFFFF
        return this.state

    def _next16(this, advances: int = 1):
        return (this._next(advances) >> 16) & 0xFFFF


def pidrng_static(
        seed: int,
        initial_advances: int,
        max_advances: int,
        delay: int,
):
    main_rng = PokeRNG(seed)
    advance_rng = PokeRNG(0) # 0 is a placeholder value
    main_rng._next(initial_advances + delay)
    for _ in range(max_advances + 1):
        advance_rng.state = main_rng.state
        pid = advance_rng._next16()
        pid |= advance_rng._next16() << 16
        yield pid
        main_rng._next()


def pidrng_wild(
        seed: int,
        initial_advances: int,
        max_advances: int,
        delay: int,
):
    main_rng = PokeRNG(seed)
    advance_rng = PokeRNG(0) # 0 is a placeholder value
    main_rng._next(initial_advances + delay)
    for _ in range(max_advances + 1):
        advance_rng.state = main_rng.state
        advance_rng._next(2)
        pid_nature = advance_rng._next16() % 25
        while True:
            pid = advance_rng._next16()
            pid |= advance_rng._next16() << 16
            if (pid % 25) == pid_nature:
                break
        yield pid
        main_rng._next()


def get_pidrng(
        encounter_type: EncounterType,
        seed: int,
        initial_advances: int,
        max_advances: int,
        delay: int,
):
    match encounter_type:
        case EncounterType.STATIC:
            return pidrng_static(seed, initial_advances, max_advances, delay)
        case EncounterType.WILD:
            return pidrng_wild(seed, initial_advances, max_advances, delay)


def search_pidrng(
        initial_advances: int,
        rng: Generator[int, Any, None],
        tid: int,
        game_version: GameVersion,
):
    usable_advances: list[AdvanceEntry] = []
    for advance, pid in enumerate(rng, start=initial_advances):
        if get_adjustment_type(pid) is None:
            continue
        results = calc_mon_word(pid, tid, game_version)
        if len(results) > 0:
            usable_advances.append({
                "Advance": advance,
                "PID": pid,
            })
    return tuple(usable_advances)


def get_params():
    while True:
        user_input = input("FireRed(0) or LeafGreen(1)? (0/1) ")
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
        user_input = input("Static(0) or Wild(1) encounter? (0/1) ")
        match user_input:
            case "0":
                encounter_type = EncounterType.STATIC
                break
            case "1":
                encounter_type = EncounterType.WILD
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
            user_input = input("Seed: ")
            seed = int(user_input, 16)
            if not (0x0 <= seed <= 0xFFFFFFFF):
                print("Invalid seed")
                continue
            break
        except ValueError as err:
            print(err)
    while True:
        try:
            user_input = input("Initial advances: ")
            initial_advances = int(user_input)
            if not (initial_advances >= 0):
                print("Initial advances can only be a positive number")
                continue
            break
        except ValueError as err:
            print(err)
    while True:
        try:
            user_input = input("Advances: ")
            advances = int(user_input)
            if not (advances >= 0):
                print("Advances can only be a positive number")
                continue
            break
        except ValueError as err:
            print(err)
    while True:
        try:
            user_input = input("Delay: ")
            delay = int(user_input)
            if not (delay >= 0):
                print("Delay can only be a positive number")
                continue
            break
        except ValueError as err:
            print(err)
    return game_version, encounter_type, tid, seed, initial_advances, advances, delay


def main():
    (
        game_version,
        encounter_type,
        tid,
        seed,
        initial_advances,
        advances,
        delay,
    ) = get_params()
    pidrng = get_pidrng(
        encounter_type,
        seed,
        initial_advances,
        advances,
        delay)
    results = search_pidrng(
        initial_advances,
        pidrng,
        tid,
        game_version
    )
    print(
        "\n".join([
            f"Advance: {entry['Advance']} | PID: {entry['PID']:08X}"
            for entry in results
            ])
        )
