import threading
import socket

class ChatClient:
    def __init__(self) -> None:
        """Initializes instance."""
        self.HOST = socket.gethostbyname()
        self.PORT = 5432
        pass

    def start(self):
        """Creat and connect clients to the server."""
        self.nickname = input("Choose a nackname: ")
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.HOST, self.PORT))

        # Threads => so that the call can interact at the same time
        receive_thread = threading.Thread(target=cc.receive)
        receive_thread.start()

        write_thread = threading.Thread(target=cc.receive)
        write_thread.start()

    def receive(self):
        """Handle incoming messages."""
        while True:
            try:
                msg = self.client.recv(1024).decode("ascii")
                # Server will ask client for nickname
                if msg == "NICK":
                    self.client.send(self.nickname.encode("ascii"))
                else:
                    print(msg)
            except:
                print("Error occured. Client is gone.")
                self.client.close()
                break

    def write(self):
        """Send the messages to the server."""
        while True:
            msg = f"{self.nickname}: {input('')}"
            self.client.send(msg.encode("ascii"))

if __name__ == "__main__":
    cc = ChatClient()
    cc.start()
