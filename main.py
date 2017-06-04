# Author: junzew
# Date: 2017 May 27
# Adapted from code written by Alex I. Ramirez @alexram1313 arcompware.com

from pypinyin import lazy_pinyin
import pypinyin
import wave
import pyaudio
import _thread
import time

class TextToSpeech:

    CHUNK = 1024

    def __init__(self):
        pass

    def speak(self, text):
        # syllables = lazy_pinyin(text, style=pypinyin.TONE)
        syllables = lazy_pinyin(text, style=pypinyin.TONE2)
        print(syllables)
        delay = 0
        for syllable in syllables:
            _thread.start_new_thread(TextToSpeech._play_audio, (TextToSpeech.format_syll(syllable),delay))
            # TextToSpeech._play_audio(TextToSpeech.format_syll(syllable), delay)
            delay += 0.355

    def format_syll(syllable):
        """
        ba2ng -> bang2
        """
        result = syllable
        for i in range(len(syllable)):
            if syllable[i].isdigit():
                result = syllable[:i]+syllable[i+1:]+syllable[i]
        return result

    def _play_audio(sound, delay):
        try:
            time.sleep(delay)
            # wf = wave.open("sounds/"+sound+".wav", 'rb') # deprecated path
            wf = wave.open("syllables/"+sound+".wav", 'rb')
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
    while True:
        tts.speak(input('输入中文：'))
