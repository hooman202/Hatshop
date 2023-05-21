import socket

def send_message(message, host, port):
    # Set up the sender socket
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the receiver
        sender_socket.connect((host, port))

        # Send the message
        sender_socket.send(message.encode())
    finally:
        # Close the sender socket
        sender_socket.close()

def broadcast_message(message, broadcast_address, broadcast_port):
    # Set up the socket for broadcasting
    broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        # Send the message to the broadcast address and port
        broadcast_socket.sendto(message.encode(), (broadcast_address, broadcast_port))
    finally:
        # Close the broadcast socket
        broadcast_socket.close()

# Usage example
#message = "start_program"
message = "kill_program"
broadcast_address = '10.229.40.255'  # Replace with the appropriate broadcast address
broadcast_port = 12345  # Replace with the desired port number
send_message(message, '10.229.40.97', broadcast_port)
broadcast_message(message, broadcast_address, broadcast_port)