import os

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLineEdit,
    QRadioButton,
    QProgressDialog,
)
from app.services.icon_generator import generate_3state_icon
from app.services.launcher_creator import create_launcher_ini
from app.services.variables_processor import append_launcher_to_variables_using_system_app, append_launcher_to_variables
from app.threads.get_system_apps_thread import GetSystemAppsThread
from app.utils.paths_helper import get_rainmeter_skins_path
from gui.components.item_selector import ItemSelector


def set_button_behavior(button, text, method):
    button.setText(text)
    try:
        button.clicked.disconnect()
    except TypeError:
        pass
    button.clicked.connect(method)


def stop_thread(thread, progress_dialog):
    thread.stop()
    thread.quit()
    thread.wait()
    progress_dialog.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Circle Launcher Tool")
        self.setFixedSize(530, 300)

        self.layout = QVBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Application name")
        self.layout.addWidget(self.name_input)

        method_layout = QHBoxLayout()

        self.browse_radiobutton = QRadioButton("Browse from desktop")
        self.browse_radiobutton.setChecked(True)
        self.select_radiobutton = QRadioButton("Select app from list")
        self.browse_radiobutton.toggled.connect(self.on_radio_button_selected)  # type: ignore
        method_layout.addWidget(self.browse_radiobutton)
        method_layout.addWidget(self.select_radiobutton)
        self.layout.addLayout(method_layout)

        exe_layout = QHBoxLayout()
        self.exe_input = QLineEdit()
        self.exe_input.setPlaceholderText("Path to the .exe file")
        self.exe_input.setReadOnly(True)
        self.exe_input.setFixedWidth(300)
        exe_layout.addWidget(self.exe_input)
        self.exe_button = QPushButton("Browse...")
        self.exe_button.clicked.connect(self.select_exe)  # type: ignore
        exe_layout.addWidget(self.exe_button)
        self.layout.addLayout(exe_layout)

        icon_layout = QHBoxLayout()
        self.icon_input = QLineEdit()
        self.icon_input.setPlaceholderText("Path to the .png icon file")
        self.icon_input.setReadOnly(True)
        self.icon_input.setFixedWidth(300)
        icon_layout.addWidget(self.icon_input)
        self.icon_button = QPushButton("Browse...")
        self.icon_button.clicked.connect(self.select_icon)  # type: ignore
        icon_layout.addWidget(self.icon_button)
        self.layout.addLayout(icon_layout)

        self.generate_button = QPushButton("Create launcher")
        self.generate_button.clicked.connect(self.create_launcher)  # type: ignore
        self.layout.addWidget(self.generate_button)

        self.status_label = QLabel("")
        self.layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        self.exe_path = ""
        self.icon_path = ""
        self.output_path = get_rainmeter_skins_path()
        self.selected_item = None

    def on_radio_button_selected(self):
        self.exe_input.clear()
        self.exe_path = None
        if self.browse_radiobutton.isChecked():
            self.exe_input.setPlaceholderText("Path to the .exe file")
            set_button_behavior(self.exe_button, "Browse...", self.select_exe)
        if self.select_radiobutton.isChecked():
            self.exe_input.setPlaceholderText("Select an app from the list")
            set_button_behavior(self.exe_button, "Select app", self.open_app_selector)

    def open_app_selector(self):
        progress_dialog = QProgressDialog("Loading system applications...", "Cancel", 0, 0, self)
        progress_dialog.setWindowTitle("Opening app selector")
        progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        progress_dialog.setCancelButtonText("Cancel")
        progress_dialog.setMinimumDuration(0)

        thread = GetSystemAppsThread()
        thread.result.connect(lambda apps: self.on_apps_loaded(apps, progress_dialog))
        thread.error.connect(lambda error_message: self.on_apps_error(error_message, progress_dialog))
        progress_dialog.canceled.connect(lambda: stop_thread(thread, progress_dialog)) # type: ignore

        progress_dialog.show()
        thread.start()

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
        if self.browse_radiobutton.isChecked():
            append_launcher_to_variables(self.exe_path, app_name, circle_launcher_path)
        if self.select_radiobutton.isChecked():
            append_launcher_to_variables_using_system_app(app_name, self.selected_item, circle_launcher_path)

        self.status_label.setText("Launcher created successfully!")

    def update_selected_item(self):
        """
        Update the selected item in the input fields based on the item selected in the ItemSelector.
        """
        self.selected_item = self.sender().get_selected_item() # type: ignore
        if self.selected_item:
            self.exe_input.setText(self.selected_item['AppID'])
            self.exe_path = self.selected_item['AppID']

    def on_apps_loaded(self, apps, progress_dialog):
        progress_dialog.close()
        if not apps:
            self.status_label.setText("No applications found.")
            return
        selector = ItemSelector(apps, self)
        selector.item_selected.connect(self.update_selected_item)
        selector.exec()

    def on_apps_error(self, error_message, progress_dialog):
        progress_dialog.close()
        self.status_label.setText(f"Error loading applications: {error_message}")

