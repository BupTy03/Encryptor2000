import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.Qt import QTranslator, QLocale, QFile, QIODevice, QByteArray
from mainwindow import MainWindow
import res.resources


def main():

    app = QApplication(sys.argv)

    styles = QFile(":/style/styles.qss")
    styles.open(QIODevice.ReadOnly)

    app.setStyleSheet(styles.readAll().data().decode("latin1"))

    translator = QTranslator()
    if translator.load(QLocale(), "localization", "_", ":/localization"):
        app.installTranslator(translator)
    else:
        print("Unable to load localization")

    w = MainWindow()
    w.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
