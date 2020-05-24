const express = require('express')
var bodyParser = require('body-parser');
const spawn = require('child_process').spawn;
var fs = require('fs');

const app = express()
app.use(express.static('public'))
app.use('/audio', express.static('audio'))
app.use(bodyParser.json()); // for parsing application/json

app.listen(process.env.PORT || 3000, function () {
	console.log('app listening on port 3000')
	var dir = './audio';
	if (!fs.existsSync(dir)){
	    fs.mkdirSync(dir);
	    console.log("created directory ./audio")
	}
});

app.post("/", function(req, res) {
	var text = req.body.text;
	console.log(text)
	args = ["./main.py", 'synthesize', '--text', text, '--src', "./syllables/", '--dst', "./audio/"]
	var process = spawn('python', args);
	var output = "";
    process.stdout.on('data', function(data){ output += data });
	process.on("close", function(code) {
		if (code !== 0) {
			return res.send('error')
		}
		console.log(output)
		console.log("sending response")

		res.send('<audio src="./audio/generated.wav" controls="true"></audio>')
	});
});

app.get("/file", function(req, res) {
	res.download("./audio/generated.wav")
});
