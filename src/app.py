from waveoperation.generateWaveFile_1channel import generateWaveFile
from waveoperation.playWaveform import playWaveform
from voice.findSongName import findSongName
from nielvis import Bank, AIChannel

# Preset Parameters
wavefile = '/home/admin/app.wav'
sampleRate = 16000
duration = 30 
bank = Bank.B
channel = AIChannel.AI0

def application():
    generateWaveFile(wavefile, sampleRate, duration, bank, channel)
    songName = findSongName(wavefile)
    # text to audio
    playWaveform(wavefile)
    
if __name__ == "__main__":
    application()