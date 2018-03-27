from flask import Flask, render_template, request, jsonify, Response
import json
import MySQLdb
from workerFunctions import frontEndCheckIn, getSubRequestableShifts, getSubbableShifts, frontEndGetSubbableShifts, frontEndRequestSub, frontEndUnrequestSub, frontEndPickupSub, frontEndDropSub,getCurrentShift, getCurrentEmployee, getSubbingShifts, getSubStatus

import workerFunctions
from datetime import datetime
import queue

app = Flask(__name__)


eventStream = queue.Queue() #must be global.



#TODO- Essentially, rework all these methods to be frontend. Login to the database upon accessing this page, and just pass the database to every single method as its called.

@app.route('/workerConsole')
def gotoWorkerConsole():
	#TODO- Implement a check so that you can't go to this website without first logging in.
	return render_template('workerConsole.html')

@app.route('/')
def main(**kwargs):
	checkedIn = False
	checkInTime = None
	shiftInfo = None
	eventStream.put("")
	#Eventually you'll want to call this code only if the user is authenticated and logged in.
	db = MySQLdb.connect(host = "localhost",
						 user = "Anirudh",
						 passwd = "password",
						 db = "test")

	#when you have an authenticated user, make sure to replace this line with their username.
	username = "appachara"
	location = kwargs.get("location", "ResearchIT")
	print (location)
	#location = "ResearchIT" #Placeholder
	
	employeeID = getCurrentEmployee(db, username)
	currentShiftID = getCurrentShift(db, location, employeeID)
	print (currentShiftID)
	#print (employeeID)
	#TODO -implement check for if there is no employee or shift at this time.
	cur = db.cursor()
	# cur.execute("SELECT checkintime FROM shiftemployeelinker WHERE employeeid = 1001 ORDER BY shiftId DESC LIMIT 1")

	if currentShiftID != None:
		cur.execute("SELECT checkinTime from shiftemployeelinker WHERE employeeID = %s AND shiftID = %s", (employeeID, currentShiftID))
		result = cur.fetchone()
		#print (result) #Investigate why this can sometimes give none but subbingshifts() only ever gives an empty tuple
		if result[0] != None:
			checkedIn = True
			checkInTime = result[0]

		cur.execute("SELECT checkinTime, location from shiftlist where id = %s", (currentShiftID,))
		shiftInfo = cur.fetchone()
	
	cur.close()

	
	subRequestableShifts = getSubRequestableShifts(db, employeeID)
	subbingShifts = getSubbingShifts(db, employeeID)

	#print (subbingShifts)

	subbableShifts = getSubbableShifts(db)
	#print (len(subbableShifts))
	#subbableShifts = []
	db.close()
	#check if the user is already checked in for this shift.
	
	#will need to implement check for those times when it doesn't even find a result. 
	


	#loggedInEmployeeID = 1038

	return render_template('workerConsole.html', data = (checkedIn, checkInTime), subRequestableShifts = subRequestableShifts, subbableShifts = subbableShifts, subbingShifts = subbingShifts, employeeID = employeeID, shiftID = currentShiftID, shiftInfo = shiftInfo, location = location)



#background process happening without any refreshing
@app.route('/checkin', methods = ['POST'])
def checkIn():
	
	employeeID = request.form['employeeID']
	shiftID = request.form['shiftID']
	#print ("Hello")
	checkInTime = frontEndCheckIn(employeeID, shiftID)


	return jsonify({"checkInTime":checkInTime})
	

@app.route('/requestSub', methods = ['POST'])
def requestSub():
	
	shiftID = request.form['shiftID']
	employeeID = request.form['employeeID']
	frontEndRequestSub(shiftID, employeeID)

	return ("nothing")

@app.route('/unrequestSub', methods = ['POST'])
def unrequestSub():
	
	shiftID = request.form['shiftID']
	employeeID = request.form['employeeID']
	frontEndUnrequestSub(shiftID, employeeID)

	return ("nothing")

@app.route('/pickupSub', methods = ['POST'])
def pickupSub():
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")
	
	origEmployeeID = request.form["origEmployeeID"]
	subEmployeeID = request.form["subEmployeeID"]
	shiftID = request.form["shiftID"]
	

	frontEndPickupSub(shiftID, origEmployeeID, subEmployeeID)

	data = "pickupSub_shift_" + shiftID + "_emp_" + origEmployeeID #transmit that the sub was picked up"
	transmit(data)
	return ("nothing")


