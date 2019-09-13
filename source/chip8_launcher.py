from PySide2 import QtCore, QtWidgets
import sys


class Launcher():
    def __init__(self):
        self.init_emulator_attributes()
        self.create_window()
    
    def init_emulator_attributes(self):
        self.rom_path = ""
        self.off_pixel_color = (36, 36, 36)
        self.on_pixel_color = (0, 217, 0)
    
    def bind_buttons(self):
        self.left_btn.clicked.connect(self.left_btn_pressed)
        self.right_btn.clicked.connect(self.right_btn_pressed)
        self.open_rom_btn.clicked.connect(self.open_rom_button_pressed)
        self.start_game_btn.clicked.connect(self.start_game_btn_pressed)
    
    def left_btn_pressed(self):
        pass

    def right_btn_pressed(self):
        pass

    def open_rom_button_pressed(self):
        pass

    def start_game_btn_pressed(self):
        pass 

    def create_window(self):
        self.Launcher = QtWidgets.QMainWindow()
        self.Launcher.resize(290, 180)
        self.Launcher.setWindowTitle("Chip8 Launcher")

        self.centralwidget = QtWidgets.QWidget(self.Launcher)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)

        self.open_rom_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.open_rom_btn.setSizePolicy(sizePolicy)
        self.open_rom_btn.setText("Open Rom")
        self.verticalLayout_2.addWidget(self.open_rom_btn)

        self.start_game_btn = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.start_game_btn.setSizePolicy(sizePolicy)
        self.start_game_btn.setText("Start Game")
        self.verticalLayout_2.addWidget(self.start_game_btn)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        self.left_btn = QtWidgets.QPushButton(self.centralwidget)
        self.left_btn.setStyleSheet(f"background-color:rgb{self.on_pixel_color}")
        self.gridLayout.addWidget(self.left_btn, 1, 0, 1, 1)

        self.right_btn = QtWidgets.QPushButton(self.centralwidget)
        self.right_btn.setStyleSheet(f"background-color:rgb{self.off_pixel_color}")
        self.gridLayout.addWidget(self.right_btn, 1, 1, 1, 1)

        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setText("On Pixel Color")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setText("Off Pixel Color")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)
        self.Launcher.setCentralWidget(self.centralwidget)

        self.Launcher.show()
