import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
import kivy.storage.jsonstore 
import Global  

import datetime
import time

kivy.require('2.1.0')

class MyRoot(BoxLayout):

        def __init__(self):
            super(MyRoot, self).__init__()
            self.store=kivy.storage.jsonstore.JsonStore('OnOffLog.json', indent=2)
            # print(self.ids) #→ used for listing up available objects in .kv file
        

        def checkWifiConnection(self):
            self.checkSwitchStatus('192.168.0.100', 'switch1')
            self.initializeWifiStatus('192.168.0.100')
            self.initializeOnOffLogger()

        def initializeOnOffLogger(self):
            # if self.store.store_exists(self.ids['id_name_switch'].text):
            #     with open('OnOffLog.json') as jn:
            #         dict=kivy.storage.jsonstore.JsonStore.store_load(str(jn))
            #     self.ids['id_status_time'].text = "Zuletzt eingeschaltet: " + dict['Büro-Licht']['Datum']
            self.ids['id_status_time'].text = "Zuletzt eingeschaltet: " + self.store.store_get('Büro-Licht')['Datum']

        def changeOfflineColors(self):
            self.ids['id_headline'].color = 247/255, 220/255, 247/255, 1

        def request_callback(self, req, result):
            print(f'HttpStatus: {req.resp_status}')
            print(f'Response Headers: {req.resp_headers}')
            print(f'Response: {result}')

        def switch_click(self, switchIP, switchID):
            httpResult = self.checkSwitchStatus(switchIP, switchID)
            httpResult.wait()
            
            #print(httpResult.result)
        
            if "STATE=ON" in httpResult.result:
                {
                    UrlRequest('http://192.168.0.100/control.html?STATE=0')
                }

            elif "STATE=OFF" in httpResult.result:
                {
                    UrlRequest('http://192.168.0.100/control.html?STATE=1')
                }
            
            httpResult = self.checkSwitchStatus(switchIP, switchID)
            
        def checkSwitchStatus(self, switchIP, switchID):
            ipadress = 'http://' + switchIP + '/control.html?GET=state'
            httpResult = UrlRequest(ipadress, self.request_callback, debug=True)
            httpResult.wait()

            if switchID   == 'switch1':
                switchStatus = 'id_status_switch'
                switchName = 'id_switch'
                statusTimeName = self.ids['id_name_switch'].text
            elif switchID == 'switch2':
                switchStatus = 'id_status_switch2'
                switchName = 'id_switch2'
                statusTimeName2 = self.ids['id_name_switch2'].text
            elif switchID == 'switch3':
                switchStatus = 'id_status_switch3'
                switchName = 'id_switch3'
                statusTimeName3 = self.ids['id_name_switch3'].text
            elif switchID == 'switch4':
                switchStatus = 'id_status_switch4'
                switchName = 'id_switch4'
                statusTimeName4 = self.ids['id_name_switch4'].text
            else: print('Steckdose undefiniert!')

            if "STATE=OFF" in httpResult.result:
                self.ids[switchStatus].text = "Aus"
                self.ids[switchStatus].color = 'black'              
                self.ids[switchStatus].outline_color = 168/255, 9/255, 241/255, 1

            elif "STATE=ON" in httpResult.result:
                self.ids[switchStatus].text = "An"
                self.ids[switchStatus].color = 168/255, 9/255, 241/255, 1       
                self.ids[switchStatus].outline_color = 'black'

            self.getTime(self.ids[switchStatus].text, statusTimeName)
            
            return httpResult
        
        def initializeWifiStatus(self, switchIP):
            ipadress = 'http://' + switchIP + '/control.html?GET=state'
            httpResult = UrlRequest(ipadress, self.request_callback, debug=True)
            httpResult.wait()
            
            if "STATE=ON" in httpResult.result:
                wifiStatusBool = True
                
            elif "STATE=OFF" in httpResult.result:
                wifiStatusBool = False

            return wifiStatusBool

        def getTime(self, onoff, switchName):
            timestamp = datetime.datetime.now()

            if onoff == 'An':
                self.ids['id_status_time'].text = "Zuletzt eingeschaltet: " + str(timestamp)[0:16]
                self.store.put(str(switchName), letzterStatus="An", Datum=str(timestamp)[0:16])
            elif onoff == 'Aus':
                self.ids['id_status_time'].text = "Zuletzt ausgeschaltet: " + str(timestamp)[0:16]
                self.store.put(str(switchName), letzterStatus="Aus", Datum=str(timestamp)[0:16])


class RemoteWifi(App):
    def build(self):
        # print(dir(self.root))
        return MyRoot()

remoteWifi = RemoteWifi()
RemoteWifi().run()      