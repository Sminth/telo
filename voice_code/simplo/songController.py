import pygame
from pygame import mixer
import threading
import time,os,random
import pyglet
import signal
class SongController(object):
    def __init__(self):
        self.files = ['./musiques/spot.wav','./musiques/ukulele.wav','./musiques/Animation.wav','./musiques/family.wav']
        #pygame.init()
        mixer.init()
        self.stepper = 0
        self.control="paus"
        with open('song',"w") as f: f.write("paus")
        self.player = pyglet.media.Player()
        threading.Thread(target=self.isPaused).start()
        # threading.Thread(target=self.run).start()
        self.a_deja_jouer =0

    def isPaused(self):
    #    print("je commence")
       while 1:
           time.sleep(1)
           with open("song", 'r') as f: 
               self.control=f.read()
           if(self.control== "pause"):
               #self.player.pause()
               mixer.music.pause()
               try: os.system("amixer --quiet set Master 80")
               except: pass

           elif self.control == "play" :
               
               #if self.player.source : self.player.play()
               if mixer.music.get_busy() == 1: pass

               else :
                   try: os.system("amixer --quiet set Master 50")
                   except: pass
                   mixer.music.load(random.choice(self.files))
                   mixer.music.play()
                   self.a_deja_jouer =1
                   """src = pyglet.media.load(random.choice(self.files))
                   self.player.queue(src)
                   self.player.play()"""
               
           #print(self.control)     

    """ def run(self):
        while 1:
            if(self.control=="play"):
                self.start_song()
            time.sleep(1)

    def start_song(self):
        os.getcwd()
        while self.stepper < len(self.files):
            print("Playing:",self.files[self.stepper])
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
                    print (str(timer))"""
                    #elif int(timer) > 10:
                    #print ("True")
                    #pygame.mixer.music.stop()
                    #break
                #else: continue"""

#SongController()
