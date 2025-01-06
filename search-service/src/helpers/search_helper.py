import os
import random
import time

from src.helpers.db_helper import DBHelper
from src.logfactory import LogFactory
from usearch.index import Index

logger = None

class SearchHelper:
    def __init__(self, config, db_client: DBHelper, logFactory: LogFactory, is_mini: bool = False):
        self.is_mini = is_mini
        self.config = config
        self.db_client = db_client
        self.search_tree = None
        self.EMB_SIZE = self.config['search']["index"]['emb_size']
        self.TOTAL_KEYS = 0

        global logger
        self.logfactory = logFactory
        logger = self.logfactory.get_logger(__name__)

        dimensions = int(self.EMB_SIZE)
        self.search_tree = Index(
            ndim=dimensions, 
            metric=self.config['search']['index']['metric'],
            connectivity=self.config['search']['index']['connectivity'],
            expansion_add=self.config['search']['index']['expansion_add'],
            expansion_search=self.config['search']['index']['expansion_search']
        )

        search_tree_path = self.config['search_index_path'] if is_mini == False else self.config['search_index_path_mini']
        if is_mini: self.search_tree.load('src' + os.sep + search_tree_path)
        else: self.search_tree.view('src' + os.sep + search_tree_path) # View from disk without loading in memory
        logger.info("search index loaded")

        self.TOTAL_KEYS = len(self.search_tree)
        logger.info(f"total_keys::{self.TOTAL_KEYS}")

        logger.info(f"SearchHelper class initialized")


    def get_search_results_from_query(self, query_idx: int, **kwargs):
        request = kwargs.get("request", {})
        search_response = []
        result_idxs = self.do_search(query_idx)
        logger.debug(result_idxs)
        start_time = time.time()
        results = self.db_client.get_item_details(result_idxs) 
        search_response = [[results[idx].id, results[idx].name, results[idx].cover] for idx in result_idxs]
        end_time = time.time()
        logger.info(f"query response time:: {(end_time - start_time)}", extra=request)
        return search_response

    def get_random_playlist_index(self) -> int:
        return random.randint(0, self.TOTAL_KEYS)
        
    def do_search(self, query_idx: int):
        keyInIndex = self.search_tree.contains(query_idx)
        if not keyInIndex:
            logger.info(f"key {query_idx} not in index.")
            return []
        
        query_vector = self.search_tree.get(query_idx)
        nearest_idxs = self.search_tree.search(query_vector, 
                                                        (self.config['search']['num_results']))
        return [ int(item.key) for item in nearest_idxs]
    
    def check_health(self):
        index_size = self.search_tree.size
        if index_size is None or index_size == 0:
            raise Exception(f"Search index health check failed. Index size: {index_size}")
        return True


