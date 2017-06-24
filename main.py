# -*- coding=utf-8 -*-
# Author: junzew
# Date: 2017 May 27
# Adapted from code written by Alex I. Ramirez @alexram1313 arcompware.com

from pypinyin import lazy_pinyin
import pypinyin
from pydub import AudioSegment
from pathlib import Path
import wave
import pyaudio
import _thread
import time
import sys
import os
import requests

class TextToSpeech:

    CHUNK = 1024
    punctuation = ['，', '。','？','！','“','”','；','：','（',"）",":",";",",",".","?","!","\"","\'","(",")"]

    def __init__(self):
        pass

    def speak(self, text):
        # syllables = lazy_pinyin(text, style=pypinyin.TONE)
        syllables = lazy_pinyin(text, style=pypinyin.TONE2)
        print(syllables)
        delay = 0
        
        def preprocess(syllables):
            temp = []
            for syllable in syllables:
                for p in TextToSpeech.punctuation:
                    syllable = syllable.replace(p, "")
                if syllable.isdigit():
                    syllable = atc.num2chinese(syllable)
                    new_sounds = lazy_pinyin(syllable, style=pypinyin.TONE2)
                    for e in new_sounds:
                        temp.append(e)
                else:
                    temp.append(syllable)
            return temp

        syllables = preprocess(syllables)
        for syllable in syllables:
            
            sound = TextToSpeech.format_syll(syllable)
            path = "syllables/"+sound+".wav"
            # print(path)
            _thread.start_new_thread(TextToSpeech._play_audio, (path, delay))
            # TextToSpeech._play_audio(TextToSpeech.format_syll(syllable), delay)
            delay += 0.355

    def synthesize(self, text, src="./syllables/", dst="./audio/"):
        """
        Synthesize .wav from text
        Directory is relative to server/app.js
        src is the folder that contains all syllables
        dst is the destination folder to save the synthesized file
        """
        print("Synthesizing ...")
        delay = 0
        increment = 355 # milliseconds
        pause = 500 # pause for punctuation
        syllables = lazy_pinyin(text, style=pypinyin.TONE2)

        # initialize to be complete silence, each character takes up ~500ms
        result = AudioSegment.silent(duration=500*len(text))
        for syllable in syllables:
            sound = TextToSpeech.format_syll(syllable)
            path = src+sound+".wav"
            sound_file = Path(path)
            # insert 500 ms silence for punctuation marks
            if sound in TextToSpeech.punctuation:
                short_silence = AudioSegment.silent(duration=pause)
                result = result.overlay(short_silence, position=delay)
                delay += increment
                continue
            # skip sound file that doesn't exist
            if not sound_file.is_file():
                continue
            segment = AudioSegment.from_wav(path)
            result = result.overlay(segment, position=delay)
            delay += increment

        directory = dst
        if not os.path.exists(directory):
            os.makedirs(directory)

        result.export(directory+"generated.wav", format="wav")
        print("Exported.")

    def format_syll(syllable):
        """
        ba2ng -> bang2
        """
        result = syllable
        for i in range(len(syllable)):
            if syllable[i].isdigit():
                result = syllable[:i]+syllable[i+1:]+syllable[i]
        return result

    def _play_audio(path, delay):
        try:
            time.sleep(delay)
            wf = wave.open(path, 'rb')
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
            
            data = wf.readframes(TextToSpeech.CHUNK)
            
            while data:
                stream.write(data)
                data = wf.readframes(TextToSpeech.CHUNK)
        
            stream.stop_stream()
            stream.close()

            p.terminate()
            return
        except:
            pass

    
import atc
APIkey = "64c88489ad7f432591d702ec1334dedc";
if __name__ == '__main__':
    tts = TextToSpeech()
    if len(sys.argv[1:]) == 0:
        while True:
            tts.speak(input('输入中文：'))
    else:
        option = sys.argv[1:][0]
        if option == '-s': # synthesize    
            text = sys.argv[1:][1]
            tts.synthesize(text)
        elif option == '-c': # chat
            print("Hello there!")
            while True:
                sentence = input('输入中文：')
                r = requests.post(
                    "http://www.tuling123.com/openapi/api", 
                    json = {
                    "key": APIkey,
                    "info": sentence, 
                    "loc":"北京市中关村", 
                    "userid":"1"
                    })
                response = r.json()["text"]
                print(response)
                tts.speak(response)
        else:
            print("usage: python main.py [-sc] {text}")
            print("                       -s synthesize")
            print("                       -c chat")


