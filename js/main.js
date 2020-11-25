heistsData = null;
difficultiesData = null;
gearData = null;

gameToRoll = "Payday2";

// https://stackoverflow.com/questions/2532218/pick-random-property-from-a-javascript-object
var randomProperty = function (obj) {
    var keys = Object.keys(obj);
    var key = keys[ keys.length * Math.random() << 0]
    return {"key": key, "value": obj[key] };
};

window.onload = startup;


function startup() {
	$.ajax({
		async: false,
		url: 'js/data/heists.json',
		dataType: 'json',
		success: function(response) {
			try { 
				heistsData = response;
			} catch (err) {
				(console.error || console.log).call(console, err.stack || err);
				alert('Error retrieving data from the JSON file!\nPlease contact the developers!');
			}
		},
		error: function() { alert('Unable to contact the server!\nPlease contact the developers!'); }
	});
	$.ajax({
		async: false,
		url: 'js/data/difficulties.json',
		dataType: 'json',
		success: function(response) {
			try { 
				difficultiesData = response;
			} catch (err) {
				(console.error || console.log).call(console, err.stack || err);
				alert('Error retrieving data from the JSON file!\nPlease contact the developers!');
			}
		},
		error: function() { alert('Unable to contact the server!\nPlease contact the developers!'); }
	});
	$.ajax({
		async: false,
		url: 'js/data/gear.json',
		dataType: 'json',
		success: function(response) {
			try { 
				gearData = response;
			} catch (err) {
				(console.error || console.log).call(console, err.stack || err);
				alert('Error retrieving data from the JSON file!\nPlease contact the developers!');
			}
		},
		error: function() { alert('Unable to contact the server!\nPlease contact the developers!'); }
	});

	RandomizeHeists()
	RandomizeGear()
}

function ChangeGameType() {
	if(gameToRoll == "Payday2") gameToRoll = "Payday1";
	else if(gameToRoll == "Payday1") gameToRoll = "Payday2";

	RandomizeHeists();
	RandomizeGear();
}

function RandomizeHeists() {
	console.log("Rolling heists roulette for game: " + gameToRoll)

	gameHeists = heistsData[gameToRoll]
	gameDifficulties = difficultiesData[gameToRoll]

	randomHeistDict = randomProperty(gameHeists)
	randomDifficulty = randomProperty(gameDifficulties)

	randomHeistName = randomHeistDict["key"]
	randomHeistData = randomHeistDict["value"]
	heistLength = randomHeistData["days"]

	console.log("Rolled heist: " + randomHeistName + " | Difficulty: " + randomDifficulty["key"])

	document.getElementById("heistName").innerText = randomHeistName
	document.getElementById("contractor").innerText = randomHeistData["contractor"]
	document.getElementById("heistLength").innerText = heistLength + (heistLength > 1 ? " Days" : " Day")

	document.getElementById("diffImg").src = randomDifficulty["value"]
	document.getElementById("diffImg").title = randomDifficulty["key"]
	
	if(randomHeistData["stealthable"] && randomHeistData["loudable"]) {
		document.getElementById("stealthable").innerText = (Math.random() << 0 == true) ? "No" : "Yes"
		document.getElementById("stealthImg").src = "./img/assets/notes/ghost/cn_minighost.png"
	}
	else if(randomHeistData["loudable"] && !randomHeistData["stealthable"]) {
		document.getElementById("stealthable").innerText = "No"
		// Empty 16x16 pixel for browser compatability
		document.getElementById("stealthImg").src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAQAAAC1+jfqAAAAEUlEQVR42mNkIAAYRxWMJAUAE5gAEdz4t9QAAAAASUVORK5CYII="
	}
	else if(randomHeistData["stealthable"]) {
		document.getElementById("stealthable").innerText = "Yes"
		document.getElementById("stealthImg").src = "./img/assets/notes/ghost/cn_minighost.png"
	}
}

function RandomizeGear() {
	console.log("Rolling gear roulette for game: " + gameToRoll)
	gameGear = gearData[gameToRoll]
	primaryWep = randomProperty(gameGear["Primary"])["value"]
	secondaryWep = randomProperty(gameGear["Secondary"])["value"]
	throwableWep = ("Throwable" in gameGear) ? randomProperty(gameGear["Throwable"])["value"] : "N/A"
	meleeWep = ("Melee" in gameGear) ? randomProperty(gameGear["Melee"])["value"] : "N/A"

	document.getElementById("primary").innerText = primaryWep
	document.getElementById("secondary").innerText = secondaryWep
	document.getElementById("throwable").innerText = throwableWep
	document.getElementById("melee").innerText = meleeWep
}