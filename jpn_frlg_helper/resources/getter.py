import csv
from typing import TypedDict
from jpn_frlg_helper.constants import ECSEntry, GlitchPokemonEntry


PokemonEntry = TypedDict("PokemonEntry", {
    "Index": int,
    "Name": str
})


def get_ecs_data() -> tuple[ECSEntry, ...]:
    with open("jpn_frlg_helper/resources/easy_chat.csv", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return tuple([
            {
                "Index": int(entry["Index"], 16),
                "Group": entry["Group"],
                "Word": entry["Word"],
            } for entry in reader
        ])


def get_glitchmon_data(version: str) -> tuple[GlitchPokemonEntry, ...]:
    with open(f"jpn_frlg_helper/resources/{version}.csv", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return tuple([
            {
                "Index": int(entry["Index"], 16),
                "Raw Address": int(entry["Raw Address"], 16),
                "Actual Address": int(entry["Actual Address"], 16),
                "Mode": entry["Mode"],
                "Box Entrypoint": entry["Box Entrypoint"]
            } for entry in reader
        ])


def get_pokemon_index() -> tuple[PokemonEntry, ...]:
    with open("jpn_frlg_helper/resources/pokemon_index.csv", "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return tuple([
            {
                "Index": int(row["Index"]),
                "Name": row["Name"]
            } for row in reader
        ])


easy_chat_system = get_ecs_data()
firered_data = get_glitchmon_data("firered")
leafgreen_data = get_glitchmon_data("leafgreen")
pokemon_data = get_pokemon_index()