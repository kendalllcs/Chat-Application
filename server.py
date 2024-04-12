import os
import socket
from rich.console import Console
from datetime import datetime
import threading

console = Console()
console_lock = threading.Lock()
exit_event = threading.Event()  # Event to signal threads to exit

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_server_input(prompt, default):
    """Prompt the user for input, returning the default value if input is empty."""
    user_input = input(prompt).strip()
    return user_input if user_input else default

def receive_messages(sock):
    try:
        while not exit_event.is_set():
            data = sock.recv(1024).decode()
            if data.lower() == 'exit':
                console.print("\nExiting...", style="red")
                break
            timestamp, sender, msg = data.split('|')
            with console_lock:
                console.print(f"\n[{timestamp}][{sender}]: {msg}", style="bold magenta")
    except Exception as e:
        console.print(f"Error in receive_messages: {e}", style="red")

def main():
    clear_screen()
    console.print("[center][bold cyan]--Chat-Application--[/bold cyan][/center]")
    console.print("[center]To send a message just type it and press enter[/center]", style="bold cyan")

    ip = get_server_input("Enter IP address (or press enter for localhost): ", '127.0.0.1')
    port = get_server_input("Enter port number (or press enter for default port 65432): ", '65432')
    username = get_server_input("Enter your username: ", "ServerUser")

    try:
        port = int(port)
    except ValueError:
        console.print("Invalid port number, using default port 65432.", style="red")
        port = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((ip, port))
        server_socket.listen()
        console.print(f"\nServer running on [bold]{ip}:{port}[/bold]. Waiting for a connection...", style="green")
        
        conn, addr = server_socket.accept()
        console.print(f"Connected to [bold]{addr}[/bold]", style="green")

        threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

        with conn:
            while not exit_event.is_set():
                message = input()
                if message.lower() == 'exit':
                    conn.sendall('exit'.encode())
                    exit_event.set()  # Set exit event to signal thread to exit
                    break
                else:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    conn.sendall(f"{timestamp}|{username}|{message}".encode())
                    with console_lock:
                        console.print(f"\n[{timestamp}][{username}]: {message}", style="bold green")
    except Exception as e:
        console.print(f"An error occurred: {e}", style="red")
    finally:
        server_socket.close()

    # Clear the console before exiting
    clear_screen()

if __name__ == "__main__":
    main()
