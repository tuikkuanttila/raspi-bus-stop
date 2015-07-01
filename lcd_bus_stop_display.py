# -*- coding: utf-8 -*-
import os
import json
import urllib2
from settings_file import user,passkey
from Adafruit_CharLCD import Adafruit_CharLCD
import time

class BusDisplay(object):
    
    def format_bus_number(self,original_string):
        num = original_string.split()[0]
        num = num[1:]
        return num
        
    def format_time(self,original_string):
        ostr = str(original_string)
        hours = ostr[0:2]
        mins = ostr[2:]
        return hours + ":" + mins

    def get_departures(self,urlbase,stop_code):
        url = urlbase + stop_code
        json_data = urllib2.urlopen(url).read()
        data = json.loads(json_data.decode())
        departures = data[0]["departures"]
        
        if departures:
            for d in departures:
                d["code"] = self.format_bus_number(d["code"])
                d["time"] = self.format_time(d["time"])

        return departures
    
    def stop_information(self,display_name,stop_code):
        departures = [] 
        urlbase = "http://api.reittiopas.fi/hsl/prod/?user=" + user + "&pass=" + passkey + "&request=stop&code="
        code = stop_code
        stop = {}
        stop["departures"] = self.get_departures(urlbase,code)
        stop["stop_name"] = display_name

        return stop
        

if __name__ == '__main__':

    lcd = Adafruit_CharLCD()

    # If you have a bigger display, you could increase this value to show more departures 
    next_departures = 2
	
    while True:
        
        bus_stop = BusDisplay()
        departures_550 = bus_stop.stop_information("Westbound ring I, Leppavaara","2112261")
        
        depts = 0
        lcd.clear()
		
        for dept in departures_550["departures"]:

            if dept["code"] == "550":

                lcd.message(dept["code"] + " " + dept["time"] + "\n")
                depts += 1

                if depts == next_departures:
                    time.sleep(10)
                    break
