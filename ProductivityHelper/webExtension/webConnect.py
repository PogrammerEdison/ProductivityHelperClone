import socket
import struct
import threading
import urllib.parse
from datetime import datetime
import time

class WebConnect:
    def __init__(self) -> None:
        # Create thread
        with open("websites.txt", 'r') as f:
            self.bad_sites = f.readlines()
        for i in range(len(self.bad_sites)):
            self.bad_sites[i] = self.bad_sites[i].lower().strip()
        self.thread = threading.Thread(target=self.thread_entry_point)
        self.thread.setDaemon(True)
        self.thread.start()
        self.recording = False
        self.data = []
        self.current_distraction = None
    
    def start_period(self):
        self.data = []
        self.current_distraction = None
        self.recording = True
    
    def end_period(self):
        self.record_url(None)
        self.recording = False
    
    def get_data(self):
        return self.data
    
    def record_url(self, url):
        if not self.recording:
            return
        if self.current_distraction != None:
            # The last URL was a distraction. Record it
            self.current_distraction[1] = datetime.now()
            self.data.append(self.current_distraction)
            self.current_distraction = None
        # Now check if current url is a distraction, and if so, add it
        if url != None:
            netloc = urllib.parse.urlparse(url).netloc
            for bad_site in self.bad_sites:
                if netloc.endswith(bad_site):
                    self.current_distraction = [datetime.now(), datetime.now(), bad_site]
                    print("Entered bad site " + bad_site)
                    break

    def thread_entry_point(self):
        host = socket.gethostname()
        port = 38584
        was_connected = False
        
        while True:
            s = socket.socket()
            try:
                s.bind((host, port))
                s.listen(1)
                c, address = s.accept()
                was_connected = True

                while True:
                    # Get the length first
                    length_bytes = c.recv(4)
                    if (len(length_bytes) == 0):
                        break
                    bytes_remaining = struct.unpack('i', length_bytes)[0]

                    # Now read the string, and keep reading until we're done
                    message = ""
                    while bytes_remaining > 0:
                        chunk_bytes = c.recv(bytes_remaining)
                        bytes_remaining = bytes_remaining - len(chunk_bytes)
                        message = message + chunk_bytes.decode("utf-8")
                    if message == "":
                        print("No tab")
                        self.record_url(None)
                    else:
                        print("Loaded " + message)
                        self.record_url(message)
            except Exception:
                s.close() # We're probably here because the user closed their browser. Close the socket and wait for them to open it again
                if was_connected:
                    was_connected = False
                    self.record_url(None)