import os
from pathlib import Path 
from PyQt5 import QtCore, QtGui, QtWidgets 

annotations = []

def abs(x):
    if x < 0: return -x
    else: return x

class ImageBoxLabel(QtWidgets.QLabel):
    def __init__(self, parent):
        super().__init__(parent)
        self.setMouseTracking(True)

        # Qlabel to show selected area
        self.roi = QtWidgets.QLabel(self)
        # scale factor representing how many times smaller the display image is
        self.scale_factor = 1
        # click begin and end coordinates
        self.click_begin = []
        self.click_end = []
        # click flag, set true while mouse is being pressed
        self.click_in_progress = False

        # this is the (x, y, width, height) data, properly scaled, to be outputed
        self.bounding_rect = []

        # image filename
        self.filename = ''

        # callback function
        self.onMouseReleaseFunc = (lambda: print('mouse release func not assigned'))

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

        self.click_end = [e.x(), e.y()]

        self.click_begin = [f / self.scale_factor for f in self.click_begin]
        self.click_end = [f / self.scale_factor for f in self.click_end]

        x = int(min(self.click_begin[0], self.click_end[0]))
        y = int(min(self.click_begin[1], self.click_end[1]))
        width = int(abs(self.click_begin[0] - self.click_end[0]))
        height = int(abs(self.click_begin[1] - self.click_end[1]))

        self.bounding_rect = [x, y, width, height]

        if width != 0 and height != 0:
            annotations.append([self.filename])
            annotations[-1].append(1)
            annotations[-1] += self.bounding_rect
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

        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave.triggered.connect(lambda: self.saveToFile())

        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(lambda: self.saveAndQuit())


        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionSave)
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
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))


    def saveToFile(self):
        with open(self.imageDir + '/annotation.dat', 'w') as f:
            for annotation in annotations:
                for part in annotation:
                    f.write(str(part))
                    f.write(' ')
                f.write('\n')
    
    def saveAndQuit(self):
        self.saveToFile()
        quit()


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
        self.label.onMouseRelease(lambda: self.showImage(imageIdx + 1))
        # get relative filepath
        self.label.filename = self.imagePaths[imageIdx][len(self.imageDir)+1:]

        og_height = px.height()
        og_width = px.width()

        if og_width > og_height and og_width > 500:
            # scale width
            px = px.scaledToWidth(500)
            self.label.scale_factor = (px.width() / og_width)
        elif og_height >= og_width and og_height > 500:
            #scale height
            px = px.scaledToHeight(500)
            self.label.scale_factor = (px.height() / og_height)



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






