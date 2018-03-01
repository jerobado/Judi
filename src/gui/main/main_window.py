# Judi's main user interface

import pyodbc
from PyQt5.QtCore import (Qt,
                          QDate,
                          QSettings)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QDateEdit,
                             QHBoxLayout,
                             QLabel,
                             QLineEdit,
                             QPushButton,
                             QTextEdit,
                             QVBoxLayout,
                             QWidget)
from src.gui.widgets.combobox import JudiComboBox
from src.core import judi
from src.resources.constant import (__appname__,
                                    __version__,
                                    AB_EMAIL_TYPE,
                                    AB_TEMPLATE,
                                    BMO,
                                    BM_OFFICES_COMPLETER,
                                    CC,
                                    DATE_FORMAT,
                                    NON_AB_TEMPLATE,
                                    SETTINGS_GEOMETRY,
                                    STYLE_QSS_FILE,
                                    USERNAME)
from src.resources import judi_resources


class JudiWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.profiling_date = QDate.currentDate()
        self.settings = QSettings()
        self._widgets()
        self._layout()
        self._properties()
        self._connections()
        self._gsmconnect()
        self._read_settings()

    def _widgets(self):

        self.grnLabel = QLabel()
        self.grnLineEdit = QLineEdit()
        self.sentDateEdit = QDateEdit()
        self.trademarkLineEdit = QLineEdit()
        self.countrycodeLineEdit = QLineEdit()
        self.emailtypeComboBox = JudiComboBox()
        self.descriptionLineEdit = QLineEdit()
        self.senderLineEdit = QLineEdit()
        self.switchPushButton = QPushButton()
        self.recipientLineEdit = QLineEdit()
        self.dncTextEdit = QTextEdit()

    def _properties(self):

        self.grnLabel.setText('&GRN:')
        self.grnLabel.setBuddy(self.grnLineEdit)

        self.grnLineEdit.setPlaceholderText('Trademarks')
        self.grnLineEdit.setObjectName('grnLineEdit')

        self.sentDateEdit.setObjectName('sentDateEdit')
        self.sentDateEdit.setDisplayFormat('dd-MMM-yy')
        self.sentDateEdit.setDate(self.profiling_date)
        self.sentDateEdit.setCalendarPopup(True)

        self.trademarkLineEdit.setPlaceholderText('Trademark')
        self.trademarkLineEdit.setObjectName('trademarkLineEdit')

        self.countrycodeLineEdit.setPlaceholderText('CC')
        self.countrycodeLineEdit.setObjectName('countrycodeLineEdit')

        self.emailtypeComboBox.addItems(AB_EMAIL_TYPE)
        self.emailtypeComboBox.setObjectName('emailtypeComboBox')

        self.descriptionLineEdit.setPlaceholderText('Brief Description')
        self.descriptionLineEdit.setObjectName('descriptionLineEdit')

        self.senderLineEdit.setPlaceholderText('Sender')
        self.senderLineEdit.setObjectName('senderLineEdit')
        self.senderLineEdit.setCompleter(BM_OFFICES_COMPLETER)

        self.switchPushButton.setObjectName('switchPushButton')
        self.switchPushButton.setShortcut('Alt+S')
        self.switchPushButton.setFlat(True)
        self.switchPushButton.setIcon(QIcon(':/switch1-16.png'))

        self.recipientLineEdit.setPlaceholderText('Recipient')
        self.recipientLineEdit.setObjectName('recipientLineEdit')
        self.recipientLineEdit.setCompleter(BM_OFFICES_COMPLETER)

        self.dncTextEdit.setObjectName('dncTextEdit')
        self.dncTextEdit.setPlaceholderText('Document Naming Convention')

        self.setWindowTitle(f'{__appname__} {__version__} - {USERNAME}')
        self.setObjectName('JudiWindow')
        self.resize(616, 110)   # width, height
        self.setStyleSheet(STYLE_QSS_FILE)
        self.setTabOrder(self.senderLineEdit, self.recipientLineEdit)

    def _layout(self):

        first_layer = QHBoxLayout()
        first_layer.addWidget(self.grnLabel)
        first_layer.addWidget(self.grnLineEdit)
        first_layer.addStretch()

        second_layer = QHBoxLayout()
        second_layer.addWidget(self.sentDateEdit)
        second_layer.addWidget(self.trademarkLineEdit)
        second_layer.addWidget(self.countrycodeLineEdit)
        second_layer.addWidget(self.emailtypeComboBox)
        second_layer.addWidget(self.descriptionLineEdit)
        second_layer.addWidget(self.senderLineEdit)
        second_layer.addWidget(self.switchPushButton)
        second_layer.addWidget(self.recipientLineEdit)

        third_layer = QHBoxLayout()
        third_layer.addWidget(self.dncTextEdit)

        first_col = QVBoxLayout()
        first_col.addLayout(first_layer)
        first_col.addLayout(second_layer)
        first_col.addLayout(third_layer)

        self.setLayout(first_col)

    def _connections(self):

        self.grnLineEdit.textChanged.connect(self.on_grnLineEdit_textChanged)
        self.sentDateEdit.dateChanged.connect(self.on_criteriaChanged)
        self.trademarkLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.countrycodeLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.emailtypeComboBox.currentIndexChanged.connect(self.on_criteriaChanged)
        self.descriptionLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.senderLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.switchPushButton.clicked.connect(self.on_switchPushButton_clicked)
        self.recipientLineEdit.textChanged.connect(self.on_criteriaChanged)

    def _gsmconnect(self):
        """ Connect to server and database.

            return -> bool
        """

        judi.connect()  # using the core

    def _read_settings(self):

        self.restoreGeometry(self.settings.value(SETTINGS_GEOMETRY, self.saveGeometry()))

    def on_grnLineEdit_textChanged(self):

        try:
            # Get the package to deliver
            grn = self.grnLineEdit.text().strip()
            record = judi.search(grn)   # perform the search
            print(f'[JUDI]: result -> {record}')
            if record:
                # Deliver the package
                self.trademarkLineEdit.setText(record.trademark)
                self.countrycodeLineEdit.setText(CC.get(record.countryid))
                self.senderLineEdit.setText(self.determine_agent(agent=record.agent,
                                                                 agent_id=record.agentid))
            else:   # has no content
                self.clear_criteria_fields()
                self.dncTextEdit.clear()

        # [] TODO: group related exceptions
        except TypeError as e:  # No record found
            self.clear_criteria_fields()
            self.dncTextEdit.setText('No record found. Try again.')
            print(f'on_grnLineEdit_textChanged: {e} - {type(e)}')

        except pyodbc.OperationalError as e:   # Disconnect error?
            self.dncTextEdit.setText('Session has timed-out. Try re-opening the app.')
            print(f'on_grnLineEdit_textChanged: {e} - {type(e)}')
            # [] TODO: create an auto recon when this error happens

        except AttributeError as e:
            self.dncTextEdit.setText('AttributeError. Try re-opening the app.')
            print(f'on_grnLineEdit_textChanged: {e} - {type(e)}')

        except Exception as e:
            self.dncTextEdit.setText('Judi is not feeling well. Try re-opening the app.')
            print(f'on_grnLineEdit_textChanged: {e} - {type(e)}')

    def clear_criteria_fields(self):
        """ Method that will clear the content of the input fields. """

        self.trademarkLineEdit.clear()
        self.countrycodeLineEdit.clear()
        self.descriptionLineEdit.clear()
        self.senderLineEdit.clear()
        self.recipientLineEdit.clear()

    def determine_agent(self, agent, agent_id):
        """ Determine if the current agent is 3rd party or part of the Firm. """

        baker = BMO.get(agent_id)
        return f'BM {baker}' if baker else agent

    def on_criteriaChanged(self):

        self.profiling_date = self.sentDateEdit.date()
        dnc = self.generate_dnc(self.emailtypeComboBox.currentIndex())
        self.dncTextEdit.setText(dnc)
        self.clipboard.setText(dnc)

    def generate_dnc(self, index):

        if not index:
            return NON_AB_TEMPLATE.substitute(sent=self.profiling_date.toString(DATE_FORMAT),
                                              trademark=self.trademarkLineEdit.text(),
                                              countrycode=self.countrycodeLineEdit.text(),
                                              description=self.descriptionLineEdit.text(),
                                              sender=self.senderLineEdit.text(),
                                              recipient=self.recipientLineEdit.text())

        return AB_TEMPLATE.substitute(sent=self.profiling_date.toString(DATE_FORMAT),
                                      trademark=self.trademarkLineEdit.text(),
                                      countrycode=self.countrycodeLineEdit.text(),
                                      emailtype=self.emailtypeComboBox.currentText(),
                                      description=self.descriptionLineEdit.text(),
                                      sender=self.senderLineEdit.text(),
                                      recipient=self.recipientLineEdit.text())

    def on_switchPushButton_clicked(self):
        """ Event handler that will 'switch' the entries of the Sender and Recipient fields. """

        # Get the current values of the fields
        sender = self.senderLineEdit.text()
        recipient = self.recipientLineEdit.text()

        # Perform the simple switching of values
        self.senderLineEdit.setText(recipient)
        self.recipientLineEdit.setText(sender)

    def resizeEvent(self, event):

        #print(f'w x h: {self.height()} x {self.width()}')
        pass

    def keyPressEvent(self, event):

        # When the user pressed the keys 'Ctr+Q'
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()

    def closeEvent(self, event):

        self._write_settings()

    def _write_settings(self):

        self.settings.setValue(SETTINGS_GEOMETRY, self.saveGeometry())
