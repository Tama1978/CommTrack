import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class EraseLogsPromptUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("!! Erase All Logs !!")
        self.setWindowIcon(QIcon('app/assets/HamLog-Logo.png'))
        self.setGeometry(500, 500, 800, 200)
       
def main():
    app = QApplication(sys.argv)
    station_ui = EraseLogsPromptUI()
    station_ui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()