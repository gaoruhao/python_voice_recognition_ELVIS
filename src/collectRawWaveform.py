import time
from nielvis import AnalogInput, Bank, AIChannel, AIRange, AIMode

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

def main():
    duration = 5
    sampleRate = 44100
    sampleSize = sampleRate * duration
    
    waveform = readWaveformFromAI(sampleRate, sampleSize)
    print('waveform size = %d' % len(waveform))
    
    with open('/home/admin/rawaudio.txt', 'w') as rawAudioFile:
        for data in waveform:
            rawAudioFile.write("%f\n" % float(data))
            
main()