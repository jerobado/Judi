# Judi's main user interface

import logging
import sqlite3
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
                                    AB_MASTER_GRN,
                                    AB_TEMPLATE,
                                    BMO,
                                    CC,
                                    COUNTRY_COMPLETER,
                                    DATE_FORMAT,
                                    DESCRIPTION_COMPLETER,
                                    LOGGER,
                                    MODULES_LABEL,
                                    NON_AB_TEMPLATE,
                                    OFFICE_COMPLETER,
                                    SETTINGS_GEOMETRY,
                                    STYLE_QSS_FILE,
                                    TRADEMARK_COMPLETER,
                                    USERNAME)
from src.resources import judi_resources

LOGGER = logging.getLogger(__name__)


class JudiWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.profiling_date = QDate.currentDate()
        self.settings = QSettings()
        self._widgets()
        self._layout()
        self._properties()
        self._connections()
        self._connect()
        self._read_settings()
        self.AUTOCOPY = False

    def _widgets(self):

        self.grnLabel = QLabel()
        self.grnLineEdit = QLineEdit()
        self.modulesLabel = QLabel()
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

        self.grnLineEdit.setPlaceholderText('GRN')
        self.grnLineEdit.setObjectName('grnLineEdit')

        self.modulesLabel.setText(MODULES_LABEL)
        self.modulesLabel.setObjectName('modulesLabel')

        self.sentDateEdit.setObjectName('sentDateEdit')
        self.sentDateEdit.setDisplayFormat('dd-MMM-yy')
        self.sentDateEdit.setDate(self.profiling_date)
        self.sentDateEdit.setCalendarPopup(True)

        self.trademarkLineEdit.setPlaceholderText('Trademark')
        self.trademarkLineEdit.setObjectName('trademarkLineEdit')
        self.trademarkLineEdit.setCompleter(TRADEMARK_COMPLETER)

        self.countrycodeLineEdit.setPlaceholderText('C. Code')
        self.countrycodeLineEdit.setObjectName('countrycodeLineEdit')
        self.countrycodeLineEdit.setCompleter(COUNTRY_COMPLETER)

        self.emailtypeComboBox.addItems(AB_EMAIL_TYPE)
        self.emailtypeComboBox.setObjectName('emailtypeComboBox')
        self.emailtypeComboBox.setVisible(False)

        self.descriptionLineEdit.setPlaceholderText('Brief Description')
        self.descriptionLineEdit.setObjectName('descriptionLineEdit')
        self.descriptionLineEdit.setCompleter(DESCRIPTION_COMPLETER)

        self.senderLineEdit.setPlaceholderText('Sender')
        self.senderLineEdit.setObjectName('senderLineEdit')
        self.senderLineEdit.setCompleter(OFFICE_COMPLETER)

        self.switchPushButton.setObjectName('switchPushButton')
        self.switchPushButton.setShortcut('Alt+S')
        self.switchPushButton.setToolTip('Switch Sender and Recipient (Alt+S)')
        self.switchPushButton.setFlat(True)
        self.switchPushButton.setIcon(QIcon(':/switch1-16.png'))

        self.recipientLineEdit.setPlaceholderText('Recipient')
        self.recipientLineEdit.setObjectName('recipientLineEdit')
        self.recipientLineEdit.setCompleter(OFFICE_COMPLETER)

        self.dncTextEdit.setObjectName('dncTextEdit')
        self.dncTextEdit.setPlaceholderText('Document Naming Convention')

        self.setWindowTitle(f'{__appname__} {__version__} - {USERNAME}')
        self.setObjectName('JudiWindow')
        self.resize(616, 110)   # width, height
        self.setStyleSheet(STYLE_QSS_FILE)
        self.setTabOrder(self.senderLineEdit, self.recipientLineEdit)

    def _layout(self):

        first_layer = QHBoxLayout()
        first_layer.addWidget(self.grnLineEdit)
        first_layer.addWidget(self.modulesLabel)
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
        """ Connections of Signals and Slots for widgets. """

        self.grnLineEdit.textChanged.connect(self.on_grnLineEdit_textChanged)
        self.sentDateEdit.dateChanged.connect(self.on_criteriaChanged)
        self.trademarkLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.countrycodeLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.emailtypeComboBox.currentIndexChanged.connect(self.on_criteriaChanged)
        self.descriptionLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.senderLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.switchPushButton.clicked.connect(self.on_switchPushButton_clicked)
        self.recipientLineEdit.textChanged.connect(self.on_criteriaChanged)

    def _connect(self):
        """ Connection to GIPM. """

        if judi.connect():
            # [] TODO: have a sample of valid random GIPM records
            self.dncTextEdit.setText('You are now connected to GIPM. Try searching this record: GRN 6120345.')
        else:
            self.dncTextEdit.setText('Disconnected from GIPM. Press \'<b>F6</b>\' or reopen the app to reconnect.')
            LOGGER.error('Initial connection failed')

    def _read_settings(self):

        self.restoreGeometry(self.settings.value(SETTINGS_GEOMETRY, self.saveGeometry()))

    def on_grnLineEdit_textChanged(self):

        # [] TODO: your try...except is looking ugly XD, try using the with context manager
        try:
            if self.grnLineEdit.text():
                grn = self.grnLineEdit.text().strip()
                record = judi.search(grn)
                self.verify_record(grn, record)
                LOGGER.info(f'record: {record}')
            else:
                self.dncTextEdit.clear()

        # [] TODO: group related exceptions
        except TypeError as e:
            self.dncTextEdit.setText('TypeError. Try again.')
            LOGGER.error(f'{e} - {type(e)}')

        except (pyodbc.OperationalError, sqlite3.ProgrammingError) as e:   # Disconnect error?
            self.dncTextEdit.setText('Disconnected from GIPM. Press \'<b>F6</b>\' or reopen the app to reconnect.')
            LOGGER.error(f'{e} - {type(e)}')

        except AttributeError as e:     # Invalid keys or user is searching while disconnected
            self.dncTextEdit.setText('Not connected to GIPM. Press \'<b>F6</b>\' or reopen the app to reconnect.')
            LOGGER.error(f'{e} - {type(e)}')

        except Exception as e:
            self.dncTextEdit.setText('You found a new error. Try reopening the app.')
            LOGGER.error(f'{e} - {type(e)}')

    def verify_record(self, grn, record):
        """ Verify record if valid or not. """

        if record:
            self.AUTOCOPY = True
            visible = True if record.clientid == AB_MASTER_GRN else False
            self.emailtypeComboBox.setVisible(visible)
            self.display_record(record)
        else:
            self.AUTOCOPY = False
            self.modulesLabel.setText(MODULES_LABEL)
            self.clear_criteria_fields(clear_all=False)
            self.dncTextEdit.setText(f'No record found for GRN \'{grn}\'. Try again.')

    def display_record(self, record):
        """ Display found record to widgets. """

        self.modulesLabel.setText(record.module)
        self.trademarkLineEdit.setText(record.trademark)
        self.countrycodeLineEdit.setText(CC.get(record.countryid))
        self.senderLineEdit.setText(self.determine_agent(agent=record.agent,
                                                         agent_id=record.agentid))

    def clear_criteria_fields(self, clear_all=True):
        """ Method that will clear the content of the input fields. """

        if not clear_all:
            self.trademarkLineEdit.clear()
            self.countrycodeLineEdit.clear()
            self.senderLineEdit.clear()
        else:
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
        dnc = self.generate_dnc()
        self.dncTextEdit.setText(dnc)
        if self.AUTOCOPY:
            self.clipboard.setText(dnc)

    def generate_dnc(self):

        if not self.emailtypeComboBox.isVisible():
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
        """ Event handler that will 'switch' the current text of the Sender and Recipient fields. """

        # Get the current values of the fields
        sender, recipient = self.senderLineEdit.text(), self.recipientLineEdit.text()

        # Perform the simple switching of values
        self.senderLineEdit.setText(recipient)
        self.recipientLineEdit.setText(sender)

    def resizeEvent(self, event):

        LOGGER.info(f'w x h: {self.width()} x {self.height()}')

    def keyPressEvent(self, event):

        # 'Ctr+Q' -> close the app
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()

        # 'F5' -> clear fields
        if event.key() == Qt.Key_F5:
            self.AUTOCOPY = False
            self.clear_criteria_fields()
            self.grnLineEdit.clear()
            self.dncTextEdit.clear()

        # 'F6' -> reconnect to GIPM
        if event.key() == Qt.Key_F6:
            LOGGER.info('Reconnecting...')
            self.dncTextEdit.setText('Reconnecting...')
            self._connect()

        # TEST: adding 'F7' to disconnect from SQLite database -> for development only
        # if event.key() == Qt.Key_F7:
        #     judi.disconnect()
        #     LOGGER.error('Disconnected from SQLite')

    def closeEvent(self, event):

        self._write_settings()

    def _write_settings(self):

        self.settings.setValue(SETTINGS_GEOMETRY, self.saveGeometry())
