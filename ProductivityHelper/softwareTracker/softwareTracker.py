import os
from win32gui import GetWindowText, GetForegroundWindow, FindWindow, GetWindowPlacement
import time
import keyboard
import psutil
import win32process
import pygetwindow as gw
import win32con
from datetime import datetime
import threading
## For Test
import keyboard

class SoftwareTracker():
    def __init__(self, event):
        self.endevent = event
        self.process_list = open("processes.txt", "r")
        self.processes_to_kill = self.process_list.read().split("\n")
        [distraction.lower() for distraction in self.processes_to_kill]
        self.current = None
        self.end = False
        self.temp = []
        self.distractionlist = []
        self.finish = False

    def thread_start(self):
        self.finish = False
        self.process_list = open("processes.txt", "r")
        self.processes_to_kill = self.process_list.read().split("\n")
        [distraction.lower() for distraction in self.processes_to_kill]
        self.current = None
        self.end = False
        self.temp = []
        self.distractionlist = []

        thread = threading.Thread(target = self.tracker_main)
        thread.setDaemon(True)
        thread.start()

    def tracker_main(self):
        while not self.end:
            time.sleep(0.1)
            if not self.current:
                self.create_check()
            else:
                self.ongoing_check()

            if self.endevent.is_set(): #### Really - if signal for end 
                self.end = True
        self.commit_entry()
        if not self.distractionlist:
            self.distractionlist = None
        self.finish = True

    def create_check(self):
        current_app_fullname = None
        try:
            current_app_fullname = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1])
        except:
            pass 
        if current_app_fullname != None:
            try:
                fullname = (current_app_fullname.name().replace(".exe", "").title())
                if fullname.lower() in self.processes_to_kill:
                    self.current = fullname
                    self.temp = [datetime.now(), None, self.current]
            except UnboundLocalError or ValueError:
                pass
            
    def ongoing_check(self):
        current_app_fullname = None
        try:
            current_app_fullname = psutil.Process(win32process.GetWindowThreadProcessId(GetForegroundWindow())[1])
        except psutil.NoSuchProcess:
            self.commit_entry() 
        if current_app_fullname:
            fullname = (current_app_fullname.name().replace(".exe", "").title())
            if fullname != self.current:
                self.commit_entry()
        
    def commit_entry(self):
        if self.current:
            self.temp[1] = datetime.now()
            self.distractionlist.append(self.temp)
            self.current = None
            print(self.distractionlist)
        



"""
####### When there is no ongoing active distraction process     ## when current = None
Get the active process name
If process within the distraction txt file
Then the process should be added to a temp list, later be added to the ongoing distraction list  
    this should be in the format [startime, endtime, softwarename]
    it should be initialised with [time.now, None, CurrentProcessName]
the processname should be saved as = current    ## no longer None   

So each time:

####### If there is an active distraction process, checking if it has ended, or if its continuing
Get active process name.
If active process name != current:      ## Current should start as None so it works 
    update the temp process list with the correct end time
    Then append that temp list to the full ongoing distraction list
    ## At this stage a process will have ended 
Else:
    Pass? - So it would be the same process so it can just continue

####### Emergency Ending function
End the current distraciton process if there is one and return the list - Called by the ending function

"""