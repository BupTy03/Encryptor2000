from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from design.mainwindow_ui import Ui_MainWindow
import encryption_algorithms as encrypt


class MainWindow(QMainWindow):
    def __init__(self):
        # init GUI
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # setup GUI
        self.setWindowTitle('Encryptor2000')
        self.ui.pathToFileGroupBox.setVisible(False)
        self.ui.resultPlainTextEdit.setReadOnly(True)
        self.ui.pathLineEdit.setReadOnly(True)

        # connect window buttons
        self.ui.exitPushButton.clicked.connect(self.close)
        self.ui.startPushButton.clicked.connect(self.on_start_btn_clicked)
        self.ui.viewPushButton.clicked.connect(self.on_view_push_button_clicked)
        self.ui.savePushButton.clicked.connect(self.on_save_btn_clicked)

        # connect radio buttons
        self.ui.encryptionModeRadioButton.toggled.connect(self.on_encryption_mode_radio_btn_toggled)

        self.ui.fileRadioButton.toggled.connect(self.on_from_file_radio_btn_toggled)
        self.ui.plainTextRadioButton.toggled.connect(self.on_from_plain_text_radio_btn_toggled)

        # connect combobox
        self.ui.encryptionMethodComboBox.currentTextChanged.connect(self.on_encryption_method_changed)

        # setup encryption algorithms
        self.encryptAlgorithms = {
            'Cesar cipher': [encrypt.cesar_cipher_encrypt, encrypt.cesar_cipher_decrypt],
            'Vigenere cipher': [encrypt.vigenere_cipher_encrypt, encrypt.vigenere_cipher_decrypt]
        }

        self.ui.encryptionMethodComboBox.addItems(self.encryptAlgorithms.keys())
        self.currentMethod = self.encryptAlgorithms[self.ui.encryptionMethodComboBox.currentText()][0]
        self.ui.encryptionModeRadioButton.toggle()

    def on_encryption_method_changed(self, curr_text: str):
        encrypt_mode_index = 0 if self.ui.encryptionModeRadioButton.isChecked() else 1
        self.currentMethod = self.encryptAlgorithms[curr_text][encrypt_mode_index]

    def on_encryption_mode_radio_btn_toggled(self, toggled: bool):
        encrypt_mode_index = 0 if toggled else 1
        self.currentMethod = self.encryptAlgorithms[self.ui.encryptionMethodComboBox.currentText()][encrypt_mode_index]

    def on_from_plain_text_radio_btn_toggled(self, toggled: bool):
        self.ui.sourceLabel.setVisible(toggled)
        self.ui.sourcePlainTextEdit.setVisible(toggled)

    def on_from_file_radio_btn_toggled(self, toggled: bool):
        if not toggled:
            self.ui.pathToFileGroupBox.setVisible(False)
            return

        self.ui.pathToFileGroupBox.setVisible(True)
        self.ui.resultPlainTextEdit.clear()

    def on_view_push_button_clicked(self):
        (filename, ext) = QFileDialog.getOpenFileName(self, self.tr('Open file'), '/', self.tr('*.txt'))
        self.ui.pathLineEdit.setText(filename)

    def show_error(self, text: str):
        QMessageBox.critical(self, self.tr('Error'), self.tr(text))

    def on_save_btn_clicked(self):
        (filename, ext) = QFileDialog.getSaveFileName(self, self.tr('Open file'), '/', self.tr('*.txt'))
        file = open(filename, 'w')
        if not file:
            self.show_error('Unable to open file: "' + filename + '" to write')
            return

        file.write(self.ui.resultPlainTextEdit.toPlainText())
        file.close()

    def on_start_btn_clicked(self):
        key = self.ui.keyLineEdit.text()
        text = ''

        if self.ui.fileRadioButton.isChecked():
            filename = self.ui.pathLineEdit.text()
            file = open(filename, 'r')
            if not file:
                self.show_error('Unable to open file: "' + filename + '" to read')
                return

            text = file.read()
            file.close()
            if len(text) <= 0:
                self.show_error('File is empty')
                return
        else:
            text = self.ui.sourcePlainTextEdit.toPlainText()
            if len(text) <= 0:
                self.show_error('Enter text before press start')
                return

        text = self.currentMethod(text, key)
        self.ui.resultPlainTextEdit.setPlainText(text)





