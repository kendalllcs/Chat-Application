import subprocess
import os
import platform

def clear_screen():
    # Clear the terminal screen based on the operating system
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def run_server():
    clear_screen()
    print("Starting server...")
    subprocess.run(['python', 'server.py'])

def run_client():
    clear_screen()
    print("Starting client...")
    if platform.system() == 'Windows':
        subprocess.run(['start', 'cmd', '/k', 'python', 'client.py'], shell=True)
    elif platform.system() == 'Linux':
        subprocess.run(['gnome-terminal', '--', 'python', 'client.py'])
    else:
        print("Unsupported operating system for running client.")

def main():
    choice = input("Enter 's' to start server or 'c' to start client: ").strip().lower()

    if choice == 's':
        run_server()
    elif choice == 'c':
        run_client()
    else:
        print("Invalid choice. Please enter 's' or 'c'.")

if __name__ == "__main__":
    main()

