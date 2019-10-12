from waveoperation.generateWaveFile_1channel import generateWaveFile
from waveoperation.playWaveform import playWaveform
from waveoperation.pcmToWav import pcmToWav

from voice.findSongName import findSongName
from voice.convertTextToAudio import textToPcm

from nielvis import Bank, AIChannel

# Preset Parameters
wavefile = './app.wav'
sampleRate = 16000
duration = 30 
bank = Bank.B
channel = AIChannel.AI0
pcmfile = './temp.pcm'

def application():
    #generateWaveFile(wavefile, sampleRate, duration, bank, channel)
    
    songName = findSongName(wavefile)
    
    print('text to wave starting ...')
    textToPcm(songName, pcmfile)
    pcmToWav(pcmfile)
    print('text to wave stopped')
    
    playWaveform(pcmfile + '.wav')
    
if __name__ == "__main__":
    application()