from tts import *

voiceId = voiceIds['Female']['Adult'][1]
synthesize_speech(f'Hello, my name is {voiceId}. I am a robot.',
                  voiceId, 'speech.mp3')
