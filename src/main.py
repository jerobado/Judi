""" Judi the profiler, is a desktop application that can find a GIPM record with 100% full confidence.

    Interface: GUI (PyQt5)
    Language: Python 3.6.3
    Created: 19 Dec 2017 7:45 PM
    Author: mokachokokarbon
 """

import sys

from PyQt5.QtWidgets import QApplication

from src.resources.constant import (__appname__,
                                    __orgname__)

APP = QApplication(sys.argv)
APP.setOrganizationName(__orgname__)
APP.setApplicationName(__appname__)

if __name__ == '__main__':
    from src.gui.main.main_window import JudiWindow
    window = JudiWindow()
    window.clipboard = APP.clipboard()
    window.show()
    APP.exec()
