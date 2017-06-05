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

class TextToSpeech:

    CHUNK = 1024
    punctuation = ['，', '。','？','！','“','”','；','：','（',"）"]

    def __init__(self):
        pass

    def speak(self, text):
        # syllables = lazy_pinyin(text, style=pypinyin.TONE)
        syllables = lazy_pinyin(text, style=pypinyin.TONE2)
        print(syllables)
        delay = 0
        for syllable in syllables:
            sound = TextToSpeech.format_syll(syllable)
            path = "syllables/"+sound+".wav"
            print(path)
            _thread.start_new_thread(TextToSpeech._play_audio, (path, delay))
            # TextToSpeech._play_audio(TextToSpeech.format_syll(syllable), delay)
            delay += 0.355

    def synthesize(self, text):
        """
        Synthesize .wav from text
        Directory is relative to server/app.js
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
            path = "../syllables/"+sound+".wav"
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

        result.export("./audio/generated.wav", format="wav")
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

if __name__ == '__main__':
    tts = TextToSpeech()
    # while True:
    #     tts.speak(input('输入中文：'))
    text = sys.argv[1:][0]
    tts.synthesize(text)
