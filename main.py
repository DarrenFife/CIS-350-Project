"""This module is where the GUI and all its elements are created"""
from datetime import date
import os
import sys
from sys import platform
import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as Qtg
import PyQt5.QtCore as Qtc
import pytube
import qdarktheme as qdt
import requests
import pytube_code


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
        self.setFixedSize(1600, 900)

        # center screen
        self.center()

        # dark mode by default
        qdt.setup_theme("dark")

        # keep track of theme
        self._theme_number = 0

        # keep track of organized search list for page view
        self.search_page_view = []

        # keep track of page number
        self.page_number = 0

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

        # call sub gui
        self.sub_gui()

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

        # dropdown menu to change max resolution
        self.resolution = 720
        res_action1 = Qtw.QAction("144p", self)
        res_action2 = Qtw.QAction("240p", self)
        res_action3 = Qtw.QAction("360p", self)
        res_action4 = Qtw.QAction("480p", self)
        res_action5 = Qtw.QAction("720p", self)
        menu_bar = Qtw.QMenuBar()
        menu_bar.setMaximumWidth(385)
        menu_bar.setFont(Qtg.QFont("Times", 20))
        res_menu = menu_bar.addMenu("&Download Resolution")
        res_menu.addAction(res_action1)
        res_action1.triggered.connect(lambda: self.set_res(144))
        res_menu.addAction(res_action2)
        res_action2.triggered.connect(lambda: self.set_res(240))
        res_menu.addAction(res_action3)
        res_action3.triggered.connect(lambda: self.set_res(360))
        res_menu.addAction(res_action4)
        res_action4.triggered.connect(lambda: self.set_res(480))
        res_menu.addAction(res_action5)
        res_action5.triggered.connect(lambda: self.set_res(720))

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

        # button to access subscribed channels
        subscribed_button = Qtw.QPushButton("Subscribed")
        subscribed_button.setFixedHeight(45)
        subscribed_button.setFont(Qtg.QFont("Times", 20))
        subscribed_button.clicked.connect(self.switch_to_subscribed)

        # add the widgets to inner top layer
        buttons_layout.addWidget(menu_bar)
        buttons_layout.addWidget(self.search_button)
        buttons_layout.addWidget(self.url_gui_button)
        buttons_layout.addWidget(theme_button)
        buttons_layout.addWidget(folder_button)
        buttons_layout.addWidget(subscribed_button)

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

        # create layout of widget
        layout = Qtw.QVBoxLayout()

        # create input box for video url
        self.url_box = Qtw.QLineEdit()
        self.url_box.setPlaceholderText("Insert URL")

        # create download button
        download_button = Qtw.QPushButton("Download")
        download_button.clicked.connect(self.on_click)

        # add widget to layout and adjust it to the top of the widget
        layout.addWidget(self.url_box)
        layout.addWidget(download_button,
                         alignment=Qtc.Qt.Alignment(Qtc.Qt.AlignTop))

        # add layout to page and add it to stackedLayout
        url_gui.setLayout(layout)
        self.stacked.addWidget(url_gui)

    def video_gui(self):
        """Arrange the video browse page."""
        video_gui = Qtw.QWidget()

        # create outer layout for page
        video_outer_layout = Qtw.QVBoxLayout()
        video_gui.setLayout(video_outer_layout)

        # create layouts for each element of page
        # (search line, videos, and page buttons))
        inner_layer1 = Qtw.QHBoxLayout()
        self.inner_layer2 = Qtw.QVBoxLayout()
        self.inner_layer3 = Qtw.QHBoxLayout()

        # create search box
        self.search_box = Qtw.QLineEdit()
        self.search_box.setPlaceholderText("Search")

        # create search button
        search_button = Qtw.QPushButton("Go")
        search_button.clicked.connect(self.search_click)

        # add widgets to first layer
        inner_layer1.addWidget(self.search_box)
        inner_layer1.addWidget(search_button)

        # adjusts first inner layer to the top of the layout
        inner_layer1.setAlignment(Qtc.Qt.AlignTop)

        # add layouts to page
        video_outer_layout.addLayout(inner_layer1, 0)
        video_outer_layout.addLayout(self.inner_layer2, 9)
        video_outer_layout.addLayout(self.inner_layer3, 1)

        # add page to stackedLayout
        self.stacked.addWidget(video_gui)

    def sub_gui(self):
        """Arrange the subscribed channels page."""
        def append_file(string, file_list):
            """Appends a string to the next line of a file."""
            if pytube_code.check_channel_or_playlist_url(string):
                file_list.append("\n" + string)
                with open(os.pardir + "/YouTube-Downloads/programInfo.txt",
                          'w') as fhand:
                    fhand.writelines(file_list)
                self.clear_window(self.sub_layout)
                for i in range(0, len(programInfo)):
                    if i == 0:
                        sub_label = Qtw.QLabel("Subscribed Channels:\n")
                        sub_label.setFont(Qtg.QFont("Times", 30))
                        self.sub_layout.addWidget(
                            sub_label, 1, Qtc.Qt.Alignment(Qtc.Qt.AlignTop))
                    else:
                        channel_label = Qtw.QLabel(programInfo[i])
                        channel_label.setFont(Qtg.QFont("Times", 15))
                        self.sub_layout.addWidget(
                            channel_label, 1,
                            Qtc.Qt.Alignment(Qtc.Qt.AlignTop))

        sub_gui = Qtw.QWidget()

        self.sub_layout = Qtw.QVBoxLayout()
        sub_gui.setLayout(self.sub_layout)

        fhand = open(os.pardir + "/YouTube-Downloads/programInfo.txt", 'r')
        programInfo = fhand.readlines()
        fhand.close()

        for i in range(0, len(programInfo)):
            if i == 0:
                sub_label = Qtw.QLabel("Subscribed Channels:\n")
                sub_label.setFont(Qtg.QFont("Times", 30))
                self.sub_layout.addWidget(sub_label, 1,
                                          Qtc.Qt.Alignment(Qtc.Qt.AlignTop))
            else:
                channel_label = Qtw.QLabel(programInfo[i])
                channel_label.setFont(Qtg.QFont("Times", 15))
                self.sub_layout.addWidget(channel_label, 1,
                                          Qtc.Qt.Alignment(Qtc.Qt.AlignTop))

        bottom_label = Qtw.QHBoxLayout()
        channel_box = Qtw.QLineEdit()
        channel_box.setPlaceholderText("Type channel URL here...")
        channel_button = Qtw.QPushButton("Add Channel")
        channel_button.clicked.connect(lambda: append_file(channel_box.
                                                          text(), programInfo))
        bottom_label.addWidget(channel_box)
        bottom_label.addWidget(channel_button)
        self.sub_layout.addLayout(bottom_label)

        self.stacked.addWidget(sub_gui)

    def on_click(self):
        """Perform the download pytube function."""
        if self.url_box.text() != "":
            pytube_code.download_link(self.url_box.text(), self.resolution)

    def search_click(self):
        """Create sorted list and shows them on search page"""
        if self.search_box.text() != "":
            search_list = pytube.Search(self.search_box.text()).results
            self.search_page_view = self.page_view_list(search_list)
            self.show_videos(self.search_page_view)

    def show_videos(self, organized_search_list):
        """Show videos on search page when clicking go"""
        if self.inner_layer2.count() > 0:
            self.clear_window(self.inner_layer2)
        for video in organized_search_list[self.page_number]:
            time = self.get_time(video.length)
            button = Qtw.QPushButton(f"     {video.title}\n\n     "
                                     f"Created by: {video.author}\n\n   "
                                     f"  Length: {time[0]}:{time[1]}")
            button.setFont(Qtg.QFont("Times", 20))
            pixmap = Qtg.QPixmap()
            pixmap.loadFromData(requests.get(video.thumbnail_url, timeout=5).content)
            button.setIcon(Qtg.QIcon(pixmap))
            button.setIconSize(Qtc.QSize(400, 235))
            button.setStyleSheet("text-align:left;")
            url = video.watch_url
            button.clicked.connect(lambda: pytube_code.download_link(url))
            button.setMinimumSize(0, 250)
            self.inner_layer2.addWidget(button, 1,
                                        Qtc.Qt.Alignment(Qtc.Qt.AlignTop))
        prev_button = Qtw.QPushButton("Previous")
        prev_button.clicked.connect(self.previous_button)
        nxt_button = Qtw.QPushButton("Next")
        nxt_button.clicked.connect(self.next_button)
        self.clear_window(self.inner_layer3)
        if 0 < self.page_number < len(organized_search_list) - 1:
            self.inner_layer3.addWidget(prev_button)
            self.inner_layer3.addWidget(nxt_button)
        if self.page_number == 0:
            self.inner_layer3.addWidget(nxt_button)
        if self.page_number == len(organized_search_list) - 1:
            self.inner_layer3.addWidget(prev_button)

    def next_button(self):
        """Next button when searching through videos"""
        self.page_number += 1
        self.show_videos(self.search_page_view)

    def previous_button(self):
        """Back button when searching through videos"""
        self.page_number -= 1
        self.show_videos(self.search_page_view)

    def set_res(self, res):
        """Set resolution download for videos"""
        self.resolution = res

    def switch_to_subscribed(self):
        """Load subscribed channels page."""
        self.stacked.setCurrentIndex(2)

    def switch_to_url(self):
        """Load video browse page."""
        self.stacked.setCurrentIndex(1)

    def switch_to_search(self):
        """Load search and download page."""
        self.stacked.setCurrentIndex(0)

    def switch_theme(self):
        """Toggle button for switching themes"""
        # doing the change twice is required to fully change theme
        if self._theme_number == 0:
            qdt.setup_theme("light")
            qdt.setup_theme("light")
            self._theme_number += 1
        else:
            qdt.setup_theme("dark")
            qdt.setup_theme("dark")
            self._theme_number -= 1

    def access_folder(self):
        """Access folder from within the app"""
        if platform == "linux" or platform == "linux2":
            # linux
            path = os.pardir + "/YouTube-Downloads/"
            Qtw.QFileDialog.getOpenFileName(self, directory=path)
        elif platform == "darwin":
            # OS X
            print("OS X detected")
        elif platform == "win32":
            # Windows...
            print("Windows detected lol")
        os.system("explorer.exe " + os.pardir)

    def clear_window(self, layout):
        """Clears the videos from search page
        once we don't need them anymore"""
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if isinstance(item, Qtw.QWidgetItem):
                item.widget().close()
            layout.removeItem(item)

    def page_view_list(self, lov):
        """Create sorted list of video objects for show_videos to reference from"""
        num = 0
        if len(lov) % 3 == 0:
            num = len(lov) // 3
        else:
            num = (len(lov) // 3) + 1
        new_lst = [[] for i in range(num)]
        for i in new_lst:
            for j in range(3):
                if len(lov) >= 3:
                    i.append(lov[j])
                elif len(lov) > 0:
                    for x in lov:
                        i.append(x)
                    break
                else:
                    break
            lov = lov[3:]
        return new_lst

    def get_time(self, seconds):
        min = seconds // 60
        sec = seconds % 60
        return min, sec


def fetch_updates():
    try:
        fhand = open(os.pardir + "/YouTube-Downloads/programInfo.txt", 'r')
        programInfo = fhand.readlines()
    except:
        if not os.path.exists(os.pardir + "/YouTube-Downloads/"):
            os.makedirs(os.pardir + "/YouTube-Downloads/")
        fhand = open(os.pardir + "/YouTube-Downloads/programInfo.txt", 'x')
        programInfo = [date.today().ctime() + "\n"]
        fhand.writelines(programInfo)
    if programInfo[0] != date.today().ctime() + "\n":
        print("Fetching updates!")
        for i in range(1, len(programInfo)):
            pytube_code.download_link(programInfo[i], 720)
    fhand.close()


def update_date():
    with open(os.pardir + "/YouTube-Downloads/programInfo.txt", 'r') as fhand:
        programInfo = fhand.readlines()
    programInfo[0] = date.today().ctime() + "\n"
    fhand = open(os.pardir + "/YouTube-Downloads/programInfo.txt", 'w')
    fhand.writelines(programInfo)
    fhand.close()
    app.exec_()


if __name__ == "__main__":
    """Close the window."""
    app = Qtw.QApplication(sys.argv)
    fetch_updates()
    window = Window()
    window.show()
    sys.exit(update_date())
