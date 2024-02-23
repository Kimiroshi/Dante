import sys

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from qt_main_interface import Ui_MainWindow
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QSizeGrip


class MainPage(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.verison_label.setText('Dante v0.4.5')

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
        self.setWindowIcon(QtGui.QIcon('qt_icons/book.svg'))
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec_())
