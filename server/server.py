import pygame
import socket
import threading
from gui.message import MessageRenderer
from paper import Paper

class Server:
    def __init__(self, screen, host="localhost", port=5555, username = str):
        self.screen = screen
        self.host = host
        self.port = port
        self.username = username
        self.clients = []

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        self.renderer = MessageRenderer(self.screen)


    def run_server(self):
        print("Server started, listening for connections...")
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Connection from {client_address}")
            self.clients.append(client_socket)
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()


            initial_message = f"Welcome to the server, {self.username}"
            crazy = f"[Server] you are crazy"
            client_socket.send(initial_message.encode())
            client_socket.send(crazy.encode())

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = data.decode()
                print(f"Received message: {message}")
                self.broadcast(message)

            except ConnectionResetError:
                print("Client disconnected.")
                self.clients.remove(client_socket)
                break

    def broadcast(self, message):
        self.renderer.add_message(message)
        self.renderer.render()
        for client in self.clients:
            try:
                client.send(message.encode())
            except Exception as e:
                print(f"Error broadcasting message: {e}")

    def start(self):
        paper = Paper(self.screen, self.screen.get_width(), self.screen.get_height())
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()
        paper.init()
