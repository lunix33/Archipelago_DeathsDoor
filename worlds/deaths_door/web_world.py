from BaseClasses import Tutorial
from worlds.AutoWorld import WebWorld

class Web(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "Guide to setup Death's Door multiworld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Lunix33"]
        )
    ]

