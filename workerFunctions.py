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

def checkInEmployeeID(db, employeeID, actualCheckInTime, shiftID): #TODO: Decide if you should checkin based on worker name or username. If username, how do you populate the employeeinfo with all the usernames at the getgo?
	cursor = db.cursor()
	
	# #get employee info.
	# employeeQuery = ("SELECT id FROM employeeInfo WHERE username = %s")
	# cursor.execute(employeeQuery, username)
	# result = cursor.fetchone()
	# employeeID = result[0]


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

def frontEndCheckIn(employeeID, shiftID):

	workerNameTuple = ("Anirudh", "Appachar")
	username = "appachara"
	
	#Figure out how to get location. Perhaps from IP? IN ANY CASE THIS IS A PLACEHOLDER.
	#location = "CMC"
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")
	#getCurrentShift(db, location, currentTime, currentDate)
	currentInfo = datetime.today()	#NOTE- This approach means that you checkin based on the server time, not hte javascript time.
	currentDate = currentInfo.strftime("%Y-%m-%d")
	checkinTime = currentInfo.strftime("%H:%M")

	checkInEmployeeID(db, employeeID, checkinTime, shiftID)
	#implement a successcheck..
	return checkinTime
	#ALSO FIGURE OUT HOW TO GET THE WORKER NAME/ USERNAME. PRESUMABLY FROM THE LOGGING IN ITSELF

#TODO: FIGURE OUT HOW THIS FLOW SHOULD WORK
#current idea: have every worker login as the same "worker" account, then just deal with checkingin via the names.


def getCurrentShift(db, location): #Given the current time, location, you must find the shift that a worker is in in.
	#todo- work based on username
	#todo- Maybe make it so that you generate a datetime object within the function itself?
	currentInfo = datetime.today()	#NOTE- This approach means that you checkin based on the server time, not hte javascript time.
	currentDate = currentInfo.strftime("%Y-%m-%d")
	currentTime = currentInfo.strftime("%H:%M")
	cursor = db.cursor()
	

	#get shift info.
	shiftQuery = ("SELECT id FROM shiftList WHERE checkinTime <= %s AND location = %s AND Date = %s "
					"ORDER BY id DESC LIMIT 1")
	cursor.execute(shiftQuery, (currentTime, location, currentDate))
	#print (cursor._last_executed)
	result = cursor.fetchone()
	cursor.close()
	shiftID = result[0]

	return shiftID

def getCurrentEmployee(db, username):
	cursor = db.cursor()
	print (username)
	cursor.execute("SELECT id from employeeInfo WHERE username = %s", (username,))
	result = cursor.fetchone()
	cursor.close()
	employeeID = result[0]

	return employeeID

def getSubbableShifts(db):#TODO- Modify to work based on username.       #This will get the list of shifts that are in the future that you can request subs for.
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

	#next get all shifts in the future that have an unfulfilled sub request in and that are not the employee's own shifts.
	subQuery = ("SELECT shiftlist.id, shiftlist.checkinTime, shiftlist.location, shiftlist.date, shiftlist.day, shiftEmployeeLinker.employeeid FROM ShiftList "
						"INNER JOIN ShiftEmployeeLinker "
						"ON ShiftList.id = ShiftEmployeeLinker.shiftID "
						"WHERE ShiftEmployeeLinker.subRequested = TRUE "
						"AND NOT EXISTS "
							"(SELECT 1 from subbedShifts WHERE subbedShifts.shiftID = shiftEmployeeLinker.shiftID and subbedShifts.origEmployeeID = shiftEmployeeLinker.employeeID) "
						"AND (ShiftList.date = %s AND ShiftList.checkinTime > %s ) "
						
						"OR (ShiftEmployeeLinker.subRequested = TRUE "
						"AND NOT EXISTS "
							"(SELECT 1 from subbedShifts WHERE subbedShifts.shiftID = shiftEmployeeLinker.shiftID and subbedShifts.origEmployeeID = shiftEmployeeLinker.employeeID) "
						"AND (ShiftList.date > %s) )")
							

	try:
	  subQueryData = (currentDate, currentTime, currentDate)
	  cursor.execute(subQuery, subQueryData)
	except Exception as e:
	  print (e)
	  print (cursor._last_executed)
	subbableShifts = cursor.fetchall()
	return subbableShifts
	#Here's a challenge- can you inner join across all three tables to get the employeename in the results as well?

