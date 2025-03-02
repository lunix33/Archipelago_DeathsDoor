from BaseClasses import Item, MultiWorld, Region
from worlds.AutoWorld import World

from .web_world import Web
from .items import ItemData
from .location import LocationData
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
    options_dataclass = Options
    options: Options

    web = Web()

    item_name_to_id = ItemData.name_to_id_dict()
    location_name_to_id = LocationData.name_to_id_dict()

    def __init__(self, multiworld: MultiWorld, player: int):
        ItemData.load()
        LocationData.load()
        super().__init__(multiworld, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        pass

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)

        for loc_data in LocationData.get_data():
            loc = loc_data.to_game_location(self.player, menu_region)
            menu_region.locations.append(loc)

        self.multiworld.regions.append(menu_region)
    
    def create_item(self, name: str) -> Item:
        item = ItemData.from_name(name)
        if item is None:
            raise Exception(f"Invalid item: {item}")
        return item.to_game_item(self.player)

    def create_items(self) -> None:
        for item in ItemData.get_data():
            for _ in range(item.count):
                self.multiworld.itempool.append(self.create_item(item.name))
    
    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda _: True 
    
    def fill_slot_data(self) -> dict[str, object]:
        return {}
    
    def get_filler_item_name(self) -> str:
        return "Life Seed"
