from dataclasses import dataclass

from Options import PerGameCommonOptions, DeathLink

class DDDeathLink(DeathLink):
    """
    When you or anyone else die, kills everybody.
    """

@dataclass
class Options(PerGameCommonOptions):
    death_link: DDDeathLink
