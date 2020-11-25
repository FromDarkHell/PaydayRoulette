heistsData = null;
difficultiesData = null;
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

	RollRoulette()
}

function ChangeGameType() {
	if(gameToRoll == "Payday2") gameToRoll = "Payday1";
	else if(gameToRoll == "Payday1") gameToRoll = "Payday2";
	RollRoulette();
}

function RollRoulette() {
	console.log("Rolling roulette for game: " + gameToRoll)

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
		document.getElementById("stealthImg").src = ""
	}
	else if(randomHeistData["stealthable"]) {
		document.getElementById("stealthable").innerText = "Yes"
		document.getElementById("stealthImg").src = "./img/assets/notes/ghost/cn_minighost.png"
	}

}