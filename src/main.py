from PyQt5 import QtCore, QtGui, QtWidgets

def abs(x):
    if x < 0:
        return -x
    else:
        return x

class ImageBoxLabel(QtWidgets.QLabel):
    def __init__(self, *args):
        super().__init__(*args)

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


    def mouseReleaseEvent(self, e):
        self.click_in_progress = False
        self.click_end = [e.x(), e.y()]

        box_x = min(self.click_end[0], self.click_begin[0])
        box_y = min(self.click_end[1], self.click_begin[1])
        box_width = abs(self.click_end[0] - self.click_begin[0])
        box_height = abs(self.click_end[1] - self.click_begin[1])

        self.roi.setGeometry(box_x, box_y, box_width, box_height)
        self.roi.setStyleSheet("""background-color: rgba(102, 255, 153, 0.6)""")
        self.roi.show()

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        self.imagePath = '/home/third-meow/datasets/bicycle_images/sandpit/bike.jpg'

        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(540, 540)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = ImageBoxLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 20, 0, 0))
        self.label.setObjectName("label")

        '''
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setGeometry(QtCore.QRect(195, 230, 80, 20))
        self.openButton.setText('Start Here')
        self.openButton.setObjectName("openButton")
        self.openButton.clicked.connect(lambda: self.showFileDialog())
        '''

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


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Annotate"))
        self.label.setText(_translate("MainWindow", ""))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))


    def showFileDialog(self):
        self.imagePath = QtWidgets.QFileDialog.getOpenFileName(directory='/home')[0]
        self.showImage()

    def showImage(self):
        px = QtGui.QPixmap(self.imagePath)
        px = px.scaled(500, 500)
        self.label.setPixmap(px)
        self.label.adjustSize()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())






