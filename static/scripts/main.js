window.onload = () => {
    var map = document.getElementById("map");
    console.log(map);
    map = L.map('map').setView([30.3708772695315, -97.7714258778241], 13);
    L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWRkaXlwIiwiYSI6ImNrejVxc2NmZjBzeXMyd25rYWt0dTV0eHoifQ.SBPsvrufSeHGFn5oyMDzKw', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiYWRkaXlwIiwiYSI6ImNrejVxc2NmZjBzeXMyd25rYWt0dTV0eHoifQ.SBPsvrufSeHGFn5oyMDzKw'
    }).addTo(map);

    var marker = `
    <h1>This is an event</h1>
    <p>This is the content of the event. <a href="/EventSignUp?eventID=120">Here is the signup page</a></p>
    <button>Hello</button>
    `;

    L.marker([30.3708772695315, -97.7714258778241]).addTo(map).bindPopup(marker).openPopup();
}
