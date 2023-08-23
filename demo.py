from MyLib import MyWidgets
from PyQt5 import QtWidgets, QtCore, QtGui



if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = MyWidgets.RoundedWidget()
    window.resize(500, 400)
    window.setDarkStyle()
    window.setRadius(25)
    window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    window.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    grad = QtGui.QLinearGradient()
    grad.setStart(0, window.height())
    grad.setFinalStop(window.width(), 0)
    grad.setColorAt(0, QtGui.QColor(30, 20, 40))
    grad.setColorAt(1, QtGui.QColor(125, 125, 200, 180))
    window.setBackgroundGradient(grad)

    button = MyWidgets.RoundedButton(window, "Close")
    button.resize(60, 40)
    button.move(window.width() - 80, 20)
    button.setDarkStyle()
    button.setStrokeColor(QtGui.QColor(200, 200, 200, 50))
    button.clicked.connect(window.close)
    window.show()

    app.exec_()