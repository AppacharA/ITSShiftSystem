from flask import Flask, render_template, request, jsonify
import json
import MySQLdb
from workerFunctions import frontEndCheckIn, getSubRequestableShifts, frontEndGetSubbableShifts, frontEndRequestSub, frontEndUnrequestSub
import workerFunctions
app = Flask(__name__)

#TODO- Essentially, rework all these methods to be frontend. Login to the database upon accessing this page, and just pass the database to every single method as its called.

@app.route('/workerConsole')
def gotoWorkerConsole():
	#TODO- Implement a check so that you can't go to this website without first logging in.
	return render_template('workerConsole.html')

@app.route('/')
def main():
	checkedIn = False
	checkInTime = None
	#Eventually you'll want to call this code only if the user is authenticated and logged in.
	db = MySQLdb.connect(host = "localhost",
						 user = "Anirudh",
						 passwd = "password",
						 db = "test")

	cur = db.cursor()
	cur.execute("SELECT checkintime FROM shiftemployeelinker WHERE employeeid = 1001 ORDER BY shiftId DESC LIMIT 1")
	result = cur.fetchone()
	cur.close()
	subRequestableShifts = getSubRequestableShifts(db)
	subbableShifts = frontEndGetSubbableShifts()#getSubbableShifts(db)
	print (len(subbableShifts))
	db.close()
	#check if the user is already checked in for this shift.
	
	if result[0] != None:
		checkedIn = True
		checkInTime = result[0]

	loggedInEmployeeID = 1038

	print (checkedIn)
	print (len(subRequestableShifts))
	return render_template('workerConsole.html', data = (checkedIn, checkInTime), subRequestableShifts = subRequestableShifts, subbableShifts = subbableShifts, employeeID = loggedInEmployeeID)

# #rendering the HTML page which has the button
# @app.route('/json')
# def json():
#     return render_template('json.html')

#background process happening without any refreshing
@app.route('/checkin', methods = ['POST'])
def background_process_test():
	
	print ("Hello")
	frontEndCheckIn()


	return ("nothing")

@app.route('/requestSub', methods = ['POST'])
def requestSub():
	
	shiftID = request.form['shiftID']
	frontEndRequestSub(shiftID)

	return ("nothing")

@app.route('/unrequestSub', methods = ['POST'])
def unrequestSub():
	
	shiftID = request.form['shiftID']
	frontEndUnrequestSub(shiftID)

	return ("nothing")

@app.route('pickupSub', methods = ['POST'])
def frontEndPickupSub():
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")

	origEmployeeID = request.get_json.get('origEmployeeID')
	subEmployeeID = request.get_json.get("subEmployeeID")
	shiftID = request.get_json.get("shiftID")


	pickupSub(db, shiftID, origEmployeeID, subEmployeeID)

	return ("nothing")


@app.route('dropSub', methods = ['POST'])
def frontEndDropSub():
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")

	origEmployeeID = request.get_json.get('origEmployeeID')
	subEmployeeID = request.get_json.get("subEmployeeID")
	shiftID = request.get_json.get("shiftID")

	dropSub(db, shiftID, origEmployeeID, subEmployeeID)

	return ("nothing")


@app.route('/getSubRequestStatus', methods = ['GET'])
def getSubRequestStatus():
	shiftID = request.args.get('shiftID') #https://stackoverflow.com/questions/10434599/how-to-get-data-received-in-flask-request
	db = MySQLdb.connect(host = "localhost",
										   user = "Anirudh",
										   passwd = "password",
										   db = "test")

	subStatus = workerFunctions.getSubStatus(db, shiftID)
	subFilled = subStatus[1]
	subRequested = subStatus[0]
	db.close()

	#return ("nothing")
	return (jsonify({"subFilled":subFilled, "subRequested":subRequested}))

@app.route('/getSubbableShiftIDs', methods = ['GET'])
def getSubbableShiftIDs():
	shifts = frontEndGetSubbableShifts()

	shiftInfoList = []
	for elem  in shifts:
		shiftID = elem[0]
		origEmployeeID = elem[5]
		diclist = {"shiftID":shiftID, "origEmployeeID":origEmployeeID}
		shiftInfoList.append(diclist)
		#shiftInfoList.update({shiftID : origEmployeeid}) #respectively, shiftid and origemployeeid.
		

	#JSONIFY A LIST. https://stackoverflow.com/questions/12435297/how-do-i-jsonify-a-list-in-flask/35000418#35000418
	print (shiftInfoList)
	return jsonify(shiftInfoList)

if __name__ == '__main__':
	app.run(debug=True)