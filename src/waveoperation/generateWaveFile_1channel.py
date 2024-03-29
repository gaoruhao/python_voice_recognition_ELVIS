import wave
import struct
import time
from nielvis import AnalogInput, Bank, AIChannel, AIRange, AIMode

def printString(p_text):
    print(p_text.encode("utf-8").decode('unicode_escape'))

def writeWaveFile(p_file, p_param, p_intArray):
    with wave.open(p_file, 'w') as wavefile:
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

def readWaveformFromAI(p_sampleRate, p_sampleSize, p_bank=Bank.A, p_channel=AIChannel.AI0, p_channelRef=None):
    ai_range = AIRange.PLUS_OR_MINUS_1V
    ai_mode = AIMode.SINGLE_ENDED
    isNewChannel = p_channelRef is None;
    
    value_array = []
    if isNewChannel:
        p_channelRef = AnalogInput(
            {
                'bank': p_bank,
                'channel': p_channel,
                'range': ai_range,
                'mode': ai_mode
            }
        );

    # configure the sample rate and start the acquisition
    p_channelRef.start_continuous_mode(p_sampleRate)
    printString('开始10秒录音...')    
    
    # read the value
    timeout = -1
    value_array = p_channelRef.read(p_sampleSize, timeout)

    printString('结束录音')
    
    # stop signal acquisition
    p_channelRef.stop_continuous_mode()
    
    if isNewChannel:
        p_channelRef.close()
    
    return value_array[0]

def generateWaveFile(p_filename, p_sampleRate=44100, p_duration=5, p_bank=Bank.A, p_channel=AIChannel.AI0, p_channelref=None):
    sampleSize = p_sampleRate * p_duration
    
    waveforms = readWaveformFromAI(p_sampleRate, sampleSize, p_bank, p_channel, p_channelref)
    nchannels = len(waveforms)
    
    pcmChannels = []
    for waveform in waveforms:
        pcmResults = encodePCM(waveform, 1.5)
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
    factor = 1
    params = (nchannels, 2, int(p_sampleRate / (nchannels * factor)), sampleSize, 'NONE', 'not compressed')
    # print(params)
    writeWaveFile(p_filename, params, pcmMerged)

if __name__ == "__main__":
    generateWaveFile('./output_1chan.wav')