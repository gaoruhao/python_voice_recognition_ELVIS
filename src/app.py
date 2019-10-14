from waveoperation.generateWaveFile_1channel import generateWaveFile
from waveoperation.playWaveform import playWaveform
from waveoperation.pcmToWav import pcmToWav

import json

from voice.findSongName import findSongName
from voice.convertTextToAudio import textToPcm

from nielvis import Bank, AIChannel

# Preset Parameters
wavefile = './app.wav'
sampleRate = 16000
duration = 15 
bank = Bank.B
channel = AIChannel.AI0
pcmfile = './temp.pcm'

def printString(p_text):
    print(p_text.encode("utf-8").decode('unicode_escape'))

def application():
    generateWaveFile(wavefile, sampleRate, duration, bank, channel)
    
    songName = findSongName(wavefile)
    
    if songName == "":
        songName = '对不起，您所唱的歌曲无法识别。'
    
    printString('歌名处理中...')
    textToPcm(songName, pcmfile)
    pcmToWav(pcmfile)
    
    playWaveform(pcmfile + '.wav')
    
if __name__ == "__main__":
    application()