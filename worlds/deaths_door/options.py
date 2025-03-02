from dataclasses import dataclass

from Options import Choice, PerGameCommonOptions, DeathLink

class StartWeapon(Choice):
    """Player's starting weapon"""
    display_name = "Starting weapon"
    option_reapers_sword = 0
    option_rogue_daggers = 1
    option_discarded_umbrella = 2
    option_reapers_greatsword = 3
    option_thuder_hammer = 4
    default = 0

    def to_item_name(self) -> str:
        match self.value:
            case 0:
                return "Reaper's Sword"
            case 1:
                return "Rogue Daggers"
            case 2:
                return "Discarded Umbrella"
            case 3:
                return "Reaper's Greatsword"
            case 4:
                return "Thunder Hammer"
            case _:
                raise Exception("Invalid option")

@dataclass
class Options(PerGameCommonOptions):
    death_link: DeathLink
    start_weapon: StartWeapon
