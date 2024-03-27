import socket

def get_input(prompt):
    user_input = input(prompt).strip()
    return user_input if user_input else None

def main():
    # Get user input for IP address, port, and username
    ip = input("Enter server IP address: ")
    port = int(input("Enter server port number: "))
    username = input("Enter your username: ")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((ip, port))
        print("Connected to server")

        while True:
            message = input("Send a message (or type 'exit' to quit): ")
            client_socket.sendall(message.encode())

            if message.lower() == 'exit':
                break

            data = client_socket.recv(1024).decode()
            print(f"Server: {data}")

if __name__ == "__main__":
    main()