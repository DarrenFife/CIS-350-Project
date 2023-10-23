import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as Qtg
import PyQt5.QtCore as Qtc
import qdarktheme as qdt
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

        # dark mode by default
        qdt.setup_theme("dark")

        # set layout of window
        outer_layout = Qtw.QVBoxLayout()
        self.setLayout(outer_layout)

        # set layout for buttons
        buttons_layout = Qtw.QHBoxLayout()
        outer_layout.addLayout(buttons_layout)

        # create stacked layout for different windows
        self.stacked = Qtw.QStackedLayout()
        outer_layout.addLayout(self.stacked)

        # call video gui
        self.video_gui()

        # call url gui
        self.url_gui()

        # button to switch to url download
        self.url_gui_button = Qtw.QPushButton("Download")
        self.url_gui_button.clicked.connect(self.switch_to_url)

        # button to switch to search
        self.search_button = Qtw.QPushButton("Search")
        self.search_button.clicked.connect(self.switch_to_search)

        # dark mode button
        dark_mode = Qtw.QPushButton("Dark Mode")
        dark_mode.clicked.connect(self.switch_dark)

        # light mode button
        light_mode = Qtw.QPushButton("Light Mode")
        light_mode.clicked.connect(self.switch_light)

        # add the widgets to inner top layer
        buttons_layout.addWidget(self.search_button)
        buttons_layout.addWidget(self.url_gui_button)
        buttons_layout.addWidget(dark_mode)
        buttons_layout.addWidget(light_mode)

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

        video_outer_layout = Qtw.QVBoxLayout()
        video_gui.setLayout(video_outer_layout)

        inner_layer1 = Qtw.QHBoxLayout()
        inner_layer2 = Qtw.QVBoxLayout()

        search_box = Qtw.QLineEdit()
        search_box.setPlaceholderText("Search")

        search_button = Qtw.QPushButton("Go")
        # search_button.clicked.connect(self.videos)

        inner_layer1.addWidget(search_box)
        inner_layer1.addWidget(search_button)

        inner_layer1.setAlignment(Qtc.Qt.AlignTop)

        button = Qtw.QPushButton("Video1")
        button.setMinimumSize(0, 250)
        inner_layer2.addWidget(button, alignment=Qtc.Qt.Alignment(Qtc.Qt.AlignTop))
        button = Qtw.QPushButton("Video2")
        button.setMinimumSize(0, 250)
        inner_layer2.addWidget(button, alignment=Qtc.Qt.Alignment(Qtc.Qt.AlignTop))
        button = Qtw.QPushButton("Video3")
        button.setMinimumSize(0, 250)
        inner_layer2.addWidget(button, 1, Qtc.Qt.Alignment(Qtc.Qt.AlignTop))

        video_outer_layout.addLayout(inner_layer1, 0)
        video_outer_layout.addLayout(inner_layer2, 10)

        self.stacked.addWidget(video_gui)

    def switch_to_url(self):
        self.stacked.setCurrentIndex(1)

    def switch_to_search(self):
        self.stacked.setCurrentIndex(0)

    def switch_dark(self):
        qdt.setup_theme("dark")

    def switch_light(self):
        qdt.setup_theme("light")


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
