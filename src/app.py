from waveoperation.generateWaveFile_1channel import generateWaveFile
from waveoperation.playWaveform import playWaveform
from waveoperation.pcmToWav import pcmToWav

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

def application():
    generateWaveFile(wavefile, sampleRate, duration, bank, channel)
    
    songName = findSongName(wavefile)
    
    if songName == "":
        print('对不起，您所唱的歌曲无法识别。')
        return
    
    print('歌名处理中...')
    textToPcm(songName, pcmfile)
    pcmToWav(pcmfile)
    
    playWaveform(pcmfile + '.wav')
    
if __name__ == "__main__":
    application()