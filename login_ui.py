# login_ui.py
# Desing for login window
from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QDialogButtonBox, QLabel, QPushButton

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Login')
        self.setStyleSheet("""
            QDialog {
                background-color: #2c3e50;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                padding: 5px;
            }
            QLineEdit {
                background-color: #34495e;
                color: #ecf0f1;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #3498db;
                color: #ecf0f1;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)

        layout = QFormLayout()
        self.username_input = QLineEdit()
        layout.addRow(QLabel('Username:'), self.username_input)

        self.room_code_input = QLineEdit()
        layout.addRow(QLabel('Room Code:'), self.room_code_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def get_inputs(self):
        return self.username_input.text(), self.room_code_input.text()
