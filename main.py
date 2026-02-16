from machine import Pin, I2C
import network
import urequests
import time
import os
import gc
import sh1106  # Hardware Driver
import ds3231
from secrets import secrets # secrets

# 1. Display & RTC Management
class DisplayManager:
    def __init__(self, sda_pin, scl_pin):
        self.i2c = I2C(0, sda=Pin(sda_pin), scl=Pin(scl_pin), freq=400000)
        try:
            self.display = sh1106.SH1106_I2C(128, 64, self.i2c, rotate=180)
            self.display.sleep(False)
            self.rtc = ds3231.DS3231(self.i2c)
            print("OLED & RTC initialized!")
        except Exception as e: 
            print("Failed connecting:", e)
            self.rtc = None
    
    def get_time_str(self):
        if self.rtc:
            t = self.rtc.get_time()
            return "{:04d}-{:02d}-{:02d}".format(t[0], t[1], t[2]), "{:02d}:{:02d}:{:02d}".format(t[4], t[5], t[6])
        return "0000-00-00", "00:00:00"
    
    def display_start(self):
        self.display.fill(0)
        self.display.text("Ready to Click!", 5, 25, 1)
        self.display.show()
        
    def draw_mood(self, mood_text, wifi_on=False):
        date_s, time_s = self.get_time_str()
        self.display.fill(0)
        self.display.rect(0, 0, 128, 64, 1)
        
        if wifi_on:    # wifi status
            self.display.text("o", 115, 5, 1) # connected: o
        else:
            self.display.text("x", 115, 5, 1) # disconnceted: x
            
        self.display.text("Now I feel...", 13, 15, 1)
        self.display.text(mood_text, 13, 30, 1)
        self.display.text(time_s, 13, 50, 1)
        self.display.show()

    def show_uploading(self):      # show uploading screen
        self.display.fill(0)
        self.display.rect(0, 0, 128, 64, 1)
        self.display.text("uploading", 25, 25, 1)
        self.display.text("my mood...", 13, 40, 1)
        self.display.show()
        
# 2. Wifi 
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
    
# 3. Log Record
class LocalLogger:
    def __init__(self, filename="mood_log.csv"):
        self.filename = filename
    
    def save(self, data_str):
        with open(self.filename, "a") as f:
            f.write(data_str + "\n")
            
    def read_all(self):
        if self.filename in os.listdir():
            with open(self.filename, "r") as f:
                return f.readlines()
        return []
    
    def clear(self):
        if self.filename in os.listdir():
            os.remove(self.filename)

# 4. Cloud Sync & Memory Management
class GoogleUploader:
    def __init__(self):
        self.url = secrets['google_url']
        
    def sync_from_file(self, logger, display_man):
        lines = logger.read_all()
        if not lines: return
        
        display_man.show_uploading()
        print(f"start sync: {len(lines)}records")
        all_ok = True
        
        for line in lines:
            line = line.strip()
            if not line: continue
            
            # encoding characters
            d, t, m = line.split(',')
            m_safe = m.replace(" ", "%20").replace(":", "%3A").replace("^", "%5E")
            full_url = f"{self.url}?date={d}&time={t}&mood={m_safe}"
            
            resp = None # initialzing
            try:
                resp = urequests.get(full_url)
                
                # handling HTTP 302 redirect(if needed)
                if resp.status_code == 302:
                    new_url = resp.headers.get("Location")
                    resp.close() # close earlier response
                    resp = urequests.get(new_url)
                
                # check final uploading
                if resp.status_code == 200 and "Success" in resp.text:
                    print(f"uploading success: {m}")
                else:
                    all_ok = False
                    print(f"failed uploadig(status code): {resp.status_code}")
            
            except Exception as e:
                print(f"network error: {e}")
                all_ok = False
                break # escape
                
            finally:
                if resp:
                    resp.close() # memory off
            pass
        
        if all_ok:
            logger.clear()
            print("success uploading & removing all logs!")
            
        gc.collect()  # garbage collecting
        print(f"memory optimalized: {gc.mem_free()}bytes free")
        
# Main Code
# 1. call classes
dm = DisplayManager(4, 5)                         # 1. display
wm = WifiManager()                                # 2. wifi
logger = LocalLogger()                            # 3. local record
uploader = GoogleUploader()                       # 4. Google upload & remove cash

# 2. buttons setting (GP10, 11, 12, 13, 14, 15)
button_pins = [10, 11, 12, 13, 14, 15]
buttons = [Pin(p, Pin.IN, Pin.PULL_UP) for p in button_pins]
moods = ["Happy :D", "Peace :)", "Anxious X(", "Angry -_-^", "Excited XD", "Tired -_-"]

# 3. start screen
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