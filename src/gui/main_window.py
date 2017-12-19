# Judi Main Window

from string import Template
from PyQt5.QtCore import (Qt,
                          QDate)
from PyQt5.QtWidgets import (QWidget,
                             QLineEdit,
                             QLabel,
                             QHBoxLayout,
                             QVBoxLayout,
                             QDateEdit,
                             QPushButton)

__version__ = '0.1a'
__appname__ = 'Judi'


unilever = {'grn': '3125786',
            'trademark': 'DOVE (STYLISED)',
            'country_code': 'KOS',
            'agent': 'Kim & Chang'}
swarovski = {'grn': '5412462',
             'trademark': 'SWAROVSKI',
             'country_code': 'JAP',
             'agent': 'BM Tokyo'}
records = (swarovski, unilever)
non_abbott_template = Template('$sent $trademark ($country_code) $description $sender $recipient')


# class ProfilingLabel(QLabel):
#
#     def mousePressEvent(self, event):
#
#         print('click?!')

# [x] TODO: forked Gee
# [] TODO: redesign UI
class GeeWindow(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)
        self.date_format = 'yyyyMMdd'
        self.profiling_date = QDate.currentDate()
        self._widgets()
        self._layout()
        self._properties()
        self._connections()

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
        #self.profilingLabel = ProfilingLabel()
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

    def on_grnLineEdit_textChanged(self):

        grn = self.grnLineEdit.text()
        for entry in records:
            if grn == entry['grn']:
                self.trademarkLineEdit.setText(entry['trademark'])
                self.country_codeLineEdit.setText(entry['country_code'])
                self.senderLineEdit.setText(entry['agent'])
                break
            else:
                self.profilingLabel.setText(f'No record found for GRN {grn}. Try again.')

    def on_criteriaChanged(self):

        self.profiling_date = self.sentDateEdit.date()
        profiling_text = non_abbott_template.substitute(sent=self.profiling_date.toString(self.date_format),
                                                        trademark=self.trademarkLineEdit.text(),
                                                        country_code=self.country_codeLineEdit.text(),
                                                        description=self.descriptionLineEdit.text(),
                                                        sender=self.senderLineEdit.text(),
                                                        recipient=self.recipientLineEdit.text())
        self.profilingLabel.setText(profiling_text)

    def resizeEvent(self, event):

        print(f'w x h: {self.height()} x {self.width()}')
