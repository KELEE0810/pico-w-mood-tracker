# ds3231.py
from machine import I2C, Pin

class DS3231:
    def __init__(self, i2c):
        self.i2c = i2c
        self.addr = 0x68

    def _dec_to_bcd(self, dec):
        return (dec // 10) << 4 | (dec % 10)

    def _bcd_to_dec(self, bcd):
        return (bcd >> 4) * 10 + (bcd & 0x0F)

    def save_time(self, year, month, day, weekday, hour, minute, second):
        data = bytearray(7)
        data[0] = self._dec_to_bcd(second)
        data[1] = self._dec_to_bcd(minute)
        data[2] = self._dec_to_bcd(hour)
        data[3] = self._dec_to_bcd(weekday) # Mon(1)~Sun(7)
        data[4] = self._dec_to_bcd(day)
        data[5] = self._dec_to_bcd(month)
        data[6] = self._dec_to_bcd(year - 2000)
        self.i2c.writeto_mem(self.addr, 0, data)

    def get_time(self):
        # Get time from RTC
        data = self.i2c.readfrom_mem(self.addr, 0, 7)
        return [
            self._bcd_to_dec(data[6]) + 2000, # Year
            self._bcd_to_dec(data[5]),        # Month
            self._bcd_to_dec(data[4]),        # Date
            self._bcd_to_dec(data[3]),        # Day
            self._bcd_to_dec(data[2]),        # Hour
            self._bcd_to_dec(data[1]),        # Miniute
            self._bcd_to_dec(data[0])         # Second
        ]

