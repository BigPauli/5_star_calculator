from PyQt6.QtWidgets import QApplication, QWidget
from application import MyApplication
import sys

app = QApplication(sys.argv)
my_app = MyApplication()
my_app.show()
sys.exit(app.exec())