from math import e
import socketio
import requests
import os,time
import sys
import io
import json
import numpy as np
import logging
import speech_recognition as sr
import pyttsx3 
import queue,threading
from google_speech import Speech
import signal


"""
#Connect to Socket
ss = socketio.Client()
print("socket")    
#Connexion au serveur
ss.connect('http://192.168.252.226:9400', namespaces=['/service'])
print('my sid is', sio.sid)
#sio.wait()    
"""
f = open("../../ipVenv","r")
sio = socketio.Client()
try:
	sio.connect('http://'+f.read()+':9400', namespaces=['/speech'])
    
except Exception as e:
    print(e)
    print("connexion non etablie")
    pass

class Dialog():
    def __init__(self):
        super(Dialog, self).__init__()
        self.userText = ""
        #self.song = song
        self.sio = sio
        self.machineText = ""
        self.en_lecture = False
        self.attente = queue.Queue(3)
        self.attente_isplein=self.attente.full()
        
        threading.Thread(target=self.speak).start()
        
#        self.sio.emit("home", "1",namespace='/speech')
	#self.sio.emit("home", "1",namespace='/service')
        #self.sio = socketio.Client()
        #self.socket()
#listen en pitch event
#sio.connect('http://192.168.252.216:9400', namespaces=['/service','/speech'])
    

    
    def socket(self):
         print("socket")    
         #Connexion au serveur
         #sio.connect('http://192.168.252.216:9400', namespaces=['/speech'])
         print('my sid is', sio.sid)
         # self.sio.emit("requests-count", "1",namespace='/speech')


    @sio.on('pitch', namespace='/speech')
    def on_pitch(data):
         tt=data['content']
         Dialog().SpeakText(tt)
         time.sleep(6)
         sio.emit("home", "AKW@BA",namespace='/speech')
    
    @sio.on('speak-section', namespace='/speech')
    def on_speak(data):
         text=data['content']
         Dialog().SpeakText(text)
         time.sleep(8)
         sio.emit("home", "AKW@BA",namespace='/speech') 

    @sio.on('song', namespace='/speech')
    def on_song(data):
         value=data['content']
         if(value=='on'):
             with open("song",'w') as f : f.write("play")
         elif(value=='off'):
              with open("song",'w') as f : f.write("pause")


    def add_file_attente(self,item):
        self.attente_isplein=self.attente.full()
        if self.attente_isplein : return 
        self.attente.put(item)

    def speak(self):
        while True:
            n=self.attente.qsize()
            if n==0 : pass
            else : 
                for i in range(n):
                    self.SpeakText(self.attente.get())

    def process_init(self,text):
        # AudioRecorder().pause=True
        
        print("process fpour : "+str(text))
        self.set_user_message(text)
        self.process_user_message()
        self.process_machine_message()
        print("fin process pour : "+str(text))
        
        return
        # AudioRec  order().pause=False
    def get_french_voice(self,engine):
        voices = engine.getProperty('voices')
        for voice in voices:
            #print(voice)
            if voice.languages[0] == b'\x05fr-fr':
                return voice
                #engine.say('Bonjour, je suis telo votre assistant personel')
        return ""

        
    def SpeakText(self,command):
        self.en_lecture = True
        with open("is_lecture", "w") as f : f.write("True")
       	"""engine = pyttsx3.init()
        if engine._inLoop:
            engine.endLoop()
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if voice.languages[0] == b'\x05fr-fr':
                engine.setProperty('voice', voice.id)
        engine.setProperty("rate",120)
        engine.say(command) 
        engine.runAndWait()"""
        speech = Speech(command, "fr")
        speech.play()
        self.en_lecture = False 
        with open("is_lecture", "w") as f : f.write("False")
    def process_user_message(self):
        ''' envoie du message du user a la machine'''
        
        self.send_user_msg_to_chatbot(self.userText)
        logging.debug("message user : {self.textResponse}")

    def set_user_message(self, string):
        self.userText = string

    def send_face(self):
        try:
            sio.emit("count-face", "1", namespace='/speech')
            print("envoyé")
        except: pass
    def send_user_msg_to_chatbot(self, message):
        # sio.emit("requests-user", message, namespace='/speech')
        
        tps1 = time.time()
        temp=0.02
        try :
            headers = {"Content-type": "application/json"}
            data = "{\"sender\": \"user1\", \"message\": \" " + message + "\"}"
            print(f.read())
            self.response = requests.post("http://"+f.read()+":5005/webhooks/rest/webhook",
                         headers=headers, data=data.encode('utf-8'),timeout=4)
            
            print("temps de reponse rasa : "+ str(temp) +" seconde")
            # sio.emit("rasa-responses",[temp,self.response],namespace='/speech')

                        # sio.emit("requests-time",time,namespace='/speech')

        except :
            logging.error("ERROR :connection au serveur rasa impossible ")
            # sio.emit("rasa-responses",['0.5','connection au serveur rasa impossible'],namespace='/speech')
            self.response = "connection au serveur rasa impossible"
            if self.attente_isplein : return 
            else : Dialog().SpeakText("je ne peux vous repondre actuellement")
            #else : Dialog().SpeakText("je ne suis pas en mesure de vous repondre pour le moment")
            # else : self.add_file_attente("je ne suis pas en mesure de vous repondre pour le moment")
            # self.SpeakText("je ne suis pas en mesure de vous repondre pour le moment")
        temp=str(time.time()-tps1)
        try:
            sio.emit("requests-count", "1", namespace='/speech')
            sio.emit("requests-user", [message,self.response,temp], namespace='/speech')
        except :
            pass
    def process_machine_message(self):
        '''lecture de la reponse de la machine'''
        try:
            if json.loads(self.response.text):
                self.textResponse = json.loads(self.response.text)[0]["text"]
                print(self.textResponse)
                if self.attente_isplein : return 
                self.add_file_attente(self.textResponse)
                # self.SpeakText(self.textResponse)
                logging.debug("message Machine : {self.textResponse}")
                return
            else:
                #self.SpeakText("je vous ai pas compris")
                logging.error("Une erreur s'est produite dans le serveur Rasa et il n'y a aucun message à afficher.")
        except :
            # self.SpeakText("je vous ai pas compris")
            logging.error("Une erreur s'est produite dans le serveur Rasa et il n'y a aucun message à afficher.")

if __name__ == "__main__":
    arg =sys.argv
    if(len(arg)==3 and arg[1]=="--input"):
        print("argument : "+arg[2])
        entre = arg[2]
        d=Dialog()
        d.process_init(entre)
        # for i, arg in enumerate(arg):
        #     print("Argument"+str(i)+":"+str(arg))
