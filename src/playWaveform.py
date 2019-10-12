import wave
import struct
from nielvis import AnalogOutput, Bank, AOChannel

def readWaveFile(p_file):
    with wave.open(p_file, 'rb') as wavefile:
        params = wavefile.getparams()
        frameInBytes = wavefile.readframes(wavefile.getnframes())
        print(len(list(frameInBytes)))
        if params.sampwidth != 2:
            print('ERROR wavefile sample width is not 2 (16bit)')
        
        int_iter = struct.iter_unpack('<h', frameInBytes)
        intArray = []
        for int_tuple in int_iter:
            intArray.append(int_tuple[0])
            
        print(len(intArray))
        return intArray, params

def decodePCM(p_intArray, p_amplitude, p_bitWidth=16):
    totalRange = p_amplitude * 2
    maxDigital = 2 ** p_bitWidth
    
    waveform = []
    for point in p_intArray:
        analogValue = ((point + 2 ** (p_bitWidth - 1)) * totalRange / maxDigital) - p_amplitude
        waveform.append(analogValue)
    
    return waveform
    
def writeWaveformToAO(p_waveform, p_sampleRate):
    bank = Bank.B
    channel = AOChannel.AO0
    
    with AnalogOutput({'bank': bank,
                   'channel': channel}) as AO_single_channel:
        # configure the sample rate and timeout, then starts the signal generation
        timeout = -1
        print('start to play ...')
        AO_single_channel.start_continuous_mode([p_waveform[0:200000]], p_sampleRate, timeout)

        AO_single_channel.write([p_waveform[0:200000]], p_sampleRate)
        AO_single_channel.write([p_waveform[200001:]], p_sampleRate)
        print('stop play')

        # stop signal generation
        AO_single_channel.stop_continuous_mode()

def playWaveform():
    pcmArray, pcmParams = readWaveFile('/home/admin/output_1chan.wav')
    print(pcmParams)
    
    waveformToWrite = decodePCM(pcmArray, 3.3, pcmParams.sampwidth * 8)
    
    print(len(waveformToWrite))
    writeWaveformToAO(waveformToWrite, pcmParams.framerate)

playWaveform()