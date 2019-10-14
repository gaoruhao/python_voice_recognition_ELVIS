# -*- coding:utf-8 -*-
from waveoperation.generateWaveFile_1channel import generateWaveFile
from waveoperation.playWaveform import playWaveform
from waveoperation.pcmToWav import pcmToWav

import json

from voice.findSongName import findSongName
from voice.convertTextToAudio import textToPcm

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
        inputText = input("Press Enter to start or 'q' to quit")
        if inputText == 'q' or inputText == 'Q':
            break
        
        generateWaveFile(wavefile, sampleRate, duration, ai_bank, ai_channel, AIchannelRef)
        
        songName = findSongName(wavefile)
        
        if songName == "":
            # songName = '对不起，您所唱的歌曲无法识别。'
            songName = 'Sorry, cannot find you song name.'
            return
        
        # print('歌名处理中...')
        printString('歌名处理中...')
        textToPcm(songName, pcmfile)
        pcmToWav(pcmfile)
        
        playWaveform(pcmfile + '.wav')
    
    AIchannelRef.close()
    AOchannelRef.close()
    
if __name__ == "__main__":
    application()