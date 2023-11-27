import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as Qtg
import PyQt5.QtCore as Qtc
import pytube
import qdarktheme as qdt
import sys
import pytube_code
import os
import requests


class Window(Qtw.QWidget):
    """The main program window.

    Keyword arguments:
    """
    def __init__(self):
        """Initialize the main window given default parameters."""
        super().__init__()

        # set window title
        self.setWindowTitle("Pytube Video Player")

        # set window geometry
        self.resize(1600, 900)

        # center screen
        self.center()

        # dark mode by default
        qdt.setup_theme("dark")

        # keep track of theme
        self._theme_number = 0

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
        self.url_gui_button.setFixedHeight(45)
        self.url_gui_button.setFont(Qtg.QFont("Times", 20))
        self.url_gui_button.clicked.connect(self.switch_to_url)

        # button to switch to search
        self.search_button = Qtw.QPushButton("Search")
        self.search_button.setFixedHeight(45)
        self.search_button.setFont(Qtg.QFont("Times", 20))
        self.search_button.clicked.connect(self.switch_to_search)

        # button to switch themes
        theme_button = Qtw.QPushButton("Themes")
        theme_button.setFixedHeight(45)
        theme_button.setFont(Qtg.QFont("Times", 20))
        theme_button.clicked.connect(self.switch_theme)

        # button to access video folder
        folder_button = Qtw.QPushButton("Folder")
        folder_button.setFixedHeight(45)
        folder_button.setFont(Qtg.QFont("Times", 20))
        folder_button.clicked.connect(self.access_folder)

        # add the widgets to inner top layer
        buttons_layout.addWidget(self.search_button)
        buttons_layout.addWidget(self.url_gui_button)
        buttons_layout.addWidget(theme_button)
        buttons_layout.addWidget(folder_button)

    def center(self):
        """Define the center of the screen."""
        application = self.frameGeometry()
        center = Qtw.QDesktopWidget().availableGeometry().center()
        application.moveCenter(center)
        self.move(application.topLeft())

    def url_gui(self):
        """Arrange the search and download page."""
        # TODO: Perhaps should change to self instead of url_gui?
        url_gui = Qtw.QWidget()

        layout = Qtw.QVBoxLayout()

        self.url_box = Qtw.QLineEdit()
        self.url_box.setPlaceholderText("Insert URL")

        download_button = Qtw.QPushButton("Download")
        download_button.clicked.connect(self.on_click)

        layout.addWidget(self.url_box)
        layout.addWidget(download_button,
                         alignment=Qtc.Qt.Alignment(Qtc.Qt.AlignTop))

        url_gui.setLayout(layout)
        self.stacked.addWidget(url_gui)

    def video_gui(self):
        """Arrange the video browse page."""
        video_gui = Qtw.QWidget()

        video_outer_layout = Qtw.QVBoxLayout()
        video_gui.setLayout(video_outer_layout)

        inner_layer1 = Qtw.QHBoxLayout()
        self.inner_layer2 = Qtw.QVBoxLayout()

        self.search_box = Qtw.QLineEdit()
        self.search_box.setPlaceholderText("Search")

        search_button = Qtw.QPushButton("Go")
        search_button.clicked.connect(self.search_click)

        inner_layer1.addWidget(self.search_box)
        inner_layer1.addWidget(search_button)

        inner_layer1.setAlignment(Qtc.Qt.AlignTop)

        video_outer_layout.addLayout(inner_layer1, 0)
        video_outer_layout.addLayout(self.inner_layer2, 10)

        self.stacked.addWidget(video_gui)

    def on_click(self):
        """Perform the download pytube function."""
        if self.url_box.text() != "":
            pytube_code.download_link(self.url_box.text())

    def search_click(self):
        """Arrange top 3 search results as buttons."""
        if self.search_box.text() != "":
            vid_list = pytube.Search(self.search_box.text())
            for i in range(3):
                video = vid_list.results[i]
                button = Qtw.QPushButton(video.title)
                button.setFont(Qtg.QFont("Times", 12))
                pixmap = Qtg.QPixmap()
                pixmap.loadFromData(requests.get(video.thumbnail_url).content)
                button.setIcon(Qtg.QIcon(pixmap))
                button.setIconSize(Qtc.QSize(450, 150))
                url = video.watch_url
                button.clicked.connect(lambda: pytube_code.download_link(url))
                button.setMinimumSize(0, 250)
                self.inner_layer2.addWidget(button, 1,
                                            Qtc.Qt.Alignment(Qtc.Qt.AlignTop))

    def switch_to_url(self):
        """Load video browse page."""
        self.stacked.setCurrentIndex(1)

    def switch_to_search(self):
        """Load search and download page."""
        self.stacked.setCurrentIndex(0)

    def switch_theme(self):
        if self._theme_number == 0:
            qdt.setup_theme("light")
            qdt.setup_theme("light")
            self._theme_number += 1
        else:
            qdt.setup_theme("dark")
            qdt.setup_theme("dark")
            self._theme_number -= 1

    def access_folder(self):
        path = os.pardir + "/YouTube-Downloads/"
        Qtw.QFileDialog.getOpenFileName(self, directory=path)


if __name__ == "__main__":
    """Close the window."""
    app = Qtw.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
