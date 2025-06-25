import os
from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QLineEdit
)
from app.services.icon_generator import generate_3state_icon
from app.services.launcher_creator import create_launcher_ini
from app.utils.paths_helper import get_rainmeter_skins_path

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circle Launcher Tool")
        self.setMinimumSize(500, 300)

        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Nombre de la app")
        self.layout.addWidget(self.name_input)

        self.exe_button = QPushButton("Seleccionar .exe")
        self.exe_button.clicked.connect(self.select_exe) # type: ignore
        self.layout.addWidget(self.exe_button)

        self.icon_button = QPushButton("Seleccionar ícono PNG")
        self.icon_button.clicked.connect(self.select_icon) # type: ignore
        self.layout.addWidget(self.icon_button)

        self.generate_button = QPushButton("Crear launcher")
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
            self.status_label.setText(f"EXE seleccionado: {file}")

    def select_icon(self):
        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar ícono PNG", "", "PNG Files (*.png)")
        if file:
            self.icon_path = file
            self.status_label.setText(f"Ícono seleccionado: {file}")

    def create_launcher(self):
        app_name = self.name_input.text().strip()
        if not app_name or not self.exe_path or not self.icon_path:
            self.status_label.setText("Faltan datos")
            return

        os.makedirs(self.output_path, exist_ok=True)

        # Crear INI y 3 estados
        create_launcher_ini(app_name, self.output_path)
        generate_3state_icon(app_name, self.output_path)

        self.status_label.setText("Launcher creado con éxito.")