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
  
}


function checkIn(employeeID, shiftID){ //A function to check in a worker.

  
  var theButton = document.getElementById("checkinButton")
  //First, disable the button.
  theButton.disabled = true;    
  theButton.innerText = "Checking you in..";

  // console.log(employeeID)
  // console.log(shiftID)

    checkinData = {"employeeID": employeeID, "shiftID": shiftID}
    $.post("/checkin", checkinData, function(data){
    
    //Assuming the checkin Succeeds.
    theButton.innerText = "Checked In " + data.checkInTime

  } ) //This goes and uses AJAX to post to the server and call the python method frontendcheckin()

  

}



function requestUnrequestSub(element, shiftID, employeeID){
  if (element.value == "subRequested" ) {//In this case, we are unrequesting a sub.
    $.post("/unrequestSub", {"shiftID": shiftID, "employeeID": employeeID})

    element.innerText = "Request Sub";

    element.style.background = "#4CAF50";

    element.value = "subUnrequested" //update button value to reflect that we unrequested a sub.
  }

  else if (element.value == "subUnrequested"){ //In this case, we must request a sub.
    $.post("/requestSub", {"shiftID": shiftID, "employeeID": employeeID})

    element.innerText = "Unrequest Sub";

    element.style.background = "#b30000";

    element.value = "subRequested" //update button value to reflect that we requested a sub.
  }

  $.get('/')
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

  postData = JSON.stringify({"shiftID":shiftID})
   
   $.get("/getSubRequestStatus", postData, function(data){ //If subrequest is filled, then you will need to update the button.
      //TODO: Figure out how to deal with this and JSON.
      
      var subFilled = data.subFilled;
      //If a sub has been filled, we must change the button's text.
      if (subFilled == 1){
        buttonID.innerHTML = "Filled"
        buttonID.value = "subRequested"
      } 
     


    }, "json" )
}


// function refreshSubbableShifts(){
//   var Table = document.getElementById("subbableShiftTable")
//   var shiftDic = {}//we will have key value pairs of the form {employeeID: [array of shiftIDS]}
//   //Get all the shifts 
//   //Now, we iterate through every row in the table:
//   for (i = 1; i < Table.rows.length; i++){
//     row = Table.rows[i];
//     //At each row, find the 5th cell, index 4, which has the button for sub requests.
//     cell = row.cells[4]

//     //next get the button's id, and then the shiftid.
//     theButton = cell.firstChild;
//     var idArray = theButton.id.split("_"); //subbableshiftbuttons have names of the form sub_shift_shiftid_emp_origEmployeeID
//     var shiftID = idArray[2];
//     var origEmployeeID = idArray[4]

    
//     if (origEmployeeID in shiftDic) {//A key for that employee exists already, with an associated array for its value.


//       shiftDic[origEmployeeID].push(shiftID)

//     }
//     else{ //A new key.
//       // console.log("hello")
//       shiftDic[origEmployeeID] = [shiftID]  //https://stackoverflow.com/questions/7196212/how-to-create-dictionary-and-add-key-value-pairs-dynamically/22315575
        



//     }


//     //shiftArray.push([shiftID, origEmployeeID]) //keep track of what shifts are in the table.
//     deleteSubbableShiftRow(Table, i, shiftID, origEmployeeID); //will check if a given shift is subbed for or if it's been removed, and if so, will delete it from the table.
//     }

//   //once you've hit the end of a table, it's time to see if there are any new subs that have been requested
//   findNewSubbableShifts(Table, shiftDic);

// }

function deleteSubbableShiftRow(Table, rowindex, shiftID, employeeID){
  postData = {"shiftID":shiftID, "employeeID":employeeID}
  $.get("/getSubRequestStatus", postData, function(data){ //If sub is filled, then we will delete the row that it originally came from.
      //TODO: Figure out how to deal with this and JSON.
      
      var subFilled = data.subFilled;
      var subRequested = data.subRequested;
      //If a sub has been filled or the request has been rescinded, we must delete the row.
      if (subFilled == 1 || subRequested == 0){
        Table.deleteRow(rowindex)
      } 
     


    }, "json" )

}

// function findNewSubbableShifts(Table, shiftDic){
// //TODO/Schematic of how this works:
// //We will first do an ajax call to get all the shift ids and employeeids of all subbable shifts.
// $.get("/getSubbableShifts", function(data){

//     for (var i = 0; i < data.length; i++){ //https://stackoverflow.com/questions/42499535/passing-a-json-object-from-flask-to-javascript
//       var employeeID = data[i].origEmployeeID.toString() //Didn't have tostring previously, and as a result isIn() below was returnign false, as shiftDic had a dictionary array of strings and I was comparing numbers.
//       var shiftID = data[i].shiftID.toString()
//       var combo = [shiftID, employeeID]
      
      
      
//       if (isIn(combo, shiftDic) == false){ //For a shift that's not already in the table.

//       insertNewSubbableShiftRow(Table, shiftID, employeeID)                                      //Submit a new shiftrequest.
//       //console.log(combo)
//       }
        
        
      

//       }
//     }

    
//     //Then, we will compare shiftArray to that list and see what remains i.e what new shifts there are.
// //Finally, we will iterate through the new shifts.
// //for each shift, we will submit an asynchronous call via insertNewSubbableShiftRow(), a callback function which will insert the new row.
   
// , "json")

// }

