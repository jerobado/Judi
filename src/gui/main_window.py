# Judi Main Window

from PyQt5.QtCore import (Qt,
                          QDate)
from PyQt5.QtWidgets import (QWidget,
                             QLineEdit,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                             QDateEdit,
                             QPushButton)
from src.resources.constant import (__version__,
                                    __appname__,
                                    NON_AB_TEMPLATE,
                                    CONNECTION_STR)


def connect_judi():
    """  Method that will connect Judi to the server and its databases. This will return conn.

        return conn.cursor()
    """

    _methodname = 'connect_judi'

    try:
        import pyodbc
        # Attempting to connect to the server
        print(f'{_methodname}: Connecting to GSM...')
        conn = pyodbc.connect(CONNECTION_STR)
        print(f'{_methodname}: Good! You are now connected to GSM.')
        return conn.cursor()

    except Exception as e:
        print(f'{_methodname}: Connection to GSM failed. Try again.\n{e}')


def search_grn(raw_grn):  # STATUS: inactive
    """ Method that will connect to the database and return a GIPM record based on the GRN entered.

        raw_grn -> list
    """

    # Let's connect to the server
    try:
        import pyodbc

        # Try connection to GSM's server
        print('Initiating spin...')
        conn = pyodbc.connect(CONNECTION_STR)

        # Tuplelized
        grn = (raw_grn,)

        # Get the cursor
        cursor = conn.cursor()
        cursor.execute(trademark_query_sql, grn)

        # Get the retrieved record
        record = cursor.fetchone()

        return record

    except Exception as e:
        print(f'Try again. Error: {e}')


def load_sql():
    """ Method that will retrieve an SQL text. """

    sql_file = open('../sql/search_grn.sql', 'r')
    return sql_file.read()


class JudiWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.date_format = 'yyyyMMdd'
        self.profiling_date = QDate.currentDate()
        self.search_grn_sql = load_sql()
        self._widgets()
        self._layout()
        self._properties()
        self._connections()
        self._gsmconnect()

    def _widgets(self):

        self.grnLabel = QLabel()
        self.grnLineEdit = QLineEdit()
        self.sentDateEdit = QDateEdit()
        self.trademarkLineEdit = QLineEdit()
        self.country_codeLineEdit = QLineEdit()
        self.descriptionLineEdit = QLineEdit()
        self.senderLineEdit = QLineEdit()
        self.recipientLineEdit = QLineEdit()
        self.profilingLabel = QLabel()
        self.flatPushButton = QPushButton()

    def _properties(self):

        self.grnLabel.setText('GRN:')
        self.grnLineEdit.setPlaceholderText('Trademarks, Searches, etc.')
        self.grnLineEdit.setMaximumWidth(150)
        self.sentDateEdit.setObjectName('sentDateEdit')
        self.sentDateEdit.setDate(self.profiling_date)
        self.sentDateEdit.setCalendarPopup(True)
        self.trademarkLineEdit.setPlaceholderText('Trademark')
        self.country_codeLineEdit.setPlaceholderText('Country Code')
        self.descriptionLineEdit.setPlaceholderText('Brief Description')
        self.descriptionLineEdit.setObjectName('descriptionLineEdit')
        self.senderLineEdit.setPlaceholderText('Sender')
        self.recipientLineEdit.setPlaceholderText('Recipient')
        self.recipientLineEdit.setObjectName('recipientLineEdit')
        self.profilingLabel.setText('Copy profile here')
        self.profilingLabel.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextSelectableByKeyboard)

        self.flatPushButton.setText('Test button')
        self.flatPushButton.setFlat(True)

        self.setWindowTitle(f'{__appname__} {__version__}')
        self.setObjectName('JudiWindow')
        self.resize(616, 110)   # width, height

    def _layout(self):

        first_layer = QHBoxLayout()
        first_layer.addWidget(self.grnLabel)
        first_layer.addWidget(self.grnLineEdit)
        first_layer.addStretch()

        second_layer = QHBoxLayout()
        second_layer.addWidget(self.sentDateEdit)
        second_layer.addWidget(self.trademarkLineEdit)
        second_layer.addWidget(self.country_codeLineEdit)
        second_layer.addWidget(self.descriptionLineEdit)
        second_layer.addWidget(self.senderLineEdit)
        second_layer.addWidget(self.recipientLineEdit)

        third_layer = QHBoxLayout()
        third_layer.addWidget(self.profilingLabel)

        first_col = QVBoxLayout()
        first_col.addLayout(first_layer)
        first_col.addLayout(second_layer)
        first_col.addLayout(third_layer)

        self.setLayout(first_col)

    def _connections(self):

        self.grnLineEdit.textChanged.connect(self.on_grnLineEdit_textChanged)
        self.grnLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.sentDateEdit.dateChanged.connect(self.on_criteriaChanged)
        self.trademarkLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.country_codeLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.descriptionLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.senderLineEdit.textChanged.connect(self.on_criteriaChanged)
        self.recipientLineEdit.textChanged.connect(self.on_criteriaChanged)

    def _gsmconnect(self):
        """ Connect to GSM's server and database and will get the cursor. """

        self.cursor_ = connect_judi()

    def on_grnLineEdit_textChanged(self):

        grn = self.grnLineEdit.text()
        #record = search_grn(grn)
        record = self.search_grn_(grn)

        trademark = record[2]
        country_code = record[4]
        agent = record[5]

        self.trademarkLineEdit.setText(trademark)
        self.country_codeLineEdit.setText(country_code)
        self.senderLineEdit.setText(agent)

    def search_grn_(self, grn):
        """ Method that will search a record based on the given GRN. """

        try:
            print(f'Searching for {grn}...')
            grn = (grn,)    # Tuplelized :)

            # Execute search query
            self.cursor_.execute(self.search_grn_sql, grn)

            # Get the retrieved record
            record = self.cursor_.fetchone()
            print(f'Record found!')
            return record

        except Exception as e:
            print(f'Judi has pressed the self-destruct button!\n{e}')

    def on_criteriaChanged(self):

        self.profiling_date = self.sentDateEdit.date()
        profiling_text = NON_AB_TEMPLATE.substitute(sent=self.profiling_date.toString(self.date_format),
                                                    trademark=self.trademarkLineEdit.text(),
                                                    country_code=self.country_codeLineEdit.text(),
                                                    description=self.descriptionLineEdit.text(),
                                                    sender=self.senderLineEdit.text(),
                                                    recipient=self.recipientLineEdit.text())
        self.profilingLabel.setText(profiling_text)

    def resizeEvent(self, event):

        print(f'w x h: {self.height()} x {self.width()}')
