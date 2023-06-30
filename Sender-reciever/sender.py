import tkinter as tk
import socket
import codecs
import time
import subprocess
from multiprocessing import Pool
import threading


root = tk.Tk()
root.title("Tenchou - てんちょう ")

broadcast_ip = '192.168.128.255'
port = 12345

mac_pc_dict = {
    '00-00-00-00-00-00': 'PC01',
    '00-00-00-00-00-01': 'PC02',
    '24-4B-FE-BC-4D-A9': 'PC03',
    '24-4B-FE-BC-43-83': 'PC04',
    '00-00-00-00-00-02': 'PC05',
    '00-00-00-00-00-03': 'PC06',
    '00-00-00-00-00-04': 'PC07',
    '00-00-00-00-00-05': 'PC08',
    'D4-93-90-20-92-78': 'PC09',
    'D4-93-90-20-93-B9': 'PC10',
    'D4-93-90-20-92-D0': 'PC11',
    '00-00-00-00-00-06': 'PC12',
    '00-00-00-00-00-07': 'PC13',
    '00-00-00-00-00-08': 'PC14'
}

computer_status = [False] * len(mac_pc_dict)

def send_broadcast_message(message, ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    try:
        sock.sendto(message.encode('utf-8'), (ip, port))
    finally:
        sock.close()

def wake_on_lan(mac_address):
    mac_address = mac_address.replace('-', '')
    if len(mac_address) % 2 != 0:
        mac_address = '0' + mac_address

    mac_bytes = codecs.decode(mac_address.replace(':', ''), 'hex')
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(magic_packet, ('<broadcast>', 9))

def ping_computer(pc_name):
    try:
        ip_address = socket.gethostbyname(pc_name)
        process = subprocess.Popen(['ping', '-c', '1', ip_address], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _, error = process.communicate()

        return process.returncode == 0 and not error
    except socket.gaierror:
        return False

def check_computer():
    num_processes = len(mac_pc_dict) + 1
    with Pool(num_processes) as pool:
        results = pool.map(ping_computer, mac_pc_dict.values())

    reachable_computers = [result for result in results if result is not None]
    print("Reachable computers:")
    for computer in reachable_computers:
        print(computer)

def on_button_click(command):
    if command == "turn_on":
        for mac_address, pc_name in mac_pc_dict.items():
            wake_on_lan(mac_address)
            print(f"Message sent - Waking up {pc_name} with MAC address {mac_address}")
    elif command == "restart":
        message = "reset"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Restarting all PCs")
    elif command == "start_app":
        message = "start_app"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Starting Skeleton.exe on all PCs")
    elif command == "kill_app":
        message = "kill_app"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Killing Skeleton.exe on all PCs")
    elif command == "turn_off":
        message = "turn_off"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Turning off all PCs")
    elif command == "sleep":
        send_broadcast_message("kill_app", broadcast_ip, port)
        print("Message sent - Killing Skeleton.exe on all PCs")
        time.sleep(1)
        message = "sleep"
        send_broadcast_message(message, broadcast_ip, port)
        print("Message sent - Putting all PCs to sleep")
    elif command == "check_status":
        for mac_address, pc_name in mac_pc_dict.items():
            if ping_computer(pc_name):
                print(f"{pc_name} is OK!")
            else:
                print(f"{pc_name} is Dead!")


port_receive = 12346
def receive_message(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    data, addr = sock.recvfrom(1024)
    message = data.decode('utf-8')
    sock.close()
    return message

def start_receive_thread():
    while True:
        message = receive_message(port_receive)
        computer_status[int(message.removeprefix("PC"))-1] = True
        print(f"Received message from {message}")


receive_thread = threading.Thread(target=start_receive_thread, daemon=True)
receive_thread.start()

# Create a frame for PC boxes
frame = tk.Frame(root)
frame.grid(row=0, column=0, columnspan=len(mac_pc_dict), padx=10, pady=10)

# Create PC boxes
boxes = []
for idx, (mac_address, pc_name) in enumerate(mac_pc_dict.items()):
    box = tk.Label(frame, relief='solid', width=10, height=2, bg='green', text=pc_name)
    box.grid(row=0, column=idx, padx=5, pady=5)
    boxes.append(box)

def update_boxes():
    global computer_status
    for idx, status in enumerate(computer_status):
        color = 'green' if status else 'red'
        boxes[idx].configure(bg=color)

    root.after(2000, update_boxes)
    computer_status = [False] * len(mac_pc_dict)  # Reset computer_status to False


# Start updating the PC boxes
update_boxes()

button_turn_on = tk.Button(root, text="Turn on all PCs", command=lambda: on_button_click("turn_on"), width=15)
button_turn_on.grid(row=1, column=0, padx=10, pady=10)

button_turn_off = tk.Button(root, text="Turn off all PCs", command=lambda: on_button_click("turn_off"), width=15)
button_turn_off.grid(row=2, column=0, padx=10, pady=10)

button_restart = tk.Button(root, text="Restart all PCs", command=lambda: on_button_click("restart"), width=15)
button_restart.grid(row=3, column=0, padx=10, pady=10)

button_start_app = tk.Button(root, text="Start Skeleton.exe on All PCs", command=lambda: on_button_click("start_app"), width=30)
button_start_app.grid(row=3, column=1, padx=10, pady=10)

button_kill_app = tk.Button(root, text="Kill Skeleton.exe on All PCs", command=lambda: on_button_click("kill_app"), width=30)
button_kill_app.grid(row=4, column=1, padx=10, pady=10)

button_sleep = tk.Button(root, text="Sleep All PCs", command=lambda: on_button_click("sleep"), width=30)
button_sleep.grid(row=5, column=1, padx=10, pady=10)

button_check_status = tk.Button(root, text="Check Computers Status", command=lambda: on_button_click("check_status"), width=30)
button_check_status.grid(row=6, column=1, columnspan=2, padx=10, pady=10)

root.mainloop()
