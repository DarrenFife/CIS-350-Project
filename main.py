import PyQt5.QtWidgets as Qtw
import PyQt5.QtGui as Qtg
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

    def center(self):
        application = self.frameGeometry()
        center = Qtw.QDesktopWidget().availableGeometry().center()
        application.moveCenter(center)
        self.move(application.topLeft())

    def url_gui(self):
        gui = Qtw.QWidget()



    def video_gui(self):
        pass


if __name__ == "__main__":
    app = Qtw.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

