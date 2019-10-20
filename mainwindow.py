from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread
from PyQt5.Qt import pyqtSignal, pyqtSlot, QTranslator, QLocale
from design.mainwindow_ui import Ui_MainWindow
import encryption_algorithms as encrypt
from packaged_task import PackagedTask


def encrypt_data(from_file: bool, to_file: bool, argstr1: str, argstr2: str, cipher_method, key: str):
    if from_file and to_file:
        input_file = open(file=argstr1, mode="r", encoding="1251")
        output_file = open(file=argstr2, mode="w+", encoding="1251")
        while True:
            current_bytes = input_file.read(1024)
            if len(current_bytes) == 0:
                break

            output_file.write(cipher_method(current_bytes, key))

        input_file.close()
        output_file.close()
        return ""
    elif from_file:
        with open(file=argstr1, mode="r", encoding="1251") as input_file:
            return cipher_method(input_file.read(), key)
    elif to_file:
        with open(file=argstr2, mode="w+", encoding="1251") as output_file:
            output_file.write(cipher_method(argstr1, key))
        return ""
    else:
        return cipher_method(argstr1, key)


class MainWindow(QMainWindow):
    def __init__(self):
        # init GUI
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # setup tasks processor
        self.second_thread = QThread()
        self.packaged_task = PackagedTask()
        self.start_processing_task.connect(self.packaged_task.start_task)
        self.packaged_task.task_done.connect(self.on_task_done)
        self.packaged_task.moveToThread(self.second_thread)
        self.second_thread.start()

        # setup GUI
        self.setWindowTitle("Encryptor2000")
        self.ui.pathToSourceGroupBox.setVisible(False)
        self.ui.pathToDestFileGroupBox.setVisible(False)

        self.ui.resultPlainTextEdit.setReadOnly(True)

        self.ui.pathToSourceLineEdit.setReadOnly(True)
        self.ui.pathToDestLineEdit.setReadOnly(True)

        self.ui.startPushButton.setDefault(True)

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
            self.tr("Cesar cipher"): [encrypt.cesar_cipher_encrypt, encrypt.cesar_cipher_decrypt, self.hide_key_input],
            self.tr("Vigenere cipher"): [encrypt.vigenere_cipher_encrypt, encrypt.vigenere_cipher_decrypt, self.show_key_input],
            "DES": [encrypt.des_cipher_encrypt, encrypt.des_cipher_decrypt, self.show_key_input],
            "AES": [encrypt.aes_cipher_encrypt, encrypt.aes_cipher_decrypt, self.show_key_input]
        }

        # setup menu
        self.ui.menu_exit.triggered.connect(self.close)
        self.ui.menu_start.triggered.connect(self.on_start_btn_clicked)
        self.ui.menu_save.triggered.connect(self.on_save_btn_clicked)

        # setup languages
        self.language_menu_table = {
            self.ui.language_russian: QLocale.Russian,
            self.ui.language_english: QLocale.English,
            self.ui.language_deutsch: QLocale.German
        }
        self.ui.language_russian.triggered.connect(self.change_language)
        self.ui.language_english.triggered.connect(self.change_language)
        self.ui.language_deutsch.triggered.connect(self.change_language)

        self.ui.encryptionMethodComboBox.addItems(self.encryptAlgorithms.keys())
        self.currentMethod = self.encryptAlgorithms[self.ui.encryptionMethodComboBox.currentText()][0]
        self.encryptAlgorithms[self.ui.encryptionMethodComboBox.currentText()][2]()
        self.ui.encryptionModeRadioButton.toggle()

# signals:
    start_processing_task = pyqtSignal()

