# -*- coding:utf-8 -*-
import json
import time
import glob, os

from waveoperation.generateWaveFile_1channel import generateWaveFile
from waveoperation.playWaveform import playText
# from waveoperation.pcmToWav import pcmToWav

from voice.findSongName import findSongName
# from voice.convertTextToAudio import textToPcm

from nielvis import Bank, AnalogInput, AIChannel, AIRange, AIMode, AnalogOutput, AOChannel

# Preset Parameters
wavefile = './song.wav'
sampleRate = 16000
duration = 10 
ai_bank = Bank.B
ai_channel = AIChannel.AI1
ai_range = AIRange.PLUS_OR_MINUS_1V
ai_mode = AIMode.SINGLE_ENDED

pcmfile = './songname.pcm'

ao_bank = Bank.B
ao_channel = AOChannel.AO0

def printString(p_text):
    print(p_text.encode("utf-8").decode('unicode_escape'))

def inputString(p_text):
    return input(p_text.encode("utf-8").decode('unicode_escape'))

def removeWavFiles():
    for filename in glob.glob("*.wav"):
        os.remove(filename)
    
    for filename in glob.glob("*.pcm"):
        os.remove(filename)

def application():
    AIchannelRef = AnalogInput(
        {
            'bank': ai_bank,
            'channel': ai_channel,
            'range': ai_range,
            'mode': ai_mode
        }
    );
    AOchannelRef = AnalogOutput(
        { 'bank': ao_bank, 'channel': ao_channel }
    );
    
    while(True):
        removeWavFiles()
        inputText = inputString("按回车键开始 或者 按 Q 退出")
        if inputText == 'q' or inputText == 'Q':
            break
        
        printString('准备演唱...')
        for i in range(3):
            print(3 - i)
            time.sleep(1)
        
        generateWaveFile(wavefile, sampleRate, duration, ai_bank, ai_channel, AIchannelRef)
        
        printString('歌名查找中，请耐心等待...')
        songName = findSongName(wavefile)
        
        if songName == "":
            songName = '对不起，您所唱的歌曲无法识别。'
        else:
            songName = "歌名是，" + songName
        
        playText(songName, pcmfile)
    
    AIchannelRef.close()
    AOchannelRef.close()
    
if __name__ == "__main__":
    application()