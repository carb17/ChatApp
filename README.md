# 🧠 Python Chat Client with GUI

## Core Functionality

This Python code implements a chat client application that enables users to:

- **Register**: Create a new account with a username and password.  
- **Log in**: Access the application using their registered credentials.  
- **Public Chat**: Send and receive messages in a general chat with all connected users.  
- **Private Chat**: Initiate private conversations with specific users.

---

## Code Structure

The code is divided into several classes, each serving a specific purpose:

- **LoginWindow**: Creates the login window, allowing users to input their username and password. Upon successful login, it opens the main chat window.
- **RegistrationWindow**: Creates the registration window, enabling users to create new accounts.
- **ChatWindow**: The main application window after login. It displays a list of online users, allows sending public messages, and facilitates private chats.
- **PrivateChat**: Creates a separate window for private conversations.

---

## How it Works

- **Graphical User Interface**: Tkinter is used to create the user interface with windows, buttons, text fields, and lists.
- **Server Connection**: The client connects to a specified server using sockets.
- **Message Sending and Receiving**: Messages are sent and received in a specific format (e.g., `login:username:password`).
- **Event Handling**: Events like button clicks and text input are handled to trigger actions.
- **Threading**: A thread is used to continuously receive messages from the server, ensuring a responsive user interface.

---

## Additional Features

- **User List Updates**: The client periodically requests an updated list of online users from the server.
- **Private Chats**: Users can initiate private conversations by double-clicking on a username.
- **Error Handling**: The code includes mechanisms to handle common errors like connection failures and authentication issues.

---

## 🛠️ How to Run

1. Download the project:
   - Option 1: Clone the repository using Git:
     ```bash
     git clone https://github.com/carb17/ChatApp.git
     ```
   - Option 2: [Download the .ZIP file](https://github.com/carb17/ChatApp/archive/refs/heads/main.zip) and extract it on your computer.

2. Open a terminal and navigate to the project folder.

3. **Run the server first**:
   ```bash
   python server.py
   ```
4. **Run the client**:
   ```bash
   python client.py
   ```
 
