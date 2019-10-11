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
        int_iter = struct.iter_unpack('<i', frameInBytes)
        intArray = []
        for int_tuple in int_iter:
            intArray.append(int_tuple[0])
            
        print(len(intArray))
        return intArray, params

def writeWaveFile(p_file, p_param, p_intArray):
    with wave.open(p_file, 'wb') as wavefile:
        wavefile.setparams(p_param)
        packFormat = '<' + str(len(p_intArray)) + 'i'
        dataInBytes = struct.pack(packFormat, *p_intArray);
        wavefile.writeframes(dataInBytes)

def readWaveformFromAI(p_sampleRate, p_sampleSize):
    ai_bank = Bank.A
    ai_channel = AIChannel.AI0
    ai_range = AIRange.PLUS_OR_MINUS_1V
    ai_mode = AIMode.SINGLE_ENDED
    
    value_array = []
    with AnalogInput({'bank': ai_bank,
                  'channel': ai_channel,
                  'range': ai_range,
                  'mode': ai_mode}) as AI_single_channel:
        # specify the period of time, in milliseconds, to wait for the acquisition
        # to complete
        timeout = -1
        
        # configure the sample rate and start the acquisition
        AI_single_channel.start_continuous_mode(p_sampleRate)
        
        print('start recording...')
        
        # read the value
        value_array = AI_single_channel.read(p_sampleSize, timeout)

        print('stop recording')
        # stop signal acquisition
        AI_single_channel.stop_continuous_mode()
    
    return value_array[0][0]

# return int
def encodePCM(p_waveform, p_amplitude, p_bitWidth=16):
    totalRange = p_amplitude * 2
    maxDigital = 2 ** p_bitWidth
    
    pcmResults = []
    for point in p_waveform:
        pcmResult = int((float(point) + p_amplitude) * maxDigital / totalRange)
        pcmResults.append(pcmResult)
    
    return pcmResults

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def main():
    # intArray, params = readWaveFile('/home/admin/test123.wav')
    # print(params.nchannels)
    
    # duration = 5
    # sampleRate = 44100
    # sampleSize = sampleRate * duration
    
    # waveform = readWaveformFromAI(sampleRate, sampleSize)
    # print('waveform size = %d' % len(waveform))
    # # for i in range(0, 10):
    # #     print(waveform[i])
    
    # with open('/home/admin/rawaudio.txt', 'w') as rawAudioFile:
    #     for data in waveform:
    #         rawAudioFile.write("%f\n" % float(data))
    
    waveform = []
    with open('./rawaudio.txt', 'r') as rawAudioFile:
        lines = rawAudioFile.readlines()
        for line in lines:
            point = float(line)
            waveform.append(point)
            
    waveform_ns = np.asarray(waveform)
    filtered_waveform_ns = butter_bandpass_filter(waveform_ns, 300, 3000, 44100, order=6)
    print(len(filtered_waveform_ns.tolist()))
    
    pcmResults = encodePCM(filtered_waveform_ns, 1.0)
    print('pcmResults size = %d' % len(pcmResults))
    # for i in range(0, 10):
    #     print(pcmResults[i])
    
    params = (1, 2, 44100, len(pcmResults), 'NONE', 'not compressed')
    writeWaveFile('./output_test123.wav', params, pcmResults)

main()