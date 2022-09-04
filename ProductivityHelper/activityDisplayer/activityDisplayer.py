from datetime import date
from datetime import datetime
from datetime import timedelta
import calendar
import os
from pathlib import Path
from excelLinearConverter.excelLinearConverterModule import excelToLinear
from win10toast import ToastNotifier
from main import jsonimport
import random
import sqlite3

class ActivityDisplayer():
    def __init__(self, jsondict, label11, label12, label13, label21, label22, label23, st, endevent, wt):
        ## [Current Activity:, Activity:, Time Period], [Next Activity:, Activity:, Time Period]
        self.labellist = [[label11, label12, label13], [label21, label22, label23]]
        self.labellist[0][0].setText("Current Activity:")
        self.labellist[0][1].setText("")
        self.labellist[0][2].setText("")
        
        self.labellist[1][0].setText("Next Activity:")
        self.labellist[1][1].setText("")
        self.labellist[1][2].setText("")
        self.wt = wt
        self.st = st
        self.endevent = endevent

        self.excelLocation = os.path.join(Path().absolute(), Path("excelLinearConverter\TemplateExcelforCodeUpdated.xlsx"))
        self.scheduledict = jsondict
        # self.activitystart = None
        # self.activityend = None
        self.currentactivity = None
        worksheet_name = self.scheduledict.get(calendar.day_name[date.today().weekday()])
        #print(worksheet_name)
        self.linearData = excelToLinear(worksheet_name)
        self.activitygroups = self.activityGrouper(self.linearData)
        self.toaster = ToastNotifier()
        self.checkCurrent()
        self.checkNext()
        
        
        
    
    def activityGrouper(self, linearData):
        start = 0
        activity = False
        groups = []
        alldata = linearData[0]
        for count, slot in enumerate(alldata):
            #print(slot[1])
            if slot[1] == 'Studying':
                if activity == False:
                    
                    start = count
                    activity = True
            else:
                if activity == True:
                    activity = False
                    ## Beginning would be start index, end would be current index 
                    groups.append([alldata[start][0], alldata[count][0]])

        if activity == True:
            groups.append([alldata[start][0], '00:00:00'])
        
        return groups

    def checkCurrent(self):
        # print(self.currentactivity)
        ## Finding current if none already assigned
        # if self.currentactivity != None:
        #     checkbool = False
        #     # print(self.currentactivity)
        #     # print(self.activitygroups)
        #     for activity in self.activitygroups:
        #         if self.currentactivity[1] in activity:
        #             checkbool = True

        #     if checkbool == False: 
        #         self.endPeriod()
                
        if self.currentactivity == None:
            periodfound = False
            for period in self.activitygroups:
                current_time = datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S")
                # print(period)
                # print(datetime.strptime(period[0], "%H:%M:%S"), datetime.strptime(period[1], "%H:%M:%S"))
                if current_time >= datetime.strptime(period[0], "%H:%M:%S") and current_time <= datetime.strptime(period[1], "%H:%M:%S"):
                    sentperiod = [datetime.now().strftime("%H:%M:%S"), period[1]]
                    self.startPeriod(sentperiod)
        else:
            current_time = datetime.strptime(datetime.now().strftime("%H:%M:%S"), "%H:%M:%S") 
            if current_time >= datetime.strptime(self.currentactivity[1], "%H:%M:%S"):
                self.endPeriod()
        
    def refreshChangeCheck(self):

        pass

    def groupRefresh(self):
        self.scheduledict = jsonimport()
        worksheet_name = self.scheduledict.get(calendar.day_name[date.today().weekday()])
        self.linearData = excelToLinear(worksheet_name)
        # print("#########")
        # print(self.linearData)
        # print("#########")
        self.activitygroups = self.activityGrouper(self.linearData)

    def checkNext(self):
        if self.currentactivity != None:
            endtime = datetime.strptime(self.currentactivity[1], "%H:%M:%S")
            nextperiod = None
            for period in self.activitygroups:
                if datetime.strptime(period[0], "%H:%M:%S") > endtime:
                    nextperiod = period
                    break
            #print("next:", nextperiod)
        else:
            current_time = datetime.strptime(datetime.now().strftime("%H:%M"), "%H:%M")
            nextperiod = None
            for period in self.activitygroups:
                #print(datetime.strptime(period[0], "%H:%M:%S"))
                if datetime.strptime(period[0], "%H:%M:%S") > current_time:
                    nextperiod = period
                    break
            #print("next:", nextperiod)
        
        if nextperiod == None:
            self.labellist[1][1].setText("")
            self.labellist[1][2].setText("")
        else:
            self.labellist[1][1].setText("Work")
            self.labellist[1][2].setText(nextperiod[0][0:5] + " - " + nextperiod[1][0:5])    


    def startPeriod(self, activity):
        self.currentactivity = activity
        #print("starting", datetime.now(), self.currentactivity)
        self.labellist[0][1].setText("Work")
        self.labellist[0][2].setText(self.currentactivity[0][0:5] + " - " + self.currentactivity[1][0:5])       

        self.toaster.show_toast("Work Period Started",self.currentactivity[0][0:5] + " - " + self.currentactivity[1][0:5], duration=3, threaded=True)

        # Notification and create activity variable 
        self.st.thread_start()
        self.wt.start_period()
        pass

    def endPeriod(self):
        # Set end period event to true for other threads to notice
        self.wt.end_period()
        self.endevent.set()
        

        # Notification and None activity variable 
        self.labellist[0][1].setText("")
        self.labellist[0][2].setText("")
        self.toaster.show_toast("Work Period Ended",self.currentactivity[0][0:5] + " - " + self.currentactivity[1][0:5], duration=3, threaded=True)
        self.currentactivity = None
        
        # While the software tracker finish flag has not been set to True, then just wait 
        while self.st.finish != True:
            print("Waiting")
            pass

        # Print the software tracker's list attribute
        # if self.st.distractionlist != None:
        #     print(self.st.distractionlist)
        # pass

        # Set event to false
        self.endevent.clear()

        

        tabledb = sqlite3.connect('test.db')
        cursor = tabledb.cursor()

        ### Example software distraction list - would be replaced by sparsh code
        softwarelist = [[datetime(2022, 4, 3, 12, 51, 42, 565252), datetime(2022, 4, 3, 12, 55, 44, 315510), 'Code'],
                        [datetime(2022, 4, 3, 12, 45, 45, 105640), datetime(2022, 4, 3, 12, 49, 46, 310069), 'Code'],
                        [datetime(2022, 4, 3, 12, 56, 49, 689262), datetime(2022, 4, 3, 13, 12, 18, 665625), 'Discord'],
                        [datetime(2022, 4, 3, 12, 30, 18, 773769), datetime(2022, 4, 3, 12, 32, 19, 427968), 'Code']]

        ### Example website distraction list - would be replaced by Theo code
        weblist = [[datetime(2022, 4, 3, 12, 24, 42, 565252), datetime(2022, 4, 3, 12, 48, 44, 315510), 'Reddit'],
                        [datetime(2022, 4, 3, 12, 14, 45, 105640), datetime(2022, 4, 3, 12, 22, 46, 310069), 'BBC'],
                        [datetime(2022, 4, 3, 12, 49, 49, 689262), datetime(2022, 4, 3, 13, 8, 18, 665625), 'Amazon'],
                        [datetime(2022, 4, 3, 12, 59, 18, 773769), datetime(2022, 4, 3, 13, 5, 19, 427968), 'Reddit']]

        softwarelist = self.st.distractionlist
        print(softwarelist)
        weblist = self.wt.get_data()
        print(weblist)

        ### Gather time stamps from both lists, creating list of time stamps
        mergelisttimes = []
        for entry in softwarelist:
            mergelisttimes.append([entry[0], entry[1]])

        for entry in weblist:
            mergelisttimes.append([entry[0], entry[1]])

        # Sort list in order of start time to prep it for merging 
        sortedmergelist = sorted(mergelisttimes)

        ## https://stackoverflow.com/questions/34797525/how-to-correctly-merge-overlapping-datetime-ranges-in-python
        finalmergelist = []
        tempold = sortedmergelist[0]
        for t in sortedmergelist[1:]:
            if tempold[1] >= t[0]: 
                tempold = ((min(tempold[0], t[0]), max(tempold[1], t[1])))
            else:
                finalmergelist.append(tempold)
                tempold = t
        else:
            finalmergelist.append(tempold)

        #print(finalmergelist)

        # Calculate the total amount of time spent on distractions (cumulate all of the times in the merge list)
        timeinthold = datetime.strptime('00:00:00',"%H:%M:%S")
        for entry in finalmergelist:
            interval = entry[1] - entry[0]
            timeinthold+=interval

        ## A helper function for the mock data to split a listen time (distraction or work time) into different genres
        def songassign(time):
            mydelta = timedelta(hours=time.hour, minutes = time.minute, seconds = time.second, microseconds = time.microsecond)
            # print(mydelta.seconds)
            secondcounter = mydelta.seconds
            genres = [['Pop',0],['Metal',0], ['LoFi',0], ['Classical',0],['Rock',0],['HipHop',0], ['Electronic',0]]
            exit = False
            while not exit:
                chunk = random.uniform(0.1, 0.4) * mydelta.seconds
                secondcounter -= chunk
                if secondcounter < 0:
                    chunk += secondcounter
                    index = random.randrange(0, len(genres)-1)
                    genres[index][1] += chunk
                    break
                else:
                    index = random.randrange(0, len(genres)-1)
                    genres[index][1] += chunk
            return genres

        tempwork = datetime.strptime('00:00:00',"%H:%M:%S")

        workstart = datetime(2022, 4, 3, 12, 00, 00, 105640) # Would be replaced by activity start time
        workend = datetime(2022, 4, 3, 13, 15, 00, 105640) # would be replacedb by current time 
        worktime = tempwork + (workend - workstart)
        distractiontime = timeinthold
        zerotime = datetime.strptime('00:00:00',"%H:%M:%S")
        distmusic = random.uniform(0.5, 0.75) * (distractiontime - zerotime) + zerotime ### amount of distraction time on music 
        workmusic = random.uniform(0.25, 0.5) * (worktime - zerotime) + zerotime ### amount of work time on music 
        #print("work", worktime.time(), workmusic.time())
        #print("distraction", distractiontime.time(), distmusic.time())
        workgenres = songassign(workmusic.time())
        distractiongenres = songassign(distmusic.time())
        # print(workgenres)
        # print(distractiongenres)
        # print(datetime.timedelta(seconds=(workgenres[0][1]+distractiongenres[0][1])))

        today = date.today()
        d1 = today.strftime("%d/%m/%Y")

        for entry in zip(workgenres, distractiongenres): #Add on the activity listen times to appropriate genres
            cursor.execute("SELECT GENRE FROM MUSIC WHERE DATE = ? AND GENRE = ?", (d1,entry[0][0]))
            data=cursor.fetchall()
            # print(entry[0][0], len(data))
            if len(data) == 0:
                tabledb.execute("INSERT INTO MUSIC VALUES(?,?,?,?)", (d1, entry[0][0], 0, 0))

            cursor.execute("SELECT TOTALLISTENTIME FROM MUSIC WHERE DATE = ? AND GENRE = ?", (d1,entry[0][0]))
            newtotal = (float(cursor.fetchone()[0]) + entry[0][1] + entry[1][1])
            tabledb.execute("UPDATE MUSIC SET TOTALLISTENTIME = ? WHERE DATE = ? AND GENRE = ?", (newtotal,d1,entry[0][0]))
            cursor.execute("SELECT DISTLISTENTIME FROM MUSIC WHERE DATE = ? AND GENRE = ?", (d1,entry[0][0]))
            newdist = (float(cursor.fetchone()[0]) + entry[1][1])
            tabledb.execute("UPDATE MUSIC SET DISTLISTENTIME = ? WHERE DATE = ? AND GENRE = ?", (newdist,d1,entry[0][0]))

        ## Add on total distraction and intended work time 
        wtime = (worktime.time())
        wdelta = timedelta(hours=wtime.hour, minutes = wtime.minute, seconds = wtime.second)
        # print(wdelta.seconds)
        dtime = (distractiontime.time())
        ddelta = timedelta(hours=dtime.hour, minutes = dtime.minute, seconds = dtime.second)
        # print(ddelta.seconds)
        cursor.execute("SELECT INTENDEDWORKTIME FROM MAIN WHERE DAY = ?", (d1,))
        newwt = (float(cursor.fetchone()[0]) + wdelta.seconds)
        tabledb.execute("UPDATE MAIN SET INTENDEDWORKTIME = ? WHERE DAY = ?", (newwt,d1))
        cursor.execute("SELECT DISTRACTIONTIME FROM MAIN WHERE DAY = ?", (d1,))
        newdt = (float(cursor.fetchone()[0]) + ddelta.seconds)
        tabledb.execute("UPDATE MAIN SET DISTRACTIONTIME = ? WHERE DAY = ?", (newdt,d1))

        tabledb.commit()







# data = self.table.item(row, column).text()
# now = datetime.now()
# time_slot = datetime.strptime(data, "%H:%M")
# current_time = datetime.strptime(now.strftime("%H:%M"), "%H:%M")
# if current_time >= time_slot and current_time <= time_slot + timedelta(minutes=14):
#     self.table.item(row, column).setBackground(QtGui.QColor(255,153,187))