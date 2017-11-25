const express = require('express')
var bodyParser = require('body-parser');
const spawn = require('child_process').spawn;
var fs = require('fs');
var requests = 0;
const app = express()
app.use(express.static('public'))
app.use('/audio', express.static('audio'))
app.use(bodyParser.json()); // for parsing application/json
app.use(function (req, res, next) { // no cache
    res.header('Cache-Control', 'private, no-cache, no-store, must-revalidate');
    res.header('Expires', '-1');
    res.header('Pragma', 'no-cache');
    next()
});

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
app.get("/count", function(req,res) {
	requests++;
	res.send(requests.toString());
});
app.post("/", function(req, res) {
	var text = req.body.text;
	var IP = req.ip;
	console.log('POST / ' + IP);
	console.log(text);
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
		res.send(IP);
		// res.send('<audio id="sound0" src="../audio/generated'+IP+'.wav" controls="true"></audio>')
	});
});

app.get("/file", function(req, res) {
	var IP = req.ip;
	console.log("GET /file " + IP)
	var file = './audio/generated'+IP+'.wav'
	if(!fs.existsSync()) {
		console.log(file + " does not exist")
		return res.status(404).end();
	}
	res.download(file, function(err) {
		if (err) {
			console.log(err)
		} else {
			console.log("download success")
		}
	})
});
