import pygame
import threading
import time
from audioplayer import AudioPlayer
import multiprocessing
from playsound import playsound
class SongController(object):
    def __init__(self):
        self.files = ['musiques/beethoven.mp3','musiques/mozart.mp3']
        pygame.init()
        pygame.mixer.init()
        self.stepper = 0
        self.control="pause"
        with open('song',"w") as f: f.write("paus")
        threading.Thread(target=self.isPaused).start()
        threading.Thread(target=self.run).start()
        threading.Thread(target=self.verif).start()


    def isPaused(self):
       while 1:
           time.sleep(1)
           with open("song", 'r') as f: 
               self.control=f.read()
    def verif(self):
        # if(self.control=="play") :playsound()
        if(self.control=="pause") : self.p.terminate()
    def run(self):
        
        if(self.control=="play"):
                self.start_song()
            # time.sleep(1)
    def start_song(self):
        self.p = multiprocessing.Process(target = playsound, args = (self.files[self.stepper],))
        self.p.start()
        # playsound(self.files[self.stepper])
        print("continue")
        # player.play()
        """while self.stepper < len(self.files):

            print("Playing:",self.files[self.stepper])
            player = AudioPlayer(self.files[self.stepper])
            player.play()"""
            # if self.control == "pause": player.pause()
            # elif self.control == "play" : player.unpause()
            # else: continue
        """
            pygame.mixer.music.load(self.files[self.stepper])
            self.stepper += 1
            pygame.mixer.music.play()
#play and pause
            while pygame.mixer.music.get_busy():
                timer = pygame.mixer.music.get_pos()
                time.sleep(1)
                #self.control = input('>')
                pygame.time.Clock().tick(10)
                if self.control == "pause":
                    pygame.mixer.music.pause()
                elif self.control == "play" :
                    pygame.mixer.music.unpause()
                elif self.control == "time":
                    timer = pygame.mixer.music.get_pos()
                    timer = timer/1000
                    print (str(timer))
                    #elif int(timer) > 10:
                    #print ("True")
                    #pygame.mixer.music.stop()
                    #break
                else:
                    continue

"""
#SongController()
