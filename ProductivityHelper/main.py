# Code to open JSON
import json

def jsonimport():
    with open('weekschedule.json') as json_file:
        weekDict = json.load(json_file)
    return weekDict

import sys
import sqlite3
import hashlib
import random
from datetime import date
from datetime import datetime
from datetime import timedelta
import threading

from openpyxl import Workbook

import excelLinearConverter.excelLinearConverterModule
import twitterCollector.twitterCollector as tc
import weekScheduleSelector.weekScheduleSelector as wss
import digital_clock.digital_clock as dc
import excelLinearConverter.ssdClass as ssd
import webExtension.webConnect as wc
import activityDisplayer.activityDisplayer as ad
import softwareTracker.softwareTracker as st
import graphModule.dataGraph as dg

from PyQt5.QtCore import QTimer,QDateTime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QMainWindow, QAction, QWidget

# Boiler plate code with Main Window class from https://youtu.be/Vq1laKeSk9M
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from UI.Ui_MainWindow import Ui_MainWindow
class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.excellocation = "excelLinearConverter\TemplateExcelforCodeUpdated.xlsx"
        self.excelhash = self.hash(self.excellocation)
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)

        

        self.ui.homeButton.clicked.connect(self.showHome) # Calls func to change stacked widget to home screen
        self.ui.scheduleButton.clicked.connect(self.showSchedule)
        self.ui.pushButton.clicked.connect(self.showGoals)
        self.ui.pushButton_6.clicked.connect(self.showHome)

        ### Threading handle
        self.endevent = threading.Event()
        self.softwareTracker = st.SoftwareTracker(self.endevent)

        self.selectedScheduleDisplayer = ssd.SelectedScheduleDisplayer(self.ui.scheduleTable, jsonimport(), self.ui.displayLabel)
        self.mainssd = ssd.mainSSD(self.ui.mainTable, jsonimport(), self.ui.displayLabelMain)

        self.clock = dc.DigitalClock(self.ui.labelClockDate, self.ui.labelClockTime)
        self.twitter= tc.Twitter(self.ui.labelTwitter)
        self.webConnection = wc.WebConnect()
        ### Start - Arthur Week Schedule Selector Code 
        self.activityDisplayer = ad.ActivityDisplayer(jsonimport(), self.ui.label11, self.ui.label12, self.ui.label13, self.ui.label21, self.ui.label22, self.ui.label23, self.softwareTracker, self.endevent, self.webConnection)

        labelList = [self.ui.weekLabel, self.ui.weekLabel_2, self.ui.weekLabel_3, self.ui.weekLabel_4, self.ui.weekLabel_5, self.ui.weekLabel_6, self.ui.weekLabel_7] # List to later easily iterate through assigned schedule label widgets
        self.scheduleSelector = wss.scheduleSelector(jsonimport(), self.ui.scheduleList, labelList, self.ui.editingLabel, self.selectedScheduleDisplayer, self.ui.scheduleTable) # Creating a schedule selector object that deals with selector ui, passes in widgets so selector object can access more easily 

        self.ui.confirmButton.clicked.connect(self.scheduleSelector.confirmClick) # Calls confirm click routine when confirm button pressed
        self.ui.scheduleList.itemClicked.connect(self.scheduleSelector.listClick) # Calls list click routine when an element on the list is pressed
        self.ui.excelButton.clicked.connect(self.scheduleSelector.excelClick) # Calls excel click routine when open excel button pressed

        ### 7 calls for 7 weekday buttons. Each button calls the same function but with a different paramater: the day it's meant to represent --- In future this should be cleaned up  
        self.ui.weekButton.clicked.connect(lambda: self.scheduleSelector.weekClick("Monday"))
        self.ui.weekButton_2.clicked.connect(lambda: self.scheduleSelector.weekClick("Tuesday"))
        self.ui.weekButton_3.clicked.connect(lambda: self.scheduleSelector.weekClick("Wednesday"))
        self.ui.weekButton_4.clicked.connect(lambda: self.scheduleSelector.weekClick("Thursday"))
        self.ui.weekButton_5.clicked.connect(lambda: self.scheduleSelector.weekClick("Friday"))
        self.ui.weekButton_6.clicked.connect(lambda: self.scheduleSelector.weekClick("Saturday"))
        self.ui.weekButton_7.clicked.connect(lambda: self.scheduleSelector.weekClick("Sunday"))

        ### End - Arthur Week Schedule Selector Code 
        self.mainssd.refresh()
        ## Code to allow our code to run concurrently - as long as they are called from main loop 
        self.timer=QTimer()
        self.timer.timeout.connect(self.mainloop)
        self.timer.start(1000)

        ### Code to make sure current day has db entry
        self.tabledb = sqlite3.connect('test.db')
        today = date.today().strftime("%d/%m/%Y")
        self.tabledb.execute('''
        INSERT OR IGNORE INTO MAIN (DAY, INTENDEDWORKTIME, DISTRACTIONTIME, EXERCISEINTENSITY, DAYSATISFACTION)
        VALUES (?, ?, ?, ?, ?)
        ''', (today,0, 0, 0, None))
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        self.tabledb.execute("UPDATE MAIN SET EXERCISEINTENSITY = ? WHERE DAY = ?", (random.randint(0, 10),d1))
        self.tabledb.commit()

        ### Ryan Day Satisfaction setup
        self.currtime = self.setCurrentTime()
        self.checktime = self.setCheckTime()

        ### Dump
        self.ui.dumpButton.clicked.connect(self.dumpDataButton)


        ### Graph
        self.graph = dg.DataGraph(self.ui.pushButton_exi, self.ui.pushButton_pro,  self.ui.pushButton_md,  self.ui.pushButton_tlt, self.ui.comboBox_days, self.ui.home)
        
        # self.can2 = dg.PlotCanvas(self.ui.home, width = 4, height = 5)
        # self.can2.move(0,0)

        ### Feedback labels 
        self.exipro = self.ui.exihelp
        self.mostdistgen = self.ui.genreminhelp
        self.leastdistpergen = self.ui.leastdisthelp
        
        self.exipro.setWordWrap(True)
        self.exipro.setStyleSheet("Font : 9pt")
        self.mostdistgen.setWordWrap(True)
        self.mostdistgen.setStyleSheet("Font : 9pt")
        self.leastdistpergen.setWordWrap(True)
        self.leastdistpergen.setStyleSheet("Font : 9pt")

        self.exilabel()
        #self.musiclabels()

        

        #################################################               ### For Edison ###
        ################################################################################################
        self.activitycombo = self.ui.comboBox
        self.inequalitycombo = self.ui.comboBox_2
        self.valueinput = self.ui.lineEdit
        self.starttimeinp = self.ui.dateEdit
        self.endtimeinp = self.ui.dateEdit_2
        self.confirm = self.ui.pushButton_2
        self.delete = self.ui.pushButton_5
        self.selected = self.ui.label_6
        self.currmode = self.ui.label_8
        self.createnew = self.ui.pushButton_4
        self.editongoing = self.ui.pushButton_3
        self.ongoinglist = self.ui.listWidget
        self.finishedlist = self.ui.listWidget_2

        self.confirm.clicked.connect(self.write)
        self.createnew.clicked.connect(lambda: self.setMode("create"))
        self.editongoing.clicked.connect(lambda: self.setMode("edit"))
        self.delete.clicked.connect(self.deleteItem)
        self.ongoinglist.itemClicked.connect(self.listClicked)
        self.item = None
        text = "(" + "18/04/2022" + " - " + "20/04/2022" + ") " + "Exercise Intensity" + " " + ">=" + " " + "4" + " " + "🏆"
        self.finishedlist.addItem(text)
        text = "(" + "13/04/2022" + " - " + "17/04/2022" + ") " + "Productivity" + " " + ">=" + " " + "90"
        self.finishedlist.addItem(text)
        text = "(" + "06/04/2022" + " - " + "12/04/2022" + ") " + "Productivity" + " " + ">=" + " " + "60" + " " + "🏆"
        self.finishedlist.addItem(text)

    def deleteItem(self):
        if(self.currmode.text() != "Current Mode: Create New" and self.item != None):
            for i in range (self.ongoinglist.count()):
                if self.ongoinglist.item(i) == self.item:
                    self.ongoinglist.takeItem(i)

    def write(self):
        if(self.valueinput.text() == ""):
            return
        if(self.currmode.text() != "Current Mode: Create New"):
            if(self.currmode.text() != "Current Mode: Create New" and self.item != None):
                
                text = "(" + str(self.starttimeinp.date().toString('dd/MM/yyyy')) + " - " + str(self.endtimeinp.date().toString('dd/MM/yyyy')) + ") " + self.activitycombo.currentText() + " " + self.inequalitycombo.currentText() + " " + self.valueinput.text()
                self.item.setText(text)
                self.listClicked(self.item)
                return "changed"
        else:
            text = "(" + str(self.starttimeinp.date().toString('dd/MM/yyyy')) + " - " + str(self.endtimeinp.date().toString('dd/MM/yyyy')) + ") " + self.activitycombo.currentText() + " " + self.inequalitycombo.currentText() + " " + self.valueinput.text()
            self.ongoinglist.addItem((text))
            # with open("ongoing.json", "r") as read_file:
            #     data = json.loads(read_file)
            # print(2)
            # data['items'] = data['items'] + text
            # print(3)
            # data2 = data['items'] + text
            # print(4)
            # with open('ongoing.json', 'w') as f:
            #     json.dump(data2, f)

            return "item added"



    
    def setMode(self, mode):
        if(mode == "create"):
            self.currmode.setText("Current Mode: Create New")
        else:
            self.currmode.setText("Current Mode: Edit Ongoing")

    def listClicked(self, item):
        if(self.currmode.text() == "Current Mode: Edit Ongoing"):
            self.item = item
            text = item.text().split()
            starttime = text[0].replace("(", "")
            endtime = text[2].replace(")", "")
            activitytype = text[3]
            if(activitytype == "Exercise"):
                activitytype = activitytype + " " + text[4]
                inequality = text[5]
                value = text[6]
            else:
                inequality = text[4]
                value = text[5]
            self.selected.setText((f"Selected:\n{starttime}\n{endtime}\n{activitytype}\n{inequality}\n{value}"))
        else:
            self.selected.setText("Selected:")
        
        self.inequalitycombo.setCurrentText(inequality)
        self.activitycombo.setCurrentText(activitytype)
        self.valueinput.setText(value)
        
        self.starttimeinp.setDate(datetime.strptime(starttime.replace(" ", ""), '%d/%m/%Y'))
        self.endtimeinp.setDate(datetime.strptime(endtime.replace(" ", ""), '%d/%m/%Y'))



        
        ################################################################################################
        #################################################               ### For Edison ###



    def exilabel(self):
        self.exipro.setText("Over the past 30 days your exercise intensity and productivity level had a positive correlation, keep going!")
        pass

    # def musiclabels(self):
    #     # Genre, TotalListen, DistractionListen, Percentage
    #     genres = [['Pop',0,0,0],['Metal',0,0,0], ['LoFi',0,0,0], ['Classical',0,0,0],['Rock',0,0,0],['HipHop',0,0,0], ['Electronic',0,0,0]]
    #     size = 7
    #     tabledb = sqlite3.connect('test.db')
    #     cursor = tabledb.cursor()
    #     today = date.today()
    #     d1 = today.strftime("%d/%m/%Y")
    #     for i in range(size):
    #         curr = today - timedelta(days=i)
    #         d1 = curr.strftime("%d/%m/%Y")
    #         if(self.graph.daypresent(d1, "MUSIC")):
    #             for genre in genres:
    #                 cursor.execute("SELECT TOTALLISTENTIME FROM MUSIC WHERE DATE = ? AND GENRE = ?", (d1, genre[0]))
    #                 genre[1] += float(cursor.fetchone()[0])
    #                 cursor.execute("SELECT DISTLISTENTIME FROM MUSIC WHERE DATE = ? AND GENRE = ?", (d1, genre[0]))
    #                 genre[2] += float(cursor.fetchone()[0])
    #         else:
    #             pass
    #     for genre in genres:
    #         if genre[1] != 0:
    #             genre[3] = (float(genre[2])/float(genre[1])) * 100
    #         else:
    #             genre[3] = 0
        
    #     minperc = min([[genre[3],genre[0]] for genre in genres if genre[1]!=0])
    #     maxminu = max([[genre[2],genre[3],genre[0]] for genre in genres])

    #     self.mostdistgen.setText(f"The largest volume of your distraction minutes over past week the came from {maxminu[2]} music, which has {int(maxminu[0]/60)} minutes overlapping with distractions. Listening to {maxminu[2]} had a {int(maxminu[1])}% distraction correlation rate. Perhaps listen to {maxminu[2]} music less in order to increase productivity.")
    #     self.leastdistpergen.setText(f"The genre you listened to with the smallest percentage of distraction minutes was {minperc[1]}, with a distraction percentage of {int(minperc[0])}%. Less distractions occur when you listen to {minperc[1]}, perhaps switch your music consumption to {minperc[1]} to improve productivity.")
    #     # print(minperc, maxminu)
    #     # print(genres)
        
    
    @staticmethod
    def setCheckTime():  # Gather from .txt file
        f = open("DS.txt", "r")
        time = f.readline()
        f.close()
        return time

    @staticmethod
    def setCurrentTime():  # Set current time
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        return current_time 
         
    def getCheckTime(self):
        return self.currtime == self.checktime
    
    def popupmanage(self):
        self.currtime = self.setCurrentTime()
        self.checktime = self.setCheckTime()
        today = date.today().strftime("%d/%m/%Y")
        mybool = self.tabledb.execute("SELECT EXISTS (SELECT 1 FROM MAIN WHERE DAY = ? AND DAYSATISFACTION IS NOT NULL)", (today,))
        booly = []
        for row in mybool:
            booly.append(row)

        if self.getCheckTime()and not booly[0][0]:
            nums = [str(i) for i in range(1, 11)]
            # Data to be stored = s_num
            s_num, done1 = QtWidgets.QInputDialog.getItem(
                self, 'Daily Satisfaction', 'How satisfied are you with your day? (1-10):', nums)
            self.tabledb.execute("UPDATE MAIN SET DAYSATISFACTION = ? WHERE DAY = ?", (s_num, today))
            self.tabledb.commit()

    def show(self):
        self.main_win.show()

    def hash(self, location): # https://nitratine.net/blog/post/how-to-hash-files-in-python/
        file_hash = hashlib.sha256()
        size = 65536 
        with open(location, 'rb') as f:
            fb = f.read(size)
            while len(fb) > 0:
                file_hash.update(fb) 
                fb = f.read(size) 
        return file_hash.hexdigest()

    def hashcheck(self):
        currenthash = self.hash(self.excellocation)
        if currenthash != self.excelhash:
            #print("change made")
            self.mainssd.refresh()
            self.selectedScheduleDisplayer.refresh()
            self.scheduleSelector.listWidgetUpdater()
            self.excelhash = currenthash

            ##
            self.activityDisplayer.groupRefresh()
            self.activityDisplayer.refreshChangeCheck()
    

    def showHome(self): # Function to change to home on stacked widget
        self.mainssd.refresh()
        self.ui.stackedWidget.setCurrentWidget(self.ui.home)

    def showGoals(self): # Function to change to goals on stacked widget
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
    
    
    def showSchedule(self): # Funciton to change to schedule ui on stacked widget - more complicated as ui elements need to be refreshed to default
        self.scheduleSelector.refresh() ## Change current selection focus date to current day 
        self.selectedScheduleDisplayer.refresh() ## Refresh SSD with today's schedule
        self.ui.stackedWidget.setCurrentWidget(self.ui.schedule)
        self.selectedScheduleDisplayer.colourupdate()

    def mainloop(self):
        self.popupmanage()
        self.selectedScheduleDisplayer.colourupdate()
        self.mainssd.colourupdate()
        self.clock.redrawClock()
        self.activityDisplayer.checkCurrent()
        self.activityDisplayer.checkNext()
        self.hashcheck()
        self.activityDisplayer.groupRefresh()

    def dumpDataButton(self):
        excellocation = "output.xlsx"
        wb = Workbook()
        ws = wb.active
        result = self.tabledb.execute("select * from MAIN")
        for i, row in enumerate(result):
            ws.append(row)
        wb.save(excellocation)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()

    r = app.exec_()
    if main_win.activityDisplayer.currentactivity != None:
        main_win.activityDisplayer.endPeriod()
    sys.exit(r)
    # sys.exit(app.exec_())
