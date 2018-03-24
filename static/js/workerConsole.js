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

    updateSubRequestButton(theButton, shiftID)


   



  }

}

function updateSubRequestButton(buttonID, shiftID){//a callback function for the buttons. Further Reading: https://stackoverflow.com/questions/14754619/jquery-ajax-success-callback-function-definition
  //https://stackoverflow.com/questions/11576176/wait-for-a-jquery-ajax-callback-from-calling-function

   
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


// function pickupDropSub(element, shiftID){
 


// }


// function refreshSubbableShifts(){
//   //alert("hello")
//   $('subbableShiftDiv').load(); //https://stackoverflow.com/questions/42746801/jquery-to-reload-div-flask-jinja2

// }

function refreshSubbableShifts(){
  var Table = document.getElementById("subbableShiftTable")
  var shiftDic = [] //we will have key value pairs of the form {employeeID: [array of shiftIDS]}
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

    if (origEmployeeID in shiftDic) {//A key for that employee exists already, with an associated array for its value.

      shiftDic[origEmployeeID].push(shiftID)

    }
    else{ //A new key.
      shiftDic.push({    https://stackoverflow.com/questions/7196212/how-to-create-dictionary-and-add-key-value-pairs-dynamically/22315575
        key: origEmployeeID
        value: [shiftID]


      });

    }


    //shiftArray.push([shiftID, origEmployeeID]) //keep track of what shifts are in the table.
    deleteSubbableShiftRow(Table, i, shiftID); //will check if a given shift is subbed for or if it's been removed, and if so, will delete it from the table.
    }

  //once you've hit the end of a table, it's time to see if there are any new subs that have been requested
  findNewSubbableShifts(Table, shiftDic);


function deleteSubbableShiftRow(Table,rowindex, shiftID){
  $.get("/getSubRequestStatus", {"shiftID":shiftID}, function(data){ //If sub is filled, then we will delete the row that it originally came from.
      //TODO: Figure out how to deal with this and JSON.
      
      var subFilled = data.subFilled;
      var subRequested = data.subRequested;
      //If a sub has been filled or the request has been rescinded, we must delete the row.
      if (subFilled == 1 || subRequested == 0){
        Table.deleteRow(rowindex)
      } 
     


    }, "json" )

}

function findNewSubbableShifts(Table, shiftDic){
//TODO/Schematic of how this works:
//We will first do an ajax call to get all the shift ids and employeeids of all subbable shifts.
//var shiftDic = {1041:[144, 146]}

//alert(JSON.stringify(shiftArray))
$.get("/getSubbableShiftIDs", function(data){

    for (var i = 0; i < data.length; i++){ //https://stackoverflow.com/questions/42499535/passing-a-json-object-from-flask-to-javascript
      var employeeID = data[i].origEmployeeID
      var shiftID = data[i].shiftID
      var combo = [shiftID, employeeID]
      
      
      if (isIn(combo, shiftDic) == false){

        alert(JSON.stringify(combo))                                        //Submit a new shiftrequest.

      }
        
        
      

      }
    }

    
    //Then, we will compare shiftArray to that list and see what remains i.e what new shifts there are.
//Finally, we will iterate through the new shifts.
//for each shift, we will submit an asynchronous call via insertNewSubbableShiftRow(), a callback function which will insert the new row.
   
, "json")
}

// function insertNewSubbableShiftRow(Table, shiftID, origEmployeeID){
//   //How this will work:
//   //submit an AJAX call to get the data from the row specified by shiftID and origEmployeeID.
//   //Once you have the data, create a row and insert the necessary data.


// }

function pickupDropSub(theButton){
  //Check if you're clicking to pick up a sub.
  var idArray =  theButton.id.split("_");
  var origEmployeeID = idArray[4]
  var shiftID = idArray[2]
  var subEmployeeID = 1001 //This is a placeholder, we must put it as an input eventually.

  var postData = {"origEmployeeID":origEmployeeID, "subEmployeeID":subEmployeeID, "shiftID":shiftID}
  var postData = JSON.stringify(postData)
  
  if (theButton.value == "pickupSub"){ //on clicking you will pick up a sub.
    
    //TODO: The code that actually sends the pickup request to the server.

    element.innerText = "Subbing";

    element.value = "dropSub" //update button value to reflect that we unrequested a sub.
    //Consider also dropping the table that the button exists in. Or not-currently it'll be autodropped as the refreshSubbableShifts method runs.
  }
  else if (theButton.value == "dropSub"){
    //TODO: The code that actually sends the pickup request to the server.

    element.innerText = "Sub?";

    element.value = "pickupSub" //update button value to reflect that we unrequested a sub.

  }
}



function isIn(array, shiftDic){
  //array[0] is shiftID, array[1] is employeeID
  var employeeID = array[1];

  if (employeeID in shiftDic){//If a key exists for the employee //https://stackoverflow.com/questions/1098040/checking-if-a-key-exists-in-a-javascript-object

    if (shiftDic[employeeID].indexof(array[0]) != -1){
      return true;

    }

    else{
      return false;
    }
  }
  
  else{
    return false;
  }


}


// function isIn(subArray, array){
//   for (i = 0; i < array.length; i++){ //TODO: Optimize this search.

        
//         if (subArray[0] == array[i][0] && subArray[1] == array[i][1]){ // https://stackoverflow.com/questions/24943200/javascript-2d-array-indexof Why we can't use indexof...

//           return true;
//         }
//     }
// return false;
// }

window.onload = updateClock();
//window.onload = enableDisableCheckin(checkedIn, checkInTime)
window.setInterval('updateClock()', 1000)
//window.setInterval('refreshSubRequestStatus()', 10000)
//window.setInterval('refreshSubbableShifts()', 5000)

window.setInterval('findNewSubbableShifts()', 5000)


//https://stackoverflow.com/questions/12693947/jquery-ajax-how-to-send-json-instead-of-querystring
//https://stackoverflow.com/questions/6587221/send-json-data-with-jquery

//https://stackoverflow.com/questions/14908864/how-can-i-use-data-posted-from-ajax-in-flask

