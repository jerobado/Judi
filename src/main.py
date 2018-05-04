""" Judi the profiler, is a desktop application that can find a GIPM record with 100% full confidence.

    Interface: GUI (PyQt5)
    Implementation: Python 3.6.4
    Created: 19 Dec 2017 7:45 PM
    Author: Jero Bado
 """

import logging
import os
import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main.main_window import JudiWindow
from src.resources.constant import (__appname__,
                                    __orgname__,
                                    LOGGER)

APP = QApplication(sys.argv)
APP.setOrganizationName(__orgname__)
APP.setApplicationName(__appname__)

LOGGER = logging.getLogger(__name__)


def check_environment():
    """ Check what current environment is Judi running. """

    frozen = 'not'
    if getattr(sys, 'frozen', False):
        # Judi is now running live and frozen! #chills
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
    else:
        # Judi is currently running in Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    LOGGER.info(f'I am {frozen} frozen')
    LOGGER.info(f'bundle dir is {bundle_dir}')
    LOGGER.info(f'sys.argv[0] is {sys.argv[0]}')
    LOGGER.info(f'sys.executable is {sys.executable}')
    LOGGER.info(f'os.getcwd is {os.getcwd()}')


if __name__ == '__main__':
    check_environment()
    window = JudiWindow()
    window.clipboard = APP.clipboard()
    window.show()
    APP.exec()
