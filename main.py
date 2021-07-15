# IMPORT BEGINS

import os
import json
import random
from tkinter import filedialog
from tkinter import *

from kivy.uix.behaviors import ButtonBehavior
from pygame import *
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.properties import StringProperty
from kivy.clock import Clock

# IMPORT ENDS

# INIT BEGINS

os.chdir("C:\PlayerStorage")
queue = []
currIndex = 0
playState = StringProperty('stopped')

def initProperties():
    global playState
    playState = 'stopped'
# INIT ENDS

# UTILITY FUNCTIONS BEGINS

def startup():
    if checkFirstBoot() == True:
        createDataFile()
        initJSONData()
        askDirectory()
        loadSongList()

    loadQueue()
    print(queue)

def checkFirstBoot():
    if os.path.isfile("dataFile.json") == True:
        return False
    else:
        return True

def createDataFile():
    if os.path.isfile("/dataFile.json") == False:
        with open('dataFile.json', 'w') as openFile:
            openFile.close()

def initJSONData():
    data = {}
    data['globalVaraibles'] = []
    data['globalVaraibles'].append({"songDirectory": ""})
    with open('dataFile.json', 'w') as openFile:
        json.dump(data, openFile)

def askDirectory():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory()
    with open('dataFile.json', 'r+') as openFile:
        data = json.load(openFile)
        data['globalVaraibles'][0]['songDirectory'] = folder_selected
        openFile.seek(0)
        json.dump(data, openFile)
        openFile.truncate()
        openFile.close()

def loadSongList():
    with open('dataFile.json', 'r+') as openFile:
        data = json.load(openFile)
        data['songList'] = []
        path = data['globalVaraibles'][0]['songDirectory']
        for fileName in os.listdir(path):
            if fileName.endswith(".mp3"):
                obj = {
                    'title': fileName,
                    'path': path + "/" + fileName
                }
                data['songList'].append(obj)
        openFile.seek(0)
        json.dump(data, openFile)
        openFile.truncate()
        openFile.close()

def loadQueue():
    global queue
    with open('dataFile.json', 'r+') as openFile:
        data = json.load(openFile)
        queue = data['songList']

def shuffleQueue():
    random.shuffle(queue)

# UTILITY FUNCTIONS ENDS

# MAIN CLASS BEGIN
class ImageButton(ButtonBehavior, Image):

    def on_press(self):
        global playState
        if self.name == 'titleMinimize':
            self.source = 'D:/resources/minimize_pressed.png'
        elif self.name == 'titleCross':
            self.source = 'D:/resources/cross_pressed.png'
        elif self.name == 'playPause':
            if playState == 'stopped':
                self.source = 'D:/resources/play_pressed.png'
            elif playState == 'playing':
                self.source = 'D:/resources/pause_pressed.png'
            elif playState == 'paused':
                self.source = 'D:/resources/play_pressed.png'
        elif self.name == 'previous':
            self.source = 'D:/resources/previous_pressed.png'
        elif self.name == 'next':
            self.source = 'D:/resources/next_pressed.png'


    def on_release(self):
        global playState
        if self.name == 'titleMinimize':
            self.source = 'D:/resources/minimize.png'
            App.get_running_app().root_window.minimize()
        elif self.name == 'titleCross':
            self.source = 'D:/resources/cross.png'
            App.get_running_app().stop()
        elif self.name == 'playPause':
            if playState == 'playing':
                self.source = 'D:/resources/play.png'
                playState = 'paused'
            elif playState == 'paused':
                self.source = 'D:/resources/pause.png'
                playState = 'playing'
            elif playState == 'stopped':
                self.source = 'D:/resources/pause.png'
                playState = 'playing'
        elif self.name == 'previous':
            self.source = 'D:/resources/previous.png'
        elif self.name == 'next':
            self.source = 'D:/resources/next.png'


class Base(Widget):
    pass

class EnstrumeApp(App):
    startup()
    initProperties()
    def build(self):
        return Base()



if __name__ == '__main__':
    Window.fullscreen = 'auto'
    EnstrumeApp().run()
# MAIN CLASS ENDS


