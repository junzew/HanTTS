const express = require('express')
var bodyParser = require('body-parser');
const spawn = require('child_process').spawn;

const app = express()
app.use(express.static('public'))
app.use('/audio', express.static('audio'))
app.use(bodyParser.json()); // for parsing application/json

app.listen(3000, function () {
  console.log('app listening on port 3000')
});

app.post("/", function(req, res) {
	var text = req.body.text;
	console.log(text)
	var process = spawn('python',["../main.py", text]);
	var output = "";
    process.stdout.on('data', function(data){ output += data });
	process.on("close", function(code) {
		if (code !== 0) {
			return res.send('error')
		}
		console.log(output)
		console.log("sending response")
		res.send('<audio src="../audio/generated.wav" controls="true"></audio>')
	});

});
