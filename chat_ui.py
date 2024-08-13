from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QListWidget

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Application")

        # Set up the central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main layout: horizontal layout for the participants list and chat section
        self.main_layout = QHBoxLayout(self.central_widget)

        # Participants list section
        self.participants_layout = QVBoxLayout()
        self.user_list_label = QLabel("User List")
        self.participantsList = QListWidget()
        self.participantsList.setFixedWidth(200)  # Set fixed width for the participants list

        self.participants_layout.addWidget(self.user_list_label)
        self.participants_layout.addWidget(self.participantsList)
        self.main_layout.addLayout(self.participants_layout)

        # Chat section
        self.chat_section = QVBoxLayout()

        # Room code section
        self.room_code_layout = QHBoxLayout()
        self.roomCodeLabel = QLabel("Room Code: ")
        self.copyButton = QPushButton("Copy Room Code")
        self.room_code_layout.addWidget(self.roomCodeLabel)
        self.room_code_layout.addWidget(self.copyButton)
        self.chat_section.addLayout(self.room_code_layout)

        # Chat area
        self.chatArea = QTextEdit()
        self.chatArea.setReadOnly(True)
        self.chat_section.addWidget(self.chatArea)

        # Input field and send button
        self.input_layout = QHBoxLayout()
        self.inputField = QLineEdit()
        self.sendButton = QPushButton("Send")
        self.input_layout.addWidget(self.inputField)
        self.input_layout.addWidget(self.sendButton)
        self.chat_section.addLayout(self.input_layout)

        # Add the chat section to the main layout
        self.main_layout.addLayout(self.chat_section)

        # Apply styles
        self.apply_styles()

    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QLabel {
                color: #ecf0f1;
                font-size: 14px;
                padding: 5px;
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
            QTextEdit {
                background-color: #34495e;
                color: #ecf0f1;
                font-size: 14px;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QLineEdit {
                background-color: #34495e;
                color: #ecf0f1;
                font-size: 14px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            QListWidget {
                background-color: #34495e;
                color: #ecf0f1;
                font-size: 14px;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
        """)

    def update_participants_list(self, participants):
        self.participantsList.clear()
        for participant in participants:
            self.participantsList.addItem(participant)