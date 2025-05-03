# --------------- Server Code (server.py) ---------------
import socket
import threading

class ChatServer:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.lock = threading.Lock()
        
    def start(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()
        print(f"Server listening on {self.host}:{self.port}")
        
        while True:
            client_socket, addr = self.server_socket.accept()
            with self.lock:
                self.clients.append(client_socket)
            print(f"New connection from {addr}")
            threading.Thread(
                target=self.handle_client,
                args=(client_socket, addr),
                daemon=True
            ).start()
    
    def broadcast(self, message, sender_socket):
        with self.lock:
            for client in self.clients:
                if client != sender_socket:
                    try:
                        client.send(message.encode('utf-8'))
                    except:
                        self.clients.remove(client)
    
    def handle_client(self, client_socket, addr):
        try:
            while True:
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received from {addr}: {message}")
                self.broadcast(f"{addr}: {message}", client_socket)
        except ConnectionResetError:
            print(f"Client {addr} disconnected")
        finally:
            with self.lock:
                self.clients.remove(client_socket)
            client_socket.close()

if __name__ == "__main__":
    server = ChatServer()
    server.start()
