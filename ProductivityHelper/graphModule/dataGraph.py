from calendar import c
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QComboBox, QGridLayout, QButtonGroup, QSizePolicy
from PyQt5 import QtCore
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import random
import sqlite3
from datetime import date
import numpy as np
import datetime

# https://www.youtube.com/watch?v=d663N2xTxO0
class PlotCanvas(FigureCanvas):
    def __init__(self, parent = None, width = 5, height = 4, dpi = 100):
        
        self.figure = Figure(figsize = (width, height), dpi=dpi)
        #self.axes = self.figure.add_subplot(111)
        self.figurePlot = self.figure.subplots()
        self.X = self.figurePlot.twinx()
        FigureCanvas.__init__(self,self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes = self.figure.axes

class DataGraph():
    def __init__(self, button, button1, button2, button3, combo, mainwin):
        self.button = button
        self.button.setCheckable(True)
        #self.button.clicked.connect(lambda: self.plot(self.sampleData(self.checkCombo()), self.button, "Exercise Intensity")) #self.button.clicked.connect(self.plot(getDaySatisfaction(self.checkCombo)))
        self.button.clicked.connect(lambda: self.plot(self.exiData(self.checkCombo()), self.button, "Exercise Intensity"))

        self.button2 = button1
        self.button2.setCheckable(True)
        #self.button2.clicked.connect(lambda: self.plot(self.sampleData(self.checkCombo()), self.button2,  "Productivity"))
        self.button2.clicked.connect(lambda: self.plot(self.proData(self.checkCombo()), self.button2,  "Productivity"))


        self.button3 = button2
        self.button3.setCheckable(True)
        #self.button3.clicked.connect(lambda: self.plot(self.sampleData(self.checkCombo()), self.button3, "Music Distractions"))
        self.button3.clicked.connect(lambda: self.plot(self.mdData(self.checkCombo()), self.button3, "Music Distractions"))

        self.button4 = button3
        self.button4.clicked.connect(lambda: self.plot(self.sampleData(self.checkCombo()), self.button4, "Total Listen Time"))

        self.comboBox = combo
        self.comboBox.addItem("Last 7 days")
        self.comboBox.addItem("Last 14 days")
        self.comboBox.addItem("Last 30 days")
        self.comboBox.currentTextChanged.connect(self.on_combobox_changed) #function called anytime the value of combobox is changed
        
        self.canvas = PlotCanvas(mainwin, width = 5, height = 4)
        self.canvas.move(10,80)
        self.canvas.resize(470, 470)

        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.button, 1)
        self.buttonGroup.addButton(self.button2, 2)
        self.buttonGroup.addButton(self.button3, 3)
        self.buttonGroup.addButton(self.button4, 4)
        self.buttonGroup.setExclusive(False)

        self.showing = [None, None]

    def plot(self, xData, buttonPressed, yLabel):

        if buttonPressed.isChecked() == False: #this means the button pressed was untoggled
            #button pressed represents the first plot so remove it's line and axis
            if self.showing[0] == buttonPressed:
                self.showing[0] = None
                self.canvas.axes[0].lines.pop(0)
                self.canvas.axes[0].get_yaxis().set_visible(False)
                self.canvas.draw()    
                return
            else:
                #button pressed represents the second plot so remove it's line and axis
                self.showing[1] = None
                self.canvas.axes[1].lines.pop(0)
                self.canvas.axes[1].get_yaxis().set_visible(False)
                self.canvas.draw()   
                return

        numberOfDays = self.checkCombo() #get the number of days needed to be shown
        days = np.zeros(numberOfDays)
        #generate days, will need to decide how to represent the days
        for i in range(numberOfDays):
            days[i] = i

        if (self.showing[0] != None and self.showing[1] != None):
            buttonPressed.toggle() #two plots are already showing so untoggle the button that was just pressed
            return
        else:
            if (self.showing[0] != None or self.showing[1] != None):
                #the first plot is empty so plot data onto the first plot
                if self.showing[0] == None:
                    ax = self.canvas.figurePlot
                    ax.plot(days, xData, color='#646496')
                    ax.set_ylabel(yLabel, color='#646496')
                    self.canvas.axes[0].get_yaxis().set_visible(True)
                    self.canvas.draw()    
                    self.showing[0] = buttonPressed
                else:
                    #the second plot is empty so plot data onto the second plot
                    if self.showing[1] == None:
                        ax2 = self.canvas.X
                        ax2.plot(days, xData, color='#FF99BB')
                        ax2.set_ylabel(yLabel, color='#FF99BB')
                        self.canvas.axes[1].get_yaxis().set_visible(True)
                        self.canvas.draw()
                        self.showing[1] = buttonPressed
                    else:
                        return
            else:
                #both plots are empty
                ax = self.canvas.figurePlot
                ax.plot(days, xData, color='#646496')
                ax.set_xlabel('Days')
                ax.set_ylabel(yLabel, color='#646496')
                self.canvas.axes[0].get_yaxis().set_visible(True)
                self.canvas.draw()
                self.showing[0] = buttonPressed
            #scale
            self.canvas.figurePlot.relim()
            self.canvas.figurePlot.autoscale_view()
            self.canvas.X.relim()
            self.canvas.X.autoscale_view()
            self.canvas.draw()

    def checkCombo(self):
        value = self.comboBox.currentText()
        if(value == "Last 7 days"):
            return 7 
        else:
            if(value == "Last 14 days"):
                return 14
            else:
                if(value == "Last 30 days"):
                    return 30

    def on_combobox_changed(self):
        numberOfDays = self.checkCombo()
        days = np.zeros(numberOfDays)
        for i in range(numberOfDays):
            days[i] = i

        if self.showing[0] != None and self.showing[1] != None:
            #both plots already have data so plot the existing data to the new data range
            self.canvas.axes[0].lines.pop(0)
            self.canvas.axes[0].get_yaxis().set_visible(False)
            self.canvas.axes[0].get_xaxis().set_visible(False)
            self.canvas.axes[1].lines.pop(0)
            self.canvas.axes[1].get_yaxis().set_visible(False)
            self.canvas.axes[1].get_xaxis().set_visible(False)
            ax = self.canvas.figurePlot
            ax.plot(days, self.sampleData(numberOfDays), color='#646496')
            ax.set_xlabel('Days')
            ax.set_ylabel('Y1 data', color='#646496')
            ax2 = self.canvas.X
            ax2.plot(days, self.sampleData(numberOfDays), color='#FF99BB')
            ax2.set_ylabel('Y2 data', color='#FF99BB')
            self.canvas.axes[0].get_yaxis().set_visible(True)
            self.canvas.axes[1].get_yaxis().set_visible(True)
            self.canvas.axes[0].get_xaxis().set_visible(True)
            self.canvas.axes[1].get_xaxis().set_visible(True)
            ax.relim()
            ax.autoscale_view()
            ax2.relim()
            ax2.autoscale_view()
            self.canvas.draw()
        else:
            #second plot already has data so plot the existing data to the new data range
            if self.showing[0] == None and self.showing[1] != None:
                self.canvas.axes[1].lines.pop(0)
                self.canvas.axes[1].get_yaxis().set_visible(False)
                self.canvas.axes[1].get_xaxis().set_visible(False)
                ax2 = self.canvas.X
                ax2.plot(days, self.sampleData(numberOfDays), color='#FF99BB') #will probably end up calling function to get data or slicing existing array
                ax2.set_ylabel('Y2 data', color='#FF99BB')
                self.canvas.axes[1].get_yaxis().set_visible(True)
                self.canvas.axes[1].get_xaxis().set_visible(True)
                ax2.relim()
                ax2.autoscale_view()
                self.canvas.draw()
            else:
                #first plot already has data so plot the existing data to the new data range
                if self.showing[0] != None and self.showing[1] == None:
                    self.canvas.axes[0].lines.pop(0)
                    self.canvas.axes[0].get_yaxis().set_visible(False)
                    self.canvas.axes[0].get_xaxis().set_visible(False)
                    ax = self.canvas.figurePlot
                    ax.plot(days, self.sampleData(numberOfDays), color='#646496')
                    ax.set_xlabel('Days')
                    ax.set_ylabel('Y1 data', color='#646496')
                    self.canvas.axes[0].get_yaxis().set_visible(True)
                    self.canvas.axes[0].get_xaxis().set_visible(True)
                    ax.relim()
                    ax.autoscale_view()
                    self.canvas.draw()
                else:
                    self.canvas.figurePlot.relim()
                    self.canvas.figurePlot.autoscale_view()
                    return
        self.canvas.figurePlot.relim()
        self.canvas.figurePlot.autoscale_view()
        self.canvas.X.relim()
        self.canvas.X.autoscale_view()
        self.canvas.draw()

    #random dataset
    def sampleData(self, size):
        data = np.zeros(60)
        for i in range(60):
            data[i] = random.randint(0, 30)
        return data[:size]


    def daypresent(self, day, table):
        tabledb = sqlite3.connect('test.db')
        cursor = tabledb.cursor()
        if table == "MAIN":
            cursor.execute("SELECT DAY FROM MAIN WHERE DAY = ?", (day,))
        elif table == "MUSIC":
            cursor.execute("SELECT DATE FROM MUSIC WHERE DATE = ?", (day,))
        data=cursor.fetchall()
        if len(data) == 0:
            return False
            
        else:
            return True

        pass

    def exiData(self, size):
        ml =[]
        tabledb = sqlite3.connect('test.db')
        cursor = tabledb.cursor()
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        for i in range(size):
            curr = today - datetime.timedelta(days=i)
            d1 = curr.strftime("%d/%m/%Y")
            if(self.daypresent(d1, "MAIN")):
                cursor.execute("SELECT EXERCISEINTENSITY FROM MAIN WHERE DAY = ?", (d1,))
                ml.append(cursor.fetchone()[0])
            else:
                ml.append(0)
        #print(ml)
        return (ml)
        return self.sampleData(size)
        pass

    def proData(self, size):
        ml =[]
        tabledb = sqlite3.connect('test.db')
        cursor = tabledb.cursor()
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        for i in range(size):
            curr = today - datetime.timedelta(days=i)
            d1 = curr.strftime("%d/%m/%Y")
            if(self.daypresent(d1, "MAIN")):
                cursor.execute("SELECT INTENDEDWORKTIME FROM MAIN WHERE DAY = ?", (d1,))
                iwt = cursor.fetchone()[0]
                cursor.execute("SELECT DISTRACTIONTIME FROM MAIN WHERE DAY = ?", (d1,))
                dt = cursor.fetchone()[0]
                prod = (1-(float(dt)/float(iwt)))*100
                ml.append(prod)
            else:
                ml.append(0)
        #print(ml)
        return (ml)
        
        pass

    def mdData(self, size):
        ml =[]
        tabledb = sqlite3.connect('test.db')
        cursor = tabledb.cursor()
        today = date.today()
        d1 = today.strftime("%d/%m/%Y")
        for i in range(size):
            curr = today - datetime.timedelta(days=i)
            d1 = curr.strftime("%d/%m/%Y")
            if(self.daypresent(d1, "MUSIC")):
                cursor.execute("SELECT SUM(TOTALLISTENTIME) FROM MUSIC WHERE DATE = ?", (d1,))
                iwt = cursor.fetchone()[0]
                cursor.execute("SELECT SUM(DISTLISTENTIME) FROM MUSIC WHERE DATE = ?", (d1,))
                dt = cursor.fetchone()[0]
                prod = ((float(dt)/float(iwt)))*100
                ml.append(prod)
            else:
                ml.append(0)
        #print(ml)
        return (ml)