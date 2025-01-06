import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

class LoginWindow:
    def __init__(self, container):
        self.container = container
        self.container.title("Login")

        # LABELS AND ENTRY 
        self.username_label = tk.Label(container, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(container)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(container, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(container, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # BUTTONS
        self.login_button = tk.Button(container, text="Login", command=self.login)
        self.login_button.grid(row=2, column=1, padx=10, pady=10, sticky='e')

        self.register_button = tk.Button(container, text="Register", command=self.show_registration)
        self.register_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

        # WINDOW SIZE AND POSITION
        width = 300
        height = 150
        screen_width = self.container.winfo_screenwidth()
        screen_height = self.container.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.container.geometry(f"{width}x{height}+{x}+{y}")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect(('localhost', 5000))

                data = f"login:{username}:{password}"
                self.client_socket.send(data.encode('utf-8'))

                response = self.client_socket.recv(1024).decode('utf-8')

                if response == "login_successful":
                    self.container.destroy()
                    host = 'localhost'
                    port = 5000
                    self.chat = ChatWindow(host, port, username, self.client_socket)
                    self.chat.root.mainloop()
                elif response == "invalid_credentials":
                    messagebox.showerror("Login Error", "Incorrect username or password")
                else:
                    messagebox.showerror("Login Error", "Unknown error during login")
                self.client_socket.close()
            except Exception as e:
                messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")
        else:
            messagebox.showerror("Login Error", "Please enter both username and password")

    def show_registration(self):
        self.container.withdraw()
        registration = RegistrationWindow(self.container)

class RegistrationWindow:
    def __init__(self, container):
        self.container = tk.Toplevel(container)
        self.container.title("Registration")

        # LABELS AND ENTRY
        self.username_label = tk.Label(self.container, text="New username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.container)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.container, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.container, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # BUTTONS
        self.register_button = tk.Button(self.container, text="Register", command=self.register)
        self.register_button.grid(row=2, column=1, padx=10, pady=10)
        self.back_button = tk.Button(self.container, text="Back", command=self.close_window)
        self.back_button.grid(row=2, column=0, padx=10, pady=10)

        # WINDOW SIZE AND POSITION
        width = 250
        height = 150
        screen_width = self.container.winfo_screenwidth()
        screen_height = self.container.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.container.geometry(f"{width}x{height}+{x}+{y}")

        # CLOSE WINDOW EVENT
        self.container.protocol("WM_DELETE_WINDOW", self.close_window)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect(('localhost', 5000))

                data = f"register:{username}:{password}"
                self.client_socket.send(data.encode('utf-8'))

                response = self.client_socket.recv(1024).decode('utf-8')

                if response == "registration_successful":
                    messagebox.showinfo("Registration Successful", "User registered successfully")
                    self.container.master.deiconify()
                    self.container.destroy()
                elif response == "user_exists":
                    messagebox.showerror("Registration Error", "Username already exists. Please choose another.")
                else:
                    messagebox.showerror("Registration Error", "Unknown error during registration")
                self.client_socket.close()
            except Exception as e:
                messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")
        else:
            messagebox.showerror("Registration Error", "Please enter both username and password")

    def close_window(self):
        self.container.destroy()
        self.container.master.deiconify()

class ChatWindow:
    def __init__(self, host, port, username, client_socket):
        self.private_chats = {}  

        self.client_socket = client_socket
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"User: {self.username}")

        # REGISTERED USERS FRAME
        self.write_message_label = tk.Label(self.root, text="Registered users:")
        self.write_message_label.grid(row=0, column=4, columnspan=2, padx=10, pady=5, sticky="w")
        self.user_list = tk.Listbox(self.root, width=20, height=20)
        self.user_list.grid(row=1, column=4, padx=10, pady=10, sticky='ns')

        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.grid(row=0, column=5, rowspan=2, sticky='ns')
        self.user_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.user_list.yview)
        self.update_button = tk.Button(self.root, text="Update users", command=self.update_users)
        self.update_button.grid(row=2, column=4, columnspan=2, padx=10, pady=5, sticky="ew")

        # CHAT AREA
        self.chat_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=40, height=10)
        self.chat_area.grid(row=1, column=0, columnspan=3, padx=20, pady=5, sticky='nsew')
        self.chat_area.config(state=tk.DISABLED)  

        self.entry_message = tk.StringVar()
        self.entry_box = tk.Entry(self.root, textvariable=self.entry_message, width=30)
        self.entry_box.grid(row=2, column=0, padx=10, pady=5, sticky='ew')

        # BUTTONS
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(row=2, column=1, pady=5, sticky='ew')
        self.logout_button = tk.Button(self.root, text="Logout", command=self.close_session)
        self.logout_button.grid(row=0, column=0, pady=5, padx=10, sticky="ew")

        # BINDINGS
        self.user_list.bind('<Double-Button-1>', self.initiate_private_chat)
        self.root.bind('<Return>', lambda event: self.send_message())  

        # RECEIVE THREAD
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

        # PROTOCOL
        self.root.protocol("WM_DELETE_WINDOW", self.close_session)

        self.client_socket.send(f"Connected: {self.username}!".encode('utf-8'))

    def update_users(self):
        try:
            self.client_socket.send("update_users".encode('utf-8'))
        except Exception as e:
            messagebox.showerror("Connection Error", f"Unable to connect to server: {e}")

    def receive_users(self, user_list):
        self.user_list.delete(0, tk.END)  
        users = user_list.split(':')
        for user in users:
            if user != self.username:  
                self.user_list.insert(tk.END, user)

    def receive(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode('utf-8')

                if message.startswith("users:"):
                    user_list = message.split(':', 1)[1]
                    self.receive_users(user_list)

                elif message.startswith("private:"):
                    _, sender, recipient, message_content = message.split(':', 3)
                    if recipient == self.username:
                        if sender in self.private_chats:
                            self.private_chats[sender].receive_message(f"{sender}: {message_content}")
                        else:
                            self.private_chats[sender] = PrivateChat(self.root, self.username, sender, self.client_socket)
                            self.private_chats[sender].receive_message(f"{sender}: {message_content}")
                else:
                    self.chat_area.config(state=tk.NORMAL)
                    self.chat_area.insert(tk.END, message + '\n')
                    self.chat_area.config(state=tk.DISABLED)
            except Exception as e:
                print(f"An error occurred: {e}")
                break

    def send_message(self):
        message = self.entry_message.get()
        recipient = self.user_list.get(tk.ACTIVE)

        if message:
            if recipient:
                self.client_socket.send(f"{self.username}:{message}".encode('utf-8'))
                self.chat_area.config(state=tk.NORMAL)
                self.chat_area.insert(tk.END, f"You: {message}\n")
                self.chat_area.config(state=tk.DISABLED)
                self.entry_message.set('')
            else:
                messagebox.showerror("Message Error", "Please select a valid recipient")

    def initiate_private_chat(self, event):
        recipient = self.user_list.get(tk.ACTIVE)
        if recipient:
            if recipient not in self.private_chats:
                self.private_chats[recipient] = PrivateChat(self.root, self.username, recipient, self.client_socket)
            self.private_chats[recipient].window.deiconify()

    def close_session(self):
        response = messagebox.askyesno("Confirmation", "Are you sure you want to log out?")
        if response:
            try:
                self.client_socket.send(f"{self.username} has disconnected".encode('utf-8'))
                self.client_socket.close()
            except Exception as e:
                print(f"Error closing session: {e}")
            finally:
                self.root.destroy()
   
class PrivateChat:
    def __init__(self, master, username, recipient, client_socket):
        self.client_socket = client_socket
        self.username = username
        self.recipient = recipient

        self.window = tk.Toplevel(master)
        self.window.title(f"Private chat with {self.recipient}")

        self.chat_area = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, width=50, height=20)
        self.chat_area.grid(row=0, column=0, padx=10, pady=5)
        self.chat_area.config(state=tk.DISABLED)

        self.entry_message = tk.StringVar()
        self.entry_box = tk.Entry(self.window, textvariable=self.entry_message, width=40)
        self.entry_box.grid(row=1, column=0, padx=10, pady=5, sticky='ew')

        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

        self.window.protocol("WM_DELETE_WINDOW", self.close_window)
        self.entry_box.bind('<Return>', lambda event: self.enviar_mensaje())

    def send_message(self):
        message = self.entry_message.get()
        if message:
            data = f"private:{self.username}:{self.recipient}:{message}"
            self.client_socket.send(data.encode('utf-8'))
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.insert(tk.END, f"You: {message}\n")
            self.chat_area.config(state=tk.DISABLED)
            self.entry_message.set('')

    def receive_message(self, message):
        if hasattr(self, 'chat_area') and self.chat_area.winfo_exists():
            self.chat_area.config(state=tk.NORMAL)
            self.chat_area.insert(tk.END, message + '\n')
            self.chat_area.config(state=tk.DISABLED)

    def close_window(self):
        self.window.destroy()
        self.chat_area = None  
    
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)  
    root.mainloop()

