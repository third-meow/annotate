import os
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets

def abs(x):
    if x < 0: return -x
    else:
        return x

class ImageBoxLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)

        self.onMouseReleaseFunc = (lambda: print('mouse release func not assigned'))

        self.setMouseTracking(True)

        self.click_begin = []
        self.click_in_progress = False
        self.click_end = []

        self.roi = QtWidgets.QLabel(self)

    def mousePressEvent(self, e):
        self.roi = QtWidgets.QLabel(self)
        self.click_in_progress = True
        self.click_begin = [e.x(), e.y()]

    def mouseMoveEvent(self, e):
        if (self.click_in_progress):
            box_x = min(e.x(), self.click_begin[0])
            box_y = min(e.y(), self.click_begin[1])
            box_width = abs(e.x() - self.click_begin[0])
            box_height = abs(e.y() - self.click_begin[1])

            self.roi.setGeometry(box_x, box_y, box_width, box_height)
            self.roi.setStyleSheet("""background-color: rgba(102, 255, 153, 0.6)""")
            self.roi.show()

    def onMouseRelease(self, func):
        self.onMouseReleaseFunc = func

    def mouseReleaseEvent(self, e):
        self.click_in_progress = False
        self.roi.hide()
        self.onMouseReleaseFunc()

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        self.imageDir = ''
        self.imagePaths = []

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(540, 540)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = ImageBoxLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 0, 0))
        self.label.setObjectName("label")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 540, 24))
        self.menubar.setObjectName("menubar")
        self.menubar.setStyleSheet("""background-color: #D0D0E1; border-bottom: 1px solid #28283E""")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(lambda: self.showFileDialog())

        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(lambda: quit())

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)

        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.showFileDialog()
        self.showImage(0)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Annotate"))
        self.label.setText(_translate("MainWindow", ""))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))


    def showFileDialog(self):
        self.imageDir = \
            QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, 'Open Image Dir', '/home')
        self.genImageList()

    def genImageList(self):
        pathlist_png = Path(self.imageDir).glob('**/*.png')
        for filename in pathlist_png:
            self.imagePaths.append(str(filename))

        pathlist_jpg = Path(self.imageDir).glob('**/*.jpg')
        for filename in pathlist_jpg:
            self.imagePaths.append(str(filename))

    def showImage(self, imageIdx):
        try:
            px = QtGui.QPixmap(self.imagePaths[imageIdx])
        except IndexError:
            quit()
        px = px.scaled(200, 200)
        self.label.onMouseRelease(lambda: self.showImage(imageIdx + 1))
        self.label.setPixmap(px)
        self.label.adjustSize()
        self.label.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())






