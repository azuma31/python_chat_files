import socket
import threading

HOST = '0.0.0.0'  # すべてのネットワークインターフェースでリッスン
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = []

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # このIPアドレスに実際に接続しようとするわけではありません
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast(f'{username} left the chat!'.encode('utf-8'))
            usernames.remove(username)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('USERNAME'.encode('utf-8'))
        username = client.recv(1024).decode('utf-8')
        usernames.append(username)
        clients.append(client)

        print(f"Username of the client is {username}!")
        broadcast(f"{username} joined the chat!".encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    server_ip = get_ip()
    print(f"Server is listening on {server_ip}:{PORT}")
    print(f"Use this IP address when connecting from client: {server_ip}")
    receive()
