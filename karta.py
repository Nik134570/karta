import sys

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle('Шестая программа')

        self.btn = QPushButton('Сформировать карту', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100, 150)
        self.btn.clicked.connect(self.hello)

        self.label = QLabel(self)
        self.label.setText("Укажите координаты: ")
        self.label.move(30, 30)
        self.name_input1 = QLineEdit(self)
        self.name_input1.move(150, 30)

        self.name_label = QLabel(self)
        self.name_label.setText("Укажите масштаб: ")
        self.name_label.move(45, 90)

        self.name_input2 = QLineEdit(self)
        self.name_input2.move(150, 90)

    def hello(self):
        name1 = self.name_input1.text()
        name2 = self.name_input2.text()
        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

        p = name1.split()
        address_ll = p[0] + "," + p[1]

        search_params = {
            "apikey": api_key,
            "text": "аптека",
            "lang": "ru_RU",
            "ll": address_ll,
            "type": "biz"
        }

        response = requests.get(search_api_server, params=search_params)
        if not response:
            # ...
            pass

        # Преобразуем ответ в json-объект
        json_response = response.json()

        # Получаем первую найденную организацию.
        organization = json_response["features"][0]
        # Название организации.
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        # Адрес организации.
        org_address = organization["properties"]["CompanyMetaData"]["address"]

        # Получаем координаты ответа.
        point = organization["geometry"]["coordinates"]
        org_point = "{0},{1}".format(point[0], point[1])
        delta = name2

        # Собираем параметры для запроса к StaticMapsAPI:
        map_params = {
            # позиционируем карту центром на наш исходный адрес
            "ll": address_ll,
            "spn": ",".join([delta, delta]),
            "l": "map",
            # добавим точку, чтобы указать найденную аптеку
            "pt": "{0},pm2dgl".format(org_point)
        }

        map_api_server = "http://static-maps.yandex.ru/1.x/"
        # ... и выполняем запрос
        response = requests.get(map_api_server, params=map_params)

        Image.open(BytesIO(
            response.content)).show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())