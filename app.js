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
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir);
        console.log("created directory ./audio")
    }
});

app.post("/", function (req, res) {
    var text = req.body.text;

    console.log(text)
    args = ["./main.py", 'synthesize', '--text', text, '--src', "./syllables/", '--dst', "./audio/", '--type', 'wav']
    const pythonChoose = req.body.pythonChoose;
    let pythonAlias;
    if (pythonChoose && pythonChoose === 'python3') {
        pythonAlias = 'python3'
    } else {
        pythonAlias = 'python'
    }
    var process = spawn(pythonAlias, args);
    var output = "";
    process.stdout.on('data', function (data) {
        output += data
    });
    process.stderr.on('data', function (data) {
        console.error(`stderr: ${data}`);
    });
    process.on("close", function (code) {
        if (code !== 0) {
            return res.send(`child process exited with code ${code}`)
        }
        console.log(output)
        console.log("sending response")

        res.send('<audio src="./audio/generated.wav" controls="true"></audio>')
    });
});

app.get("/file", function (req, res) {
    res.download("./audio/generated.wav")
});

app.get("/:pythonVersion/:type/:decodeUTF8/:compressed/:speed/:text", function (req, res) {
    let text;
    const audioType = req.params.type;
    if (req.params.decodeUTF8 === 'true') {
        text = utf8.decode(req.params.text);
    } else {
        text = req.params.text;
    }
    const speed = req.params.speed;

    const args = ["./main.py",
        'synthesize',
        '--text', text,
        '--src', "./syllables/",
        '--dst', "./audio/",
        '--type', audioType,
        '--compressed', req.params.compressed,
        '--speed',speed
    ]
    const pythonChoose = req.params.pythonVersion;

    let pythonAlias;
    if (pythonChoose && pythonChoose === "python3") {
        pythonAlias = 'python3'
    } else {
        pythonAlias = 'python'
    }
    let process = spawn(pythonAlias, args);

    let output = "";
    process.stdout.on('data', function (data) {
        output += data
    });
    process.stderr.on('data', function (data) {
        console.error(`stderr: ${data}`);
    });
    process.on("close", function (code) {
        if (code !== 0) {
            return res.send(`child process exited with code ${code}`)
        }
        console.log(output)
        console.log("sending response")

        res.sendFile(path.join(__dirname, "./audio/generated." + audioType))
    });
});
