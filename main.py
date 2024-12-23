import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QLabel, QGridLayout, QWidget, QVBoxLayout
)
from PyQt5.QtCore import Qt


class Game2048(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2048")
        self.setGeometry(100, 100, 400, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)

        self.button_layout = QVBoxLayout()

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addLayout(self.button_layout)

        self.board_size = 4
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.cells = [[QLabel("0") for _ in range(self.board_size)] for _ in range(self.board_size)]

        for i in range(self.board_size):
            for j in range(self.board_size):
                self.grid_layout.addWidget(self.cells[i][j], i, j)
                self.cells[i][j].setStyleSheet("border: 1px solid black; font-size: 18px;")
                self.cells[i][j].setAlignment(Qt.AlignCenter)

        self.up_button = QPushButton("Вверх")
        self.down_button = QPushButton("Вниз")
        self.left_button = QPushButton("Влево")
        self.right_button = QPushButton("Вправо")

        self.button_layout.addWidget(self.up_button)
        self.button_layout.addWidget(self.down_button)
        self.button_layout.addWidget(self.left_button)
        self.button_layout.addWidget(self.right_button)

        self.up_button.clicked.connect(lambda: self.move("up"))
        self.down_button.clicked.connect(lambda: self.move("down"))
        self.left_button.clicked.connect(lambda: self.move("left"))
        self.right_button.clicked.connect(lambda: self.move("right"))

        self.generate_number()
        self.generate_number()
        self.update_board()

    def generate_number(self):
        empty_cells = [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = random.choice([2, 4])

    def update_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                value = self.board[i][j]
                self.cells[i][j].setText(str(value) if value > 0 else "")
                # Стилизация ячеек
                self.cells[i][j].setStyleSheet(
                    f"background-color: {'#EEE4DA' if value else '#CDC1B4'}; "
                    f"font-size: {24 if value < 100 else 20}px; "
                    "border: 1px solid black; font-weight: bold;"
                )

    def compress(self, line):
        new_line = [i for i in line if i != 0]
        return new_line + [0] * (len(line) - len(new_line))

    def merge(self, line):
        for i in range(len(line) - 1):
            if line[i] == line[i + 1] and line[i] != 0:
                line[i] *= 2
                line[i + 1] = 0
        return line

    def move(self, direction):
        rotated = False
        if direction in ("up", "down"):
            self.board = list(map(list, zip(*self.board)))
            rotated = True

        for i in range(self.board_size):
            if direction in ("right", "down"):
                self.board[i] = self.board[i][::-1]

            self.board[i] = self.compress(self.board[i])
            self.board[i] = self.merge(self.board[i])
            self.board[i] = self.compress(self.board[i])

            if direction in ("right", "down"):
                self.board[i] = self.board[i][::-1]

        if rotated:
            self.board = list(map(list, zip(*self.board)))

        self.generate_number()
        self.update_board()


app = QApplication(sys.argv)
game = Game2048()
game.show()
sys.exit(app.exec_())
