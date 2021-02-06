
from machine import Pin, PWM
import time
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
melody = 'cdeccdecefgefggagfecgagfeccGccGc'#'fdbge' #'egeccC' #'gaef'  #'cdfda ag cdfdg gf '    #'cdeccdecefgefggagfecgagfeccGccGc'
l = len(melody)
rhythm =  l*[15]  #[5,5,5,5,5,5,20,20,10,5,5,5,5,5,5,20,20,10]   #l*[16]

for tone, length in zip(melody, rhythm):
    beeper.freq(tones[tone])
    time.sleep(tempo/length)
beeper.deinit()
