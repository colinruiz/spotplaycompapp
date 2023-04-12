// scripts.js

document.getElementById("submit-button").addEventListener("click", function() {
  const formOne = document.getElementById("formone");
  const formTwo = document.getElementById("formtwo");

  formOne.addEventListener("submit", function(event) {
    event.preventDefault(); // prevent default form submission behavior
    const playlistOne = document.getElementById("playlist_id1").value;
    fetch('/compare-playlists', {
      method: 'POST',
      body: JSON.stringify({ playlist1: playlistOne })
    })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
  });

  formTwo.addEventListener("submit", function(event) {
    event.preventDefault(); // prevent default form submission behavior
    const playlistTwo = document.getElementById("playlist_id2").value;
    fetch('/compare-playlists', {
      method: 'POST',
      body: JSON.stringify({ playlist2: playlistTwo })
    })
    .then(response => response.json())
    .then(data => {
      // update the "result" element with the response data
      const Element = document.getElementById("compare_message");
      Element.innerHTML = data.message;
    })
    .catch(error => console.error(error));
  });
  
});



function showInput(selectElement) {
  var otherOption = "other";
  
  if (selectElement.value === otherOption) {
    var inputElement = document.createElement("input");
    inputElement.type = "text";
    if (selectElement.form.id === 'formone') {
      inputElement.id = "playlist_id1";
    } else {
      inputElement.id = "playlist_id2";
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
    } else {
      selectElement.id = "playlist_id2";
    }
  }
}


function comparePlaylists(playlist1, playlist2) {

}
