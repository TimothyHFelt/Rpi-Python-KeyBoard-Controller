import socket
import time
import threading
import sys
from pynput.keyboard import Key, Listener, KeyCode

# --- CONFIGURATION ---
PI_IP = "192.168.1.251"  # Your Pi's IP
UDP_PORT = 5005
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# State tracking for keys
keys = {Key.up: False, Key.down: False, Key.left: False, Key.right: False,
        KeyCode.from_char('w'): False, KeyCode.from_char('a'): False,
        KeyCode.from_char('s'): False, KeyCode.from_char('d'): False}

running = True


# --- MOTOR CONTROL LOGIC ---
def get_current_pkt_state():
    # Byte 1-2: Drive, Byte 3-4: Turn, Byte 5-8: Arm/Aux
    pkt = bytearray([0xFF, 0x01, 0x00, 0x01, 0x00, 0x01, 0x01, 0x01, 0x01])

    # Drivetrain
    if keys[Key.up]:
        pkt[1], pkt[2] = 0x02, 0x01
    elif keys[Key.down]:
        pkt[1], pkt[2] = 0x00, 0x01

    if keys[Key.left]:
        pkt[3], pkt[4] = 0x00, 0x01
    elif keys[Key.right]:
        pkt[3], pkt[4] = 0x02, 0x01

    # Arm / Secondary Controls (WASD)
    if keys[KeyCode.from_char('w')]: pkt[5], pkt[7] = 0x02, 0x02
    if keys[KeyCode.from_char('s')]: pkt[5], pkt[7] = 0x00, 0x00
    if keys[KeyCode.from_char('a')]: pkt[5], pkt[7] = 0x00, 0x02
    if keys[KeyCode.from_char('d')]: pkt[5], pkt[7] = 0x02, 0x00

    return pkt


def on_press(key):
    if key in keys:
        keys[key] = True
    elif hasattr(key, 'char'):
        try:
            k = KeyCode.from_char(key.char)
            if k in keys: keys[k] = True
        except:
            pass


def on_release(key):
    if key in keys:
        keys[key] = False
    elif hasattr(key, 'char'):
        try:
            k = KeyCode.from_char(key.char)
            if k in keys: keys[k] = False
        except:
            pass


def control_loop():
    global running
    last_pkt = None
    start_time = time.perf_counter()
    print("--- MOTOR CONTROL ACTIVE ---")
    print("Use Arrow Keys and WASD to drive. Press 'Esc' to quit.")

    while running:
        current_pkt = get_current_pkt_state()

        # Send only if keys change OR a 0.5s heartbeat to keep Pi connection alive
        if current_pkt != last_pkt or (time.perf_counter() - start_time > 0.5):
            sock.sendto(current_pkt, (PI_IP, UDP_PORT))
            last_pkt = current_pkt
            start_time = time.perf_counter()

        time.sleep(0.02)


# --- EXECUTION ---

# Keyboard Listener
listener = Listener(on_press=on_press, on_release=on_release)
listener.start()

# Start Control Loop
try:
    control_loop()
except KeyboardInterrupt:
    pass
finally:
    print("\nStopping motors and exiting...")
    running = False
    listener.stop()

    # Send a definitive STOP packet multiple times
    stop_pkt = bytearray([0xFF, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00])
    for _ in range(5):
        sock.sendto(stop_pkt, (PI_IP, UDP_PORT))
        time.sleep(0.01)

    sys.exit(0)