from waveoperation.generateWaveFile_1channel import generateWaveFile
from voice.findSongName import findSongName
from nielvis import Bank, AIChannel

wavefile = '/home/admin/app.wav'

def application():
    generateWaveFile(wavefile, Bank.B, AIChannel.AI0)
    findSongName(wavefile)
    
if __name__ == "__main__":
    application()