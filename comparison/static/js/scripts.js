// scripts.js

function showInput(selectElement) {
  var otherOption = "other";
  
  if (selectElement.value === otherOption) {
    var inputElement = document.createElement("input");
    inputElement.type = "text";
    if (selectElement.form.id === 'formone') {
      inputElement.id = "playlist_id1";
      inputElement.name = "data1"
    } else {
      inputElement.id = "playlist_id2";
      inputElement.name = "data2"
    }
    inputElement.placeholder = "Enter Playlist ID or Link...";
    inputElement.className = "form-control mt-2";
    selectElement.parentNode.insertBefore(inputElement, selectElement.nextSibling);
  } else {
    var inputElement = selectElement.nextSibling;
    if (inputElement && inputElement.tagName === "INPUT") {
      inputElement.remove();
    }
    if (selectElement.form.id === 'formone') {
      selectElement.id = "playlist_id1";
      selectElement.name = "data1"
    } else {
      selectElement.id = "playlist_id2";
      selectElement.name = "data2"
    }
  }
}


