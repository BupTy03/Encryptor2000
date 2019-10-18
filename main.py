import sys
from PyQt5.QtWidgets import QApplication
from mainwindow import MainWindow


def main():

    app = QApplication(sys.argv)

    application = MainWindow()
    application.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
