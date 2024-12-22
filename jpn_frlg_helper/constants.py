from enum import Enum
from typing import TypedDict


class EncounterType(Enum):
    STATIC = "static"
    WILD = "wild"


class GameVersion(Enum):
    FIRERED = "firered"
    LEAFGREEN = "leafgreen"


class AdjustmentType(Enum):
    EV = "ev"
    EXP = "experience"


ECSEntry = TypedDict("ECSEntry", {
    "Index": int,
    "Group": str,
    "Word": str,
})


ECSWord = TypedDict("ECSWord", {
    "Group": str,
    "Word": str,
})


GlitchPokemonEntry = TypedDict("GlitchPokemonEntry", {
    "Index": int,
    "Raw Address": int,
    "Actual Address": int,
    "Mode": str,
    "Box Entrypoint": str,
})


AdvanceEntry = TypedDict("AdvanceEntry", {
    "Advance": int,
    "PID": int,
})


PID_SUBSTRUCTURES = (
    'GAEM',
    'GAME',
    'GEAM',
    'GEMA',
    'GMAE',
    'GMEA',
    'AGEM',
    'AGME',
    'AEGM',
    'AEMG',
    'AMGE',
    'AMEG',
    'EGAM',
    'EGMA',
    'EAGM',
    'EAMG',
    'EMGA',
    'EMAG',
    'MGAE',
    'MGEA',
    'MAGE',
    'MAEG',
    'MEGA',
    'MEAG',
)