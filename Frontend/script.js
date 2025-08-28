function sendSOS() {
  alert('SOS Alert sent to emergency contacts!');
  
}

function getLocation() {
  const output = document.getElementById('location-output');
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition((position) => {
      const { latitude, longitude } = position.coords;
      output.innerHTML = `Latitude: ${latitude}, Longitude: ${longitude}`;
  
    }, () => {
      output.innerText = "Unable to retrieve your location.";
    });
  } else {
    output.innerText = "Geolocation not supported.";
  }


}
 
document.getElementById('sos-button').addEventListener('click', sendSOS);
document.getElementById('location-button').addEventListener('click', getLocation);    