@app.route('/dropSub', methods = ['POST'])
def dropSub():
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")

	
	origEmployeeID = request.form['origEmployeeID']
	
	shiftID = request.form["shiftID"]

	

	print (request.form)
	#print (origEmployeeID)
	
	#print (shiftID)
	frontEndDropSub(shiftID, origEmployeeID)

	data = "dropSub_shift_" + shiftID + "_emp_" + origEmployeeID #transmit that the drop happened.
	transmit(data)
	return ("nothing")



@app.route('/getSubRequestStatus', methods = ['GET'])
def getSubRequestStatus():
	shiftID = request.args.get('shiftID') #https://stackoverflow.com/questions/10434599/how-to-get-data-received-in-flask-request
	employeeID = request.args.get('employeeID')
	# employeeID = request.form['employeeID']
	# shiftID = request.form['shiftID']
	#print ((employeeID, shiftID))
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")

	subStatus = getSubStatus(db, shiftID, employeeID)
	subFilled = subStatus[1]
	subRequested = subStatus[0]
	db.close()

	#return ("nothing")
	return (jsonify({"subFilled":subFilled, "subRequested":subRequested}))

@app.route('/getSubbableShifts', methods = ['GET'])
def frontEndgetSubbableShifts():
	shifts = frontEndGetSubbableShifts()

	shiftInfoList = []
	for elem  in shifts:
		shiftID = elem[0]
		origEmployeeID = elem[5]
		diclist = {"shiftID":shiftID, "origEmployeeID":origEmployeeID}
		shiftInfoList.append(diclist)
		#shiftInfoList.update({shiftID : origEmployeeid}) #respectively, shiftid and origemployeeid.
		

	#JSONIFY A LIST. https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask/35000418#35000418
	#print (shiftInfoList)
	return jsonify(shiftInfoList)

@app.route('/getSubbingShifts', methods = ['GET']) #Given an employeeID, get all the shifts that they are subbing for.
def frontEndGetSubbingShifts():
	employeeID = request.form['employeeID']

	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")


	subbingShifts = getSubbingShifts(db, employeeID)

	db.close()

@app.route('/getSubShiftInfo', methods = ['GET'])
def getSubShiftInfo():
	subbable = True

	shiftID = request.args.get('shiftID') #https://stackoverflow.com/questions/10434599/how-to-get-data-received-in-flask-request
	origEmployeeID = request.args.get('origEmployeeID')

	employeeID = 1006 #this line is a placeholder. Eventually we'll get employeeID from flask-logins.
	
	shiftInfo = workerFunctions.frontEndGetShiftInfo(shiftID, origEmployeeID)
	#print (shiftInfo)
	# time = shiftInfo[0].strftime("%H:%M")
	time = (datetime.min + shiftInfo[0]).time().strftime("%H:%M") #Python retrieves MySQL TIME values as timedeltas, which means you have to add the timedelta interval to a 0:00 time in python to get the actual time. See https://stackoverflow.com/questions/764184/python-how-do-i-get-time-from-a-datetime-timedelta-object for more info.
	location = shiftInfo[1]
	date = shiftInfo[2]
	day = shiftInfo[3]
	employeeName = shiftInfo[4] + shiftInfo[5]
	subRequested = shiftInfo[6]

	if employeeID == origEmployeeID:
		subbable = False

	#BTW You need to rework all the employeeID stuff so that it validates on teh backend, rather than from the frontend.

	return jsonify({"time": time, "location":location, "date":date, "day":day, "subRequested":subRequested, "employeeName":employeeName, "subbable":subbable, "employeeID":employeeID})
	#return ("nothing")






@app.route('/receiveAndTransmit', methods = ['POST'])
def receive(): #stores events in a queue...
	data = request.form['data']
	print (data)

	#global eventStream
	eventStream.put(data)

	#broadcast(data)

	return ("nothing")


def transmit(data):
	#global eventStream

	eventStream.put(data)
		

@app.route('/broadcast') #experiment with seeing if you can put this in another file?
def broadcast():
	
	#global eventStream
	data = eventStream.get()
	msg = "event: ping\n"
	msg = msg + 'data: ' + data + '\n\n'
	print (msg)

	return Response(msg, mimetype="text/event-stream")


@app.route('/switchLocation')
def switchLocation():
	newLocation = request.args.get("location")

	return (main(location = newLocation))



if __name__ == '__main__':
	app.run(debug=True, threaded = True)