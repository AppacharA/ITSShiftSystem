import MySQLdb
from datetime import datetime, time, timedelta
def buildWkndSchedule(database, date): #for either those saturdays or sundays.
	#get date into YYYY/MM/DD format (as a string)
	inputDate = date.strftime("%Y/%m/%d")
	
	inputDay = date.strftime("%A")

	fulldateTime = datetime.combine(date, time(10, 0))
	#initialize cursor
	cursor = database.cursor()

	while fulldateTime < datetime.combine(date, time(23, 59, 59)): #we iterate by hour all the way to the end of the day
		inputTime = fulldateTime.strftime("%H:%M") #get an inputTime that's a string in HH:MM format.
		
		if (inputDay == "Saturday") and (fulldateTime == datetime.combine(date, time(21, 0)) ):
			#if you're on saturday, shifts end at 8.
			return

		if fulldateTime > datetime.combine(date, time(22, 0)): #If it's past 10pm on Sunday, there's only the library shifts. 
			inputLocation = "ResearchIT"

			cmd = ("INSERT INTO ShiftList (checkinTime, Location, Date, Day) "
				"VALUES (%s, %s, %s, %s)"
				)

			cursor.execute(cmd, (inputTime, inputLocation, inputDate, inputDay))

		else:
			cmd = ("INSERT INTO ShiftList (checkinTime, Location, Date, Day) "
				"VALUES (%s, %s, %s, %s)"
				)

			cursor.execute(cmd, (inputTime, "CMC", inputDate, inputDay)) 
			cursor.execute(cmd, (inputTime, "ResearchIT", inputDate, inputDay))

				

		#increment time forward by one hour
		fulldateTime = fulldateTime + timedelta(hours = 1)
		#print (fulldateTime)

	#having finished inputting shifts, commit changes.
	database.commit()

def buildMonWedSchedule(database, date):
	#get date into YYYY/MM/DD format (as a string)
	inputDate = date.strftime("%Y/%m/%d")
	
	inputDay = date.strftime("%A") #should be either Monday or Wednesday

	fulldateTime = datetime.combine(date, time(8, 0)) #start bright and early at 8am
	#initialize cursor
	cursor = database.cursor()

	#Add the lone midnight to 1am shift that happens on Mondays and Wednesdays in the libe.
	cmd = ("INSERT INTO ShiftList (checkinTime, Location, Date, Day) "
				"VALUES (%s, %s, %s, %s)"
				)
	inputTime = (time(0,0).strftime("%H:%M"))
	cursor.execute(cmd, (inputTime, "ResearchIT", inputDate, inputDay))
	print (inputTime)
	#Now to cycle....
	while fulldateTime < datetime.combine(date, time(23, 59, 59)): #we iterate by hour all the way to the end of the day
		inputTime = fulldateTime.strftime("%H:%M") #get an inputTime that's a string in HH:MM format.
		#prep the command...
		cmd = ("INSERT INTO ShiftList (checkinTime, Location, Date, Day) "
				"VALUES (%s, %s, %s, %s)"
				)
		
		if fulldateTime > datetime.combine(date, time(22, 0)): #If it's past 10pm, there's only the library shifts. 
			cursor.execute(cmd, (inputTime, "ResearchIT", inputDate, inputDay))

		else:
			cursor.execute(cmd, (inputTime, "CMC", inputDate, inputDay)) 
			cursor.execute(cmd, (inputTime, "ResearchIT", inputDate, inputDay))

		
		if fulldateTime < datetime.combine(date, time(9, 45)):
			fulldateTime = fulldateTime + timedelta(hours = 1, minutes = 45)

		elif fulldateTime < datetime.combine(date, time(16, 25)):				#FIX THE NUMBERING.
			fulldateTime = fulldateTime + timedelta(hours = 1, minutes = 20)

		elif fulldateTime < datetime.combine(date, time(18, 0)):
			fulldateTime = fulldateTime + timedelta(hours = 1, minutes = 35)

		else: #now you're at 6pm
			fulldateTime = fulldateTime + timedelta(hours = 1)

	#having finished inputting shifts, commit changes.
	database.commit()


