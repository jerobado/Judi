"""
    Core operations of Judi

    Usage:
        > import judi
        > judi.connect()
        True
        > judi.search('5134412')
        ('5134412', 'Trademark', 'AWESOME TRADEMARK', 'China', 'CHN', 'Super Awesome Agent', '1111')
"""

import logging
import sqlite3
import pyodbc
from src.resources.constant import (CONNECTION_STR_SQLITE,
                                    DB_APP,
                                    DB_DATABASE,
                                    DB_DRIVER,
                                    DB_SERVER,
                                    DB_PASSWORD,
                                    DB_USERNAME,
                                    GIPM_RECORD,
                                    SEARCH_SQL_FILE,
                                    LOGGER)

CURSOR = None
LOGGER = logging.getLogger(__name__)


def live_connection():
    """ Connecting to GIPM. """

    global CURSOR
    LOGGER.info('Connecting to GIPM...')
    conn = pyodbc.connect(driver=DB_DRIVER,
                          server=DB_SERVER,
                          database=DB_DATABASE,
                          uid=DB_USERNAME,
                          pwd=DB_PASSWORD,
                          app=DB_APP)
    CURSOR = conn.cursor()
    LOGGER.info('You are now connected to GIPM')
    return True


def dev_connection():
    """ Connecting to SQLite. For development only.

    return -> bool
    """

    global CURSOR
    LOGGER.info('Connecting to SQLite...')
    conn = sqlite3.connect(CONNECTION_STR_SQLITE)
    LOGGER.info('Good! You are now connected to SQLite')
    CURSOR = conn.cursor()
    return True


def connect():
    """ Establish server/database connection.

    return -> bool
    """

    try:
        #return live_connection()
        return dev_connection()
    except pyodbc.OperationalError as e:
        LOGGER.error(f'Connection failed. Try again. {e} -> Type: {type(e)}')
        return False


def search(grn):
    """ Search record in GIPM using the given GRN.

    return -> namedtuple
    """

    grn = (grn,)
    CURSOR.execute(SEARCH_SQL_FILE, grn)
    # return GIPM_RECORD._make(CURSOR.fetchone())

    results = CURSOR.fetchall()

    if len(results) >= 2:
        record = GIPM_RECORD._make(results[0])
        return record._replace(trademark='MULTIPLE MARKS')
    elif len(results) == 1:
        return GIPM_RECORD._make(results[0])
    else:
        raise TypeError


def disconnect():
    """ Disconnect from SQLite. For development only. """

    CURSOR.close()