# slots:
    @pyqtSlot(str, name="on_encryption_method_changed")
    def on_encryption_method_changed(self, curr_text: str):
        encrypt_mode_index = 0 if self.ui.encryptionModeRadioButton.isChecked() else 1
        self.currentMethod = self.encryptAlgorithms[curr_text][encrypt_mode_index]

        # prepare GUI
        self.encryptAlgorithms[curr_text][2]()

    @pyqtSlot(bool, name="on_encryption_mode_radio_btn_toggled")
    def on_encryption_mode_radio_btn_toggled(self, toggled: bool):
        encrypt_mode_index = 0 if toggled else 1
        self.currentMethod = self.encryptAlgorithms[self.ui.encryptionMethodComboBox.currentText()][encrypt_mode_index]

    @pyqtSlot(bool, name="on_from_plain_text_radio_btn_toggled")
    def on_from_plain_text_radio_btn_toggled(self, toggled: bool):
        if self.ui.pathToSourceGroupBox.isVisible() and self.ui.pathToDestFileGroupBox.isVisible():
            self.resize(self.width(), self.height() + 100)

        self.ui.sourceLabel.setVisible(toggled)
        self.ui.sourcePlainTextEdit.setVisible(toggled)
        self.ui.pathToSourceGroupBox.setVisible(not toggled)

        if self.ui.pathToSourceGroupBox.isVisible() and self.ui.pathToDestFileGroupBox.isVisible():
            self.resize(self.width(), self.height() - 100)

    @pyqtSlot(bool, name="on_to_plain_text_radio_btn_toggled")
    def on_to_plain_text_radio_btn_toggled(self, toggled: bool):
        if self.ui.pathToSourceGroupBox.isVisible() and self.ui.pathToDestFileGroupBox.isVisible():
            self.resize(self.width(), self.height() + 100)

        self.ui.resultLabel.setVisible(toggled)
        self.ui.resultPlainTextEdit.setVisible(toggled)
        self.ui.pathToDestFileGroupBox.setVisible(not toggled)
        self.ui.savePushButton.setVisible(toggled)

        if self.ui.pathToSourceGroupBox.isVisible() and self.ui.pathToDestFileGroupBox.isVisible():
            self.resize(self.width(), self.height() - 100)

    @pyqtSlot(name="on_view_source_push_button_clicked")
    def on_view_source_push_button_clicked(self):
        (filename, ext) = QFileDialog.getOpenFileName(self, self.tr("Open file"), '/', "*.txt")
        self.ui.pathToSourceLineEdit.setText(filename)

    @pyqtSlot(name="on_view_dest_push_button_clicked")
    def on_view_dest_push_button_clicked(self):
        (filename, ext) = QFileDialog.getSaveFileName(self, self.tr("Save file"), '/', "*.txt")
        self.ui.pathToDestLineEdit.setText(filename)

    @pyqtSlot(name="on_save_btn_clicked")
    def on_save_btn_clicked(self):
        (filename, ext) = QFileDialog.getSaveFileName(self, self.tr("Open file"), '/', "*.txt")
        if not filename:
            return

        file = open(filename, 'w')
        if not file:
            self.show_error("Unable to open file: \"" + filename + "\" to write")
            return

        file.write(self.ui.resultPlainTextEdit.toPlainText())
        file.close()

    @pyqtSlot(name="on_start_btn_clicked")
    def on_start_btn_clicked(self):
        key = self.ui.keyLineEdit.text()
        if self.ui.fromFileRadioButton.isChecked() and self.ui.toFileRadioButton.isChecked():
            self.packaged_task.set_task(task=encrypt_data, args=(
                True,
                True,
                self.ui.pathToSourceLineEdit.text(),
                self.ui.pathToDestLineEdit.text(),
                self.currentMethod,
                key
            ))
        elif self.ui.fromFileRadioButton.isChecked():
            self.packaged_task.set_task(task=encrypt_data, args=(
                True,
                False,
                self.ui.pathToSourceLineEdit.text(),
                self.ui.resultPlainTextEdit.toPlainText(),
                self.currentMethod,
                key
            ))
        elif self.ui.toFileRadioButton.isChecked():
            self.packaged_task.set_task(task=encrypt_data, args=(
                False,
                True,
                self.ui.sourcePlainTextEdit.toPlainText(),
                self.ui.pathToDestLineEdit.text(),
                self.currentMethod,
                key
            ))
        else:
            self.packaged_task.set_task(task=encrypt_data, args=(
                False,
                False,
                self.ui.sourcePlainTextEdit.toPlainText(),
                self.ui.resultPlainTextEdit.toPlainText(),
                self.currentMethod,
                key
            ))

        self.enable_ui(False)
        self.start_processing_task.emit()

    @pyqtSlot(bool, name="on_task_done")
    def on_task_done(self, success: bool):
        if not success:
            self.show_error(str(self.packaged_task.get_stored_exception()))

        text = self.packaged_task.get_result()

        if self.ui.toPlainTextRadioButton.isChecked():
            self.ui.resultPlainTextEdit.setPlainText(text)

        self.enable_ui(True)

    @pyqtSlot(name="change_language")
    def change_language(self):
        language_menu_item = self.sender()

        translator = QTranslator()
        translator.load(QLocale(self.language_menu_table[language_menu_item]), "localization", "_", "localization")
        QApplication.installTranslator(translator)
        self.ui.retranslateUi(self)

# methods:
    def show_error(self, text: str):
        QMessageBox.critical(self, self.tr("Error"), text)

    def hide_key_input(self):
        self.ui.keyLabel.setVisible(False)
        self.ui.keyLineEdit.setVisible(False)

    def show_key_input(self):
        self.ui.keyLabel.setVisible(True)
        self.ui.keyLineEdit.setVisible(True)

    def enable_ui(self, enable: bool):
        self.ui.decryptionModeRadioButton.setEnabled(enable)
        self.ui.encryptionMethodComboBox.setEnabled(enable)
        self.ui.encryptionModeRadioButton.setEnabled(enable)
        self.ui.fromFileRadioButton.setEnabled(enable)
        self.ui.fromPlainTextRadioButton.setEnabled(enable)
        self.ui.keyLineEdit.setEnabled(enable)
        self.ui.pathToDestLineEdit.setEnabled(enable)
        self.ui.pathToSourceLineEdit.setEnabled(enable)
        self.ui.resultPlainTextEdit.setEnabled(enable)
        self.ui.savePushButton.setEnabled(enable)
        self.ui.sourcePlainTextEdit.setEnabled(enable)
        self.ui.startPushButton.setEnabled(enable)
        self.ui.toFileRadioButton.setEnabled(enable)
        self.ui.toPlainTextRadioButton.setEnabled(enable)
        self.ui.viewDestPushButton.setEnabled(enable)
        self.ui.viewSourcePushButton.setEnabled(enable)



