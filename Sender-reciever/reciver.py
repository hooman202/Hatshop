import socket
import subprocess
import os

# def start_receiver(receiver_port):
#     # Set up the receiver socket
#     receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     receiver_host = ''  # Listen on all available interfaces

#     try:
#         # Bind the socket to the host and port
#         receiver_socket.bind((receiver_host, receiver_port))

#         # Listen for incoming connections
#         receiver_socket.listen(1)
#         print("Receiver is listening on port", receiver_port)

#         while True:
#             # Accept the incoming connection
#             connection, sender_address = receiver_socket.accept()
#             print("Received a connection from:", sender_address)

#             # Receive data
#             data = connection.recv(1024).decode()
#             print("Received:", data)

#             # Check for a specific message
            

#             # Close the connection
#             connection.close()
#     finally:
#         # Close the receiver socket
#         receiver_socket.close()

# def kill_program_by_file_name(file_name):
#     # Check the platform (Windows or Linux/Mac)
#     # Use taskkill command on Windows
#     subprocess.run(['taskkill', '/f', '/im', file_name])







import socket

app_name = 'skeleton.exe'

def receive_message(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    data, addr = sock.recvfrom(1024)
    message = data.decode('utf-8')
    sock.close()
    return message

port = 12345
while True:
    message = receive_message(port)
    if message == "start_app":
        shortcut_path = r"C:/skeleton.lnk"
        subprocess.Popen(['start', shortcut_path], shell=True)
        print("Program executed.")

    elif message=="kill_app":
        subprocess.run(['taskkill', '/f', '/im', app_name])

    elif message=='reset':
        os.system("shutdown /r /t 0")

            #elif data=="restart":
            #elif data=="sleeo_mode":