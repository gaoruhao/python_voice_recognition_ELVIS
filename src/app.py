from waveoperation.generateWaveFile_1channel import generateWaveFile
from voice.findSongName import findSongName

wavefile = '/home/admin/app.wav'

def application():
    generateWaveFile(wavefile)
    findSongName(wavefile)
    
if __name__ == "__main__":
    application()