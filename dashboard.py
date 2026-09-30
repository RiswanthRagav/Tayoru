from PySide6.QtCore import Signal
from PySide6.QtWidgets import *
from terminal import Terminal


class Dashboard(QWidget):

    logout_requested = Signal()

    def __init__(self, username):
        super().__init__()

        self.setWindowTitle("Tayoru Dashboard")
        self.resize(800, 500)

        layout = QVBoxLayout()

        title = QLabel("Tayoru Dashboard")
        layout.addWidget(title)

        welcome = QLabel(f"Welcome, {username}!")
        layout.addWidget(welcome)

        # Tayoru Terminal
        self.terminal = Terminal()
        layout.addWidget(self.terminal)

        logout_button = QPushButton("Logout")
        layout.addWidget(logout_button)

        self.setLayout(layout)

        logout_button.clicked.connect(self.logout_clicked)

    def logout_clicked(self):
        self.logout_requested.emit()