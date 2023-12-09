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
        self._search_page_view = []

        # keep track of page number
        self._page_number = 0

        # set layout of window
        outer_layout = Qtw.QVBoxLayout()
        self.setLayout(outer_layout)

        # set layout for buttons
        buttons_layout = Qtw.QHBoxLayout()
        outer_layout.addLayout(buttons_layout)

        # create stacked layout for different windows
        self._stacked = Qtw.QStackedLayout()
        outer_layout.addLayout(self._stacked)

        # call video gui
        self.video_gui()

        # call url gui
        self.url_gui()

        # call sub gui
        self.sub_gui()

        # button to switch to url download
        self._url_gui_button = Qtw.QPushButton("Download")
        self._url_gui_button.setFixedHeight(45)
        self._url_gui_button.setFont(Qtg.QFont("Times", 20))
        self._url_gui_button.clicked.connect(self.switch_to_url)

        # button to switch to search
        self._search_button = Qtw.QPushButton("Search")
        self._search_button.setFixedHeight(45)
        self._search_button.setFont(Qtg.QFont("Times", 20))
        self._search_button.clicked.connect(self.switch_to_search)

        # dropdown menu to change max resolution
        self._resolution = 720
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
        buttons_layout.addWidget(self._search_button)
        buttons_layout.addWidget(self._url_gui_button)
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
        url_gui = Qtw.QWidget()

        # create layout of widget
        layout = Qtw.QVBoxLayout()

        # create input box for video url
        self._url_box = Qtw.QLineEdit()
        self._url_box.setPlaceholderText("Insert URL")

        # create download button
        download_button = Qtw.QPushButton("Download")
        download_button.clicked.connect(self.on_click)

        # add widget to layout and adjust it to the top of the widget
        layout.addWidget(self._url_box)
        layout.addWidget(download_button,
                         alignment=Qtc.Qt.Alignment(Qtc.Qt.AlignTop))

        # add layout to page and add it to stackedLayout
        url_gui.setLayout(layout)
        self._stacked.addWidget(url_gui)

    def video_gui(self):
        """Arrange the video browse page."""
        video_gui = Qtw.QWidget()

        # create outer layout for page
        video_outer_layout = Qtw.QVBoxLayout()
        video_gui.setLayout(video_outer_layout)

        # create layouts for each element of page
        # (search line, videos, and page buttons)
        inner_layer1 = Qtw.QHBoxLayout()
        self._inner_layer2 = Qtw.QVBoxLayout()
        self._inner_layer3 = Qtw.QHBoxLayout()

        # create search box
        self._search_box = Qtw.QLineEdit()
        self._search_box.setPlaceholderText("Search")

        # create search button
        search_button = Qtw.QPushButton("Go")
        search_button.clicked.connect(self.search_click)

        # add widgets to first layer
        inner_layer1.addWidget(self._search_box)
        inner_layer1.addWidget(search_button)

        # adjusts first inner layer to the top of the layout
        inner_layer1.setAlignment(Qtc.Qt.AlignTop)

        # add layouts to page
        video_outer_layout.addLayout(inner_layer1, 0)
        video_outer_layout.addLayout(self._inner_layer2, 9)
        video_outer_layout.addLayout(self._inner_layer3, 1)

        # add page to stackedLayout
        self._stacked.addWidget(video_gui)

    def sub_gui(self):
        """Arrange the subscribed channels page."""
        def append_file(string, file_list):
            """Appends a string to the next line of a file."""
            if pytube_code.check_channel_or_playlist_url(string):
                file_list.append("\n" + string)
                with open(os.pardir + "/YouTube-Downloads/programInfo.txt",
                          'w', encoding="utf-8") as f_hand:
                    f_hand.writelines(file_list)
                self.clear_window(self._sub_layout)
                for i in range(0, len(program_info)):
                    if i == 0:
                        sub_label = Qtw.QLabel("Subscribed Channels:\n")
                        sub_label.setFont(Qtg.QFont("Times", 30))
                        self._sub_layout.addWidget(
                            sub_label, 1, Qtc.Qt.Alignment(Qtc.Qt.AlignTop))
                    else:
                        channel_label = Qtw.QLabel(program_info[i])
                        channel_label.setFont(Qtg.QFont("Times", 15))
                        self._sub_layout.addWidget(
                            channel_label, 1,
                            Qtc.Qt.Alignment(Qtc.Qt.AlignTop))

        sub_gui = Qtw.QWidget()

        self._sub_layout = Qtw.QVBoxLayout()
        sub_gui.setLayout(self._sub_layout)

        with open(os.pardir + "/YouTube-Downloads/programInfo.txt",
                  'r') as f_hand:
            program_info = f_hand.readlines()
            f_hand.close()

        for i in range(0, len(program_info)):
            if i == 0:
                sub_label = Qtw.QLabel("Subscribed Channels:\n")
                sub_label.setFont(Qtg.QFont("Times", 30))
                self._sub_layout.addWidget(sub_label, 1,
                                           Qtc.Qt.Alignment(Qtc.Qt.AlignTop))
            else:
                channel_label = Qtw.QLabel(program_info[i])
                channel_label.setFont(Qtg.QFont("Times", 15))
                self._sub_layout.addWidget(channel_label, 1,
                                           Qtc.Qt.Alignment(Qtc.Qt.AlignTop))

        bottom_label = Qtw.QHBoxLayout()
        channel_box = Qtw.QLineEdit()
        channel_box.setPlaceholderText("Type channel URL here...")
        channel_button = Qtw.QPushButton("Add Channel")
        text = channel_box.text()
        channel_button.clicked.connect(lambda: append_file(text, program_info))
        bottom_label.addWidget(channel_box)
        bottom_label.addWidget(channel_button)
        self._sub_layout.addLayout(bottom_label)

        self._stacked.addWidget(sub_gui)

    def on_click(self):
        """Perform the download pytube function."""
        if self._url_box.text() != "":
            pytube_code.download_link(self._url_box.text(), self.resolution)

    def search_click(self):
        """Create sorted list and shows them on search page"""
        if self._search_box.text() != "":
            search_list = pytube.Search(self._search_box.text()).results
            self.search_page_view = self.page_view_list(search_list)
            self.show_videos(self.search_page_view)

    def show_videos(self, organized_search_list):
        """Show videos on search page when clicking go"""
        if self._inner_layer2.count() > 0:
            self.clear_window(self._inner_layer2)
        for video in organized_search_list[self._page_number]:
            time = self.get_time(video.length)
            button = Qtw.QPushButton(f"     {video.title}\n\n     "
                                     f"Created by: {video.author}\n\n   "
                                     f"  Length: {time[0]}:{time[1]}")
            button.setFont(Qtg.QFont("Times", 20))
            pixmap = Qtg.QPixmap()
            pixmap.loadFromData(requests.get(video.thumbnail_url,
                                             timeout=5).content)
            button.setIcon(Qtg.QIcon(pixmap))
            button.setIconSize(Qtc.QSize(400, 235))
            button.setStyleSheet("text-align:left;")
            url = video.watch_url
            button.clicked.connect(lambda:
                                   pytube_code.download_link(url,
                                                             self._resolution))
            button.setMinimumSize(0, 250)
            self._inner_layer2.addWidget(button, 1,
                                         Qtc.Qt.Alignment(Qtc.Qt.AlignTop))
        prev_button = Qtw.QPushButton("Previous")
        prev_button.clicked.connect(self.previous_button)
        nxt_button = Qtw.QPushButton("Next")
        nxt_button.clicked.connect(self.next_button)
        self.clear_window(self._inner_layer3)
        if 0 < self._page_number < len(organized_search_list) - 1:
            self._inner_layer3.addWidget(prev_button)
            self._inner_layer3.addWidget(nxt_button)
        if self._page_number == 0:
            self._inner_layer3.addWidget(nxt_button)
        if self._page_number == len(organized_search_list) - 1:
            self._inner_layer3.addWidget(prev_button)

    def next_button(self):
        """Next button when searching through videos"""
        self._page_number += 1
        self.show_videos(self.search_page_view)

    def previous_button(self):
        """Back button when searching through videos"""
        self._page_number -= 1
        self.show_videos(self.search_page_view)

    def set_res(self, res):
        """Set resolution download for videos"""
        self._resolution = res

    def switch_to_subscribed(self):
        """Load subscribed channels page."""
        self._stacked.setCurrentIndex(2)

    def switch_to_url(self):
        """Load video browse page."""
        self._stacked.setCurrentIndex(1)

    def switch_to_search(self):
        """Load search and download page."""
        self._stacked.setCurrentIndex(0)

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
        if platform in ("Linux", "Linux2"):
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
        """Create sorted list of video objects for show_videos to
        reference from"""
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
        """
        Get time in minutes and seconds
        :param seconds: int
        :return: minute: int, sec: int
        """
        minute = seconds // 60
        sec = seconds % 60
        return minute, sec


