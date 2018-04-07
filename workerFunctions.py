import MySQLdb
from openpyxl import Workbook
from openpyxl import load_workbook
from datetime import date, datetime, timedelta
import daySchedulingFunctions
import AuxiliaryFunctions
import re

def checkInEmployee(db, employeeID, actualCheckInTime, shiftID): #TODO: Decide if you should checkin based on worker name or username. If username, how do you populate the employeeinfo with all the usernames at the getgo?
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

	checkInEmployee(db, employeeID, checkinTime, shiftID)
	#implement a successcheck..
	return checkinTime
	#ALSO FIGURE OUT HOW TO GET THE WORKER NAME/ USERNAME. PRESUMABLY FROM THE LOGGING IN ITSELF

#TODO: FIGURE OUT HOW THIS FLOW SHOULD WORK
#current idea: have every worker login as the same "worker" account, then just deal with checkingin via the names.


def getCurrentShift(db, location, employeeID): #Given the current time, location, and ID you must find the shift that a worker is in in.
	#todo- work based on username
	#todo- Maybe make it so that you generate a datetime object within the function itself?
	currentInfo = datetime.today()	#NOTE- This approach means that you checkin based on the server time, not hte javascript time.
	currentDate = currentInfo.strftime("%Y-%m-%d")
	currentTime = currentInfo.strftime("%H:%M")
	cursor = db.cursor()
	# currentDate = "2018/03/26"
	# currentTime = "08:00"
	

	#get shift info. This query will search for all possible shifts for an employee, including shifts they are subbing for.
	shiftQuery = ("SELECT shiftid FROM shiftEmployeeLinker "
					"INNER JOIN shiftlist "
					"ON shiftlist.id = shiftEmployeeLinker.shiftid "
					"WHERE (shiftlist.checkinTime <= %s AND Date = %s AND employeeID = %s) "
					"UNION "
					"SELECT shiftid FROM subbedShifts "
					"INNER JOIN shiftlist "
					"ON shiftlist.id = subbedShifts.shiftid "
					"WHERE (shiftlist.checkinTime <= %s AND Date = %s AND subEmployeeID = %s) "

					
					"ORDER BY id DESC LIMIT 1")
	cursor.execute(shiftQuery, (currentTime, currentDate, employeeID))
	print (location)
	print (cursor._last_executed)
	result = cursor.fetchone()
	cursor.close()
	#db.close()
	if result:
		shiftID = result[0]
	else:
		shiftID = None

	return shiftID

def getCurrentEmployee(db, username):
	cursor = db.cursor()
	print (username)
	cursor.execute("SELECT id from employeeInfo WHERE username = %s", (username,))

	result = cursor.fetchone()
	cursor.close()
	#db.close()
	employeeID = result[0]

	return employeeID

