import io

from ui import *
from PyQt6.QtWidgets import QWidget
from PyQt6 import QtWidgets
import os
import json


class MyApplication(QWidget):
    def __init__(self):
        super(MyApplication, self).__init__()

        self.data = None

        # set up ui from ui file
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # populate combo box with options
        self.ui.comboBox.addItems(['5 ⭐', '4 ⭐', '3 ⭐', '2 ⭐', '1 ⭐'])

        # get current amount of reviews from json file
        self.read_json()

        # populate the graphics view with the current number of needed reviews
        self.scene = QtWidgets.QGraphicsScene(self)
        self.ui.graphicsView.setScene(self.scene)
        self.add_big_number()

        # add functionality to push buttons
        self.ui.pushButton.clicked.connect(self.add_reviews)
        self.ui.pushButton_2.clicked.connect(self.remove_reviews)
        self.ui.pushButton_3.clicked.connect(self.return_totals)

        # add message boxes and set messages
        self.messageBox = QtWidgets.QMessageBox()
        self.messageBox.setText('Warning: Reviews cannot be a negative number')

        self.messageBox_2 = QtWidgets.QMessageBox()

        # set spin box maximum to 999
        self.ui.spinBox.setMaximum(999)

    def read_json(self):
        try:
            with open('data.json', 'r') as data_file:
                self.data = json.load(data_file)
        except FileNotFoundError:
            self.data = {
                '5 ⭐': 0,
                '4 ⭐': 0,
                '3 ⭐': 0,
                '2 ⭐': 0,
                '1 ⭐': 0,
            }

            with open('data.json', 'w') as data_file:
                json.dump(self.data, data_file)

    def add_big_number(self):
        width, height = self.ui.graphicsView.width(), self.ui.graphicsView.height()
        big_mf_font = QtGui.QFont()
        big_mf_font.setPointSize(100)
        num = self.get_needed_reviews()
        num = num if num > 0 else 0
        text = self.scene.addText(f'{num}', font=big_mf_font)
        text.setPos(width/2, height/2)

    def get_needed_reviews(self):
        return 79*self.data['1 ⭐'] + 59*self.data['2 ⭐'] + 39*self.data['3 ⭐'] + 19*self.data['4 ⭐'] \
                - self.data['5 ⭐']

    def add_reviews(self):
        stars = self.ui.comboBox.currentText()
        amount = int(self.ui.spinBox.cleanText())

        self.data[stars] += amount
        with open('data.json', 'w') as data_file:
            json.dump(self.data, data_file)

        self.scene.clear()
        self.add_big_number()

    def remove_reviews(self):
        stars = self.ui.comboBox.currentText()
        amount = int(self.ui.spinBox.cleanText())

        if amount > self.data[stars]:
            self.messageBox.exec()
            return

        self.data[stars] -= amount
        with open('data.json', 'w') as data_file:
            json.dump(self.data, data_file)

        self.scene.clear()
        self.add_big_number()

    def return_totals(self):
        self.messageBox_2.setText(f'5 ⭐: {self.data["5 ⭐"]}'
                                  f'\n4 ⭐: {self.data["4 ⭐"]}'
                                  f'\n3 ⭐: {self.data["3 ⭐"]}'
                                  f'\n2 ⭐: {self.data["2 ⭐"]}'
                                  f'\n1 ⭐: {self.data["1 ⭐"]}'
                                  f'\nTotal: {sum(self.data.values())}')
        print('executed')
        self.messageBox_2.exec()