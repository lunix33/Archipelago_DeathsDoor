from typing import ClassVar
from worlds.AutoWorld import World

from .web_world import Web
from .items import ItemData
from .options import Options

class DeathsDoorWorld(World):
    """
    Death's Door
    Reaping souls of the dead and punching a clock might get monotonous but it's
    honest work for a Crow. The job gets lively when your assigned soul is
    stolen and you must track down a desperate thief to a realm untouched by
    death - where creatures grow far past their expiry.
    """ # From https://store.steampowered.com/app/894020

    game = "Death's Door"
    required_client_version = (0, 5, 1)
    settings_key = "deaths_door_options"
    options_dataclass = options
    web = Web()

    item_name_to_id = ItemData.name_to_id_dict()
    location_name_to_id = {}
