import socket
import random
import tkinter as tk

def diffie_hellman(p, g):
    # Generate private key
    private_key = random.randint(1, p - 1)
    print(f"private key of client is = {private_key}")

    # Compute public key
    public_key = pow(g, private_key, p)
    print(f"public key of client = {public_key}")

    return private_key, public_key

def compute_shared_secret(their_public_key, private_key, p):
    shared_secret = pow(their_public_key, private_key, p)
    return shared_secret

def connect_to_server():  
    global client_socket

    # Server configuration
    host = '127.0.0.1'
    port = 12345

    # Diffie-Hellman parameters
    p = 14327  # Prime number
    g = 100  # Generator

    # Create a socket and connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    log("Connected to server for key exchange: {}:{}".format(host, port))

    # Perform Diffie-Hellman key exchange
    private_key, public_key = diffie_hellman(p, g)

    # Send the public key to the server
    client_socket.send(str(public_key).encode())

    # Receive the server's public key
    their_public_key = int(client_socket.recv(1024).decode())

    # Compute the shared secret
    shared_secret = compute_shared_secret(their_public_key, private_key, p)
    log("Shared secret: {}".format(shared_secret))

    # Close the client socket
    client_socket.close()

def log(message):
    text_log.config(state=tk.NORMAL)
    text_log.insert(tk.END, message + "\n")
    text_log.config(state=tk.DISABLED)
    text_log.see(tk.END)

# Create the client window
client_window = tk.Tk()
client_window.title("Client")

# Client log text widget
text_log = tk.Text(client_window, height=10, width=40)
text_log.pack()

# Connect to server button
button_connect = tk.Button(client_window, text="Connect to Server", command=connect_to_server)
button_connect.pack()

# Run the client GUI
client_window.mainloop()
