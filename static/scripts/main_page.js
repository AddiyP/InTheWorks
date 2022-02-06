var map;
var currLat;
var currLong;
var allMarkers = [];
var allMarkersNum = 0;

function init_map() {
    map = L.map('map').setView([30.264071306509383, -97.74124145507812], 13);
  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiYWRkaXlwIiwiYSI6ImNrejVxc2NmZjBzeXMyd25rYWt0dTV0eHoifQ.SBPsvrufSeHGFn5oyMDzKw', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'your.mapbox.access.token'
    }).addTo(map);

    map.on('contextmenu', function(e) {
        context_toggle(e.originalEvent);
        currLat = e.latlng.lat;
        currLong = e.latlng.lng;
    });
}
function context_hide() {
    document.querySelector("#custom_context_menu").style.display = "none";
}
function context_toggle(event) {
    var menu = document.querySelector("#custom_context_menu");
    if (menu.style.display === "none") {
        menu.style.display = "block";
        menu.style.left = event.pageX + "px";
        menu.style.top = event.pageY + "px";
    }
    else if (menu.style.display === "block") {
        context_hide();
        menu.style.left = event.pageX + "px";
        menu.style.top = event.pageY + "px";
    }
    menu.style.left = event.pageX + "px";
    menu.style.top = event.pageY + "px";
}
function open_event_menu() {
    context_hide();
    console.log("opening event menu");
}
function handle_sign_up(event) {
    event.preventDefault();
    var sign_up_form = document.querySelector("#sign_up_form");
    var span = document.querySelector("#sign_up_close");
    // Setup POST request
    var requestArgs = {};
    requestArgs.username = sign_up_form.username.value;
    requestArgs.email = sign_up_form.email.value;
    console.log(requestArgs);
    //document.body.style.cursor = "wait";
    //Post request. headers field ensures body is parsed as json
    fetch("/sign_up_handle", {method : "POST", body: JSON.stringify(requestArgs), headers: {"Content-type": "application/json; charset=UTF-8"}})
    .then(response => response.json())
    .then(json => {
        console.log(json["error"]);
        if (json["error"] === "false") {
            sessionStorage.setItem("user_id", json["user_id"]);
            sessionStorage.setItem("username", json["username"]);
            span.onclick();
        }
        else {
            console.log(json.error_message);
            document.querySelector("#sign_up_error").textContent = json["error_message"];
        }
    }).catch(error => {
        document.body.style.cursor = "normal";
    });
}
function handle_sign_in(event) {
    event.preventDefault();
    var sign_in_form = document.querySelector("#sign_in_form");
    var span = document.querySelector("#sign_in_close");
    //Setup POST request
    var requestArgs = {};
    requestArgs.username = sign_in_form.username.value;
    console.log(requestArgs);
    fetch("/sign_in_handle", {method:"POST", body:JSON.stringify(requestArgs), headers: {"Content-type": "application/json; charset=UTF-8"}})
    .then(response => response.json())
    .then(json => {
        if (json["error"] === "false") {
            sessionStorage.setItem("user_id", json["user_id"]);
            sessionStorage.setItem("username", json["username"]);
            span.onclick();
        }
        else {
            console.log(json["error_message"]);
            document.querySelector("#sign_in_error").textContent = json["error_message"];
        }
    });
}
function handle_create_event(event) {
    event.preventDefault();
    var create_event_form = document.querySelector("#create_event_form");
    var span = document.querySelector("#create_event_close");
    //Setup POST request
    var requestArgs = {};
    requestArgs.creator_id = sessionStorage.getItem("user_id") || "0";
    requestArgs.name = create_event_form.name.value;
    requestArgs.description = create_event_form.description.value;
    requestArgs.lat = currLat;
    requestArgs.lng = currLong;
    console.log(requestArgs);
    fetch("/create_event_handle", {method:"POST", body:JSON.stringify(requestArgs), headers:{"Content-type": "application/json; charset=UTF-8"}})
    .then(response => response.json())
    .then(json => {
        console.log(json["error"]);
        if (json["error"] === "false") {
            span.onclick();
        }
        else{
            console.log(json["error_message"]);
            console.log(document.querySelector("#create_event_error"));
            document.querySelector("#create_event_error").innerHTML = json["error_message"];
        }
    });
}
function init_sign_up_block() {
    var sign_up_block = document.querySelector("#sign_up_block");
    var sign_up_button = document.querySelector("#sign_up_button");
    var span = document.querySelector("#sign_up_close");

    sign_up_button.onclick = function() {
        sign_up_block.style.display = "block";
        document.querySelector("#sign_in_block").style.display = "none";
    }
    span.onclick = function() {
        sign_up_block.style.display = "none";
    }
    
    var sign_up_form = document.querySelector("#sign_up_form");
    sign_up_form.onsubmit = handle_sign_up;
}
function init_sign_in_block() {
    var sign_in_block = document.querySelector("#sign_in_block");
    var sign_in_button = document.querySelector("#sign_in_button");
    var span = document.querySelector("#sign_in_close");
    sign_in_button.onclick = function() {
        sign_in_block.style.display = "block";
    }
    span.onclick = function() {
        sign_in_block.style.display = "none";
    }
    var sign_in_form = document.querySelector("#sign_in_form");
    sign_in_form.onsubmit = handle_sign_in;
}
function init_create_event_block() {
    var create_event_block = document.querySelector("#create_event_block");
    var create_event_button = document.querySelector("#create_event_button");
    var span = document.querySelector("#create_event_close");
    create_event_button.onclick = function() {
        create_event_block.style.display = "block";
        context_hide();
    }
    span.onclick = function() {
        create_event_block.style.display = "none";
    }
    var create_event_form = document.querySelector("#create_event_form");
    create_event_form.onsubmit = handle_create_event;
}
function init_exit_blocks() {
    var modals = [
        document.querySelector("#sign_in_block"),
        document.querySelector("#sign_up_block"),
        document.querySelector("#create_event_block")
    ];
    window.onclick = function(event) {
        for (var i = 0; i < modals.length; i++) {
            if (event.target == modals[i]) {
                modals[i].style.display = "none";
            }
        }
    }
}
function handle_user_interest(event) {
    requestArgs = {
        "user_id" : sessionStorage.getItem("user_id"),
        "event_id" : event,
    }
    ;

    console.log(event);
    fetch("/show_interest", {method:"POST", body:JSON.stringify(requestArgs), headers: {"Content-type": "application/json; charset=UTF-8"}})
    .then(response => response.json())
    .then(json => console.log(json))
    ;
}
function template_pop_up(event) {
    return returned = `
    <h6>${event["name"]}<small> by ${event["creator_name"]}</small></h6>
    <p id="event_description">${event["description"]} <br>
    <a href="#">${event["num_interest"]}</a> are interested. <a href="#" onclick=\"handle_user_interest(${parseInt(event["event_id"])})\">Express your interest.</a>
    </p>
    </div>
    
    `;
}
function template_nav_block(event) {
    var icon = `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-megaphone-fill" viewBox="0 0 16 16">
    <path d="M13 2.5a1.5 1.5 0 0 1 3 0v11a1.5 1.5 0 0 1-3 0v-11zm-1 .724c-2.067.95-4.539 1.481-7 1.656v6.237a25.222 25.222 0 0 1 1.088.085c2.053.204 4.038.668 5.912 1.56V3.224zm-8 7.841V4.934c-.68.027-1.399.043-2.008.053A2.02 2.02 0 0 0 0 7v2c0 1.106.896 1.996 1.994 2.009a68.14 68.14 0 0 1 .496.008 64 64 0 0 1 1.51.048zm1.39 1.081c.285.021.569.047.85.078l.253 1.69a1 1 0 0 1-.983 1.187h-.548a1 1 0 0 1-.916-.599l-1.314-2.48a65.81 65.81 0 0 1 1.692.064c.327.017.65.037.966.06z"/>
  </svg>`;
    return `
    <div id="nav_event">
    
    <h6>${event["name"]}<small> by ${event["creator_name"]}</small></h6>
    <p id="event_description"><small>${event["description"]} -
    <a href="#">${event["num_interest"]}</a> are interested.</small>
    </p>
    <a href="#"onclick=\"handle_user_interest(${parseInt(event["event_id"])})\">${icon}</a>
    </div><hr>
    `;
}
function query_to_map() {
    var requestArgs = {};
    fetch("/get_events_handle", {method:"POST", body:JSON.stringify(requestArgs), headers: {"Content-type": "application/json; charset=UTF-8"}})
    .then(response => response.json())
    .then(json => {
        for (var i = 0; i < allMarkersNum; i++) {
            map.removeLayer(allMarkers[i]);
        }
        var events = json["events"];
        var navbar_events_holder = document.querySelector("#event_block_holder");
        navbar_events_holder.innerHTML = '';
        for (var ev in events) {
            var curr_event = events[ev];
            console.log(curr_event);
            var marker = L.marker([parseFloat(curr_event["lat"]), parseFloat(curr_event["lng"])]).addTo(map);
            marker.bindPopup(template_pop_up(curr_event));
            allMarkers[allMarkersNum] = marker;
            allMarkersNum++; 

            var newEntry = document.createElement("div");
            newEntry.innerHTML = template_nav_block(curr_event);
            navbar_events_holder.appendChild(newEntry);
                }
    }).catch(error => {
        console.log("error")
    });
}
window.onload = function() {
    init_map();
    init_sign_up_block();
    init_sign_in_block();
    init_create_event_block();
    init_exit_blocks();

    document.querySelector("#refresh_map").onclick = query_to_map;

    document.addEventListener("mousedown", function(event) {
        var x = event.clientX;
        var y = event.clientY;
        var elemUnder = document.elementFromPoint(x, y);
        if (elemUnder === document.querySelector("#create_event_button")) {
        }
        else {
            context_hide();
        }
    });
}