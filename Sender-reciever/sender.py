import socket
import struct
import codecs
import binascii
import time

ip = '192.168.128.109'  # IP address of the specific computer
broadcast_ip = '192.168.128.255' #ATC
# broadcast_ip = '10.229.40.255' #Kyoto University
port = 12345

# Specify the MAC address of the sleeping computer
mac_pc_dict = {}

# Add MAC addresses and PC names to the dictionary
mac_pc_dict[''] = 'PC01'
mac_pc_dict[''] = 'PC02'
mac_pc_dict['24-4B-FE-BC-4D-A9'] = 'PC03'
mac_pc_dict['24-4B-FE-BC-43-83'] = 'PC04'
mac_pc_dict[''] = 'PC05'
mac_pc_dict[''] = 'PC06'
mac_pc_dict[''] = 'PC07'
mac_pc_dict[''] = 'PC08'
mac_pc_dict['D4-93-90-20-92-78'] = 'PC09'
mac_pc_dict['D4-93-90-20-93-B9'] = 'PC10'
mac_pc_dict['D4-93-90-20-92-D0'] = 'PC11'
mac_pc_dict[''] = 'PC12'
mac_pc_dict[''] = 'PC13'
mac_pc_dict[''] = 'PC14'




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

def wake_on_lan(mac_address):
    # Create a magic packet with the MAC address
    mac_address = mac_address.replace('-', '')  # Replace dashes with colons
    if len(mac_address) % 2 != 0:
        mac_address = '0' + mac_address  # Prepend '0' if length is odd

    mac_bytes = codecs.decode(mac_address.replace(':', ''), 'hex')
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    # Send the magic packet to the broadcast address
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, ('<broadcast>', 9))

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
        for mac_address, pc_name in mac_pc_dict.items():
            wake_on_lan(mac_address)
            print(f"Message sent - Waking up {pc_name} with Mac address {mac_address}")
    
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
        send_broadcast_message("kill_app", broadcast_ip, port)
        print("Message sent - Killing Skeleton.exe on all PCs")
        time.sleep(1)
        message = "sleep"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent 4- Put all PCs to sleep")

    elif(input_command == "7"):
        print("Which PC do you like to Talk with - not done")
        message = "start_app"
        send_message(message, ip, port)

    elif(input_command == "q" or 'Q'):
        break