def fetch_updates():
    """Fetch new videos from channels we are subscribed to"""
    try:
        f_hand = open(os.pardir + "/YouTube-Downloads/programInfo.txt", 'r',
                      encoding="utf-8")
        program_info = f_hand.readlines()
    except FileNotFoundError:
        if not os.path.exists(os.pardir + "/YouTube-Downloads/"):
            os.makedirs(os.pardir + "/YouTube-Downloads/")
        f_hand = open(os.pardir + "/YouTube-Downloads/programInfo.txt", 'x',
                      encoding="utf-8")
        program_info = [date.today().ctime() + "\n"]
        f_hand.writelines(program_info)
    if program_info[0] != date.today().ctime() + "\n":
        print("Fetching updates!")
        for i in range(1, len(program_info)):
            pytube_code.download_link(program_info[i], 720)
    f_hand.close()


def update_date():
    """Update date in txt file for fetching_updates """
    with open(os.pardir + "/YouTube-Downloads/programInfo.txt", 'r') as f_hand:
        program_info = f_hand.readlines()
    program_info[0] = date.today().ctime() + "\n"
    with open(os.pardir + "/YouTube-Downloads/programInfo.txt", 'w',
              encoding="utf-8") as f_hand:
        f_hand.writelines(program_info)
        f_hand.close()
    app.exec_()


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    fetch_updates()
    window = Window()
    window.show()
    sys.exit(update_date())
