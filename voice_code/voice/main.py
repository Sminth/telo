import sys
import os
import threading
import logging
import subprocess
import time
import socketio
from dialog import Dialog
from audioManager import AudioRecorder
from faceManager import FaceRecognition
logging.basicConfig(filename='voice-assistant.log', level=logging.INFO)

#Connect to Socket
sio = socketio.Client()

#listen en pitch event
@sio.on('pitch', namespace='/speech')
def on_pitch(data):
    tt=data['content']

    dialog.SpeakText(tt)
    time.sleep(6)
    sio.emit("home", "AKW@BA",namespace='/speech')

def main():
    
    #Connexion au serveur
    sio.connect('http://192.168.252.64:9400', namespaces=['/speech'])
    print('my sid is', sio.sid)
    #sio.on("pitch",message,namespace=['/speech'])
    sio.wait()

if __name__ == "__main__":
    logging.info('debut')
    
    dialog = Dialog()
    audio_recorder = AudioRecorder(dialog)
    # face = FaceRecognition(audio_recorder)
    main()
  
    # subprocess.Popen("python3 faceManager.py", shell=True)
    print("fy")
    logging.info('fin')
    