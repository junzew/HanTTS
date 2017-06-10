const express = require('express')
var bodyParser = require('body-parser');
const spawn = require('child_process').spawn;
var fs = require('fs');

const app = express()
app.use(express.static('public'))
app.use('/audio', express.static('audio'))
app.use(bodyParser.json()); // for parsing application/json

app.listen(3000, function () {
  console.log('app listening on port 3000')
	var dir = './audio';
	if (!fs.existsSync(dir)){
	    fs.mkdirSync(dir);
	    console.log("created directory ./audio")
	}
});

app.options("/", function(req, res) {
	res.set("Access-Control-Allow-Origin", "*");
	res.set("Content-Type","text/plain");
	res.set("Access-Control-Allow-Methods","POST, GET, OPTIONS");
	res.set("Access-Control-Allow-Headers", "Content-Type, x-requested-with ");
	res.status(200).end();
	
});
app.post("/", function(req, res) {
	var text = req.body.text;
	console.log(text);
	var IP = req.ip;
	var process = spawn('python3',["../main.py", text, IP]);
	var output = "";
    process.stdout.on('data', function(data){ output += data });
	process.on("close", function(code) {
		res.set("Access-Control-Allow-Origin", "*");
		res.set("Content-Type","text/plain");
		res.set("Access-Control-Allow-Headers", "x-requested-with");
		if (code !== 0) {
			return res.send('error')
		}
		console.log(output)
		console.log("sending response")

		res.send('<audio id="sound0" src="../audio/generated'+IP+'.wav" controls="true"></audio>')
	});

});
