import sqlite3
tabledb = sqlite3.connect('test.db')
# tabledb.execute('''CREATE TABLE MAIN
#          (
#          DAY TEXT NOT NULL PRIMARY KEY UNIQUE,
#          INTENDEDWORKTIME TEXT NOT NULL,
#          DISTRACTIONTIME TEXT NOT NULL,
#          AVERAGEPERIODLENGTH TEXT NOT NULL,
#          EXERCISEINTENSITY DOUBLE NOT NULL,        
#          DAYSATISFACTION INT
#          );''')

# tabledb.execute('''
#         INSERT INTO MAIN(DAY, INTENDEDWORKTIME, DISTRACTIONTIME, AVERAGEPERIODLENGTH, EXERCISEINTENSITY, DAYSATISFACTION)
#         VALUES ('26/03/2022', '04:00:00', '01:33:04', '00:36:00', 9.6, 10)
#         ''')
# tabledb.commit()

tabledb.execute('''CREATE TABLE MUSIC
         (
         DATE TEXT NOT NULL,
         GENRE TEXT NOT NULL,
         TOTALLISTENTIME TEXT,
         DISTLISTENTIME TEXT,
         PRIMARY KEY(DATE, GENRE)
         );''')


# tabledb.execute('''CREATE TABLE Electronic
#          (
#          DAY TEXT NOT NULL PRIMARY KEY UNIQUE,
#          TOTALLISTENTIME TEXT NOT NULL,
#          DISTLISTENTIME TEXT NOT NULL
#          );''')

# tabledb.execute('''
#         INSERT INTO Electronic(DAY, TOTALLISTENTIME, DISTLISTENTIME)
#         VALUES ('26/03/2022', '01:05:00', '00:59:04')
#         ''')
tabledb.commit()


# tabledb.execute('''
#         INSERT INTO MAIN(DAY, INTENDEDWORKTIME, DISTRACTIONTIME, AVERAGEPERIODLENGTH, EXERCISEINTENSITY, DAYSATISFACTION)
#         VALUES ('27/03/2022', '03:00:00', '01:37:04', '00:22:00', 6, 6)
#         ''')
# tabledb.commit()

# tabledb.execute('''
#         INSERT INTO MAIN (DAY, INTENDEDWORKTIME, DISTRACTIONTIME, AVERAGEPERIODLENGTH, EXERCISEINTENSITY, DAYSATISFACTION)
#         VALUES ('28/03/2022', '12:00:00', '01:37:04', '00:22:00', 6, 6)
#         ''')
# tabledb.commit()

# from openpyxl import Workbook
# excellocation = "excelfile.xlsx"
# wb = Workbook()
# ws = wb.active


# c = tabledb.cursor()
# result = c.execute("select * from MAIN")
# for i, row in enumerate(result):
#     ws.append(row)

# wb.save(excellocation)