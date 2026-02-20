import network
import time
from secrets import secrets

class WifiManager:
    def __init__(self):
        self.ssid = secrets['ssid']
        self.pw = secrets['password']
        self.wlan = network.WLAN(network.STA_IF)
        
    def connect(self):
        self.wlan.active(True)
        if not self.wlan.isconnected():
            print(f"trying connecting Wifi...: {self.ssid}")
            self.wlan.connect(self.ssid, self.pw)
            for _ in range(10):
                if self.wlan.isconnected(): break
                time.sleep(1)
        return self.wlan.isconnected()

    def disconnect(self):
        print("disconnecting Wifi...")
        self.wlan.active(False)
        return self.wlan.isconnected()

