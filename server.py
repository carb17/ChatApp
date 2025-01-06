import socket
import threading
import sqlite3

def create_user_table():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  _user_name TEXT NOT NULL UNIQUE,
                  _password TEXT NOT NULL
                 )''')
    conn.commit()
    conn.close()

create_user_table()

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                parts = message.split(':')
                if parts[0] == "register":
                    register_user(parts[1], parts[2], client_socket)
                elif parts[0] == "login":
                    login(parts[1], parts[2], client_socket)
                elif parts[0] == "update_users":
                    send_registered_users(client_socket)
                else:
                    chat(message, client_socket)
            else:
                remove(client_socket)
                chat(f"User: {client_socket.getpeername()} disconnected.", client_socket)
                break
        except Exception as e:
            print(f"Error handling client: {e}")
            remove(client_socket)
            break

private_chat = {}

def send_private_message(sender, recipient, message):
    try:
        recipient_socket = private_chat.get((sender, recipient))
        if recipient_socket:
            recipient_socket.send(f"{sender}:{message}".encode('utf-8'))
        else:
            print(f"Error: No connection found for private chat between {sender} and {recipient}")
    except Exception as e:
        print(f"Error sending private chat message: {e}")

def register_user(username, password, client_socket):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE _user_name=?", (username,))
        existing_user = c.fetchone()
        if not existing_user:
            c.execute("INSERT INTO users (_user_name, _password) VALUES (?, ?)", (username, password))
            conn.commit()
            client_socket.send("registration_successful".encode('utf-8'))
        else:
            client_socket.send("user_exists".encode('utf-8'))
        conn.close()
    except Exception as e:
        print(f"Error registering user: {e}")
        client_socket.send("registration_error".encode('utf-8'))

def login(username, password, client_socket):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE _user_name=? AND _password=?", (username, password))
        user = c.fetchone()
        if user:
            client_socket.send("login_successful".encode('utf-8'))
            send_registered_users(client_socket)  
            print(f"Login successful: {username}")
        else:
            client_socket.send("invalid_credentials".encode('utf-8'))
        conn.close()
    except Exception as e:
        print(f"Error logging in: {e}")
        client_socket.send("login_error".encode('utf-8'))

def chat(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove(client)

    for (sender, recipient), recipient_socket in private_chat.items():
        if client_socket in (recipient_socket, private_chat.get((recipient, sender))):
            try:
                recipient_socket.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending private chat message: {e}")

def remove(client_socket):
    if client_socket in clients:
        clients.remove(client_socket)

def send_registered_users(client_socket):
    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT _user_name FROM users")
        users = c.fetchall()
        conn.close()
        user_list = ':'.join(user[0] for user in users)
        client_socket.send(f"users:{user_list}".encode('utf-8'))
    except Exception as e:
        print(f"Error sending user list: {e}")

clients = []
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 5000))
server.listen(5)

print("Server started. Waiting for connections on localhost:5000 ...")

while True:
    try:
        client_socket, client_address = server.accept()
        print(f"Connection established with {client_address}")
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()
    except Exception as e:
        print(f"Error in incoming connection: {e}")

server.close()
