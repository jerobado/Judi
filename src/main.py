""" Judi the profiler, is a desktop application that can find a GIPM record with 100% full confidence.

    Interface: GUI (PyQt5)
    Language: Python 3.6.3
    Created: 19 Dec 2017 7:45 PM
    Author: Jero Bado
 """

import os
import sys
from PyQt5.QtWidgets import QApplication
from src.resources.constant import (__appname__,
                                    __orgname__)

APP = QApplication(sys.argv)
APP.setOrganizationName(__orgname__)
APP.setApplicationName(__appname__)


def check_environment():
    frozen = 'not'
    if getattr(sys, 'frozen', False):
        # we are running in a bundle
        frozen = 'ever so'
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))
    print('we are', frozen, 'frozen')
    print('bundle dir is', bundle_dir)
    print('sys.argv[0] is', sys.argv[0])
    print('sys.executable is', sys.executable)
    print('os.getcwd is', os.getcwd())


if __name__ == '__main__':
    from src.gui.main.main_window import JudiWindow
    check_environment()
    window = JudiWindow()
    window.clipboard = APP.clipboard()
    window.show()
    APP.exec()
