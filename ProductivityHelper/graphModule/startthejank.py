from calendar import c
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QComboBox, QGridLayout, QButtonGroup, QSizePolicy
from PyQt5 import QtCore
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import random

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

        #self.plot()

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setFixedSize(1280, 900)

        #self.figure = plt.figure()
        #self.figurePlot = self.figure.subplots() #add suplot to figure
        #self.X = self.figurePlot.twinx() #second y will use the same x axis

        # self.canvas = FigureCanvas(self.figure)

        #1##################################################################
        #setting buttons and checkable i.e toggleable
        #when clicked, they call plot and pass in data for the amount of days in the combo box into the plot function with the name of the data
        #my idea is that for each function that gets data, it gets a parameter based on the data range that the graph will show and returns that data range
        self.button = QPushButton('Day Satisfaction')
        self.button.setCheckable(True)
        self.button.clicked.connect(lambda: self.plot(self.sampleData(self.checkCombo()), self.button, "Day Satisfaction")) #self.button.clicked.connect(self.plot(getDaySatisfaction(self.checkCombo)))

        self.button2 = QPushButton('Excersie Intensity')
        self.button2.setCheckable(True)
        self.button2.clicked.connect(lambda: self.plot(self.sampleData(self.checkCombo()), self.button2,  "Exercise Intensity"))

        self.button3 = QPushButton('Total Intended Work')
        self.button3.setCheckable(True)
        self.button3.clicked.connect(lambda: self.plot(self.sampleData(self.checkCombo()), self.button3, "Total Intended Work"))

        self.button4 = QPushButton('Total Effective Work')
        self.button4.clicked.connect(self.plot)

        self.button5 = QPushButton('Total Distraction Time')
        self.button5.clicked.connect(self.plot)

        self.comboBox = QComboBox()
        self.comboBox.addItem("Last 7 days")
        self.comboBox.addItem("Last 30 days")
        self.comboBox.addItem("Last 60 days")
        self.comboBox.currentTextChanged.connect(self.on_combobox_changed) #function called anytime the value of combobox is changed
        #2##################################################################

        #1##################################################################
        self.canvas = PlotCanvas(self, width = 5, height = 4)
        self.canvas.move(10,100)
        #2##################################################################

        layout = QGridLayout()
        self.comboBox.setFixedWidth(500)
        self.comboBox.setFixedHeight(40)
        self.button.setFixedHeight(50)
        self.button.setFixedWidth(50)
        self.button2.setFixedHeight(50)
        self.button2.setFixedWidth(50)
        self.button3.setFixedHeight(50)
        self.button3.setFixedWidth(50)
        self.button4.setFixedHeight(50)
        self.button4.setFixedWidth(50)
        self.button5.setFixedHeight(50)
        self.button5.setFixedWidth(50)
        # self.canvas.setFixedHeight(400)
        # self.canvas.setFixedWidth(500)
        # layout.addWidget(self.canvas)
        layout.addWidget(self.comboBox)
        layout.addWidget(self.button)
        layout.addWidget(self.button2, 2, 1)
        layout.addWidget(self.button3, 2, 2)
        layout.addWidget(self.button4, 2, 3)
        layout.addWidget(self.button5, 2, 4)
        layout.setRowMinimumHeight(50, 0)
        self.setLayout(layout)


        #1##################################################################
        self.buttonGroup = QButtonGroup()
        self.buttonGroup.addButton(self.button, 1)
        self.buttonGroup.addButton(self.button2, 2)
        self.buttonGroup.addButton(self.button3, 3)
        self.buttonGroup.addButton(self.button4, 4)
        self.buttonGroup.addButton(self.button5, 5)
        self.buttonGroup.setExclusive(False)
        #2##################################################################

        self.showing = [None, None] #variable used to keep track of which of the two axes are being showed

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
                    ax.plot(days, xData, color='g')
                    ax.set_ylabel(yLabel, color='g')
                    self.canvas.axes[0].get_yaxis().set_visible(True)
                    self.canvas.draw()    
                    self.showing[0] = buttonPressed
                else:
                    #the second plot is empty so plot data onto the second plot
                    if self.showing[1] == None:
                        ax2 = self.canvas.X
                        ax2.plot(days, xData, color='y')
                        ax2.set_ylabel(yLabel, color='y')
                        self.canvas.axes[1].get_yaxis().set_visible(True)
                        self.canvas.draw()
                        self.showing[1] = buttonPressed
                    else:
                        return
            else:
                #both plots are empty
                ax = self.canvas.figurePlot
                ax.plot(days, xData, color='g')
                ax.set_xlabel('Days')
                ax.set_ylabel(yLabel, color='g')
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
            if(value == "Last 30 days"):
                return 30
            else:
                if(value == "Last 60 days"):
                    return 60

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
            ax.plot(days, self.sampleData(numberOfDays), color='g')
            ax.set_xlabel('Days')
            ax.set_ylabel('Y1 data', color='g')
            ax2 = self.canvas.X
            ax2.plot(days, self.sampleData(numberOfDays), color='y')
            ax2.set_ylabel('Y2 data', color='y')
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
                ax2.plot(days, self.sampleData(numberOfDays), color='y') #will probably end up calling function to get data or slicing existing array
                ax2.set_ylabel('Y2 data', color='y')
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
                    ax.plot(days, self.sampleData(numberOfDays), color='g')
                    ax.set_xlabel('Days')
                    ax.set_ylabel('Y1 data', color='g')
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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    
    sys.exit(app.exec_())


