import os
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLineEdit
)
from app.services.icon_generator import generate_3state_icon
from app.services.launcher_creator import create_launcher_ini
from app.services.variables_processor import append_launcher_to_variables
from app.utils.paths_helper import get_rainmeter_skins_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circle Launcher Tool")
        self.setFixedSize(530, 300)

        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Application name")
        self.layout.addWidget(self.name_input)

        exe_layout = QVBoxLayout()
        exe_layout.setDirection(QVBoxLayout.Direction.LeftToRight)

        self.exe_input = QLineEdit()
        self.exe_input.setPlaceholderText("Path to the .exe file")
        self.exe_input.setReadOnly(True)
        self.exe_input.setFixedWidth(300)
        exe_layout.addWidget(self.exe_input)

        self.exe_button = QPushButton("Browse...")
        self.exe_button.clicked.connect(self.select_exe) # type: ignore
        self.exe_button.setFixedWidth(200)
        exe_layout.addWidget(self.exe_button)

        self.layout.addLayout(exe_layout)

        icon_layout = QVBoxLayout()
        icon_layout.setDirection(QVBoxLayout.Direction.LeftToRight)

        self.icon_input = QLineEdit()
        self.icon_input.setPlaceholderText("Path to the .png icon file")
        self.icon_input.setReadOnly(True)
        self.icon_input.setFixedWidth(300)
        icon_layout.addWidget(self.icon_input)
        self.icon_button = QPushButton("Browse...")
        self.icon_button.clicked.connect(self.select_icon) # type: ignore
        self.icon_button.setFixedWidth(200)
        icon_layout.addWidget(self.icon_button)

        self.layout.addLayout(icon_layout)

        self.generate_button = QPushButton("Create launcher")
        self.generate_button.clicked.connect(self.create_launcher) # type: ignore
        self.layout.addWidget(self.generate_button)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.exe_path = ""
        self.icon_path = ""
        self.output_path = get_rainmeter_skins_path()

    def select_exe(self):
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar EXE", "", "EXE Files (*.exe)")
        if file:
            self.exe_path = file
            self.exe_input.setText(self.exe_path)

    def select_icon(self):
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar ícono PNG", "", "PNG Files (*.png)")
        if file:
            self.icon_path = file
            self.icon_input.setText(self.icon_path)

    def create_launcher(self):
        app_name = self.name_input.text().strip()
        if not app_name or not self.exe_path or not self.icon_path:
            self.status_label.setText("Data is missing. Please fill all fields.")
            return

        os.makedirs(self.output_path, exist_ok=True)

        circle_launcher_path = os.path.join(self.output_path, "Circle Launcher")

        # creates launcher.ini with the app name
        create_launcher_ini(app_name, circle_launcher_path)
        # generates the 3-state icon
        generate_3state_icon(self.icon_path, app_name, circle_launcher_path)
        # append the launcher to the Circle Launcher Variables.inc
        append_launcher_to_variables(self.exe_path, app_name, circle_launcher_path)

        self.status_label.setText("Launcher created successfully!")