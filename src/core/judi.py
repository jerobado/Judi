"""
    Core operations of Judi

    Usage:
        > import judi
        > judi.connect()
        True
        > judi.search('5134412')
        ('5134412', 'Trademark', 'AWESOME TRADEMARK', 'China', 'CHN', 'Super Awesome Agent', '1111')
"""

import sqlite3
import pyodbc
from collections import namedtuple
from src.resources.constant import (CONNECTION_STR_SQLITE,
                                    DB_DATABASE,
                                    DB_DRIVER,
                                    DB_SERVER,
                                    DB_TRUSTED_CONN,
                                    GIPM_RECORD,
                                    SEARCH_GRN_SQL,
                                    USERNAME)

CURSOR = None


def connect():
    """ Establish server/database connection.

    return -> bool
    """

    global CURSOR

    try:
        # Connecting to GSM
        # print(f'[JUDI]: Connecting to GSM...')
        # conn = pyodbc.connect(driver=DB_DRIVER,
        #                       host=DB_SERVER,
        #                       database=DB_DATABASE,
        #                       user=USERNAME,
        #                       trusted_connection=DB_TRUSTED_CONN)
        # CURSOR = conn.cursor()
        # print(f'[JUDI]: Good! You are now connected to GSM.')
        # return True

        # Connecting to SQLite
        print(f'[JUDI]: Connecting to SQLite')
        conn = sqlite3.connect(CONNECTION_STR_SQLITE)
        print(f'[JUDI]: Good! You are now connected to SQLite')
        CURSOR = conn.cursor()
        return True

    except Exception as e:
        print(f'[JUDI]: {e}')


def search(grn):
    """ Search record in GIPM using the given GRN.

    return -> namedtuple
    """

    grn = (grn,)
    CURSOR.execute(SEARCH_GRN_SQL, grn)
    return GIPM_RECORD._make(CURSOR.fetchone())
