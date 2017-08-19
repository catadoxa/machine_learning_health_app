//document.addEventListener("DOMContentLoaded", execute_call);

function execute_call() {

	var req = new XMLHttpRequest();

	var payload = {"username": "123", "password": "123"};


    req.open("POST", "https://ml-health-app-stage.herokuapp.com/api/ml_data", true);
    //req.open("POST", "http://127.0.0.1:5000/api/ml_data", true);
    req.setRequestHeader("Content-type", "application/json");
	req.addEventListener("load", function() {
		if(req.status >= 200 && req.status < 400) {
			var response = JSON.parse(req.responseText);
            document.getElementById("data").textContent = "success!";
		} else {
			document.getElementById("data").textContent = "There was an error.";
		}
        event.preventDefault();	
	});
    req.send(JSON.stringify(payload));
	
}

execute_call();
