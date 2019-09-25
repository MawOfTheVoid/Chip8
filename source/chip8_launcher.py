from PySide2 import QtCore, QtWidgets, QtGui
from emulation import start_emulation


class Launcher():
    def __init__(self):
        self.init_emulator_attributes()
        self.create_window()
        self.bind_buttons()

    def init_emulator_attributes(self):
        self.rom_path = ""
        self.off_pixel_color = (36, 36, 36, 255)
        self.on_pixel_color = (0, 217, 0, 255)

    def bind_buttons(self):
        self.left_btn.clicked.connect(self.left_btn_pressed)
        self.right_btn.clicked.connect(self.right_btn_pressed)
        self.open_rom_btn.clicked.connect(self.open_rom_button_pressed)
        self.start_game_btn.clicked.connect(self.start_game_btn_pressed)

    def left_btn_pressed(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.on_pixel_color = color.getRgb()
            self.left_btn.setStyleSheet(f"background-color:rgba{self.on_pixel_color}")
        self.open_rom_btn.setFocus()

    def right_btn_pressed(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.off_pixel_color = color.getRgb()
            self.right_btn.setStyleSheet(f"background-color:rgba{self.off_pixel_color}")
        self.open_rom_btn.setFocus()

    def open_rom_button_pressed(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName()[0]
        file_name = file_path.replace("\\", "/").split("/")[-1]
        if file_path:
            # check if the rom doesnt have a fileending or a .ch8 one
            if len(file_name.split(".")) == 1 or file_name.endswith(".ch8"):
                self.rom_path = file_path
                self.open_rom_btn.setText(file_name)
                self.start_game_btn.setFocus()
            else:
                QtWidgets.QMessageBox.warning(
                    self.launcher_window, 'U trying to trick me?',
                    """<b>If you try to open the wrong files I will delete your PC!!!</b>""",
                    QtWidgets.QMessageBox.Ok)
                self.open_rom_btn.setFocus()
        else:
            self.open_rom_btn.setFocus()

    def start_game_btn_pressed(self):
        if self.rom_path != "":
            self.launcher_window.close()
            start_emulation(
                self.rom_path, self.on_pixel_color,
                self.off_pixel_color, self.fps_box.value()
            )

    def create_window(self):
        self.launcher_window = QtWidgets.QMainWindow()
        self.launcher_window.resize(260, 290)
        self.launcher_window.setWindowTitle("Chip8 Launcher")
        self.launcher_window.setWindowIcon(QtGui.QIcon("Chip8Boy.png"))

        self.centralwidget = QtWidgets.QWidget(self.launcher_window)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)

        self.open_rom_btn = QtWidgets.QPushButton(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.open_rom_btn.setSizePolicy(size_policy)
        self.open_rom_btn.setText("Open Rom")
        self.open_rom_btn.setFocus()
        self.verticalLayout_2.addWidget(self.open_rom_btn)

        self.start_game_btn = QtWidgets.QPushButton(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.start_game_btn.setSizePolicy(size_policy)
        self.start_game_btn.setText("Start Game")
        self.verticalLayout_2.addWidget(self.start_game_btn)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        self.left_btn = QtWidgets.QPushButton(self.centralwidget)
        self.left_btn.setStyleSheet(f"background-color:rgba{self.on_pixel_color}")
        self.gridLayout.addWidget(self.left_btn, 1, 0, 1, 1)

        self.right_btn = QtWidgets.QPushButton(self.centralwidget)
        self.right_btn.setStyleSheet(f"background-color:rgba{self.off_pixel_color}")
        self.gridLayout.addWidget(self.right_btn, 1, 1, 1, 1)

        self.on_pixel_lbl = QtWidgets.QLabel(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.on_pixel_lbl.setSizePolicy(size_policy)
        self.on_pixel_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.on_pixel_lbl.setText("On Pixel Color")
        self.gridLayout.addWidget(self.on_pixel_lbl, 0, 0, 1, 1)

        self.off_pixel_lbl = QtWidgets.QLabel(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.off_pixel_lbl.setSizePolicy(size_policy)
        self.off_pixel_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.off_pixel_lbl.setText("Off Pixel Color")
        self.gridLayout.addWidget(self.off_pixel_lbl, 0, 1, 1, 1)

        self.fps_lbl = QtWidgets.QLabel(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.fps_lbl.setSizePolicy(size_policy)
        self.fps_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.fps_lbl.setText("CPU cycles / second")
        self.fps_lbl.setToolTip("Controls the game speed.")
        self.verticalLayout_2.addWidget( self.fps_lbl)

        self.fps_box = QtWidgets.QSpinBox(self.centralwidget)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        self.fps_box.setSizePolicy(size_policy)
        self.fps_box.setAlignment(QtCore.Qt.AlignCenter)
        self.fps_box.setRange(1, 1000)
        self.fps_box.setValue(240)
        self.verticalLayout_2.addWidget(self.fps_box)

        self.verticalLayout_2.addLayout(self.gridLayout)
        self.launcher_window.setCentralWidget(self.centralwidget)

        self.launcher_window.show()
