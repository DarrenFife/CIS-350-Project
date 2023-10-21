import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as Qtg
import PyQt5.QtCore as Qtc
import sys


class Window(Qtw.QWidget):
    def __init__(self):
        super().__init__()

        # set window title
        self.setWindowTitle("Pytube Video Player")

        # set window geometry
        self.resize(1000, 1000)

        # center screen
        self.center()

        # set layout of window
        layout = Qtw.QVBoxLayout()
        self.setLayout(layout)

        # create stacked layout for different windows
        self.stacked = Qtw.QStackedLayout()

        # call video gui
        self.video_gui()

        # call url gui
        self.url_gui()

        # create combo box to switch between options
        self.combo_box = Qtw.QComboBox()
        self.combo_box.addItems(["Search", "Download"])
        self.combo_box.activated.connect(self.switch)

        # add the widgets
        layout.addWidget(self.combo_box)
        layout.addLayout(self.stacked)

    def center(self):
        application = self.frameGeometry()
        center = Qtw.QDesktopWidget().availableGeometry().center()
        application.moveCenter(center)
        self.move(application.topLeft())

    def url_gui(self):
        url_gui = Qtw.QWidget()
        layout = Qtw.QVBoxLayout()

        url_box = Qtw.QLineEdit()
        url_box.setPlaceholderText("Insert URL")

        download_button = Qtw.QPushButton("Download")

        layout.addWidget(url_box)
        layout.addWidget(download_button, alignment=Qtc.Qt.Alignment(Qtc.Qt.AlignTop))

        url_gui.setLayout(layout)
        self.stacked.addWidget(url_gui)

    def video_gui(self):
        video_gui = Qtw.QWidget()
        layout = Qtw.QVBoxLayout()
        inner_layer1 = Qtw.QHBoxLayout()
        inner_layer2 = Qtw.QVBoxLayout()

        search_box = Qtw.QLineEdit()
        search_box.setPlaceholderText("Stuff")

        search_button = Qtw.QPushButton("Download")

        label = Qtw.QLabel("Hi")

        inner_layer1.addWidget(search_box)
        inner_layer1.addWidget(search_button)
        inner_layer1.setAlignment(Qtc.Qt.AlignTop)

        layout.addLayout(inner_layer1)
        layout.addLayout(inner_layer2)

        video_gui.setLayout(layout)
        self.stacked.addWidget(video_gui)

    def switch(self):
        self.stacked.setCurrentIndex(self.combo_box.currentIndex())


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
