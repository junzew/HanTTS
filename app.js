const express = require('express')
var bodyParser = require('body-parser');
const spawn = require('child_process').spawn;
var fs = require('fs');
const path = require('path');
const utf8 = require('utf8');

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

app.get("/:text", function(req, res) {
	var text = utf8.decode(req.params.text);
	console.log(text)
	args = ["./main.py", 'synthesize', '--text', text, '--src', "./syllables/", '--dst', "./audio/"]
	var process = spawn('python3', args);
	var output = "";
    process.stdout.on('data', function(data){ output += data });
    process.stderr.on('data', function(data){ console.error(`stderr: ${data}`); });
	process.on("close", function(code) {
		if (code !== 0) {
			return res.send(`child process exited with code ${code}`)
		}
		console.log(output)
		console.log("sending response")

		res.sendFile(path.join(__dirname, "./audio/generated.mp3"))
	});
});
