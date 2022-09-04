from excelLinearConverter import excelLinearConverterModule
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QAbstractItemView, QHeaderView, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt
import pandas as pd
from PyQt5 import QtGui
import json
import sys
from datetime import date
import calendar
from datetime import datetime
from datetime import timedelta
from main import jsonimport

class SelectedScheduleDisplayer():


    def __init__(self, table, jsondict, displayLabel):

        self.table = table
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.setSelectionMode(QAbstractItemView.NoSelection)

        self.scheduledict = jsondict
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.displayLabel = displayLabel

    def refresh(self):
        self.table.setRowCount(0)
        self.scheduledict = jsonimport()
        self.displayExcel(self.scheduledict.get(calendar.day_name[date.today().weekday()]))
        
        pass


    def colourupdate(self):
        for row in range(self.table.rowCount()):
            for column in range(self.table.columnCount()):
                if not column%2:
                    self.table.item(row, column).setBackground(QtGui.QColor(255,255,255))

                    data = self.table.item(row, column).text()
                    #print(data)
                    now = datetime.now()
                    time_slot = datetime.strptime(data, "%H:%M")
                    current_time = datetime.strptime(now.strftime("%H:%M"), "%H:%M")
                    if current_time >= time_slot and current_time <= time_slot + timedelta(minutes=14):
                        self.table.item(row, column).setBackground(QtGui.QColor(255,153,187))
                        

    def displayExcel(self, worksheet_name):
        self.displayLabel.setText("Currently Showing:   " + worksheet_name)
        linearData = excelLinearConverterModule.excelToLinear(worksheet_name)
        excel_file_dir = 'excelLinearConverter\\TemplateExcelforCodeUpdated.xlsx'
        wb = pd.read_excel(excel_file_dir, worksheet_name)
        if wb.size == 0:
            return
        wb.fillna('', inplace=True)
        self.table.setRowCount(16)
        self.table.setColumnCount(12)
        for i in range(17):
            self.table.setColumnWidth(i, 70)

        #Test = linearData[0]
        rowNum = 0
        for row in linearData[0]:
            rowNum = linearData[0].index(row)
            value = row[0]
            for col_index in range(1):
                ##print(rowNum)
                col_index = 0
                row_index = rowNum
                tableItem = QTableWidgetItem(str(value[:-3]))
                if(rowNum > 15):
                    ##print("hi2")
                    col_index = col_index + 2
                    row_index = row_index - 16
                if(rowNum > 31):
                    col_index = col_index + 2
                    row_index= row_index - 16
                if(rowNum > 47):
                    col_index = col_index + 2
                    row_index = row_index - 16
                if(rowNum > 63):
                    col_index = col_index + 2
                    row_index = row_index - 16
                if(rowNum > 79):
                    col_index = col_index + 2
                    row_index = row_index - 16
                if(rowNum > 95):
                    col_index = col_index + 2
                    row_index = row_index - 16

                self.table.setItem(row_index, col_index, tableItem)
                if (str(value) in linearData[1]):
                    self.table.setItem(row_index, col_index+1, QTableWidgetItem(str("")))
                    self.table.item(row_index, col_index+1).setBackground(QtGui.QColor(100,100,150))

        self.colourupdate()
        return 

class mainSSD(SelectedScheduleDisplayer):
    def __init__(self, table, jsondict, displayLabel):
        super().__init__(table, jsondict, displayLabel)

    def displayExcel(self, worksheet_name):
        self.displayLabel.setText("Currently Showing:   " + worksheet_name)
        linearData = excelLinearConverterModule.excelToLinear(worksheet_name)
        excel_file_dir = 'excelLinearConverter\\TemplateExcelforCodeUpdated.xlsx'
        wb = pd.read_excel(excel_file_dir, worksheet_name)
        if wb.size == 0:
            return
        wb.fillna('', inplace=True)
        self.table.setRowCount(24)
        self.table.setColumnCount(8)
        Test = linearData[0]
        rowNum = 0
        for row in linearData[0]:
            rowNum = linearData[0].index(row)
            value = row[0]
            for col_index in range(1):
                ##print(rowNum)
                col_index = 0
                row_index = rowNum
                tableItem = QTableWidgetItem(str(value[:-3]))
                if(rowNum > 23):
                    ##print("hi2")
                    col_index = col_index + 2
                    row_index = row_index - 24
                if(rowNum > 47):
                    col_index = col_index + 2
                    row_index= row_index - 24
                if(rowNum > 71):
                    col_index = col_index + 2
                    row_index = row_index - 24
                if(rowNum > 95):
                    col_index = col_index + 2
                    row_index = row_index - 24

                self.table.setItem(row_index, col_index, tableItem)
                if (str(value) in linearData[1]):
                    self.table.setItem(row_index, col_index+1, QTableWidgetItem(str("")))
                    self.table.item(row_index, col_index+1).setBackground(QtGui.QColor(100,100,150))

        self.colourupdate()
        #print(self.table.horizontalHeader().minimumSectionSize())
        self.table.horizontalHeader().setMinimumSectionSize(5)
        self.table.verticalHeader().setMinimumSectionSize(5)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        return 