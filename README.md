# HanTTS [![Build Status](https://travis-ci.org/junzew/HanTTS.svg?branch=master)](https://travis-ci.org/junzew/HanTTS)

Chinese Text-to-Speech(TTS)

汉字 => ["han4", "zi4"] => .wav audio

*Read this page in [简体中文](https://github.com/junzew/HanTTS/blob/master/README.zh.md)*
## Libraries Used

#### For turning Chinese characters into pinyin
- [pypinyin](https://github.com/mozillazg/python-pinyin)
- [jieba](https://github.com/fxsjy/jieba)

#### For processing .wav files
- [pydub](https://github.com/jiaaro/pydub)
- [pyAudio](https://people.csail.mit.edu/hubert/pyaudio/)

#### Web backend
- [Express](https://expressjs.com)

A list of all Chinese characters is obtained from [倉頡平台2012](https://chinese.stackexchange.com/questions/22484/list-of-all-traditional-chinese-characters), a Chinese input software.

## Build and Run

```
git clone https://github.com/junzew/HanTTS.git
cd HanTTS
pip install --user -r requires.txt
```

Download [`syllables.zip`](https://sourceforge.net/projects/hantts/files/?source=navbar) from SourceForge, and decompress under the directory `HanTTS`.

* Either run locally: `python main.py` 
* Or through web interface:
	`cd` into the `server` folder
	```
	npm install
	node app.js
	```
	Navigate to `localhost:3000` in a browser

## Use your own voice
- Record [five tones](https://en.wikipedia.org/wiki/Pinyin#Tones) of each [pinyin](https://en.wikipedia.org/wiki/Pinyin_table) listed in `mapping.json`
- Group them by the first letter (a,b,c,d, etc.), and save under folder `./recording` as `{letter}.wav`
- Then run `python process.py {letter}`for each `letter` to split recordings into individual pinyin
- Move valid .wav files from `./pre` to the folder `./syllables`
##
Based on the [text-to-speech-sample](https://github.com/alexram1313/text-to-speech-sample) project by [@alexram1313](https://github.com/alexram1313)