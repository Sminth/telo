import pyttsx3
import time
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
    print(voice)
    if voice.languages[0] == b'\x05fr-fr':
#    if b'\x05fr' in voice.languages[0] :
        engine.setProperty('voice', voice.id)
#        engine.setProperty('age', 28)
        engine.setProperty('rate', 110)
        engine.say('Bonjour, je suis telo votre assistant personel, je reste à votre disposition pour toutes informations holistiques ou spécifiques. sur ODC')
        #break
#        time.sleep(5)


engine.runAndWait()
