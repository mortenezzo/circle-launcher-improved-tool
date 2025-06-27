from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLineEdit, QPushButton


class ItemSelector(QDialog):
    item_selected = pyqtSignal(dict)

    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Item")
        self.setFixedSize(300, 400)

        layout = QVBoxLayout()

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search items...")
        self.search_bar.textChanged.connect(self.filter_items) # type: ignore
        layout.addWidget(self.search_bar)

        # List widget
        self.apps = [item['Name'] for item in items] if isinstance(items, list) and all(
            isinstance(i, dict) for i in items) else items
        self.list_widget = QListWidget()
        self.list_widget.addItems(self.apps)
        layout.addWidget(self.list_widget)

        # Make button to select item disabled on default, enabled when an item is selected
        self.select_button = QPushButton("Select")
        self.select_button.setEnabled(False)
        self.select_button.clicked.connect(self.on_accept)  # type: ignore

        self.list_widget.itemSelectionChanged.connect(self.get_selected_item) # type: ignore
        layout.addWidget(self.select_button)

        self.setLayout(layout)
        self.items = items
        self.filtered_items = items
        self.selected_item = None

    def filter_items(self, text):
        """
        Filter the items in the list based on the search bar input.
        :param text: The text to filter the items by.
        """
        self.list_widget.clear()
        # get filtered items based on the search bar input
        filtered = [app for app in self.apps if text.lower() in app.lower()]
        # get filtered indexes from the original items
        self.filtered_items = [app for app in self.items if app['Name'] in filtered]
        self.list_widget.addItems(filtered)

    def get_selected_item(self) -> dict | None:
        """
        Select the currently highlighted item in the list widget.
        """
        if self.select_button.isEnabled() is False:
            self.select_button.setEnabled(True)
        else:
            filtered_index = self.list_widget.currentRow()
            return self.filtered_items[filtered_index]

        return None

    def on_accept(self):
        """
        Override the accept method to return the selected item.
        """
        selected_item = self.get_selected_item()
        if selected_item:
            self.item_selected.emit(selected_item) # type: ignore
        self.accept()
