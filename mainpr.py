import os
import sys

import requests
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()
        self.mstb = float()

    def getImage(self):
        self.server_address = 'https://static-maps.yandex.ru/v1?'
        self.api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        self.first_coord = float(input('Введите первую координату: ')) # 37.530887
        self.second_coord = float(input('Введите вторую координату: ')) # 55.703118

        self.mstb = float(input('Введите масштаб(значение, приблеженное к 0.005): '))  # 37.530887

        ll_spn = f'll={self.first_coord},{self.second_coord}&spn={self.mstb},{self.mstb}'
        # Готовим запрос.

        map_request = f"{self.server_address}{ll_spn}&apikey={self.api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == 16777239 and self.mstb > 0:
            self.mstb = float(self.mstb) - 0.01
            print(self.mstb)
        if event.key() == 16777238:
            self.mstb = float(self.mstb) + 0.01
            print(self.mstb)
        ll_spn = f'll={self.first_coord},{self.second_coord}&spn={self.mstb},{self.mstb}'
        map_request = f"{self.server_address}{ll_spn}&apikey={self.api_key}"
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())