def getSubbableShifts(db):#TODO- Modify to work based on username.       #This will get the list of shifts that are in the future that you can sub for.
	currentInfo = datetime.today()
	#currentDate = currentInfo.strftime("%Y-%m-%d")
	#currentTime = currentInfo.strftime("%H:%M")
	currentDate = "2018/03/26"
	currentTime = "18:30"
	workerNameTuple = ("Alexis", "Engel")

	#first get employeeid
	cursor = db.cursor()
	
	#next get all shifts in the future that have an unfulfilled sub request in and (eventually? that are not the employee's own shifts.)
	subQuery = ("SELECT shiftlist.id, shiftlist.checkinTime, shiftlist.location, shiftlist.date, shiftlist.day, shiftEmployeeLinker.employeeid, employeeInfo.firstName, employeeInfo.lastname FROM ShiftList "
						"INNER JOIN ShiftEmployeeLinker "
						"ON ShiftList.id = ShiftEmployeeLinker.shiftID "
						"INNER JOIN employeeInfo "
						"ON ShiftEmployeeLinker.employeeID = employeeInfo.id "
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
	cursor.close()
	return subbableShifts
	#Here's a challenge- can you inner join across all three tables to get the employeename in the results as well?

def frontEndGetSubbableShifts():
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")
	subbableShifts = getSubbableShifts(db)

	return subbableShifts


def getSubbingShifts(db, employeeID):
	cursor = db.cursor()

	theNow = datetime.now() #Note: This line means that this method currently gets shifts based on server time, not frontend time.
	currentTime = theNow.strftime("%H:%M")
	currentDate = theNow.strftime("%Y/%m/%d")
	#want to get all shifts that user is subbing for in the future.
	subQuery = subQuery = ("SELECT shiftlist.id, shiftlist.checkinTime, shiftlist.location, shiftlist.date, shiftlist.day, employeeInfo.id, employeeInfo.firstName, employeeInfo.lastname FROM ShiftList "
						"INNER JOIN subbedShifts "
						"ON ShiftList.id = subbedShifts.shiftID "
						"INNER JOIN employeeInfo "
						"ON subbedShifts.origEmployeeID = employeeInfo.id "
						"WHERE (subbedShifts.subEmployeeID = %s "
						"AND (ShiftList.date = %s AND ShiftList.checkinTime > %s) )"
						"OR (subbedShifts.subEmployeeID = %s AND ShiftList.date > %s)")

	cursor.execute(subQuery, (employeeID, currentDate, currentTime, employeeID, currentDate))
	subbingShifts = cursor.fetchall()

	cursor.close()

	return subbingShifts

def getSubRequestableShifts(db, employeeID):#TODO- MOdify to work based on employeeID
	currentInfo = datetime.today()
	currentDate = currentInfo.strftime("%Y-%m-%d")
	currentTime = currentInfo.strftime("%H:%M")
	
	# workerNameTuple = ("Alexis", "Engel")

	# #first get employeeid
	cursor = db.cursor()
	# shiftQuery = ("SELECT id from employeeinfo where firstName = %s and lastName = %s")
	# cursor.execute(shiftQuery, workerNameTuple)
	# result = cursor.fetchone()
	# employeeID = result[0]

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
	cursor.close()

	return subRequestableShifts

def frontEndRequestSub(shiftID, employeeID): #TODO- Modify to work with a username
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")
	
	subRequestSuccessful = requestSub(db, employeeID, shiftID)
	db.close()
	return subRequestSuccessful

def requestSub(db, employeeID, shiftID):
	cursor = db.cursor()
	try:
		subRequest = ("UPDATE shiftEmployeeLinker SET subRequested = TRUE WHERE employeeID = %s and shiftID = %s")
		cursor.execute(subRequest, (employeeID, shiftID))
	except Exception as e:
		#log error
		return False
	cursor.close()
	db.commit()
	return True


def frontEndUnrequestSub(shiftID, employeeID): #TODO- Modify to work with a username
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")

	subUnrequestSuccessful = unrequestSub(db, employeeID, shiftID)
	
	db.close()

	return subUnrequestSuccessful

def unrequestSub(db, employeeID, shiftID):
	cursor = db.cursor()
	
	try:
		subRequest = ("UPDATE shiftEmployeeLinker SET subRequested = FALSE, subFilled = FALSE WHERE employeeID = %s and shiftID = %s")
		cursor.execute(subRequest, (employeeID, shiftID))
	
	except Exception as e:
		#log error
		return False
	cursor.close()

	db.commit()
	return True



def getSubStatus(db, shiftID, employeeID): #TODO: Make it so that it passes in username of employee as well.
	#employeeID = 1038 #This is Alexis Engel's employeeid
	
	cursor = db.cursor()
	query = ("SELECT subRequested, subFilled FROM shiftemployeelinker WHERE employeeID = %s AND shiftID = %s")
	cursor.execute(query, (employeeID, shiftID))
	result = cursor.fetchone() #of form (subRequested, subFilled)
	#subFilled = result[]
	cursor.close()

	return result


def frontEndPickupSub(shiftID, origEmployeeID, subEmployeeID):
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")
	
	

	pickupSub(db, shiftID, origEmployeeID, subEmployeeID)

	db.close()

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



def frontEndDropSub(shiftID, origEmployeeID):
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")

	
	#print (origEmployeeID)
	
	#print (shiftID)
	dropSub(db, shiftID, origEmployeeID)

	db.close()

def dropSub(db, shiftID, origEmployeeID):

	cursor = db.cursor()
	updateQuery = ("UPDATE shiftEmployeeLinker SET subFilled = FALSE "
					"WHERE employeeID = %s AND shiftID = %s")
	
	cursor.execute(updateQuery, (origEmployeeID, shiftID))

	try:
		delQuery = ("DELETE FROM subbedShifts "
				"WHERE shiftID = %s AND origEmployeeID= %s")
				
		cursor.execute(delQuery, (shiftID, origEmployeeID))

	except:
		print(cursor._last_executed )
	cursor.close()
	db.commit()


def frontEndGetShiftInfo(shiftID, employeeID): #retrieve all data about a particular shift.
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")

	shiftInfo = getShiftInfo(db, shiftID, employeeID)

	db.close()

	return shiftInfo

def getShiftInfo(db, shiftID, employeeID):
	subQuery = ("SELECT shiftlist.checkinTime, shiftlist.location, shiftlist.date, shiftlist.day, employeeinfo.firstName, employeeInfo.lastName, shiftEmployeeLinker.subRequested, shiftEmployeeLinker.subFilled FROM ShiftList "
						"INNER JOIN ShiftEmployeeLinker "
						"ON ShiftList.id = ShiftEmployeeLinker.shiftID "
						"INNER JOIN employeeInfo "
						"ON shiftEmployeeLinker.employeeID = employeeInfo.id "
						"WHERE (ShiftEmployeeLinker.employeeID = %s "
						"AND shiftemployeelinker.shiftid = %s)")

	cursor = db.cursor()

	cursor.execute(subQuery, (employeeID, shiftID))

	print (cursor._last_executed)

	return (cursor.fetchone())


def main():
#TODO: FIGURE OUT HOW THIS FLOW SHOULD WORK
#current idea: have every worker login as the same "worker" account, then just deal with checkingin via the names.
	db = MySQLdb.connect(host = "localhost",
                                              user = "Anirudh",
                                              passwd = "password",
                                              db = "test")


	#shiftID = getCurrentShift(db, "CMC")

	#print (shiftID)

# #time to test!
# workerNameTuple = ("Anirudh", "Appachar")
# location = "CMC"
# actualcheckinTime = "13:15" #NOTE  You'll need to deal with 24 hour time as well
# date = "2018-03-27"
# checkIn(db, workerNameTuple, actualcheckinTime, location, date)


if __name__ == "__main__":
	main()

