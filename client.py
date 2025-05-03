# --------------- Client Code (client.py) ---------------
import socket
import threading

class ChatClient:
    def __init__(self, host='localhost', port=5000):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def start(self):
        self.client_socket.connect((self.host, self.port))
        print("Connected to chat server")
        
        receive_thread = threading.Thread(
            target=self.receive_messages,
            daemon=True
        )
        receive_thread.start()
        
        self.send_messages()
        
    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"\n{message}")
            except:
                break
    
    def send_messages(self):
        try:
            while True:
                message = input()
                self.client_socket.send(message.encode('utf-8'))
        except KeyboardInterrupt:
            print("\nDisconnecting...")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    client = ChatClient()
    client.start()
