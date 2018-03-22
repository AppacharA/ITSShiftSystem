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
db = MySQLdb.connect(host = "localhost",
						 user = "Anirudh",
						 passwd = "password",
						 db = "test")


#time to test!
workerNameTuple = ("Anirudh", "Appachar")
location = "CMC"
actualcheckinTime = "13:15" #NOTE  You'll need to deal with 24 hour time as well
date = "2018-03-27"
checkIn(db, workerNameTuple, actualcheckinTime, location, date)