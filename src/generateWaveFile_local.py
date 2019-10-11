import wave
import struct
import time
import numpy as np
# from nielvis import AnalogInput, Bank, AIChannel, AIRange, AIMode

def readWaveFile(p_file):
    with wave.open(p_file, 'rb') as wavefile:
        params = wavefile.getparams()
        frameInBytes = wavefile.readframes(wavefile.getnframes())
        print(len(list(frameInBytes)))
        int_iter = struct.iter_unpack('<h', frameInBytes)
        intArray = []
        for int_tuple in int_iter:
            intArray.append(int_tuple[0])
            
        print(len(intArray))
        return intArray, params

def writeWaveFile(p_file, p_param, p_intArray):
    with wave.open(p_file, 'wb') as wavefile:
        wavefile.setparams(p_param)
        packFormat = '<' + str(len(p_intArray)) + 'h'
        dataInBytes = struct.pack(packFormat, *p_intArray);
        print('dataInBytes%d' % len(dataInBytes))
        wavefile.writeframes(dataInBytes)

# return int
def encodePCM(p_waveform, p_amplitude, p_bitWidth=16):
    totalRange = p_amplitude * 2
    maxDigital = 2 ** p_bitWidth
    
    pcmResults = []
    for point in p_waveform:
        pcmResult = int((float(point) + p_amplitude) * maxDigital / totalRange)
        pcmResults.append(pcmResult - (2 ** (p_bitWidth - 1)))
        # pcmResults.append(pcmResult)
    
    return pcmResults

def main():
    intArray, params = readWaveFile('good.wav')
    print(params)
    print(params.nframes)
    print(len(intArray))
    
    pcmChannels = []
    # files = ['rawaudio_0.txt']
    files = ['rawaudio_2.txt', 'rawaudio_3.txt']
    nchannels = len(files)
    for file in files:
        waveform = []
        with open(file, 'r') as rawAudioFile:
            lines = rawAudioFile.readlines()
            for line in lines:
                point = float(line)
                waveform.append(point)
                
        pcmResults = encodePCM(waveform, 1.0)
        print('pcmResults size = %d' % len(pcmResults))
        pcmChannels.append(pcmResults)   
        # for i in range(0, 10):
        #     print(pcmResults[i])
    
    sampleSize = len(pcmChannels[0])
    
    pcmMerged = []
    if nchannels > 1:
        for i in range(sampleSize):
            pcmMerged.append(pcmChannels[0][i])
            pcmMerged.append(pcmChannels[1][i])
    else:
        pcmMerged = pcmChannels[0]
        
    params = (nchannels, 2, 44100 / 2, sampleSize, 'NONE', 'not compressed')
    print(params)
    writeWaveFile('./output_test123.wav', params, pcmMerged)

main()