def frontEndGetSubbableShifts():
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")
	subbableShifts = getSubbableShifts(db)

	return subbableShifts


def getSubRequestableShifts(db):#TODO- MOdify to work based on username.
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

	#next get all possible shifts in the future that the employee can stake using inner join
	subQuery = ("SELECT shiftlist.id, shiftlist.checkinTime, shiftlist.location, shiftlist.date, shiftlist.day, shiftemployeelinker.subRequested FROM ShiftList "
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

def unrequestSub(db, employeeID, shiftID):
	cursor = db.cursor()
	subRequest = ("UPDATE shiftEmployeeLinker SET subRequested = FALSE, subFilled = FALSE WHERE employeeID = %s and shiftID = %s")
	cursor.execute(subRequest, (employeeID, shiftID))
	cursor.close()
	db.commit()
	return

def frontEndUnrequestSub(shiftID): #TODO- Modify to work with a username
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
	unrequestSub(db, employeeID, shiftID)
	cursor.close()
	db.close()

def getSubStatus(db, shiftID): #TODO: Make it so that it passes in username of employee as well.
	employeeID = 1038 #This is Alexis Engel's employeeid

	cursor = db.cursor()
	query = ("SELECT subRequested, subFilled FROM shiftemployeelinker WHERE employeeID = %s AND shiftID = %s")
	cursor.execute(query, (employeeID, shiftID))
	result = cursor.fetchone() #of form (subRequested, subFilled)
	#subFilled = result[]
	cursor.close()

	return result

def getSubbableShiftInfo(db, shiftID, origEmployeeID):
	#find and return the information of a given shift given the original employee and shiftid.
	cursor = db.cursor()
	query = ("SELECT shiftlist.id, shiftlist.checkinTime, shiftlist.location, shiftlist.date, shiftlist.day, shiftEmployeeLinker.employeeid FROM ShiftList "
						"INNER JOIN ShiftEmployeeLinker "
						"ON ShiftList.id = ShiftEmployeeLinker.shiftID "
						"WHERE ShiftEmployeeLinker.shiftID = %s AND shiftEmployeeLinker.employeeID = %s")

	cursor.execute(query, (shiftID, origEmployeeID))
	result = cursor.fetchone()
	dataList = {}
	for elem in result:
		datalist.update({elem[0] : elem[5]})

	return dataList #this is key. We return it as a dictionary so that we can then pass it easily to javascript.

def pickupSub(db, shiftID, origEmployeeID, subEmployeeID):

	cursor = db.cursor()
	updateQuery = ("UPDATE shiftEmployeeLinker SET subFilled = TRUE "
					"WHERE employeeID = %s AND shiftID = %s")
	cursor.execute(updateQuery, (origEmployeeID, shiftID))

	insertQuery = ("INSERT INTO subbedShifts (shiftID, origEmployeeID, subEmployeeID)"
					"VALUES (%s, %s, %s)")
	cursor.execute(insertQuery, (shiftID, origEmployeeID, subEmployeeID))

	cursor.close()
	db.commit()


def dropSub(db, shiftID, origEmployeeID, subEmployeeID):

	cursor = db.cursor()
	updateQuery = ("UPDATE shiftEmployeeLinker SET subFilled = FALSE "
					"WHERE employeeID = %s AND shiftID = %s")
	cursor.execute(updateQuery, (origEmployeeID, shiftID))

	insertQuery = ("DELETE FROM subbedShifts (shiftID, origEmployeeID, subEmployeeID)"
					"VALUES (%s, %s, %s)")
	cursor.execute(insertQuery, (shiftID, origEmployeeID, subEmployeeID))

	cursor.close()
	db.commit()


def main():
#TODO: FIGURE OUT HOW THIS FLOW SHOULD WORK
#current idea: have every worker login as the same "worker" account, then just deal with checkingin via the names.
	db = MySQLdb.connect(host = "localhost",
                                              user = "Anirudh",
                                              passwd = "password",
                                              db = "test")


	shiftID = getCurrentShift(db, "CMC")

	print (shiftID)

# #time to test!
# workerNameTuple = ("Anirudh", "Appachar")
# location = "CMC"
# actualcheckinTime = "13:15" #NOTE  You'll need to deal with 24 hour time as well
# date = "2018-03-27"
# checkIn(db, workerNameTuple, actualcheckinTime, location, date)


if __name__ == "__main__":
	main()

