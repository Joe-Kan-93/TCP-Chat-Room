import threading
import socket

class ChatServer:
    def __init__(self) -> None:
        """Initializes instance."""
        self.HOST = socket.gethostbyname()
        self.PORT = 5432
        self.clients = []
        self.nicknames = []
        pass

    def start(self):
        """Creat and start the server."""
        print("Server is ready.")
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()
        self.receive()

    def broadcast(self, message):
        """Broadcast a message to all clients."""
        for client in self.clients:
            if isinstance(client, socket.socket):
                client.send(message)

    def handle(self, client : socket.socket):
        """Handle or remove clients from server."""
        while True:
            # Try to receive messages from clients
            try:
                message = client.recv(1042)
                self.broadcast(message)
            # By exception the client is terminated and removed
            except:
                index = self.clients.index(client)

                self.clients.remove(client)
                client.close()

                nickname = self.nicknames[index]
                self.broadcast(f"{nickname} left the chat.".encode("ascii"))
                self.nicknames.remove(nickname)
                break

    def receive(self):
        """Receive clients and add them to the chat server."""
        while True:
            # Accept incoming connections from clients
            client, addr = self.server.accept()
            print(f"Connected with {str(addr)}.")

            # Ask client for nickname then append nickname and client to lists
            client.send("NICK".encode("ascii"))
            nickname = client.recv(1024).decode("ascii")
            self.nicknames.append(nickname)
            self.clients.append(client)

            # Announce new clients to all and send feedback to client
            print(f"Nickname of the client is {nickname}.")
            self.broadcast(f"{nickname} joined the chat.".encode("ascii"))
            client.send("Connected to server.")

            # Threading
            thread = threading.Thread(target=self.handle, args=(client, ))
            thread.start()

if __name__ == "__main__":
    cs = ChatServer()
    cs.start()