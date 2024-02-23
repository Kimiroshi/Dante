import sys
from pathlib import Path
from circle import CircularProgress
from multiprocessing import Process
from caretaker.camera_show import take_photo

from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect

from qt_login_interface import Ui_MainWindow
from ui_splash_screen import Ui_SplashScreen


counter = 0


def progress():
    app = QApplication(sys.argv)
    window = SplashScreen()
    window.show()
    sys.exit(app.exec_())


class SplashScreen(QMainWindow, Ui_SplashScreen):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.progress = CircularProgress()
        self.progress.width = 270
        self.progress.height = 270
        self.progress.value = 0
        self.progress.setFixedSize(self.progress.width, self.progress.height)
        self.progress.move(15, 15)
        self.progress.add_shadow(True)
        self.progress.font_size = 40
        self.progress.bg_color = QColor(68, 71, 90, 140)
        self.progress.setParent(self.centralwidget)
        self.progress.show()

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.setGraphicsEffect(self.shadow)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(80)
        self.show()

    def update(self):
        global counter
        if counter >= 100:
            self.timer.stop()
            self.close()
        self.progress.set_value(counter)
        self.progress.repaint()
        counter += 1


class LoginPage(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.caretaker_btn.clicked.connect(self.caretaker)

    def caretaker(self):
        if Path('caretaker/etalon.jpg').exists():
            take_photo('rayan_gosling', 'caretaker/face.jpg', False)
            compare_images('caretaker/etalon.jpg', 'caretaker/face.jpg')
        else:
            take_photo('Make etalon photo', 'caretaker/etalon.jpg', True)


if __name__ == '__main__':
    process = Process(target=progress)
    process.start()
    from caretaker.face_compare import compare_images
    process.join()
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())