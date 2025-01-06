import os
import sqlite3
from sqlite3 import Error, Row
from typing import Dict, List, Tuple

from src.dto.item_info import ItemInfo
from src.logfactory import LogFactory

logger = None

class DBHelper:
    def __init__(self, config: dict, logFactory: LogFactory, is_mini: bool = False):
        self.is_mini = is_mini
        self.config = config
        self.connection = self.__init_connection(is_mini)

        global logger
        self.logfactory = logFactory
        logger = self.logfactory.get_logger(__name__)
        logger.info(f"DBHelper class initialized")

    def __init_connection(self, is_mini: bool = False):
        try:
            db_path = self.config['db_path'] if is_mini == False else self.config['db_path_mini']
            conn = sqlite3.connect('src' + os.sep + db_path, check_same_thread=False)
            conn.row_factory = Row 
            return conn
        except Error as ex:
            logger.error('Some exception occurred while initiaiting SQL connection', ex)
            return None

    def __get_connection(self):
        if self.connection is not None: return self.connection
        return self.__init_connection(self.is_mini)
    
    def check_health(self):
        connection = self.__get_connection()
        cursor = connection.cursor()
        
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        return result and result[0] == 1

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