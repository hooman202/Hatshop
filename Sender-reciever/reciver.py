import socket
import subprocess

def start_receiver(receiver_port):
    # Set up the receiver socket
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    receiver_host = ''  # Listen on all available interfaces

    try:
        # Bind the socket to the host and port
        receiver_socket.bind((receiver_host, receiver_port))

        # Listen for incoming connections
        receiver_socket.listen(1)
        print("Receiver is listening on port", receiver_port)

        while True:
            # Accept the incoming connection
            connection, sender_address = receiver_socket.accept()
            print("Received a connection from:", sender_address)

            # Receive data
            data = connection.recv(1024).decode()
            print("Received:", data)

            # Check for a specific message
            if data == "start_program":
                # Run the desired .exe file
                subprocess.run(r'C:\Users\hooma\eclipse\java-2023-03\eclipse\eclipse.exe')
                print("Program executed.")
            elif data=="kill_program":
                subprocess.run(['taskkill', '/f', '/im', 'eclipse.exe'])

            #elif data=="restart":
            #elif data=="sleeo_mode":



            # Close the connection
            connection.close()
    finally:
        # Close the receiver socket
        receiver_socket.close()

def kill_program_by_file_name(file_name):
    # Check the platform (Windows or Linux/Mac)
    # Use taskkill command on Windows
    subprocess.run(['taskkill', '/f', '/im', file_name])

# Usage example
file_name_to_kill = 'program.exe'  # Replace with the actual file name to kill
kill_program_by_file_name(file_name_to_kill)

    

# Usage example
receiver_port = 12345  # Replace with the desired port number
start_receiver(receiver_port)



