import MySQLdb
from openpyxl import Workbook
from openpyxl import load_workbook
from datetime import date, datetime, timedelta
import daySchedulingFunctions
import AuxiliaryFunctions
import re

def checkIn(db, workerNameTuple, actualCheckInTime, location, date): #TODO: Decide if you should checkin based on worker name or username. If username, how do you populate the employeeinfo with all the usernames at the getgo?
	cursor = db.cursor()
	
	#get employee info.
	employeeQuery = ("SELECT id FROM employeeInfo WHERE firstName = %s AND lastName = %s")
	cursor.execute(employeeQuery, workerNameTuple)
	result = cursor.fetchone()
	employeeID = result[0]

	#get shift info.
	shiftQuery = ("SELECT id FROM shiftList WHERE checkinTime <= %s AND location = %s AND Date = %s "
					"ORDER BY id DESC LIMIT 1")
	cursor.execute(shiftQuery, (actualCheckInTime, location, date))
	
	result = cursor.fetchone()
	shiftID = result[0]


	#build and execute the actual checkin Query
	checkinQuery = ("UPDATE shiftEmployeeLinker SET checkedIn = TRUE, checkinTime = %s "
					"WHERE employeeID = %s AND shiftID = %s")




	try:
		cursor.execute(checkinQuery, (actualCheckInTime, employeeID, shiftID))
		db.commit()
	except Exception as e:
		print (cursor._last_executed)
		print (e)

	cursor.close()

def frontEndCheckIn():
	
	currentInfo = datetime.today()
	currentDate = currentInfo.strftime("%Y-%m-%d")
	checkinTime = currentInfo.strftime("%H:%M")
	#Figure out how to get location. Perhaps from IP? IN ANY CASE THIS IS A PLACEHOLDER.
	location = "CMC"

	#ALSO FIGURE OUT HOW TO GET THE WORKER NAME/ USERNAME. PRESUMABLY FROM THE LOGGING IN ITSELF

#TODO: FIGURE OUT HOW THIS FLOW SHOULD WORK
#current idea: have every worker login as the same "worker" account, then just deal with checkingin via the names.



def getSubRequestableShifts(db):#TODO- Modify to work based on username.       #This will get the list of shifts that are in the future that you can request subs for.
       currentInfo = datetime.today()
       #currentDate = currentInfo.strftime("%Y-%m-%d")
       #currentTime = currentInfo.strftime("%H:%M")
       currentDate = "2018/03/26"
       currentTime = "18:30"
       workerNameTuple = ("Alexis", "Engel")

       #first get employeeid
       cursor = db.cursor()
       shiftQuery = ("SELECT id from employeeinfo where firstName = %s and lastName = %s")
       cursor.execute(shiftQuery, workerNameTuple)
       result = cursor.fetchone()
       employeeID = result[0]

      #next get all possible shifts in the future that the employee can take using inner join
      subQuery = ("SELECT * FROM ShiftList "
                              "INNER JOIN ShiftEmployeeLinker "
                              "ON ShiftList.id = ShiftEmployeeLinker.shiftID "
                              "WHERE (ShiftEmployeeLinker.employeeID = %s "
                              "AND (ShiftList.date = %s AND ShiftList.checkinTime > %s) )"
                              "OR (ShiftEmployeeLinker.employeeID = %s AND ShiftList.date > %s)")
      try:
              subQueryData = (employeeID, currentDate, currentTime, employeeID, currentDate)
              cursor.execute(subQuery, subQueryData)
      except Exception as e:
              print (e)
              print (cursor._last_executed)
      subRequestableShifts = cursor.fetchall()
      return subRequestableShifts
      #Here's a challenge- can you inner join across all three tables to get the employeename in the results as well?

def requestSub(db, employeeID, shiftID):
      cursor = db.cursor()
      subRequest = ("UPDATE shiftEmployeeLinker SET subRequested = TRUE WHERE employeeID = %s and shiftID = %s")
      cursor.execute(subRequest, (employeeID, shiftID))
      cursor.close()
      db.commit()
      return

def frontEndRequestSub(shiftID): #TODO- Modify to work with a username
      workerNameTuple = ("Alexis", "Engel")
      db = MySQLdb.connect(host = "localhost",
                                               user = "Anirudh",
                                               passwd = "password",
                                               db = "test")
      cursor = db.cursor();
      #get employeeID
      query = ("SELECT id FROM employeeinfo WHERE firstName = %s AND lastName = %s")
      cursor.execute(query, workerNameTuple)
      result = cursor.fetchone()
      employeeID = result[0]
      requestSub(db, employeeID, shiftID)
      cursor.close()
      db.close()
#TODO: FIGURE OUT HOW THIS FLOW SHOULD WORK
#current idea: have every worker login as the same "worker" account, then just deal with checkingin via the names.
# db = MySQLdb.connect(host = "localhost",
#                                               user = "Anirudh",
#                                               passwd = "password",
#                                               db = "test")


# #time to test!
# workerNameTuple = ("Anirudh", "Appachar")
# location = "CMC"
# actualcheckinTime = "13:15" #NOTE  You'll need to deal with 24 hour time as well
# date = "2018-03-27"
# checkIn(db, workerNameTuple, actualcheckinTime, location, date)