def buildFriSchedule(database, date): #As with all things in life, friday is weird.
	#get date into YYYY/MM/DD format (as a string)
	inputDate = date.strftime("%Y/%m/%d")
	
	inputDay = date.strftime("%A") #should be either Monday or Wednesday

	fulldateTime = datetime.combine(date, time(8, 0)) #start bright and early at 8am
	#initialize cursor
	cursor = database.cursor()

	#Add the lone midnight to 1am shift that happens on Mondays and Wednesdays in the libe.
	cmd = ("INSERT INTO ShiftList (checkinTime, Location, Date, Day) "
				"VALUES (%s, %s, %s, %s)"
				)
	inputTime = (time(0,0).strftime("%H:%M"))
	cursor.execute(cmd, (inputTime, "ResearchIT", inputDate, inputDay))
	print (inputTime)
	#Now to cycle....
	
	while fulldateTime < datetime.combine(date, time(23, 59, 59)): #we iterate by hour all the way to the end of the day
		inputTime = fulldateTime.strftime("%H:%M") #get an inputTime that's a string in HH:MM format.
		#prep the command...
		cmd = ("INSERT INTO ShiftList (checkinTime, Location, Date, Day) "
				"VALUES (%s, %s, %s, %s)"
				)
		
		if fulldateTime > datetime.combine(date, time(20, 0)): #If it's past 8pm, there's no shifts
			return

		else:
			cursor.execute(cmd, (inputTime, "CMC", inputDate, inputDay)) 
			cursor.execute(cmd, (inputTime, "ResearchIT", inputDate, inputDay))

		
		if fulldateTime < datetime.combine(date, time(9, 35)):
			fulldateTime = fulldateTime + timedelta(hours = 1, minutes = 35)

		elif fulldateTime < datetime.combine(date, time(15, 25)):
			fulldateTime = fulldateTime + timedelta(hours = 1, minutes = 10)

		elif fulldateTime < datetime.combine(date, time(16, 30)):
			fulldateTime = fulldateTime + timedelta(hours = 1, minutes = 5)

		elif fulldateTime < datetime.combine(date, time(18, 0)):
			fulldateTime = fulldateTime + timedelta(hours = 1, minutes = 30)

		else: #now you're at 6pm
			fulldateTime = fulldateTime + timedelta(hours = 1)

	#having finished inputting shifts, commit changes.
	database.commit()


def buildTueThuSchedule(database, date):
	#get date into YYYY/MM/DD format (as a string)
	inputDate = date.strftime("%Y/%m/%d")
	
	inputDay = date.strftime("%A") #should be either Monday or Wednesday

	fulldateTime = datetime.combine(date, time(8, 0)) #start bright and early at 8am
	#initialize cursor
	cursor = database.cursor()

	#Add the lone midnight to 1am shift that happens on Tuesdays and Thursdays in the libe.
	cmd = ("INSERT INTO ShiftList (checkinTime, Location, Date, Day) "
				"VALUES (%s, %s, %s, %s)"
				)
	inputTime = (time(0,0).strftime("%H:%M"))
	cursor.execute(cmd, (inputTime, "ResearchIT", inputDate, inputDay))
	print (inputTime)
	#Now to cycle....
	while fulldateTime < datetime.combine(date, time(23, 59, 59)): #we iterate by hour all the way to the end of the day
		inputTime = fulldateTime.strftime("%H:%M") #get an inputTime that's a string in HH:MM format.
		#prep the command...
		cmd = ("INSERT INTO ShiftList (checkinTime, Location, Date, Day) "
				"VALUES (%s, %s, %s, %s)"
				)
		
		if fulldateTime > datetime.combine(date, time(22, 0)): #If it's past 10pm, there's only the library shifts. 
			cursor.execute(cmd, (inputTime, "ResearchIT", inputDate, inputDay))

		else:
			cursor.execute(cmd, (inputTime, "CMC", inputDate, inputDay)) 
			cursor.execute(cmd, (inputTime, "ResearchIT", inputDate, inputDay))

		
		if fulldateTime < datetime.combine(date, time(10, 5)):
			fulldateTime = fulldateTime + timedelta(hours = 2, minutes = 5)

		elif fulldateTime < datetime.combine(date, time(12, 0)):				#FIX THE NUMBERING.
			fulldateTime = fulldateTime + timedelta(hours = 1, minutes = 55)

		elif fulldateTime < datetime.combine(date, time(13, 10)):
			fulldateTime = fulldateTime + timedelta(hours = 1, minutes = 10)

		elif fulldateTime < datetime.combine(date, time(17, 00)):
			fulldateTime = fulldateTime + timedelta(hours = 1, minutes = 55)

		else: #now you're at 5pm
			fulldateTime = fulldateTime + timedelta(hours = 1)

	#having finished inputting shifts, commit changes.
	database.commit()