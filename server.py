from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, QtWidgets
import sys


class GUI(QMainWindow):

    def __init__(self):

        super().__init__()
        self.__width = 600
        self.__height = 400
        self.__perc = (0.1, 0.8)

        self.__setup_GUI()

    def __setup_GUI(self):

        self.setWindowTitle("lab1")
        self.resize(self.__width, self.__height)

        self.lbLog = QtWidgets.QLabel(self)
        self.lbLog.setGeometry(QtCore.QRect(60, 20, 100, 15))
        self.lbLog.setObjectName("lbLog")
        self.lbLog.setText("Server Logs")

        self.teLog = QtWidgets.QTextEdit(self)
        self.teLog.setGeometry(QtCore.QRect(60, 40, 300, 300))
        self.teLog.setObjectName("teLog")
        self.teLog.setEnabled(False)


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())