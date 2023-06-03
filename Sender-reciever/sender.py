import socket

def send_broadcast_message(message, ip, port):
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        # Send the broadcast message
        sock.sendto(message.encode('utf-8'), (ip, port))
    finally:
        # Close the socket
        sock.close()

def send_message(message, ip, port):
    # Set up the sender socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  #  sock = sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    try:
        # Send the message
        sock.sendto(message.encode('utf-8'), (ip, port))
    finally:
        # Close the sender socket
        sock.close()

ip = '192.168.128.109'  # IP address of the specific computer
# broadcast_ip = '192.168.128.255' #ATC
broadcast_ip = '10.229.40.255' #Kyoto University
port = 12345

# Usage example
#message = "start_program"
print("-----------------------------")
print("1) Turn ON All PCs - not done")
print("2) Restart All PCs - not done")
print("3) Start Skeleton.exe on All PCs - not done")
print("4) Kill Skeleton.exe on All PCs - not done")
print("5) Turn off All PCs - not done")
print("6) Sleep All PCs - not done")
print("7) Do it for one PC - not done")
print("Q) - Quit")
print("-----------------------------")
while True: 
    input_command = input("Please enter the command: ")
    if(input_command == "1"):
        message = "turn_on"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Turning on all PCs")
    
    elif(input_command == "2"):
        message = "reset"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Restarting all PCs")
    
    elif(input_command == "3"):
        message = "start_app"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Starting Skeleton.exe on all PCs")

    elif(input_command == "4"):
        message = "kill_app"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Killing Skeleton.exe on all PCs")

    elif(input_command == "5"):
        message = "turn_off"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Turning off all PCs")

    elif(input_command == "6"):
        message = "reset"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Put all PCs to sleep")

    elif(input_command == "7"):
        print("Which PC do you like to Talk with - not done")
        message = "start_app"
        send_message(message, ip, port)

    elif(input_command == "q" or 'Q'):
        break