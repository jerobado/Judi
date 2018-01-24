# Judi Main Window

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
from src.resources.constant import (__appname__,
                                    __version__,
                                    AB_EMAIL_TYPE,
                                    AB_TEMPLATE,
                                    BM_OFFICES,
                                    BM_OFFICES_COMPLETER,
                                    CONNECTION_STR,
                                    CONNECTION_STR_SQLITE,
                                    DATE_FORMAT,
                                    NON_AB_TEMPLATE,
                                    SEARCH_GRN_SQL,
                                    SETTINGS_GEOMETRY,
                                    STYLESHEET,
                                    USERNAME)
from src.resources import judi_resources


def connect_judi():
    """  Method that will connect Judi to the server and its databases. This will return conn.

        return conn.cursor()
    """

    _methodname = 'connect_judi'
    print(CONNECTION_STR)

    try:
        import pyodbc
        # Attempting to connect to the server
        print(f'{_methodname}: Connecting to GSM...')
        conn = pyodbc.connect(CONNECTION_STR)
        print(f'{_methodname}: Good! You are now connected to GSM.')
        return conn.cursor()

    except Exception as e:
        print(f'{_methodname}: Connection to GSM failed. Try again.\n{e}')


def connect_judi2():
    """ Thiw will connect to the SQLite database. """

    _methodname = 'connect_judi2'

    try:
        print(f'{_methodname}: Connecting to SQLite...')
        import sqlite3
        conn = sqlite3.connect(CONNECTION_STR_SQLITE)
        print(f'{_methodname}: Good! You are now connected to SQLite.')
        return conn.cursor()
    except Exception as e:
        print(f'{_methodname}: Connection to SQLite failed. Try again.\n{e}')


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
        self.setStyleSheet(STYLESHEET)
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
        """ Connect to GSM's server and database and will get the cursor. """

        # don't forget to also comment load_sql()
        #self.cursor_ = connect_judi()  # connecting to GSM
        self.cursor_ = connect_judi2()   # connecting to sqlite

    def _read_settings(self):

        self.restoreGeometry(self.settings.value(SETTINGS_GEOMETRY, self.saveGeometry()))

    def on_grnLineEdit_textChanged(self):

        try:
            # Get the package to deliver
            grn = self.grnLineEdit.text()

            if grn:  # has content, perform the search
                record = self.search_grn_(grn)

                # Parse the package
                trademark = record[2]
                country = record[3]
                country_code = record[4]

                # TEST: check if country has BM Office
                if self.has_bm_office(country):
                    agent = self.has_bm_office(country)
                else:
                    agent = record[5]

                # Deliver the package
                self.trademarkLineEdit.setText(trademark)
                self.countrycodeLineEdit.setText(country_code)
                self.senderLineEdit.setText(agent)

            else:   # has no content
                self.clear_criteria_fields()
                self.dncTextEdit.clear()

        except TypeError as e:  # No record found
            self.clear_criteria_fields()
            self.dncTextEdit.setText('No record found. Try again.')
            print(f'on_grnLineEdit_textChanged: {e} - {type(e)}')

        except AttributeError as e:  # Trying to catch that 'timeout' error
            self.dncTextEdit.setText('Your sessions has timed-out. Try re-opening Judi.')
            print(f'on_grnLineEdit_textChanged: {e} - {type(e)}')

        except Exception as e:
            print(f'on_grnLineEdit_textChanged: {e} - {type(e)}')

    def search_grn_(self, grn):
        """ Method that will search a record based on the given GRN. """

        print(f'Searching for {grn}...')
        grn = (grn,)    # Tuplelized :)

        # Execute search query
        self.cursor_.execute(SEARCH_GRN_SQL, grn)

        # Get the retrieved record
        record = self.cursor_.fetchone()
        print(f'Record found! -> {record}')
        return record

    def clear_criteria_fields(self):
        """ Method that will clear the content of the input fields. """

        self.trademarkLineEdit.clear()
        self.countrycodeLineEdit.clear()
        self.descriptionLineEdit.clear()
        self.senderLineEdit.clear()
        self.recipientLineEdit.clear()

    def has_bm_office(self, country):
        """ Check if country has a BM Office. """

        return BM_OFFICES.get(country)

    def on_criteriaChanged(self):

        self.profiling_date = self.sentDateEdit.date()

        combobox_index = self.emailtypeComboBox.currentIndex()
        if combobox_index:
            # If Abbott
            profiling_text = AB_TEMPLATE.substitute(sent=self.profiling_date.toString(DATE_FORMAT),
                                                    trademark=self.trademarkLineEdit.text(),
                                                    countrycode=self.countrycodeLineEdit.text(),
                                                    emailtype=self.emailtypeComboBox.currentText(),
                                                    description=self.descriptionLineEdit.text(),
                                                    sender=self.senderLineEdit.text(),
                                                    recipient=self.recipientLineEdit.text())
        else:
            # If Non-Abbott
            profiling_text = NON_AB_TEMPLATE.substitute(sent=self.profiling_date.toString(DATE_FORMAT),
                                                        trademark=self.trademarkLineEdit.text(),
                                                        countrycode=self.countrycodeLineEdit.text(),
                                                        description=self.descriptionLineEdit.text(),
                                                        sender=self.senderLineEdit.text(),
                                                        recipient=self.recipientLineEdit.text())

        self.dncTextEdit.setText(profiling_text)
        self.clipboard.setText(profiling_text)

    def on_switchPushButton_clicked(self):
        """ Event handler that will 'switch' the entries of the Sender and Recipient LineEdits. """

        # Get the current values of the fields
        sender = self.senderLineEdit.text()
        recipient = self.recipientLineEdit.text()

        # Perform the simple switching of values
        self.senderLineEdit.setText(recipient)
        self.recipientLineEdit.setText(sender)

    def _write_settings(self):

        self.settings.setValue(SETTINGS_GEOMETRY, self.saveGeometry())

    def resizeEvent(self, event):

        #print(f'w x h: {self.height()} x {self.width()}')
        pass

    def keyPressEvent(self, event):

        # When the used pressed the shortcut 'Ctr+Q'
        if event.modifiers() & Qt.ControlModifier and event.key() == Qt.Key_Q:
            self.close()

    def closeEvent(self, event):

        self._write_settings()
