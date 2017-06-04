# HanTTS

汉语文字转语音 Chinese Text-to-Speech(TTS)

汉字 => 拼音 ["han4", "zi4"] => 读音

## 使用的库

#### 汉字转拼音
- [pypinyin](https://github.com/mozillazg/python-pinyin)
- [jieba](https://github.com/fxsjy/jieba)

#### 处理、播放.wav音频文件
- [pydub](https://github.com/jiaaro/pydub)
- [pyAudio](https://people.csail.mit.edu/hubert/pyaudio/)

全部汉字列表从[倉頡平台2012](https://chinese.stackexchange.com/questions/22484/list-of-all-traditional-chinese-characters)获得

## 运行
`
git clone https://github.com/junzew/HanTTS.git
`

解压 syllables.zip

`python main.py`

## Build a Chinese TTS engine using your own voice
Record five tones of each pinyin listed in mapping.json, group them by the keys (a,b,c,d, etc.), and save under folder /recording as {key}.wav
Then run process.py for each key to split into individual syllables.

##
基于alexram1313的[英文版](https://github.com/alexram1313/text-to-speech-sample)text-to-speech-sample