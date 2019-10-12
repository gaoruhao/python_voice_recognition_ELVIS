import wave
import struct
import time
from nielvis import AnalogInput, Bank, AIChannel, AIRange, AIMode

def writeWaveFile(p_file, p_param, p_intArray):
    with wave.open(p_file, 'wb') as wavefile:
        wavefile.setparams(p_param)
        packFormat = '<' + str(len(p_intArray)) + 'h'
        dataInBytes = struct.pack(packFormat, *p_intArray);
        # print('dataInBytes%d' % len(dataInBytes))
        wavefile.writeframes(dataInBytes)

def encodePCM(p_waveform, p_amplitude, p_bitWidth=16):
    totalRange = p_amplitude * 2
    maxDigital = 2 ** p_bitWidth
    
    pcmResults = []
    for point in p_waveform:
        pcmResult = int((float(point) + p_amplitude) * maxDigital / totalRange)
        pcmResults.append(pcmResult - (2 ** (p_bitWidth - 1)))
    
    return pcmResults

def readWaveformFromAI(p_sampleRate, p_sampleSize, p_bank=Bank.A, p_channel=AIChannel.AI0):
    ai_range = AIRange.PLUS_OR_MINUS_1V
    ai_mode = AIMode.SINGLE_ENDED
    
    value_array = []
    with AnalogInput({'bank': p_bank,
                  'channel': p_channel,
                  'range': ai_range,
                  'mode': ai_mode}) as AI_single_channel:
        # configure the sample rate and start the acquisition
        AI_single_channel.start_continuous_mode(p_sampleRate)
        print('start recording...')
        
        # read the value
        timeout = -1
        value_array = AI_single_channel.read(p_sampleSize, timeout)

        print('stop recording')
        # stop signal acquisition
        AI_single_channel.stop_continuous_mode()
    
    return value_array[0]

def generateWaveFile(p_filename, p_bank=Bank.A, p_channel=AIChannel.AI0):
    duration = 5
    sampleRate = 44100
    sampleSize = sampleRate * duration
    
    waveforms = readWaveformFromAI(sampleRate, sampleSize, p_bank, p_channel)
    nchannels = len(waveforms)
    
    pcmChannels = []
    for waveform in waveforms:
        pcmResults = encodePCM(waveform, 1.0)
        pcmChannels.append(pcmResults)   
    
    sampleSize = len(pcmChannels[0])
    
    pcmMerged = []
    if nchannels > 1:
        for i in range(sampleSize):
            pcmMerged.append(pcmChannels[0][i])
            pcmMerged.append(pcmChannels[1][i])
    else:
        pcmMerged = pcmChannels[0]

    # WORKAROUND: sampleRate / nchannels
    params = (nchannels, 2, sampleRate / nchannels, sampleSize, 'NONE', 'not compressed')
    print(params)
    writeWaveFile(p_filename, params, pcmMerged)

if __name__ == "__main__":
    generateWaveFile('./output_1chan.wav')