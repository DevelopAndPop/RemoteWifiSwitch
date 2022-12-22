# To-Dos:
#   - Manuell einstellbare Dauer → HTTP-Links müssen angepasst werden
#   - Aktueller Stecker-Status beim Start der App anzeigen
#   - Design ändern (für mehrere Stecker vorbereiten)
# --------------------


import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

import requests

kivy.require('2.1.0')

class MyRoot(BoxLayout):
    def __init__(self):
        super(MyRoot, self).__init__()

    def checkSwitchStatus(self):
        statusHTML =  requests.get('https://www.google.de/')

        if statusHTML.text.__contains__('STATE=ON'):
            statusWifi = "Steckdose AN"
        elif statusHTML.text.__contains__('STATE=OFF'):
            statusWifi = "Steckdose AUS"
        else:
            statusWifi = "Satus N/A"

        return statusWifi

    def switchOn(self):

        requests.get('https://www.google.de/')

        self.status_Switch.text = self.checkSwitchStatus()
              
    def switchOff(self):

        requests.get('https://www.google.de/')

        self.status_Switch.text = self.checkSwitchStatus()

class RemoteWifi(App):
    def build(self):
        return MyRoot()

remoteWifi = RemoteWifi()
remoteWifi.run()      