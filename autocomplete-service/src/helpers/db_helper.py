import os
import sqlite3
from sqlite3 import Error, Row
from typing import Dict, List, Tuple

from src.dto.item_info import ItemInfo
from src.logfactory import LogFactory

logger = None

class DBHelper:
    def __init__(self, config: dict, logFactory: LogFactory):
        self.config = config
        self.connection = self.__init_connection()

        global logger
        self.logfactory = logFactory
        logger = self.logfactory.get_logger(__name__)
        logger.info(f"DBHelper class initialized")

    def __init_connection(self):
        try:
            conn = sqlite3.connect('src' + os.sep + self.config['db_path'], check_same_thread=False)
            conn.row_factory = Row 
            return conn
        except Error as ex:
            logger.error('Some exception occurred while initiaiting SQL connection', ex)
            return None

    def __get_connection(self):
        if self.connection is not None: return self.connection
        return self.__init_connection()

    def get_item_details(self, idxs: List[int] = ()) -> Dict[int, ItemInfo]:
        conn = self.__get_connection()
        cur = conn.cursor()
        
        where_clause = ''
        if idxs is not None and len(idxs) > 0:
            columns = 'idx, id, name, cover'
            where_clause = f" WHERE idx IN ({','.join(['?']*len(idxs))})"
        else:
            columns = 'idx, name'

        base_query = f'SELECT {columns} FROM details {where_clause}'
        cur.execute(base_query, idxs)
        
        rows = cur.fetchall()
        results: Dict[int, ItemInfo] = {}
        for row in rows:
            item = ItemInfo(row['idx'], row['name'])
            if where_clause != '':
                item.set_id(row['id'])
                item.set_cover(row['cover'])
            results[row['idx']] = item
        return results