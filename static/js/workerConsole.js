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

function sayHello(input){
  alert(input)
  //alert(element.id)
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

// //This code is to ensure that the button remains disabled even upon page refresh.
// function enableDisableCheckin(checkedIn, checkInTime) { //Will disable the button if the same user has already checked in for that particular shift.
//     if (checkedIn == "True") { //If user is already checked in, we must make sure the button is disabled.
//         document.getElementById("checkinButton").disabled = true;    
//         document.getElementById("checkinButton").innerText = "Checked in " + checkInTime;

//       }
    
//     }



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

function refreshSubRequestStatus(){
  var Table = document.getElementById("subRequestableShiftTable")
  //Now, we iterate through every row in the table:
  for (i = 1; i < Table.rows.length; i++){
    row = Table.rows[i];
    //At each row, find the 5th cell, index 4, which has the button for sub requests.
    cell = row.cells[4]

    //next get the button's id, and then the shiftid.
    theButton = cell.firstChild;
    var idArray = theButton.id.split(" ");
    var shiftID = idArray[1];

    //alert(shiftID)

    updateSubButton(theButton, shiftID)


   



  }

}

function updateSubButton(buttonID, shiftID){//a callback function for the buttons.
   
   $.get("/getSubRequestStatus", {"shiftID":shiftID}, function(data){ //If subrequest is filled, then you will need to update the button.
      //TODO: Figure out how to deal with this and JSON.
      
      var subFilled = data.subFilled;
      //If a sub has been filled, we must change the button's text.
      if (subFilled == 1){
        buttonID.innerHTML = "Filled"
        buttonID.value = "subRequested"
      } 
     


    }, "json" )
}


function pickupDropSub(element, shiftID){
 


}


// function refreshSubbableShifts(){
//   //alert("hello")
//   $('subbableShiftTable').load(); //https://stackoverflow.com/questions/42746801/jquery-to-reload-div-flask-jinja2



// }

function refreshSubbableShifts(){
  var Table = document.getElementById("subbableShiftTable")
  var shiftArray = []
  //Get all the shifts 
  //Now, we iterate through every row in the table:
  for (i = 1; i < Table.rows.length; i++){
    row = Table.rows[i];
    //At each row, find the 5th cell, index 4, which has the button for sub requests.
    cell = row.cells[4]

    //next get the button's id, and then the shiftid.
    theButton = cell.firstChild;
    var idArray = theButton.id.split("_"); //subbableshiftbuttons have names of the form sub_shift_shiftid_emp_origEmployeeID
    var shiftID = idArray[2];
    var origEmployeeID = idArray[4]
    shiftArray.push([shiftID, origEmployeeID]) //keep track of what shifts are in the table.
    deleteSubbableShiftRow(Table, i, shiftID); //will check if a given shift is subbed for and if so, will delete it from the table.
    }

  //once you've hit the end of a table, it's time to see if there are any new subs that have been requested
  findNewSubbableShifts(Table, shiftArray);


function deleteSubbableShiftRow(Table,rowindex, shiftID){
  $.get("/getSubRequestStatus", {"shiftID":shiftID}, function(data){ //If sub is filled, then we will delete the row that it originally came from.
      //TODO: Figure out how to deal with this and JSON.
      
      var subFilled = data.subFilled;
      //If a sub has been filled, we must delete the row.
      if (subFilled == 1){
        Table.deleteRow(rowindex)
      } 
     


    }, "json" )

}

function findNewSubbableShifts(Table, shiftArray){
//TODO/Schematic of how this works:
//We will first do an ajax call to get all the shift ids and employeeids of all subbable shifts.
//Then, we will compare shiftArray to that list and see what remains i.e what new shifts there are.
//Finally, we will iterate through the new shifts.
//for each shift, we will submit an asynchronous call via insertNewSubbableShiftRow(), a callback function which will insert the new row.


}

function insertNewSubbableShiftRow(Table, shiftID, origEmployeeID){
  //How this will work:
  //submit an AJAX call to get the data from the row specified by shiftID and origEmployeeID.
  //Once you have the data, create a row and insert the necessary data.


}

window.onload = updateClock();
//window.onload = enableDisableCheckin(checkedIn, checkInTime)
window.setInterval('updateClock()', 1000)
//window.setInterval('refreshSubRequestStatus()', 10000)
window.setInterval('refreshSubbableShifts()', 5000)
