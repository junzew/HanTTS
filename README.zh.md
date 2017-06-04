# HanTTS

汉语文字转语音 (TTS)

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
* `git clone https://github.com/junzew/HanTTS.git`

* 下载并解压 [syllables.zip](https://sourceforge.net/projects/hantts/files/?source=navbar) on SourceForge

* `python main.py`

## 录制新的语音库
- 按阴平、阳平、上声、去声、轻声的顺序录下 mapping.json 里每一个音节的五个声调
- 按开头字母(letter)分组, 将文件存在 ./recording/{letter}.wav下
- 运行 `python process.py {letter}` 将{letter}.wav 完整的录音分成独立的拼音
- 检查核对`./pre`文件夹中的拼音.wav后导入文件夹`./syllables`

## 
基于[@alexram1313](https://github.com/alexram1313)的[text-to-speech-sample](https://github.com/alexram1313/text-to-speech-sample)