import network
import usocket
from machine import Pin, PWM, UART, SPI
import time
import struct
import math
import mfrc522
from ST7735 import TFT
from sysfont import sysfont


#---var---
invalid = 0
nom = 0
statut = 0
equipe = 0
ID = 0

#---client---#
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('6650 1200', 'jogalo-2824-2824')           ###### se faire white liste /!\

cnx=usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)
cnx.connect(("192.168.1.134",63714))                   ######

#---buzzer---#
tempo = 5
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
beeper = PWM(Pin(26, Pin.OUT), freq=440, duty=512)

valid_tone = 'eagc'
invalid_tone = 'cgae'
rhythm =  l*[4]

#---RDM6300---
uart1 = UART(1, baudrate=9600, tx=39, rx=16)        # 39 possiblement à changer
buf = bytearray(4)                                  # 4 changeable 

#---RC522----
rdr = mfrc522.MFRC522(14, 13, 12, 5, 21)

#---ST735---
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(27), mosi=Pin(32), miso=Pin(12))
tft=TFT(spi,33,17,18)
tft.initg()
tft.rgb(False)
tft.fill(TFT.BLACK)


#--------bouvcle principale------------
while True:

    #---lecture ID (125kHz)---#
    if uart1.any():
        uart1.readinto(buf)                          # UART.read([nbytes]) ou sinon UART.readinto(buf[, nbytes])
	ID = bytes(buf)
    
    #---lecture ID (13MHz)---#
    (stat, tag_type) = rdr.request(rdr.REQIDL)
	if stat == rdr.OK:
		(stat, raw_uid) = rdr.anticoll()
		if stat == rdr.OK:
            ID = raw_uid[0] + raw_uid[1] + raw_uid[2] + raw_uid[3]
					#print("New card detected")
					#print("  - tag type: 0x%02x" % tag_type)
					#print("  - uid	 : 0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
					#print("")
					#if rdr.select_tag(raw_uid) == rdr.OK:
					#	key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
					#	if rdr.auth(rdr.AUTHENT1A, 8, key, raw_uid) == rdr.OK:
					#		print("Address 8 data: %s" % rdr.read(8))
					#		rdr.stop_crypto1()
					#	else:
					#		print("Authentication error")
					#else:
					#	print("Failed to select tag")
    #---send ID---#
    if ID != 0:
        ID = 'ADD'+ID
        cnx.send(ID.encode())
    
        #---reception ID---#
 #       recu = cnx.recv(1024)           #est-ce qu'il faut attendre un petit peu avant ou il ne continu pas le code avant d'avoir recu qqch ?
    #    invalid=True
    #    if recu != b'invalid ID' :
    #        invalid = False
    #        nom = recu[:-2].decode()
    #        statut = recu[-1]
    #        equipe = recu[-2]
    #    
    #    #---Buzzer---#
    #    if invalid:
    #        for tone, length in zip(invalid_tone, rhythm):
    #            beeper.freq(tones[tone])
    #            time.sleep(tempo/length)
    #    else:
    #        for tone, length in zip(valid_tone, rhythm):
    #            beeper.freq(tones[tone])
    #            time.sleep(tempo/length)
    #        
    #    
    #    #---Màj écran---#
    #    if statut == 1:
    #        message = "Bienvenu !"
    #    else :
    #        message = "A bientôt !"
    #    tft.text((20, 20), message, TFT.GREEN, sysfont, 3, nowrap=True)
    #    tft.text((20, 60), nom, TFT.RED, sysfont, 3, nowrap=True)

        #---fin de la bouvle---
        ID=0
        time.sleep_ms(1000)
        tft.fill(TFT.BLACK)

    else :
        time.sleep_ms(700)                   #####