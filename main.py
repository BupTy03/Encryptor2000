import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.Qt import QTranslator, QLocale
from mainwindow import MainWindow


def main():

    app = QApplication(sys.argv)
    translator = QTranslator()
    if translator.load(QLocale(), "localization", "_", "localization"):
        app.installTranslator(translator)
    else:
        print("Unable to load localization")

    w = MainWindow()
    w.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
