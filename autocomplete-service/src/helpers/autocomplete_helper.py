from typing import List

from src.autocomplete.suggestions_engine import SuggestionsEngine
from src.helpers.db_helper import DBHelper
from src.logfactory import LogFactory

logger = None

class AutocompleteHelper:
    def __init__(self, config, db_client: DBHelper, logFactory: LogFactory):
        self.config = config
        self.db_client = db_client
        self.autocomplete_tree = None

        global logger
        self.logfactory = logFactory
        logger = self.logfactory.get_logger(__name__)

        self.autocomplete_tree = SuggestionsEngine(self.db_client.get_item_details(), 
                                                   self.config['autocomplete'])

        logger.info(f"AutocompleteHelper class initialized")

    def auto_complete(self, prefix: str, count: int = None) -> List[dict]:
        count = count if count is not None else self.config['autocomplete']['suggestions_count']
        return self.autocomplete_tree.autocomplete(prefix,  count)
    
    def check_health(self):
        result = self.autocomplete_tree.autocomplete('a',  1)
        if result is None or len(result) == 0:
            raise Exception("Autocomplete health check failed")
        return True