# !/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from datetime import datetime, time
from random import choice, shuffle
from db import add_result, results, create_bd

from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import QTimer
from PyQt5 import uic


class MainWin(QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()
        self.setFixedSize(1360, 770)
        self.TEXT = ""
        self.ui = uic.loadUi("1.ui", self)
        self.start_ui()
        create_bd()

        self.number_of_words = 5
        self.counter = 0
        self.counter_of_ex = 0

        self.text = []
        self.list_of_words = []

        self.sec = -1
        self.minut = 0
        self.update_time()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.reset_button.clicked.connect(self.reset_ex)
        self.inserted_text.setText(self.get_some_words()[self.counter])
        self.results_butt.clicked.connect(self.show_results)

        self.rb5.toggled.connect(self.on_clicked)
        self.rb15.toggled.connect(self.on_clicked)
        self.rb25.toggled.connect(self.on_clicked)
        self.rb50.toggled.connect(self.on_clicked)
        self.rb5.setChecked(True)

    def start_ui(self):
        self.ui.show()

    def keyPressEvent(self, event: QKeyEvent):     # Функция для обработки нажатий с клавиатуры
        super().keyPressEvent(event)
        text = event.text()
        if len(self.TEXT) != 0:
            if text == "\r":
                if self.check(self.text, self.TEXT, self.counter):
                    self.counter += 1
                    self.TEXT = ""
                    try:
                        self.inserted_text.setText(self.text[self.counter])
                    except IndexError:
                        self.save_result()
                        self.reset_ex()
                        self.text = []
                        self.get_some_words()
                        self.counter_of_ex += 1
                        self.inserted_text.setText(self.text[self.counter])
                        self.reset_time()
            if text == "\x08":
                self.TEXT = self.TEXT[:-1]
                self.input_text.setText(self.TEXT)
            else:
                self.TEXT += text
                self.input_text.setText(self.TEXT)
                if self.counter_of_ex == 0:
                    self.start_time()
                else:
                    self.stop_time()
                    self.counter_of_ex -= 1
                    self.reset_time()
                    self.update_time()
        else:
            self.TEXT += event.text()
            self.input_text.setText(self.TEXT)

    def get_some_words(self):  # Функция для получения случайных слов
        self.list_of_words = []
        with open("ListOfWords.txt", "r") as file:
            for words in file.readlines():
                self.list_of_words.append(words.strip())
            shuffle(self.list_of_words)
            for i in range(self.number_of_words):
                self.text.append(choice(self.list_of_words))
        return self.text

    def update_time(self):  # Функция для обновления времени
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

    def start_time(self):  # Функция для начала работы таймера
        if not self.timer.isActive():
            self.timer.start(1000)

    def stop_time(self):  # Функция для остановки работы таймеры
        self.timer.stop()

    def reset_time(self):  # Функция для сбороса времени
        self.sec = -1
        self.minut = 0

    def reset_ex(self):  # Функция для сброса текущий тренировки
        self.counter = 0
        self.inserted_text.setText(self.text[0])
        self.TEXT = ""
        self.input_text.setText(self.TEXT)
        self.reset_time()
        self.update_time()
        self.stop_time()

    def result_box(self):  # Функция для вывода окна результата текущий тренировки
        wpm = str(int((self.number_of_words * 60) / ((self.minut * 60) + self.sec)))
        box = QMessageBox.information(self, "Result", F"You result is {wpm} wpm", QMessageBox.Ok, QMessageBox.Ok)
        return box

    def show_results(self):  # Функция для вывода общий статистики
        inf = results()
        box = QMessageBox.information(self, "Statistic", F"Average value: {int(sum(inf) / len(inf))} wpm\n"
                                                         F"The best value: {max(inf)} wpm\n"
                                                         F"The worst value: {min(inf)} wpm")
        return box

    def save_result(self):  # Функция для сохранения результата текущий тренировки
        self.result_box()
        self.stop_time()
        date = str(datetime.now())[0:16]
        time_of_score = str(time(self.minut, self.sec))[0:5]
        wpm = str(int((self.number_of_words * 60) / ((self.minut * 60) + self.sec)))
        add_result(date, time_of_score, self.number_of_words, wpm, ", ".join(self.text))

    def on_clicked(self):  # Функция для смены количества слов
        rbt = self.sender()
        try:
            if rbt.isChecked():
                self.number_of_words = int(rbt.text())
        except AttributeError:
            pass
        self.change_number_of_words()

    def change_number_of_words(self):
        if len(self.text) != self.number_of_words:
            self.reset_ex()
            self.text = []
            self.get_some_words()
            self.inserted_text.setText(self.text[0])

    @staticmethod
    def check(string, current_word, index_of_word):  # Функция для проверки слов
        return string[index_of_word] == current_word.strip()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainWin()
    app.exec_()