function insertNewSubbableShiftRow(shiftID, origEmployeeID){
  var table = document.getElementById("subbableShiftTable")
  rowIndex = table.rows.length; //Get the length of the table.

  // console.log(shiftID)
  // console.log(origEmployeeID)
  //How this will work:
  //submit an AJAX call to get the data from the row specified by shiftID and origEmployeeID.
  
  $.get('/getSubShiftID', {"shiftID":shiftID, "origEmployeeID":origEmployeeID}, function (data){ 

    //First, check that the shift is still requesting a sub:
    if (data.subRequested == true){//if yes, then go ahead and insert a row into the open shifts.

    var time = data.time
    var location = data.location
    var date = data.date
    var day = data.day
    //Once you have the data, create a row and insert the necessary data.

    var row = table.insertRow(rowIndex);
    var cell1 = row.insertCell(0)
    var cell2 = row.insertCell(1)
    var cell3 = row.insertCell(2)
    var cell4 = row.insertCell(3)
    var cell5 = row.insertCell(4)
    var cell6 = row.insertCell(5)

    
    cell1.innerHTML = time
    cell2.innerHTML = location
    cell3.innerHTML = date
    cell4.innerHTML = day
    cell


    }

    


  }, "json")

  


}

function pickupDropSub(theButton, subEmployeeID){
  //Check if you're clicking to pick up a sub.
  console.log(theButton.id)
  var idArray =  theButton.id.split("_");
  var origEmployeeID = idArray[4]
  var shiftID = idArray[2]
  //var subEmployeeID = 1001 //This is a placeholder, we must put it as an input eventually.

  //store the row of the button as well.
  var parentCell = theButton.parentElement
  var parentRow = parentCell.parentElement
  var parentRowIndex = parentRow.rowIndex;



  var postData = {"origEmployeeID":origEmployeeID, "subEmployeeID":subEmployeeID, "shiftID":shiftID}
  //var postData = JSON.stringify(postData)
  
  if (theButton.value == "pickupSub"){ //on clicking you will pick up a sub.
    
    $.post('/pickupSub', postData)
    
    theButton.innerText = "Subbing";

    theButton.value = "dropSub" //update button value to reflect that we unrequested a sub.
    
    //document.getElementById("subbableShiftTable").deleteRow(parentRowIndex)

    //Consider also dropping the row that the button exists in. Or not-currently it'll be autodropped as the refreshSubbableShifts method runs.
  }
  else if (theButton.value == "dropSub"){
      
    $.post('/dropSub', postData)

    theButton.innerText = "Sub?";

    theButton.value = "pickupSub" //update button value to reflect that we unrequested a sub.

    document.getElementById("subbingShiftTable").deleteRow(parentRowIndex) //delete the row from subbing shifts table.

    
  }

  

  //Once all is said and done, you will drop the row from the table. The reason is simple: if you are picking up a sub, then the row is in the subbableshifts table, and you must drop the row to prevent the user from clicking it again.
  //If you are dropping a sub, then you have a row in the subbingShifts table that you must drop because you are no longer subbing it.
  //Table.deleteRow(parentRow.rowIndex);
}



function isIn(array, shiftDic){
  //array[0] is shiftID, array[1] is employeeID
  var employeeID = array[1];
  var shiftID = array[0]

  if (employeeID in shiftDic){//If a key exists for the employee //https://stackoverflow.com/questions/1098040/checking-if-a-key-exists-in-a-javascript-object

    //determine if the employee has this shift.

    
    if (shiftDic[employeeID].indexOf(shiftID) != -1){
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


function switchLocation(button){

  var location = button.value
  console.log(location)
  console.log(button.id)

  $.get("/switchLocation", {"location":location})

}


// function isIn(subArray, array){
//   for (i = 0; i < array.length; i++){ //TODO: Optimize this search.

        
//         if (subArray[0] == array[i][0] && subArray[1] == array[i][1]){ // https://stackoverflow.com/questions/24943200/javascript-2d-array-indexof Why we can't use indexof...

//           return true;
//         }
//     }
// return false;
// }


function transmitData(data){ //IMPORTANT- Pass in the data as a string.
  $.post('/receiveAndTransmit', {"data":data})
}



function receiveTransmission(msg){
  //Each transmission message is plaintext in the form type_data_data_data_....
  //There are a variety of transmissions that we could receive. The type of transmission can be obtained from index 0 of the array resulting from splitting the message by _
  console.log(msg)
  msgArray = msg.split("_");

  msgType = msgArray[0];

  if (msgType == "pickupSub") {//this event indicates that a particular sub-requested shift was just picked up by a sub. It has data in the form pickupSub_shift_shiftID_emp_origEmpID 
    shiftID = msgArray[2]
    origEmployeeID = msgArray[4]
  }

  else if(msgType == "dropSub"){ //this event indicates that a particular shift which was being subbed no longer is. It has data in the form dropSub_shift_shiftID_emp_origEmpID 
    //extract the relevant data
    shiftID = msgArray[2]
    origEmployeeID = msgArray[4]

    insertNewSubbableShiftRow(shiftID, origEmployeeID); //check if the shift is still requesting a sub, and insert the subbable shift back into the subbable shift table.
    
  }
  // elseif(msgType == "requestedSub"){

  // }
  // elseif(msgType == "unrequestedSub"){

  // }

}

window.onload = updateClock();
//window.onload = enableDisableCheckin(checkedIn, checkInTime)
window.setInterval('updateClock()', 1000)


var source = new EventSource('/broadcast');
source.addEventListener('message', function(e){

  console.log(e.data)
  receiveTransmission(e.data);

})


//https://stackoverflow.com/questions/12693947/jquery-ajax-how-to-send-json-instead-of-querystring
//https://stackoverflow.com/questions/6587221/send-json-data-with-jquery

//https://stackoverflow.com/questions/14908864/how-can-i-use-data-posted-from-ajax-in-flask

