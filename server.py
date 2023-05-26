import socket
import random
import tkinter as tk

def diffie_hellman(p, g):
    # Generate private key
    private_key = random.randint(1, p - 1)
    print(f"private key of server = {private_key}")

    # Compute public keye
    public_key = pow(g, private_key, p)
    print(f"public key of server = {public_key}")

    return private_key, public_key

def compute_shared_secret(their_public_key, private_key, p):
    shared_secret = pow(their_public_key, private_key, p)
    return shared_secret

def start_server():
    #global declaration irrespective if the function is called or changed
    global server_socket

    # Server configuration
    host = '127.0.0.1'
    port = 12345

    # Diffie-Hellman parameters
    p = 14327  # Prime number
    g = 100  # Generator

    # Create a socket and bind it to the host and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # af inet is IPv4 and sock stream is TCP
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    log("Server listening on {}:{}".format(host, port))

    # Accept a client connection
    client_socket, addr = server_socket.accept()
    log("Connected to client: {}".format(addr))

    # Perform Diffie-Hellman key exchange
    private_key, public_key = diffie_hellman(p, g)

    # Send the public key to the client
    client_socket.send(str(public_key).encode())

    # Receive the client's public key
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

# Create the server window
server_window = tk.Tk()
server_window.title("Server")

# Server log text widget
text_log = tk.Text(server_window, height=10, width=40)
text_log.pack()

# Start server button
button_start = tk.Button(server_window, text="Start Server", command=start_server)
button_start.pack()

# Run the server GUI
server_window.mainloop()
