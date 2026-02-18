from machine import Pin
import time
from sh1106 import SH1106
from ds3231 import DS3231
from display_manager import DisplayManager
from wifi_manager import WifiManager
from local_logger import LocalLogger
from google_uploader import GoogleUploader

# call modules
dm = DisplayManager(4, 5)                  
wm = WifiManager()                                
logger = LocalLogger()                            
uploader = GoogleUploader()                    

# buttons setting (GP10, 11, 12, 13, 14, 15)
button_pins = [10, 11, 12, 13, 14, 15]
buttons = [Pin(p, Pin.IN, Pin.PULL_UP) for p in button_pins]
moods = ["Excited XD", "Happy :D", "Peace :)", "Tired -_-", "Anxious X(", "Angry -_-^"]

# start screen
dm.display_start()

while True:
    for i, btn in enumerate(buttons):
        if btn.value() == 0:
            is_wifi = wm.wlan.isconnected()
            date_s, time_s = dm.get_time_str()  # show screen and current time
            dm.draw_mood(moods[i], wifi_on=is_wifi) 
            
            log_data = f"{date_s},{time_s},{moods[i]}" # record log locally
            logger.save(log_data)
            print(f"local saved: {log_data}") 
            
            if wm.connect():  # try connecting wifi & uploading on Google sheets
                uploader.sync_from_file(logger, dm)
                dm.draw_mood(moods[i], wifi_on=True)
                
            while btn.value() == 0:  # wait for button release(debouncing)
                time.sleep(0.05)   # stabilizing 
            time.sleep(0.5)
            dm.display_start()   # back to start scren
    time.sleep(0.1)   # small delay to reduce CPU load
