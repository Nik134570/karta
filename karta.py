import sys, os, requests

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtGui import QPixmap

URL = "http://static-maps.yandex.ru/1.x"

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 425)
        self.setWindowTitle('Часть 1')

        self.btn = QPushButton('Сформировать карту', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(100, 100)
        self.btn.clicked.connect(self.getImage)

        self.label = QLabel(self)
        self.label.setText("Укажите координаты")
        self.label.move(20, 10)

        self.name_label = QLabel(self)
        self.name_label.setText("Укажите масштаб")
        self.name_label.move(20, 70)

        self.longitude = QLineEdit(self)
        self.longitude.move(170, 10)
        self.latitude = QLineEdit(self)
        self.latitude.move(170, 30)
        self.scale = QLineEdit(self)
        self.scale.move(170, 70)

        self.image = QLabel(self)
        self.image.move(0, 125)
        self.image.resize(400, 300)

    def getImage(self):
        params = {
        "ll": f"{self.longitude.text()},{self.latitude.text()}",
        "spn": f"{self.scale.text()},{self.scale.text()}",
        "l": "map",
        "size": "400,300"
        }
        response = requests.get(URL, params=params)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

    # Запишем полученное изображение в файл.
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

        ## Изображение
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        """При закрытии формы подчищаем за собой"""
        os.remove(self.map_file)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
