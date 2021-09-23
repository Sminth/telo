
import sys
import os
import threading
import logging
import subprocess
import time
import socketio
from songController import SongController 
from dialog import Dialog
from audioManager import AudioRecorder
from faceManager import FaceRecognition
logging.basicConfig(filename='voice-assistant.log', level=logging.INFO)
import signal
import requests

f = open("../../ipVenv","r")
# print(f.readline())
#threading.Thread(target= lambda: requests.get("http://10.3.141.56/bad",timeout=1)).start()
# requests.get("http://10.106.5.135/bad",timeout=1)

#Connect to Socket
sio = socketio.Client()
 
#listen en pitch event
#sio.connect('http://192.168.252.216:9400', namespaces=['/service','/speech']) 
@sio.on('pitch', namespace='/speech')
def on_pitch(data):
    tt=data['content']
    dialog.SpeakText(tt)
    time.sleep(6)
    sio.emit("home", "AKW@BA",namespace='/speech')

def main():
    print("socket")    
    #Connexion au serveur
    sio.connect('http://'+f.read()+':9400', namespaces=['/speech'])
    print('my sid is', sio.sid)
    sio.emit("requests-count", "1",namespace='/speech')
    #sio.on("pitch",message,namespace=['/speech'])

#    sio.wait()
def on_exit(sig, func=None):
        print("exit handler")
        time.sleep(10)  # so you can see the message before program exits
        

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, on_exit)
    logging.info('debut')
    #main()
    dialog = Dialog()
    dialog.SpeakText("je parle hum, attention")
    print("a parler")
    audio_recorder = AudioRecorder(dialog)
    face = FaceRecognition(audio_recorder)
    song = SongController()
    #main()
