""" Judi, the profiler

    Interface: GUI (PyQt5)
    Language: Python 3.6.3
    Created: 19 Dec 2017 7:45 PM
    Author: mokachokokarbon
 """

import sys
from PyQt5.QtWidgets import QApplication

APP = QApplication(sys.argv)


def load_stylesheet():

    stylesheet = open('../qss/style.qss', 'r')
    return stylesheet.read()


if __name__ == '__main__':
    from src.gui.main_window import GeeWindow
    #print(type(load_stylesheet()))
    window = GeeWindow()
    window.setStyleSheet(load_stylesheet())
    window.show()
    APP.exec()