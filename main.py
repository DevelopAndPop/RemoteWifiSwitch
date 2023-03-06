import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.network.urlrequest import UrlRequest
from kivy.uix.slider import Slider
from kivy.properties import BooleanProperty
import Global


kivy.require('2.1.0')

class MyRoot(BoxLayout):

        def __init__(self):
            super(MyRoot, self).__init__()
            # print(self.ids) #→ used for listing up available objects in .kv file
   
        def checkWifiConnection(self):
            self.checkSwitchStatus('192.168.0.100', 'switch1')
            self.initializeWifiStatus('192.168.0.100')

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
            elif switchID == 'switch2':
                switchStatus = 'id_status_switch2'
                switchName = 'id_switch2'
            elif switchID == 'switch3':
                switchStatus = 'id_status_switch3'
                switchName = 'id_switch3'
            elif switchID == 'switch4':
                switchStatus = 'id_status_switch4'
                switchName = 'id_switch4'
            else: print('Steckdose undefiniert!')

            if "STATE=OFF" in httpResult.result:
                self.ids[switchStatus].text = "Aus"
                self.ids[switchStatus].color = 'black'              
                self.ids[switchStatus].outline_color = 168/255, 9/255, 241/255, 1

            elif "STATE=ON" in httpResult.result:
                self.ids[switchStatus].text = "An"
                self.ids[switchStatus].color = 168/255, 9/255, 241/255, 1       
                self.ids[switchStatus].outline_color = 'black'
            
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


class RemoteWifi(App):
    def build(self):
        # print(dir(self.root))
        return MyRoot()

remoteWifi = RemoteWifi()
RemoteWifi().run()      