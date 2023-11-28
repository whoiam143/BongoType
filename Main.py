# !/urs/bin/python3
# -*- coding: utf-8 -*-

import sys


from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QKeyEvent, QMovie
from PyQt5.QtCore import QTimer
from PyQt5 import uic
from get_words import Text


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.setFixedSize(1360, 770)
        self.TEXT = ""
        self.ui = uic.loadUi("1.ui", self)
        self.start_ui()

        self.number_of_words = 5

        self.text = Text(self.number_of_words)
        self.x = self.text.get_some_words()

        self.counter = 0
        self.sec = -1
        self.minut = 0
        self.update_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.stop_button.clicked.connect(self.stop_time)
        self.reset_button.clicked.connect(self.reset_time)
        self.inserted_text.setText(self.x[self.counter])

        self.rb5.toggled.connect(self.on_clicked)
        self.rb15.toggled.connect(self.on_clicked)
        self.rb25.toggled.connect(self.on_clicked)
        self.rb50.toggled.connect(self.on_clicked)

        self.rb5.setChecked(True)

        #self.gifka = QMovie("bongocat.gif")
        #self.gif.setMovie(self.gifka)
        #self.gifka.start()

    def start_ui(self):
        self.ui.show()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        text = event.text()
        if len(self.TEXT) != 0:
            if text == "\r":
                if self.check(self.x, self.TEXT, self.counter):
                    self.counter += 1
                    self.TEXT = ""
                    try:
                        self.inserted_text.setText(self.x[self.counter])
                    except IndexError:
                        self.save_result()
                        self.counter = 0
                        self.update_ex()
                        self.inserted_text.setText(self.x[self.counter])
                        print(self.x, self.counter)

            if text == "\x08":
                self.TEXT = self.TEXT[:-1]
                self.input_text.setText(self.TEXT)
            else:
                self.TEXT += text
                self.input_text.setText(self.TEXT)
                self.start_time()
        else:
            self.TEXT += event.text()
            self.input_text.setText(self.TEXT)

    def update_time(self):
        self.sec += 1
        if self.sec == 60:
            self.minut += 1
            self.sec = 0
        if self.sec <= 10 and self.minut >= 10:
            self.clock.setText(F"{self.minut}:0{self.sec}")
        elif self.sec < 10:
            self.clock.setText(F"0{self.minut}:0{self.sec}")
        elif self.minut >= 10 and self.sec >= 10:
            self.clock.setText(F"{self.minut}:{self.sec}")
        else:
            self.clock.setText(F"0{self.minut}:{self.sec}")

    def start_time(self):
        if not self.timer.isActive():
            self.timer.start(1000)

    def stop_time(self):
        self.timer.stop()

    def reset_time(self):
        self.sec = 0
        self.minut = 0
        self.TEXT = ""
        self.inserted_text.setText('')

    def messege_box(self):
        wpm = str(int((self.number_of_words * 60) / ((self.minut * 60) + self.sec)))
        box = QMessageBox.information(self, "Result", F"You result is {wpm} wpm", QMessageBox.Ok, QMessageBox.Ok)
        print(box)

    def save_result(self):
        self.messege_box()
        self.stop_time()
        self

    def on_clicked(self):
        rbt = self.sender()
        try:
            if rbt.isChecked():
                self.number_of_words = int(rbt.text())
                print(self.number_of_words)
        except AttributeError:
            pass

    def update_ex(self):
        self.x = " "
        self.x = self.text.get_some_words()

    @staticmethod
    def check(string, current_word, index_of_word):
        return string[index_of_word] == current_word.strip()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWin()
    app.exec_()
