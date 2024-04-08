import os
import socket
from rich.console import Console
from datetime import datetime
import threading
import pyautogui

console = Console()
console_lock = threading.Lock()
exit_event = threading.Event()  # Event to signal threads to exit

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_input(prompt, default=None):
    """Prompt the user for input, allowing default values if none is provided."""
    user_input = input(prompt).strip()
    return user_input if user_input else default

def receive_messages(sock):
    try:
        while not exit_event.is_set():
            data = sock.recv(1024).decode()
            if data.lower() == 'exit':
                console.print("\nServer has exited the chat.", style="red")
                break
            timestamp, sender, msg = data.split('|')
            with console_lock:
                console.print(f"\n[{timestamp}][{sender}]: {msg}", style="bold magenta")
    except Exception as e:
        console.print(f"Error in receive_messages: {e}", style="red")

def save_chat_history():
    screenshot = pyautogui.screenshot()
    screenshot.save('chat_history.png')
    console.print("[bold green]Chat history saved to 'chat_history.png'[/bold green]")

def main():
    clear_screen()
    console.print("[center][bold cyan]--Chat-Application--[/bold cyan][/center]")
    console.print("[center]To send a message just type it and press enter[/center]", style="bold cyan")
    console.print("[center]input 'ca-save' to save entire chat[/center]", style="bold cyan")

    ip = get_input("Enter server IP address (or press enter for localhost): ", '127.0.0.1')
    port = get_input("Enter server port number (or press enter for default port 65432): ", '65432')
    username = get_input("Enter your username: ", "ClientUser")

    try:
        port = int(port)
    except ValueError:
        console.print("Invalid port number, using default port 65432.", style="red")
        port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((ip, port))
            console.print("\nConnected to server", style="green")

            threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
            
            while not exit_event.is_set():
                message = input()
                if message.lower() == 'exit':
                    client_socket.sendall('exit'.encode())
                    exit_event.set()  # Set exit event to signal thread to exit
                    break
                elif message.lower() == 'ca-save':
                    save_chat_history()
                else:
                    timestamp = datetime.now().strftime('%H:%M:%S')
                    client_socket.sendall(f"{timestamp}|{username}|{message}".encode())
                    with console_lock:
                        console.print(f"[{timestamp}][{username}]: {message}", style="bold green")
        except Exception as e:
            console.print(f"Connection error: {e}", style="red")

    # Clear the console before exiting
    clear_screen()

if __name__ == "__main__":
    main()
