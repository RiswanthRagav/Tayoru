from PySide6.QtWidgets import *
from ai_agent import AIAgent


class Terminal(QWidget):

    def __init__(self):
        super().__init__()

        self.ai = AIAgent()

        self.setWindowTitle("Tayoru Terminal")
        self.resize(800, 500)

        layout = QVBoxLayout()

        # Chat/output area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        layout.addWidget(self.output)

        # Command input
        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask Tayoru...")
        layout.addWidget(self.input)

        # Send button
        self.send_button = QPushButton("Send")
        layout.addWidget(self.send_button)

        self.setLayout(layout)

        self.send_button.clicked.connect(self.send_command)
        self.input.returnPressed.connect(self.send_command)

    def send_command(self):

        command = self.input.text().strip()

        if command == "":
            return

        self.output.append(f"You: {command}")

        if command == "/help":

            self.output.append(
                "Tayoru: Available commands:\n"
                "/help - Show available commands\n"
                "/clear - Clear the screen\n"
                "/about - About Tayoru"
            )

        elif command == "/about":

            self.output.append(
                "Tayoru: Local AI assistant powered by Gemma."
            )

        elif command == "/clear":

            self.output.clear()

        else:

            answer = self.ai.send_message(command)

            self.output.append(
                f"Tayoru: {answer}"
            )

        self.input.clear()