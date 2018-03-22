//A file that handles all the javascript for the workerConsole frontend.

function getCurrentTime(){ //A function to get the current time from the system. Note that this function gets its time from the client-side machine, while the python method gets it from the server machine.
      var currentTime = new Date();
      var currentHour = currentTime.getHours();
      var currentMinute = currentTime.getMinutes();
      var currentSecond = currentTime.getSeconds();

      currentMinute = (currentMinute < 10 ? "0" : "") + currentMinute; //Look up ternary operator to explain why this works. It's an efficient way to write shorthand.
      currentHour = (currentHour < 10 ? "0" : "") + currentHour;

      currentSecond = (currentSecond < 10 ? "0" : "") + currentSecond;

      var currentTimeString = currentHour + ":" + currentMinute + ":" + currentSecond;

      return currentTimeString
     }

function updateClock(){ // A function to update the clock.
      
      currentTimeString = getCurrentTime()
      document.getElementById("checkinClock").firstChild.nodeValue = currentTimeString;

  }

function sayHello(){
	alert("Hello")
}

// function sayHello(input){
// 	alert (input)
// }
function checkIn(){ //A function to check in a worker.
  //checkInTime = getCurrentTime(); //Get current time.

  $.post("/checkin") //This goes and uses AJAX to post to the server and call the python method frontendcheckin()

  
  //Next, we wish to disable the button.
  document.getElementById("checkinButton").disabled = true;    
  document.getElementById("checkinButton").innerText = "Already Checked In!"
}



function requestUnrequestSub(element, shiftID){
  if (element.value == "subRequested" ) {//In this case, we are unrequesting a sub.
    $.post("/unrequestSub", {shiftID: shiftID})

    element.innerText = "Request Sub";

    element.value = "subUnrequested" //update button value to reflect that we unrequested a sub.
  }

  else if (element.value == "subUnrequested"){ //In this case, we must request a sub.
    $.post("/requestSub", {shiftID: shiftID})

    element.innerText = "Unrequest Sub";

    element.value = "subRequested" //update button value to reflect that we requested a sub.
  }

}

//This code is to ensure that the button remains disabled even upon page refresh.
function enableDisableCheckin(checkedIn, checkInTime) { //Will disable the button if the same user has already checked in for that particular shift.
    if (checkedIn == "True") { //If user is already checked in, we must make sure the button is disabled.
        document.getElementById("checkinButton").disabled = true;    
        document.getElementById("checkinButton").innerText = "Checked in " + checkInTime;
      }
    
    }


//function populateSubRequestTable(row)

function addSubRequestableShift(inputrow){
	var table = document.getElementById("subRequestableShiftTable");
	var rowCount = table.rows.length;

	//Now to insert a row at the end of the table.
	var row = table.insertRow(rowCount)

	//Next, we populate the row with the appropriate info. Our input row is a python tuple of the form (shiftID, checkinTime, Location, Date, Day, employeeID, shiftID, subRequested, checkedIn, actualcheckinTime)
	//Of these, we only are concerned with checkintime, location, date, day.

	var time = '{{inputrow[1]}}'
	var location = '{{inputrow[2]}}'
	var date = '{{inputrow[3]}}'
	var day = '{{inputrow[4]}}'

	var timeCell = row.insertCell(0);
	var locationCell = row.insertCell(1);
	var dateCell = row.insertCell(2);
	var dayCell = row.insertCell(3)

	timeCell.innerHTML = time;
	locationCell.innerHTML = location;
	dateCell.innerHTML = date;
	dayCell.innerHTML = day;



}

window.onload = updateClock();
//window.onload = enableDisableCheckin(checkedIn, checkInTime)
window.setInterval('updateClock()', 1000)
