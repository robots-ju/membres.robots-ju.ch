

import time

import network
time.sleep(0.5)
import usocket
time.sleep(0.5)
from machine import Pin, PWM, UART, SPI

import struct
import math
import mfrc522
from ST7735 import TFT
from sysfont import sysfont

import micropython

micropython.alloc_emergency_exception_buf(100)


#---var---
invalid = 0
nom = 0
statut = 0
equipe = 0
message = '0'
ID = 0

#---buzzer---#
tempo = 1
tones = {
    'c': 262, # do 
    'd': 294, # re
    'e': 330, # mi
    'f': 349, # fa
    'g': 392, # sol
    'a': 440, # la
    'b': 494, # si
    'C': 523, # do
    ' ': 0,
    'G': 196,
}


valid_tone = 'eagc'
invalid_tone = 'cgae'
l=4
rhythm =  l*[10]

#---RDM6300---
uart1 = UART(1, baudrate=9600, rx=16)



#---RC522----
rdr = mfrc522.MFRC522(14, 13, 12, 5, 21)


#---client---#
wlan = network.WLAN(network.STA_IF)
time.sleep(1)
wlan.active(True)
time.sleep(1)
wlan.connect('Robots-JU', 'robotmaker')
time.sleep(2)

cnx=usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)
time.sleep(2)
cnx.connect(("192.168.2.106",3714)) #####faire gaffe à l'addresse IP

time.sleep(0.5)
#cnx.send(b'GETcoucou')
print('ready')

#---ST735---
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(27), mosi=Pin(32))#, miso=Pin(12))

tft=TFT(spi,33,17,18)
tft.initg()
tft.rgb(False)
tft.rotation(1)
time.sleep(0.1)
tft.fill(TFT.BLACK)

if uart1.any():
    uart1.read()


#--------bouvcle principale------------
while True:
  
    #---lecture ID (125kHz)---#
  if uart1.any():
    idi=uart1.read(13)
    if len(idi)>12 and len(idi)<20:
      ID=idi[5:13]
      

  #---lecture ID (13MHz)---#
  (stat, tag_type) = rdr.request(rdr.REQIDL)
  if stat == rdr.OK:
    (stat, raw_uid) = rdr.anticoll()
    if stat == rdr.OK:
      IDp = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
      print(IDp)
      ID = IDp.encode()
      
  if ID != 0:
    print(ID)
    ID = b'GET'+ID
    cnx.send(ID)  #.encode('utf-8'))
    time.sleep(0.1)
    
    #---reception ID---#
    recu = cnx.recv(30)           #est-ce qu'il faut attendre un petit peu avant ou il ne continu pas le code avant d'avoir recu qqch ?
    
    invalid=True
    if recu != b'invalid ID' :
      invalid = False
      nom = recu[:-2].decode('utf-8')
      statut = recu[-1]-48
      equipe = recu[-2]-48
      #print(statut, 'statut')
      if equipe<5 or equipe>0 :
        equipe = 'Equipe '+ str(equipe)
      elif equipe==0:
        equipe = 'Coach'
      elif equipe==5:
        equipe = 'Groupe avance'
      print(nom)
        
    #---Buzzer---#
    beeper = PWM(Pin(26, Pin.OUT), freq=440, duty=512)
    if invalid:
      for tone, length in zip(invalid_tone, rhythm):
        beeper.freq(tones[tone])
        time.sleep(tempo/length)
    else:
      for tone, length in zip(valid_tone, rhythm):
        beeper.freq(tones[tone])
        time.sleep(tempo/length)
    beeper.deinit()
    
    #---M脿j 茅cran---#
    if invalid : 
      tft.text((10, 20), 'Invalid ID', TFT.RED, sysfont, 2, nowrap=True)
      tft.text((20, 60), "(._.)", TFT.RED, sysfont, 3, nowrap=True)
    else:
      if statut == 49:
        message = "Bienvenue !"
      elif statut == 48 :
        message = "A bientot !"
      tft.text((10, 20), message, TFT.GREEN, sysfont, 2, nowrap=True)
      tft.text((10, 60), nom, TFT.WHITE, sysfont, 2, nowrap=True)
      tft.text((10, 100), equipe, TFT.BLUE, sysfont, 2, nowrap=True) # equipe

    #---fin de la bouvle---
    ID=0
    nom = 0
    statut = 0
    equipe = 0
    time.sleep_ms(3000)
    if uart1.any():
      uart1.read() #lire pour envlever les lectures en trop du buffer
    tft.fill(TFT.BLACK)

  else :
    time.sleep_ms(700)                   #####



