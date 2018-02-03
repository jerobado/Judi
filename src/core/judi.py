"""
Soul and core operations of Judi

Usage:
    > import judi
    > judi.connect()
    True
    > judi.search('5134412')
    ('5134412', 'Trademark', 'AWESOME TRADEMARK', 'China', 'CHN', 'Super Awesome Agent', 1111)

"""

import pyodbc
from src.resources.constant import (DB_DATABASE,
                                    DB_DRIVER,
                                    DB_SERVER,
                                    DB_TRUSTED_CONN,
                                    SEARCH_GRN_SQL,
                                    USERNAME)

CURSOR = None


def connect():
    """ Establish server/database connection.

    return -> cursor()
    """

    conn = pyodbc.connect(driver=DB_DRIVER,
                          host=DB_SERVER,
                          database=DB_DATABASE,
                          user=USERNAME,
                          trusted_connection=DB_TRUSTED_CONN)

    return conn.cursor()


def search(grn):
    """ Search record in GIPM using the given GRN.

    return -> dict
    """

    grn = (grn,)
    CURSOR.execute(SEARCH_GRN_SQL, grn)
    return CURSOR.fetchone()
