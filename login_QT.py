import os
import sys
import time

import requests
import configparser

from launcher_QT import MainPage
from circle import CircularProgress
from multiprocessing import Process
from caretaker.camera_show import take_photo

from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QSizeGrip

from qt_login_interface import Ui_MainWindow
from ui_splash_screen import Ui_SplashScreen

counter = 0

config = configparser.ConfigParser()
config.read('config.ini')


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
        self.version.setText('v1.2.5')

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.setGraphicsEffect(self.shadow)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)
        self.show()

        # иконка + название
        self.setWindowIcon(QtGui.QIcon('qt_icons/codesandbox.svg'))
        self.setWindowTitle('Loading')

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
        self.main_page = MainPage()

        # удаление рамок
        self.setWindowFlags(Qt.FramelessWindowHint)

        # эффект тени
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))
        self.centralwidget.setGraphicsEffect(self.shadow)

        # иконка + название
        self.setWindowIcon(QtGui.QIcon('qt_icons/codesandbox.svg'))
        self.setWindowTitle('Dante')

        # масштабирование
        QSizeGrip(self.frame_8)

        # сворачивание окна
        self.minimize_window_button.clicked.connect(lambda: self.showMinimized())

        # закрытие окна
        self.close_window_button.clicked.connect(lambda: self.close())

        # вкл/выкл полноэкранный режим
        self.restore_window_button.clicked.connect(self.restore_or_maximize_window)

        # перетаскивание окна
        self.frame_5.mouseMoveEvent = self.move_window

        # кнопка входа
        self.submit_btn.clicked.connect(self.login_btn)

    def login_btn(self):
        login = self.login_edit.text()
        password = self.password_edit.text()
        check_account = requests.get("https://sab.purpleglass.ru/api/launcher-api/v1/accounts",
                                     params={"login": login, "password": password}).json()
        if check_account.get("code") == 4:
            pst = requests.post("https://sab.purpleglass.ru/api/launcher-api/v1/accounts",
                                params={"login": login, "password": password}).json()
            config['DEFAULT'] = {'login': login,
                                 'password': password,
                                 'token': pst["token"],
                                 'id': pst['id']}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        else:
            config['DEFAULT'] = {'login': login,
                                 'password': password,
                                 'token': check_account["token"],
                                 'id': check_account['id']}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
        self.main_page.show()
        self.main_page.refresh_info()
        self.close()

    def caretaker(self):
        try:
            err = take_photo('Take photo - spacebar. Esc - exit', 'caretaker/face.jpg', False)
            if err == 'фото не сделали':
                self.error_label.setText('Вы не сделали фото')

            else:
                url = 'https://sab.purpleglass.ru/api/launcher-api/v1/photos'
                files = {'file': ('face.jpg', open('caretaker/face.jpg', 'rb'))}

                response = requests.get(url, files=files).json()
                if response.get('code') == 16:
                    self.error_label.setText('Не найдено соответствий')
                else:
                    config['DEFAULT'] = {'login': response['login'],
                                         'password': response['password'],
                                         'token': response["token"],
                                         'id': response['id']}
                    with open('config.ini', 'w') as configfile:
                        config.write(configfile)
                    self.main_page.show()
                    self.main_page.refresh_info()
                    self.close()
        except Exception as ex:
            print(ex)

    def move_window(self, event):
        if not self.isMaximized():
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.restore_window_button.setIcon(QtGui.QIcon('qt_icons/maximize-2.svg'))
        else:
            self.showMaximized()
            self.restore_window_button.setIcon(QtGui.QIcon('qt_icons/minimize-2.svg'))


if __name__ == '__main__':
    process = Process(target=progress)
    process.start()
    process.join()
    app = QApplication(sys.argv)
    window = LoginPage()
    window.show()
    sys.exit(app.exec_())
