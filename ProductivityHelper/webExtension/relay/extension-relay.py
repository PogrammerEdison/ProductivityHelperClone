import json
import queue
import socket
import struct
import sys
from time import sleep
import threading

host = socket.gethostname()
port = 38584
send_queue = queue.Queue()

# Make stdin and stdout run in binary mode instead of text mode on Windows, since it's not the default
if sys.platform == "win32":
    import os, msvcrt
    msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

def send_to_python(s: socket.socket, text_to_send: str):
    s.send(struct.pack('I', len(text_to_send)))
    s.send(text_to_send.encode("utf-8"))

def read_from_stdin():
    length_bytes = sys.stdin.buffer.read(4) # First 4 bytes is length of message
    if len(length_bytes) == 0:
        raise Exception("Text length was 0")
    length = struct.unpack('i', length_bytes)[0]

    return_str = sys.stdin.read(length)
    return return_str

def networking_main():
    is_connected = False
    s = socket.socket()
    while True:
        # Firstly, get the text
        text = send_queue.get()
        jsonObj = json.loads(text)
        # Now, try to send it
        has_sent = False
        while not has_sent:
            try:
                if not is_connected:
                    s.connect((host, port))
                    is_connected = True
                if jsonObj != None:
                    send_to_python(s, jsonObj["text"])
                has_sent = True
            except Exception:
                sleep(1) # Prevent busy loop
                # Discard messages in queue - we don't want old URLs hanging around while we reconnect
                jsonObj = None
                while not send_queue.empty():
                    send_queue.get()
                if is_connected:
                    s.close() # Close the connection
                    s = socket.socket() # Recreate the socket - we can't call .connect after calling .close on the same object
                    is_connected = False

def send_to_stdout(text_to_send: str):
    sys.stdout.buffer.write(struct.pack('I', len(text_to_send))) # Send length first
    sys.stdout.write(text_to_send) # Send the message
    sys.stdout.flush()

if __name__ == '__main__':
    network_thread = threading.Thread(target=networking_main)
    network_thread.setDaemon(True)
    network_thread.start()
    while True:
        text = read_from_stdin()
        send_queue.put(text)