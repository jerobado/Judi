# Customize QComboBox to be crafted here

from PyQt5.QtCore import (QEvent,
                          Qt)
from PyQt5.QtWidgets import QComboBox


class JudiComboBox(QComboBox):

    def __init__(self):

        QComboBox.__init__(self)
        self.view().installEventFilter(self)

    def eventFilter(self, obj, event):

        if event.type() == QEvent.ShortcutOverride:
            if event.key() == Qt.Key_Tab:
                self.hidePopup()
                self.setCurrentIndex(self.view().currentIndex().row())
                return True
        return QComboBox.eventFilter(self, obj, event)
