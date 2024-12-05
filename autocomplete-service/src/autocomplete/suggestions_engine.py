from typing import Dict

from src.autocomplete.dawg_engine import DawgEngine
from src.dto.item_info import ItemInfo


class SuggestionsEngine:
    def __init__(self, source_lookup: Dict[int, ItemInfo], options: dict):
        self.source_lookup = source_lookup
        self.options = options
        self.engine_instance = self.__init_engine(self.source_lookup)
        # clear source
        self.source_lookup.clear()

    def __init_engine(self,source_lookup: Dict[int, ItemInfo]) -> DawgEngine:
        return DawgEngine(source_lookup)

    def autocomplete(self, prefix: str, count: int):
        return self.engine_instance.autocomplete(prefix, count, 
                                                 self.options['max_fuzzy_dist'])
