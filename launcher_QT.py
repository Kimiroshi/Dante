import os
import subprocess
import sys

import requests
import webbrowser
import configparser

from PyQt5 import QtGui
from pathlib import Path
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect, QSizeGrip, QLineEdit

from datetime import datetime
from qt_main_interface import Ui_MainWindow
from caretaker.camera_show import take_photo

config = configparser.ConfigParser()
config.read('config.ini')


class MainPage(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.verison_label.setText('Dante v1.2.5')
        self.main_body_contents.setCurrentWidget(self.welcome_page)

        # иконка на главной странице
        cur_time = datetime.now().strftime('%H')
        if 20 > int(cur_time) >= 4:
            self.welcome_label.setPixmap(QtGui.QPixmap("qt_icons/sun.svg"))

        # удаление рамок
        self.setWindowFlags(Qt.FramelessWindowHint)

        # эффект тени
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(50)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 92, 157, 550))
        self.centralwidget.setGraphicsEffect(self.shadow)

        # название
        self.setWindowTitle('Dante')

        # масштабирование
        QSizeGrip(self.size_grip)

        # сворачивание окна
        self.minimize_window_button.clicked.connect(lambda: self.showMinimized())

        # закрытие окна
        self.close_window_button.clicked.connect(lambda: self.close())
        self.exit_button.clicked.connect(lambda: self.close())

        # вкл/выкл полноэкранный режим
        self.restore_window_button.clicked.connect(self.restore_or_maximize_window)

        # перетаскивание окна
        self.header_frame.mouseMoveEvent = self.move_window

        # вкл/выкл sidebar
        self.open_close_side_bar.clicked.connect(self.slide_menu)

        # кнопка камеры
        self.camera.clicked.connect(self.camera_btn)

        # страницы
        self.clicker_button.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.clicker_page))
        self.life_button.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.life_page))
        self.dino_button.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.dino_page))
        self.clicker_button_2.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.clicker_page))
        self.life_button_2.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.life_page))
        self.dino_button_2.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.dino_page))
        self.authors_button.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.authors_page))
        self.settings.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.settings_page))
        self.settings_button.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.settings_page))
        self.nums_button.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.nums_page))
        self.nums_button_2.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.nums_page))
        self.ping_pong_button.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.ping_pong_page))
        self.ping_pong_button_2.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.ping_pong_page))
        self.maze_button.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.maze_page))
        self.maze_button_2.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.maze_page))
        self.aim_button.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.page_3))
        self.aim_button_2.clicked.connect(lambda: self.main_body_contents.setCurrentWidget(self.page_3))

        # гиты авторов
        self.kimiroshi_button.clicked.connect(lambda: webbrowser.open('https://github.com/Kimiroshi', new=0))
        self.dezcode_.clicked.connect(lambda: webbrowser.open('https://github.com/ver-tuego', new=0))
        self.dima123kr.clicked.connect(lambda: webbrowser.open('https://github.com/Dima123kr', new=0))

        # игры
        self.clicker_play.clicked.connect(
            lambda: subprocess.Popen(['emoji_clicker.py'], shell=True, creationflags=subprocess.SW_HIDE))
        self.nums_play.clicked.connect(
            lambda: subprocess.Popen(['2048.py'], shell=True, creationflags=subprocess.SW_HIDE))
        self.life_play.clicked.connect(
            lambda: subprocess.Popen(['life.py'], shell=True, creationflags=subprocess.SW_HIDE))
        self.dino_play.clicked.connect(
            lambda: subprocess.Popen(['dino.py'], shell=True, creationflags=subprocess.SW_HIDE))
        self.ping_pong_play.clicked.connect(
            lambda: subprocess.Popen(['ping_pong.py'], shell=True, creationflags=subprocess.SW_HIDE))
        self.maze_play.clicked.connect(
            lambda: subprocess.Popen(['maze.py'], shell=True, creationflags=subprocess.SW_HIDE))
        self.aim_play.clicked.connect(
            lambda: subprocess.Popen(['aim.py'], shell=True, creationflags=subprocess.SW_HIDE))

        # показать пароль
        self.show_password.clicked.connect(self.hide_btn)
        self.icon = QtGui.QIcon()
        self.icon.addPixmap(QtGui.QPixmap("qt_icons/eye.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cross_icon = QtGui.QIcon()
        self.cross_icon.addPixmap(QtGui.QPixmap("qt_icons/eye-off.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.checked = QtGui.QIcon()

        # поиск
        self.search.clicked.connect(self.search_btn)

    def move_window(self, event):
        if not self.isMaximized():
            if event.buttons() == Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.clickPosition)
                self.clickPosition = event.globalPos()
                event.accept()

    def restore_or_maximize_window(self):
        if self.isMaximized():
            self.showNormal()
            self.restore_window_button.setIcon(QtGui.QIcon('qt_icons/maximize-2.svg'))
        else:
            self.showMaximized()
            self.restore_window_button.setIcon(QtGui.QIcon('qt_icons/minimize-2.svg'))

    def mousePressEvent(self, event):
        self.clickPosition = event.globalPos()

    def camera_btn(self):
        config.read('config.ini')
        take_photo('Make etalon photo. Take photo - spacebar. Esc - exit', 'caretaker/etalon.jpg', True)
        if Path('caretaker/etalon.jpg').exists():
            url = 'https://sab.purpleglass.ru/api/launcher-api/v1/photos'
            files = {'file': ('etalon.jpg', open('caretaker/etalon.jpg', 'rb'))}

            response = requests.post(url, files=files, params={"token": config['DEFAULT']['token']})
            print(response.text)
            print(config['DEFAULT']['token'])
            os.remove('caretaker/face.jpg')

    # анимация sidebar`a
    def slide_menu(self):
        width = self.slide_menu_container.width()
        if width == 0:
            to_width = 200
            self.open_close_side_bar.setIcon(QtGui.QIcon('qt_icons/chevron-left.svg'))
        else:
            to_width = 0
            self.open_close_side_bar.setIcon(QtGui.QIcon('qt_icons/align-left.svg'))
        self.animation = QPropertyAnimation(self.slide_menu_container, b'maximumWidth')
        self.animation.setDuration(850)
        self.animation.setStartValue(width)
        self.animation.setEndValue(to_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()

    def hide_btn(self):
        # Проверка на то, скрыт ли пароль
        if self.user_password.echoMode() == 2:
            # Показать пароль
            self.user_password.setEchoMode(QLineEdit.Normal)
            self.show_password.setIcon(self.cross_icon)
            self.show_password.setIconSize(QtCore.QSize(29, 30))
        else:
            # Скрыть пароль
            self.user_password.setEchoMode(QLineEdit.Password)
            self.show_password.setIcon(self.icon)
            self.show_password.setIconSize(QtCore.QSize(29, 30))

    def search_btn(self):
        line = self.search_edit.text().lower().rstrip().lstrip()
        if line == 'настройки':
            self.main_body_contents.setCurrentWidget(self.settings_page)
            self.search_edit.setText('')
        elif line == 'кликер':
            self.main_body_contents.setCurrentWidget(self.clicker_page)
            self.search_edit.setText('')
        elif line == 'динозаврик':
            self.main_body_contents.setCurrentWidget(self.dino_page)
            self.search_edit.setText('')
        elif line == 'жизнь':
            self.main_body_contents.setCurrentWidget(self.life_page)
            self.search_edit.setText('')
        elif line == 'авторы':
            self.main_body_contents.setCurrentWidget(self.authors_page)
            self.search_edit.setText('')
        elif line == '2048':
            self.main_body_contents.setCurrentWidget(self.nums_page)
            self.search_edit.setText('')
        elif line == 'пинг-понг':
            self.main_body_contents.setCurrentWidget(self.ping_pong_page)
            self.search_edit.setText('')
        elif line == 'лабиринт':
            self.main_body_contents.setCurrentWidget(self.maze_page)
            self.search_edit.setText('')

    def refresh_info(self):
        config.read('config.ini')
        self.user_password.setText(config['DEFAULT']['password'])
        self.user_login.setText(config['DEFAULT']['login'])