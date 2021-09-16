import pygame
import threading
import time

class SongController(object):
    def __init__(self):
        self.files = ['./musiques/beethoven.mp3','./musiques/mozart.mp3']
        pygame.init()
        pygame.mixer.init()
        self.stepper = 0
        self.control="pause"
        with open('song',"w") as f: f.write("pause")
        threading.Thread(target=self.isPaused).start()
        threading.Thread(target=self.run).start()


    def isPaused(self):
       while 1:
           time.sleep(1)
           with open("song", 'r') as f: 
               self.control=f.read()

    def run(self):
        while 1:
            if(self.control=="play"):
                self.start_song()
            time.sleep(1)
    def start_song(self):
        while self.stepper < len(self.files):
            pygame.mixer.music.load(self.files[self.stepper])
            print("Playing:",self.files[self.stepper])
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
                    """elif int(timer) > 10:
                    print ("True")
                    pygame.mixer.music.stop()
                    break"""
                else:
                    continue


#SongController()