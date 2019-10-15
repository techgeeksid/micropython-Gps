from machine import UART
from micropyGPS import MicropyGPS
import utime, gc, _thread
import time
import urequests
import network
import ujson


uart = UART(1, rx=13, tx=12, baudrate=9600)
s = MicropyGPS()
URL = 'Firebase Url'
num = 0

def intern():
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  if not wlan.isconnected():
    print('connecting to network...')
    wlan.connect('iPhone' , 'nopassword')


intern()


while True:
    time.sleep(3)
    ces = uart.read()
    line = ces.splitlines()
    for x in line:
     line_to_string = str(x)
     formated_line = line_to_string[2:-1]
     if formated_line[1:-(len(formated_line)-6)] == 'GNRMC':
      for x in formated_line:
        s.update(x)
      print(formated_line)
      print(s.latitude[0]+((s.latitude[1])/60),s.longitude_string(),s.speed_string())
      lat = s.latitude[0]+((s.latitude[1])/60)
      lon = s.longitude[0]+((s.longitude[1])/60)
      speed = s.speed_string()
      num = num + 1
      datas = {"lat":lat,"lon":lon,"num":num,"speed":speed}
      datasent = ujson.dumps(datas)
      sent = urequests.put(URL,data = datasent)
      sent.close()
