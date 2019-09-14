from PySide2 import QtCore, QtWidgets, QtGui


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
        # open filedialog
        # get path to file
        # check fileending
        # set self rompath to path
        file_path = QtWidgets.QFileDialog.getOpenFileName()[0]
        file_name = file_path.replace("\\", "/").split("/")[-1]
        print(file_path)
        if file_path:
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
        # check if rompath is not empty
        # if rompath there start emuloop with class parameters
        pass 

    def create_window(self):
        self.launcher_window = QtWidgets.QMainWindow()
        self.launcher_window.resize(290, 180)
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

        self.verticalLayout_2.addLayout(self.gridLayout)
        self.launcher_window.setCentralWidget(self.centralwidget)

        self.launcher_window.show()
