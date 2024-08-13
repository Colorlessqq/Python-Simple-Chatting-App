import sys
import socket
import random
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
from chat_ui import Ui_MainWindow  # Import the generated UI class
from login_ui import LoginDialog  # Import the login UI class

# Define signals for communication between worker threads and the main GUI thread
class WorkerSignals(QObject):
    message_received = pyqtSignal(str)  # Signal to emit when a new message is received

# Worker thread class for handling network communication
class WorkerThread(QThread):
    def __init__(self, socket, signals):
        super().__init__()
        self.socket = socket  # Socket object for network communication
        self.signals = signals  # Signals object to communicate with the main thread

    def run(self):
        # Continuously receive messages from the socket
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                self.signals.message_received.emit(message)  # Emit signal with received message
            except Exception as e:
                print(f"Error receiving message: {e}")  # Print error message if any exception occurs
                self.socket.close()  # Close the socket on error
                break

# Main chat client class
class ChatClient(QMainWindow):
    def __init__(self, host, port):
        super().__init__()

        self.host = host
        self.port = port
        self.username = None
        self.room_code = None
        self.users = []

        # Create and connect the socket to the server
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

        # Initialize the UI
        self.ui = Ui_MainWindow()

        # Connect UI elements to their respective methods
        self.ui.inputField.returnPressed.connect(self.send_message)
        self.ui.sendButton.clicked.connect(self.send_message)
        self.ui.copyButton.clicked.connect(self.copy_room_code)

        # Create signals and connect them to slots
        self.signals = WorkerSignals()
        self.signals.message_received.connect(self.handle_message)

        # Show the login dialog
        self.login()

    def login(self):
        login_dialog = LoginDialog()
        if login_dialog.exec_() == QDialog.Accepted:
            # Retrieve username and room code from the login dialog
            self.username, self.room_code = login_dialog.get_inputs()
            if self.room_code:
                # Join an existing room
                self.socket.send(f"/join {self.room_code} {self.username}".encode('utf-8'))
            else:
                # Create a new room if no room code is provided
                self.room_code = self.create_room()
            # Update the window title and show the room code
            self.ui.setWindowTitle(f'Chat Application - {self.username} in Room {self.room_code}')
            self.show_room_code()
            self.ui.show()  # Show the chat UI only after login
            # Start the worker thread for receiving messages
            self.worker_thread = WorkerThread(self.socket, self.signals)
            self.worker_thread.start()
        else:
            sys.exit()  # Exit the application if the login dialog is cancelled

    # Create a new room with a unique code
    def create_room(self):
        room_code = self.generate_room_code()
        self.socket.send(f"/create {room_code} {self.username}".encode('utf-8'))
        return room_code

    # Generate a unique room code based on the username and a random number
    def generate_room_code(self):
        return f"{self.username}_{random.randint(1000, 9999)}"

    # Update the UI to display the room code
    def show_room_code(self):
        self.ui.roomCodeLabel.setText(f"Room Code: {self.room_code}")

    # Copy the room code to the clipboard and show a message box
    def copy_room_code(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.room_code)
        QMessageBox.information(self, "Room Code Copied", f"Room code {self.room_code} has been copied to the clipboard.")

    # Send a message to the server
    def send_message(self):
        message = self.ui.inputField.text()
        if message:
            self.socket.send(f"{self.room_code} {self.username}: {message}".encode('utf-8'))
            self.ui.chatArea.append(f"You: {message}")  # Update chat area with the sent message
            self.ui.inputField.clear()  # Clear the input field

    # Handle received messages by appending them to the chat area
    def handle_message(self, message):
        if message.startswith("/add"):
            username = message.split()[1]
            if username not in self.users:
                self.users.append(username)
                self.ui.update_participants_list(self.users)
        elif message.startswith("/remove"):
            username = message.split()[1]
            if username in self.users:
                self.users.remove(username)
                self.ui.update_participants_list(self.users)
        elif message.startswith("/participants"):
            participants = message.split(' ', 1)[1].split(',')
            self.users = participants
            self.ui.update_participants_list(self.users)
        else:
            self.ui.chatArea.append(message)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    host = '127.0.0.1'
    port = 12345
    client = ChatClient(host, port)
    sys.exit(app.exec_())
