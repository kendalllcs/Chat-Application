import socket

def get_input(prompt):
    user_input = input(prompt).strip()
    return user_input if user_input else None

def main():
    # Get user input for IP address, port, and username
    ip = get_input("Enter IP address (press enter for localhost): ")
    ip = ip or '127.0.0.1'  # Default to localhost if empty
    port = get_input("Enter port number (press enter for default port): ")
    port = int(port) if port else 65432  # Default port
    username = input("Enter your username: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((ip, port))
        print(f"Server started on {ip}:{port}")
        server_socket.listen()

        conn, addr = server_socket.accept()
        print(f"Connected to {addr}")

        with conn:
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break
                print(f"{username}: {data}")

                message = input("Send a message: ")
                conn.sendall(message.encode())

if __name__ == "__main__":
    main()
