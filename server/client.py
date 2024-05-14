import socket
import threading
from paper import Paper
from gui.message import MessageRenderer

class Client:
    def __init__(self, screen, host="localhost", port=5555, username = str):
        self.screen = screen
        self.host = host
        self.port = port
        self.username = username

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

        self.renderer = MessageRenderer(self.screen)

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode())
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_messages(self):
        while True:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"Server response: {message}")
                self.renderer.add_message(message)
                self.renderer.render()
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def start(self):
        paper = Paper(self.screen, self.screen.get_width(), self.screen.get_height())
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        paper.init()