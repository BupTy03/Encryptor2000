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
        self.ui.pathToSourceGroupBox.setVisible(False)
        self.ui.pathToDestFileGroupBox.setVisible(False)

        self.ui.resultPlainTextEdit.setReadOnly(True)

        self.ui.pathToSourceLineEdit.setReadOnly(True)
        self.ui.pathToDestLineEdit.setReadOnly(True)

        self.resize(self.width(), self.height() - 20)

        # connect window buttons
        self.ui.exitPushButton.clicked.connect(self.close)
        self.ui.startPushButton.clicked.connect(self.on_start_btn_clicked)
        self.ui.viewSourcePushButton.clicked.connect(self.on_view_source_push_button_clicked)
        self.ui.viewDestPushButton.clicked.connect(self.on_view_dest_push_button_clicked)
        self.ui.savePushButton.clicked.connect(self.on_save_btn_clicked)

        # connect radio buttons
        self.ui.encryptionModeRadioButton.toggled.connect(self.on_encryption_mode_radio_btn_toggled)
        self.ui.fromPlainTextRadioButton.toggled.connect(self.on_from_plain_text_radio_btn_toggled)
        self.ui.toPlainTextRadioButton.toggled.connect(self.on_to_plain_text_radio_btn_toggled)

        # connect combobox
        self.ui.encryptionMethodComboBox.currentTextChanged.connect(self.on_encryption_method_changed)

        # setup encryption algorithms
        self.encryptAlgorithms = {
            'Cesar cipher': [encrypt.cesar_cipher_encrypt, encrypt.cesar_cipher_decrypt, self.hide_key_input],
            'Vigenere cipher': [encrypt.vigenere_cipher_encrypt, encrypt.vigenere_cipher_decrypt, self.show_key_input],
            'DES': [encrypt.des_cipher_encrypt, encrypt.des_cipher_decrypt, self.show_key_input],
            'AES': [encrypt.aes_cipher_encrypt, encrypt.aes_cipher_decrypt, self.show_key_input]
        }

        self.ui.encryptionMethodComboBox.addItems(self.encryptAlgorithms.keys())
        self.currentMethod = self.encryptAlgorithms[self.ui.encryptionMethodComboBox.currentText()][0]
        self.encryptAlgorithms[self.ui.encryptionMethodComboBox.currentText()][2]()
        self.ui.encryptionModeRadioButton.toggle()

    def on_encryption_method_changed(self, curr_text: str):
        encrypt_mode_index = 0 if self.ui.encryptionModeRadioButton.isChecked() else 1
        self.currentMethod = self.encryptAlgorithms[curr_text][encrypt_mode_index]

        # prepare GUI
        self.encryptAlgorithms[curr_text][2]()

    def on_encryption_mode_radio_btn_toggled(self, toggled: bool):
        encrypt_mode_index = 0 if toggled else 1
        self.currentMethod = self.encryptAlgorithms[self.ui.encryptionMethodComboBox.currentText()][encrypt_mode_index]

    def on_from_plain_text_radio_btn_toggled(self, toggled: bool):
        if self.ui.pathToSourceGroupBox.isVisible() and self.ui.pathToDestFileGroupBox.isVisible():
            self.resize(self.width(), self.height() + 100)

        self.ui.sourceLabel.setVisible(toggled)
        self.ui.sourcePlainTextEdit.setVisible(toggled)
        self.ui.pathToSourceGroupBox.setVisible(not toggled)

        if self.ui.pathToSourceGroupBox.isVisible() and self.ui.pathToDestFileGroupBox.isVisible():
            self.resize(self.width(), self.height() - 100)

    def on_to_plain_text_radio_btn_toggled(self, toggled: bool):
        if self.ui.pathToSourceGroupBox.isVisible() and self.ui.pathToDestFileGroupBox.isVisible():
            self.resize(self.width(), self.height() + 100)

        self.ui.resultLabel.setVisible(toggled)
        self.ui.resultPlainTextEdit.setVisible(toggled)
        self.ui.pathToDestFileGroupBox.setVisible(not toggled)
        self.ui.savePushButton.setVisible(toggled)

        if self.ui.pathToSourceGroupBox.isVisible() and self.ui.pathToDestFileGroupBox.isVisible():
            self.resize(self.width(), self.height() - 100)

    def on_view_source_push_button_clicked(self):
        (filename, ext) = QFileDialog.getOpenFileName(self, self.tr('Open file'), '/', self.tr('*.txt'))
        self.ui.pathToSourceLineEdit.setText(filename)

    def on_view_dest_push_button_clicked(self):
        (filename, ext) = QFileDialog.getSaveFileName(self, self.tr('Save file'), '/', self.tr('*.txt'))
        self.ui.pathToDestLineEdit.setText(filename)

    def show_error(self, text: str):
        QMessageBox.critical(self, self.tr('Error'), self.tr(text))

    def on_save_btn_clicked(self):
        (filename, ext) = QFileDialog.getSaveFileName(self, self.tr('Open file'), '/', self.tr('*.txt'))
        if not filename:
            return

        file = open(filename, 'w')
        if not file:
            self.show_error('Unable to open file: "' + filename + '" to write')
            return

        file.write(self.ui.resultPlainTextEdit.toPlainText())
        file.close()

    def on_start_btn_clicked(self):
        key = self.ui.keyLineEdit.text()
        text = ''

        if self.ui.fromFileRadioButton.isChecked():
            filename = self.ui.pathToSourceLineEdit.text()
            if len(filename) == 0:
                self.show_error('Enter filename')
                return

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

        try:
            text = self.currentMethod(text, key)
        except Exception as ex:
            self.show_error(str(ex))
            return

        if self.ui.toPlainTextRadioButton.toggled():
            self.ui.resultPlainTextEdit.setPlainText(text)
        else:
            filename = self.ui.pathToDestLineEdit.text()
            if len(filename) == 0:
                self.show_error('Enter filename')
                return

            file = open(filename, 'w+')
            if not file:
                self.show_error('Unable to open file: "' + filename + '" to write')
                return

            file.write(text)
            file.close()

    def hide_key_input(self):
        self.ui.keyLabel.setVisible(False)
        self.ui.keyLineEdit.setVisible(False)

    def show_key_input(self):
        self.ui.keyLabel.setVisible(True)
        self.ui.keyLineEdit.setVisible(True)





