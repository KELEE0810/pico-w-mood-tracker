from machine import Pin, I2C
import sh1106   # Hardware drivers
import ds3231
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
