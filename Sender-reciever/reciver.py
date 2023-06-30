import socket
import subprocess
import os
import ctypes
import threading
import time

app_name = 'skeleton.exe'

# For heartbeat
broadcast_ip = '192.168.128.255'  # ATC
heartbeat_port = 12346
stop_heartbeat = False

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

def get_computer_name():
    hostname = socket.gethostname()
    return hostname

def send_heartbeat(port):
    while not stop_heartbeat:
        send_broadcast_message(get_computer_name(), broadcast_ip, port)
        print("Sent message: I'm alive")
        time.sleep(2)

# Start the thread for sending the "I'm alive" message
alive_thread = threading.Thread(target=send_heartbeat, args=(heartbeat_port,), daemon=True)
alive_thread.start()

# Define the necessary Windows API functions
SetSuspendState = ctypes.windll.powrprof.SetSuspendState
SetSuspendState.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int)
SetSuspendState.restype = ctypes.c_uint

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
    print(message)
    if message == "start_app":
        shortcut_path = r"C:/Hatshop/skeleton.lnk"
        subprocess.Popen(['start', shortcut_path], shell=True)
        print("Program executed.")

    elif message == "kill_app":
        subprocess.run(['taskkill', '/f', '/im', app_name])

    elif message == 'reset':
        stop_heartbeat = True
        os.system("shutdown /r /t 0")

    elif message == 'sleep':
        SetSuspendState(0, 0, 0)

    elif message == 'turn_off':
        os.system("shutdown /s /t 0")
