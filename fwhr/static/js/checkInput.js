Number.isInteger = Number.isInteger || function(value) {
  return typeof value === 'number' && 
      isFinite(value) && 
      Math.floor(value) === value;
  };
function checkCountry() {
  var f = document.getElementById("input-country").value
  if (f == '') {
    return false;
  }
  return true;
}

function checkEthn() {
  var f = document.getElementById("input-ethn").value
  if (f == '') {
    return false;
  }
  return true;
}

function checkGender() {
  var f = document.getElementById("input-gender").value
  if (f == '') {
    return false;
  }
  return true;
}

function checkAge() {
  var f = document.getElementById("input-age").value
  if (f == ''  || Number.isInteger(f) || parseInt(f) < 1 || parseInt(f) > 99) {
    return false;
  }
  return true;
}

function checkHeight() {
  var f = document.getElementById("input-height").value
  if (f == '' || Number.isInteger(f) || parseInt(f) < 100 || parseInt(f) > 255) {
    return false;
  }
  return true;
}

function checkWeight() {
  var f = document.getElementById("input-weight").value
  if (f == '' || Number.isInteger(f) || parseInt(f) < 1 || parseInt(f) > 255) {
    return false;
  }
  return true;
}

function checkGender() {
  var f = document.getElementById("input-gender").value
  if (f == '') {
    return false;
  }
  return true;
}


function checkOccupation() {
  var f = document.getElementById("input-occupation").value
  if (f == '') {
    return false;
  }
  return true;
}

function checkFile() {
  var f = document.getElementById("inputGroupFile04").value
  if (f == '') {
    return false;
  }
  return true;
}

function checkForm() {
  var warning_color = "#e91e1eb5";

  if (checkCountry() && checkEthn() && checkGender() && checkAge() && checkFile()) return true;
  else {
    if(!checkCountry()) document.getElementById("label-country").style.backgroundColor = warning_color;
    else document.getElementById("label-country").style.backgroundColor = "#e9ecef";
    
    if(!checkEthn()) document.getElementById("label-ethn").style.backgroundColor = warning_color;
    else document.getElementById("label-ethn").style.backgroundColor = "#e9ecef";

    if(!checkGender()) document.getElementById("label-gender").style.backgroundColor = warning_color;
    else document.getElementById("label-gender").style.backgroundColor = "#e9ecef";

    if(!checkAge()) document.getElementById("label-age").style.backgroundColor = warning_color;
    else document.getElementById("label-age").style.backgroundColor = "#e9ecef";

    if(!checkHeight()) document.getElementById("label-height").style.backgroundColor = warning_color;
    else document.getElementById("label-height").style.backgroundColor = "#e9ecef";

    if(!checkWeight()) document.getElementById("label-weight").style.backgroundColor = warning_color;
    else document.getElementById("label-weight").style.backgroundColor = "#e9ecef";

    if(!checkFile()) document.getElementById("label-file").style.backgroundColor = warning_color;
    else document.getElementById("label-file").style.backgroundColor = "#e9ecef";

    
    if(!checkOccupation()) document.getElementById("label-occupation").style.backgroundColor = warning_color;
    else document.getElementById("label-occupation").style.backgroundColor = "#e9ecef";


    alert("Some values are invalid.");
    return false;
  }
}