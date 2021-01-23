import network
import usocket
from machine import Pin, PWM
import time

#---var---
invalid = 0
nom = 0
statut = 0
equipe = 0

#---client---#
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('6650 1200', 'jogalo-2824-2824') ######

cnx=usocket.socket(usocket.AF_INET,usocket.SOCK_STREAM)
cnx.connect(("192.168.1.134",63714)) ######

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
beeper = PWM(Pin(12, Pin.OUT), freq=440, duty=512)

valid_tone = 'eagc'
invalid_tone = 'cgae'
rhythm =  l*[4]



while True:
    #---lecture ID (125kHz)---#
    
    #---lecture ID (13MHz)---#
    
    #---send ID---#
    ID = 'GET'+ID
    cnx.send(ID.encode())
    
    #---reception ID---#
    recu = cnx.recv(30)
    if recu == b'invalid ID' :
        invalid = True
    else :
        nom = recu[:-2].decode()
        statut = recu[-1]
        equipe = recu[-2]
    
    #---Buzzer---#
    if invalid == True :
        for tone, length in zip(invalid_tone, rhythm):
            beeper.freq(tones[tone])
            time.sleep(tempo/length)
            
    if invalid == False :
        for tone, length in zip(valid_tone, rhythm):
            beeper.freq(tones[tone])
            time.sleep(tempo/length)
        
    
    #---Màj écran---#
