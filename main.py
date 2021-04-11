# -*- coding=utf-8 -*-
# Author: junzew
# Date: 2017 May 27
# Adapted from code written by Alex I. Ramirez @alexram1313 arcompware.com

from pypinyin import lazy_pinyin
import pypinyin
import pydub
from pydub import AudioSegment
from pathlib import Path
import wave
import pyaudio
import _thread
import time
import sys
import os
import requests
import atc
import argparse

# for demo only, please replace with your own API key
Turing_API_key = "64c88489ad7f432591d702ec1334dedc" 
Turing_API_address = "http://www.tuling123.com/openapi/api"

class TextToSpeech:

    CHUNK = 1024
    punctuation = ['，', '。','？','！','“','”','；','：','（',"）",":",";",",",".","?","!","\"","\'","(",")"]

    def __init__(self):
        pass

    def speak(self, text):
        syllables = lazy_pinyin(text, style=pypinyin.TONE3)
        print(syllables)
        delay = 0
        
        def preprocess(syllables):
            temp = []
            for syllable in syllables:
                for p in TextToSpeech.punctuation:
                    syllable = syllable.replace(p, "")
                if syllable.isdigit():
                    syllable = atc.num2chinese(syllable)
                    new_sounds = lazy_pinyin(syllable, style=pypinyin.TONE3)
                    for e in new_sounds:
                        temp.append(e)
                else:
                    temp.append(syllable)
            return temp

        syllables = preprocess(syllables)
        for syllable in syllables:
            path = "syllables/"+syllable+".wav"
            _thread.start_new_thread(TextToSpeech._play_audio, (path, delay))
            delay += 0.355

    def synthesize(self, text, src, dst):
        """
        Synthesize .wav from text
        src is the folder that contains all syllables .wav files
        dst is the destination folder to save the synthesized file
        """
        print("Synthesizing ...")
        delay = 0
        increment = 355 # milliseconds
        pause = 500 # pause for punctuation
        syllables = lazy_pinyin(text, style=pypinyin.TONE3)

        # initialize to be complete silence, each character takes up ~500ms
        result = AudioSegment.silent(duration=500*len(text))
        for syllable in syllables:
            path = src+syllable+".wav"
            sound_file = Path(path)
            # insert 500 ms silence for punctuation marks
            if syllable in TextToSpeech.punctuation:
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

        result.export(directory+"/generated.wav", format="wav")
        print("Exported.")

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

def start_chatting(key, location):
    print("你好!")
    key = Turing_API_key if key is None else key
    location = "北京市中关村" if location is None else location
    while True:
        sentence = input('输入中文：')
        r = requests.post(
            Turing_API_address, 
            json = {
            "key": key,
            "info": sentence, 
            "loc": location, 
            "userid":"1"
            })
        response = r.json()["text"]
        print(response)
        tts.speak(response)

if __name__ == '__main__':
    tts = TextToSpeech()
    
    parser = argparse.ArgumentParser(description="HanTTS: Chinese Text-to-Speech program")
    subparsers = parser.add_subparsers(title="subcommands", help='optional subcommands', dest='cmd')
    
    synthesize_parser = subparsers.add_parser('synthesize', help='synthesize audio from text')
    synthesize_parser.add_argument('--text', help='the text to convert to speech', dest='text')
    synthesize_parser.add_argument('--src', help='source directory of audio library', dest='src')
    synthesize_parser.add_argument('--dst', help='destination directory for generated .wav file', dest='dst')

    chat_parser = subparsers.add_parser('chat', help='chat using Turing Robot API')
    chat_parser.add_argument('--key', help='Turing Robot API key', dest='api_key')
    chat_parser.add_argument('--location', help='your physical location', dest='location')

    args = parser.parse_args()
    if args.cmd == 'synthesize':
        if not args.text:
            synthesize_parser.print_help()
            print('ERROR: Missing argument --text')
            sys.exit(1)
        if not args.src:
            synthesize_parser.print_help()
            print('ERROR: Missing argument --src')
            sys.exit(1)
        if not args.dst:
            synthesize_parser.print_help()
            print('ERROR: Missing argument --dst')
            sys.exit(1)
        tts.synthesize(args.text, args.src, args.dst)
    elif args.cmd == 'chat':
        start_chatting(args.api_key, args.location)
    else:
        while True:
            tts.speak(input('输入中文：'))


