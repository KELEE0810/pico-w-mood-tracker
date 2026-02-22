import network
import time
from secrets import secrets

class WifiManager:
    def __init__(self):
        self.networks = secrets.get('networks', [])
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self):
        self.wlan.active(True)
        if self.wlan.isconnected():
            return True

        for net in self.networks:
            ssid = net.get('ssid')
            pw = net.get('pw')
            
            print(f"Trying to connect to {ssid}...")
            self.wlan.connect(ssid, pw)
            
            for _ in range(10):
                if self.wlan.isconnected():
                    print(f"Success! Connected to {ssid}")
                    return True
                time.sleep(1)
            
            print(f"Failed to connect to {ssid}")
            
        return False

    def disconnect(self):
        print("Disconnecting WiFi to save power...")
        self.wlan.active(False)
        return not self.wlan.isconnected()
