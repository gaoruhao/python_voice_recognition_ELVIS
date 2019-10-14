import wave
import struct
import math
import time

from waveoperation.pcmToWav import pcmToWav
from voice.convertTextToAudio import textToPcm

from nielvis import AnalogOutput, Bank, AOChannel

def printString(p_text):
    print(p_text.encode("utf-8").decode('unicode_escape'))

def readWaveFile(p_file):
    with wave.open(p_file, 'rb') as wavefile:
        params = wavefile.getparams()
        frameInBytes = wavefile.readframes(wavefile.getnframes())
        if params.sampwidth != 2:
            print('[ERROR] wavefile sample width is not 2 (16bit)')
        
        int_iter = struct.iter_unpack('<h', frameInBytes)
        
        # init intArray
        pcmDataArray = []
        for i in range(params.nchannels):
            pcmDataArray.append([])
        
        # split multiple channels audio into separate arrays
        i = 0
        for int_tuple in int_iter:
            channelIndex = i % params.nchannels
            if channelIndex == 0:
                pcmDataArray[channelIndex].append(int_tuple[0])
            i += 1

        # print('[DBG] dim: %d, size of each: %d' % (len(pcmDataArray), len(pcmDataArray[0])))
        return pcmDataArray, params

def decodePCM(p_intArray, p_amplitude, p_bitWidth=16):
    totalRange = p_amplitude * 2
    maxDigital = 2 ** p_bitWidth
    
    waveform = []
    for point in p_intArray:
        analogValue = ((point + 2 ** (p_bitWidth - 1)) * totalRange / maxDigital) - p_amplitude
        waveform.append(analogValue)
    
    return waveform
    
def writeWaveformToAO(p_waveform, p_sampleRate, p_channelRef=None):
    bank = Bank.B
    channel = AOChannel.AO0
    isNewChannel = p_channelRef is None;
    
    if isNewChannel:
        p_channelRef = AnalogOutput(
            { 'bank': bank, 'channel': channel }
        );

    # printString('朗读歌名...')
    timeout = -1
    MAX_SINGLE_WRITE = 200000
    totalSize = len(p_waveform)
    
    # limit the waveform length of single write
    numberOfChunks = math.ceil(totalSize / MAX_SINGLE_WRITE)
    for i in range(numberOfChunks):
        startOffset = i * MAX_SINGLE_WRITE
        endOffset = min(totalSize, (i + 1) * MAX_SINGLE_WRITE - 1)
        #print('[DBG] write range: %d:%d' % (startOffset, endOffset))
        
        toWrite = [p_waveform[startOffset:endOffset]]
        if i == 0:
            p_channelRef.start_continuous_mode(toWrite, p_sampleRate, timeout)

        p_channelRef.write(toWrite, p_sampleRate)
        
    time.sleep(5)
    
    # printString('结束播放')
    p_channelRef.stop_continuous_mode()
    
    if isNewChannel:
        p_channelRef.close()

def playWaveFile(p_fileToPlay, p_channelRef=None):
    pcmArray, pcmParams = readWaveFile(p_fileToPlay)
    #print('[DBG] WAVE params: %s' % (pcmParams,))
    
    # always choose pcmArray[0] because we only support 1 channel audio out for now.
    AMP_OUT = 3.3
    BITS_PER_BYTE = 8
    waveformToWrite = decodePCM(pcmArray[0], AMP_OUT, pcmParams.sampwidth * BITS_PER_BYTE)
    
    #print('[DBG] waveform length %d' % len(waveformToWrite))
    writeWaveformToAO(waveformToWrite, pcmParams.framerate, p_channelRef)

def playText(p_textToPlay, p_fileToSave):
    textToPcm(p_textToPlay, p_fileToSave)
    pcmToWav(p_fileToSave)

    printString('歌名查找完毕')
    playWaveFile(p_fileToSave + '.wav')

if __name__ == "__main__":
    playWaveFile('/home/admin/test123.wav')