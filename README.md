# HanTTS

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

A list of all Chinese characters is obtained from [倉頡平台2012](https://chinese.stackexchange.com/questions/22484/list-of-all-traditional-chinese-characters), a Chinese input software.

## How to run
* `git clone https://github.com/junzew/HanTTS.git`

* Download and decompress [`syllables.zip`](https://sourceforge.net/projects/hantts/files/?source=navbar) on SourceForge

* `python main.py`

## Build a Chinese TTS engine using your own voice
- Record [five tones](https://en.wikipedia.org/wiki/Pinyin#Tones) of each [pinyin](https://en.wikipedia.org/wiki/Pinyin_table) listed in mapping.json
- Group them by the first letter (a,b,c,d, etc.), and save under folder `./recording` as {letter}.wav
- Then run `python process.py {letter}`for each letter to split recordings into individual pinyin
- Move valid .wav files from `./pre` to the folder `./syllables`

##
Based on the [text-to-speech-sample](https://github.com/alexram1313/text-to-speech-sample) project by [@alexram1313](https://github.com/alexram1313)