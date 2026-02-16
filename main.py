from machine import Pin, I2C 
import sh1106                
import ds3231                
import time                  
import os                    
import network              
import urequests             
from secrets import secrets  

# I2C installation (SDA: 4, SCL: 5)
i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)

# Hardware initializing & Error handling
try:
    # OLED setting (you can set your own rotate option)
    display = sh1106.SH1106_I2C(128, 64, i2c, rotate=180)
    display.sleep(False)
    # RTC setting 
    rtc = ds3231.DS3231(i2c) 
    print("OLED & RTC connected! :D")
except Exception as e:
    print("Hardware connect failed! Check hardware connection:", e)
    rtc = None # Though you don't have rtc, it's ok

# Buttons & Mood setting
button_pins = [10, 11, 12, 13, 14, 15] # Pico's pin numbers for buttons
buttons = [Pin(p, Pin.IN, Pin.PULL_UP) for p in button_pins] # Buttons setting

# Moods (You can chage whatever you want)
moods = ["Happy :D", "Peace :)", "Anxious X(", "Angry -_-^", "Excited XD", "Tired -_-"]

# Local Log(RAM)
mood_queue = []

# wifi connect setting
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print(f"Wifi connecting... ({secrets['ssid']})")
        wlan.connect(secrets['ssid'], secrets['password'])
        
        # Check every 1 sec for 10 secs
        attempt = 0
        while not wlan.isconnected() and attempt < 10:
            time.sleep(1)
            attempt += 1
    
    if wlan.isconnected():
        print("Wifi connect success!", wlan.ifconfig()[0])
        return True
    else:
        print("Wifi connect failed... (offline)")
        return False

# uploading on Google Sheet
def send_to_google():
    if not connect_wifi(): 
        return # give up uploading
    
    # check unsent mood_log.csv
    if "mood_log.csv" in os.listdir():
        print("Unsent Mood_log found! Sending...")
        try:
            with open("mood_log.csv", "r") as f:
                lines = f.readlines() # read every line
            
            all_sent_successfully = True
            
            for line in lines:
                line = line.strip()
                if not line: continue
                
                parts = line.split(',')
                if len(parts) < 3: continue
                
                date_val, time_val, mood_val = parts[0], parts[1], parts[2]
                
                # Encoding special characters(For 400 Error)
                safe_mood = mood_val.replace(" ", "%20").replace(":", "%3A").replace("(", "%28").replace("^", "%5E")
                url = f"{secrets['google_url']}?date={date_val}&time={time_val}&mood={safe_mood}"
                
                resp = urequests.get(url)
                
                # Handle HTTP 302 redirect
                if resp.status_code == 302:
                    new_url = resp.headers.get("Location")
                    resp.close()
                    resp = urequests.get(new_url)
                
                if "Success" not in resp.text:
                    all_sent_successfully = False
                    print(f"Upload failed line: {line}")
                
                resp.close()
            
            # Remove all local logs if upload successed
            if all_sent_successfully:
                os.remove("mood_log.csv")
                mood_queue.clear()
                print("Unsent data uploaded! Removed local log.")
            
        except Exception as e:
            print("Error while uploading:", e)

# local log
def save_mood(mood_name):
    # check current time from RTC
    if rtc is None:
        date_str, time_str = "0000-00-00", "00:00:00"
    else:
        t = rtc.get_time() # [Year, Month, Date, Day, Hour, Minute, Second]
        date_str = "{:04d}-{:02d}-{:02d}".format(t[0], t[1], t[2])
        time_str = "{:02d}:{:02d}:{:02d}".format(t[4], t[5], t[6])
    
    log_entry = f"{date_str},{time_str},{mood_name.strip()}"
    mood_queue.append(log_entry)
    print(f"RAM queue added: {log_entry}")
    
    # backup to Flash memory (local storage)
    try:
        with open("mood_log.csv", "a") as f:
            f.write(log_entry + "\n")
        print(f"Success Logging: {log_entry}")
    except Exception as e:
        print("Failed Logging:", e)

# Display
def draw_screen(btn_num):
    display.fill(0)
    display.rect(0, 0, 128, 64, 1) # frames
    
    mood_text = moods[btn_num - 1] 
    display.text("now I feel...", 13, 15, 1)
    display.text(mood_text, 13, 40, 1)
    display.show()

# Main loop
display.fill(0)
display.text("Ready to Click!", 5, 25, 1)
display.show()

while True:
    for i, btn in enumerate(buttons): 
        if btn.value() == 0: # PULL_UP
            btn_number = i + 1
            
            draw_screen(btn_number)   # show chosen emotion
            save_mood(moods[i])    # save at RAM or Flash memory
            send_to_google()     # try uploading on Google Sheets
            time.sleep(0.3)    # debouncing
