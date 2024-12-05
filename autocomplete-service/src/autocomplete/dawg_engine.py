import string
from typing import Dict

from src.dto.item_info import ItemInfo
from fast_autocomplete import AutoComplete
from unidecode import unidecode


class DawgEngine():
    def __init__(self, source_lookup: Dict[int, ItemInfo]):
        self.source_lookup = source_lookup
        self.engine = self.__init_engine(self.source_lookup)

    def __init_engine(self, source_lookup: Dict[int, ItemInfo]) -> AutoComplete:
        valid_chars = ".'"
        valid_chars += string.ascii_lowercase
        valid_chars += string.digits
        valid_chars += string.punctuation
        valid_chars += string.whitespace

        dawg_lookup = {}
        for idx in source_lookup:
            word = unidecode(source_lookup[idx].name).lower()
            if word not in dawg_lookup:
                dawg_lookup[word] = {"idxs": [idx]}
            else:
                dawg_lookup[word]["idxs"].append(idx)
        autocomplete = AutoComplete(words=dawg_lookup, valid_chars_for_string=valid_chars)
        return autocomplete

    def autocomplete(self, prefix: str, count: int, max_cost: int):
        suggestions = self.engine.search(word=prefix, max_cost=max_cost, size=count)
        results = []
        for suggestion in suggestions:
            if len(suggestion) == 1:
                results.append({ "label": suggestion[0], 
                                "value": self.engine.words[suggestion[0]]["idxs"][0] })
            else:
                for i in range(1, len(suggestion)):
                    results.append({ "label": suggestion[i],
                                    "value": self.engine.words[suggestion[i]]["idxs"][0] })
        
        return results


