import sys
import os,time
import random
import numpy as np
import queue
import threading
import logging
import speech_recognition as sr
import pyttsx3
import subprocess

class AudioRecorder():
    def __init__(self, dialog):
        super(AudioRecorder, self).__init__()
        self.value = "inconnu"
        self.dialog = dialog
        self.th=threading.Thread(target=lambda : self.recognize_speech_from_mic()).start()
    

    def recognize_speech_from_mic(self):
        """Transcrit la parole à partir de l'enregistrement du `microphone`.

        Retourne un dictionnaire avec trois clés :
        "success" : un booléen indiquant si la requête API a été ou non
                réussie
        "error" :   `None` si aucune erreur ne s'est produite, sinon une chaîne de caractères contenant
                un message d'erreur si l'API n'a pu être atteinte ou si la
                la parole n'était pas reconnaissable
        "transcription" : `None` si la parole n'a pas pu être transcrite,
                sinon, une chaîne contenant le texte transcrit
        """

        recognizer=sr.Recognizer()
        microphone=sr.Microphone()
        # vérifier que les arguments du reconnaissant et du microphone sont de type approprié
        if not isinstance(recognizer, sr.Recognizer):
            logging.info('ERROR : recognizer doit être une instance de `Recognizer')
            #raise TypeError("`recognizer doit être une instance de `Recognizer`.")
            self.th.join()
        if not isinstance(microphone, sr.Microphone):
            
            logging.info('ERROR : microphone doit être une instance de Microphone')
            self.th.join()
            #raise TypeError("`microphone` doit être une instance de `Microphone` ")

        # régler la sensibilité du recognizer au bruit ambiant et enregistrer l'audio
        # du microphone
        while(True):
        
            print("Je vous écoute...")
            with microphone as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source)

            # essayer de reconnaître la parole dans l'enregistrement
            # si une exception RequestError ou UnknownValueError est détectée,
            # mettez à jour l'objet réponse en conséquence
            try:
                print("transcription en cours...")
                logging.info("transcription en cour")
                reponse = recognizer.recognize_google(
                    audio, language='fr-FR').lower()
                print(reponse) 
                self.value=reponse
                if("sortie" in reponse.lower() or "stop" in reponse.lower() ) :
                    break
                logging.info("transcription:"+reponse)
                #subprocess.Popen("python3 dialog.py --input \""+reponse+"\"", shell=True)
                print("en attente de rasa")
                # self.dialog.set_user_message(reponse)
                # self.dialog.process_user_message()
                # self.dialog.process_machine_message()
                os.system("python3 dialog.py --input \""+reponse+"\"")
                print("enf")
              
            except sr.RequestError:
                reponse = "que dites vous ?"
                logging.info("API non disponible")
                # self.dialog.SpeakText(reponse)
            except sr.UnknownValueError:
                reponse = "desolé je n'est pas bien compris"
                logging.info("Impossible de reconnaître la parole")
                #self.dialog.SpeakText(reponse)
            #time.sleep(2)
        
            
    def getValue(self):
        return self.value