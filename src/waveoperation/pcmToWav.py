import wave

def pcmToWav(p_file):
    with open(p_file, 'rb') as pcmfile:
        pcmdata = pcmfile.read() 

    with wave.open(p_file + '.wav', 'wb') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'not compressed'))
        wavfile.writeframes(pcmdata)

if __name__ == "__main__":
    pcmToWav('./demo.pcm')