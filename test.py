import os

import speech_recognition as sr

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

print(audio)

# recognize speech using whisper
try:
    print("Whisper thinks you said " + r.recognize_whisper(audio, language="english"))
except sr.UnknownValueError:
    print("Whisper could not understand audio")
except sr.RequestError as e:
    print(f"Could not request results from Whisper; {e}")
print '\n'.join([y['name'] 
 for y in [pa.get_device_info_by_index(x)
 for x in range(pa.get_device_count())]])