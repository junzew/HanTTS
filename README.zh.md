# HanTTS [![Build Status](https://travis-ci.org/junzew/HanTTS.svg?branch=master)](https://travis-ci.org/junzew/HanTTS)

汉语文字转语音 (TTS)

汉字 => 拼音 ["han4", "zi4"] => .wav音频

(environment: python 3)
## 使用的库

#### 汉字转拼音
- [pypinyin](https://github.com/mozillazg/python-pinyin)
- [jieba](https://github.com/fxsjy/jieba)

#### 处理、播放.wav音频文件
- [pydub](https://github.com/jiaaro/pydub)
- [pyAudio](https://people.csail.mit.edu/hubert/pyaudio/)

#### Web
- [Express](https://expressjs.com)

全部汉字列表从[倉頡平台2012](https://chinese.stackexchange.com/questions/22484/list-of-all-traditional-chinese-characters)获得

## 运行

```
git clone https://github.com/junzew/HanTTS.git
cd HanTTS
pip install --user -r requires.txt
```

- 本地执行 `python main.py`
- 或 Web
	- `cd` 到 `server` 文件夹下
	- `npm install`
	- `node app.js`
	- 浏览器里打开`localhost:3000` 

## 进阶使用
自己设置音频参数
`http://127.0.0.1:3000/pythonAlias/audioType/decodeUTF8/compressed/speed/text`

For example
```
http://127.0.0.1:3000/python3/wav/false/true/1/测试
```

|  params   | accept  |note|
|  ----  | ----  |----|
| pythonAlias  | python, python3 |如果你的设备python别名为python3，请填写python3|
| audioType  | wav, mp3 (其他没有测试) | 音频输出格式|
|decodeUTF8|true, false|是否文字需要解码utf-8|
|compressed|true, false|是否输出一个压缩文件|
|speed|数字, 比如 -0.5, 1, 3 |( 可以使用float或者负数 ), 如果不想改变速度，填写 0|
|text|中文|TTS的内容|

## 录制新的语音库
- 按阴平、阳平、上声、去声、轻声的顺序录下 mapping.json 里每一个音节的五个声调
- 按开头字母(letter)分组, 将文件存在 ./recording/{letter}.wav下
- 运行 `python process.py {letter}` 将{letter}.wav 完整的录音分成独立的拼音
- 检查核对`./pre`文件夹中的拼音.wav后导入文件夹`./syllables`

## 
基于[@alexram1313](https://github.com/alexram1313)的[text-to-speech-sample](https://github.com/alexram1313/text-to-speech-sample)