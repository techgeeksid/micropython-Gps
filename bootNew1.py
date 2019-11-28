from machine import UART
from micropyGPS import MicropyGPS
import utime, gc, _thread
import time
import urequests
import network
import ujson

s = MicropyGPS()
uart = UART(1, rx=33, tx=32, baudrate=9600)
URL = 'https://micropy1.firebaseio.com/bus1.json'
num = 0

def intern():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('Bus1' , 'SrkrecBus1')

intern()


while True:
    #print('start')
    time.sleep(3)
    line = uart.readline()
    formated_line = str(line)[2:-1]
    #print(formated_line)
    if formated_line[1:6]== 'GPRMC':
      for x in formated_line:
        s.update(x)
      #print(s.latitude)
      lat = s.latitude[0]+((s.latitude[1])/60)
      lon = s.longitude[0]+((s.longitude[1])/60)
      speed = s.speed_string()
      num = num + 1
      datas = {"lat":lat,"lon":lon,"num":num,"speed":speed}
      datasent = ujson.dumps(datas)
      #print(datasent)
      try:
        sent = urequests.put(URL,data = datasent)
        sent.close()
      except OSError:
        print("error")
      
 
