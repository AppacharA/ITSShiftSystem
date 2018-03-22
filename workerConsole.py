from flask import Flask, render_template, request
import MySQLdb
from workerFunctions import frontEndCheckIn, getSubRequestableShifts, frontEndRequestSub, frontEndUnrequestSub
app = Flask(__name__)

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
	for elem in subRequestableShifts:
		print (elem)

	db.close()
	#check if the user is already checked in for this shift.
	
	if result[0] != None:
		checkedIn = True
		checkInTime = result[0]



	print (checkedIn)
	print (len(subRequestableShifts))
	return render_template('workerConsole.html', data = (checkedIn, checkInTime), subRequestableShifts = subRequestableShifts)

#rendering the HTML page which has the button
@app.route('/json')
def json():
    return render_template('json.html')

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

if __name__ == '__main__':
	app.run(debug=True)