import time
from nielvis import AnalogInput, Bank, AIChannel, AIRange, AIMode

def readWaveformFromAI(p_sampleRate, p_sampleSize):
    ai_bank = Bank.B
    ai_channel = AIChannel.AI0
    ai_channel_2 = AIChannel.AI1
    ai_range = AIRange.PLUS_OR_MINUS_1V
    ai_mode = AIMode.SINGLE_ENDED
    
    value_array = []
    with AnalogInput({'bank': ai_bank,
                  'channel': ai_channel,
                  'range': ai_range,
                  'mode': ai_mode},
                  {'bank': ai_bank,
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
    
    return value_array[0]

def main():
    duration = 5
    sampleRate = 44100
    sampleSize = sampleRate * duration
    
    waveform = readWaveformFromAI(sampleRate, sampleSize)
    
    i = 0
    for channel in waveform:
        print('waveform size = %d' % len(channel))
        
        with open('/home/admin/rawaudio_%d.txt' % i, 'w') as rawAudioFile:
            for data in channel:
                rawAudioFile.write("%f\n" % float(data))
        
        i += 1
            
main()