from machine import UART
uart1 = UART(1, baudrate=9600, tx=14, rx=4)

import struct

# callback to run on detection
def cb(code, facility, card):
	print('Code: {}, Facility: {}, Card: {}'.format(code, facility, card))

# poll the uart
def uart_demo(callback):
	buf = bytearray(4)
	while True:
		if uart1.any():
			uart1.readinto(buf)
			code = struct.unpack('>i',buf)[0]
			facility = code >> 16
			card = code & 0xFFFF
			callback(code, facility, card)

# run the demo
uart_demo(cb)

# scan my blue EM4100 tag with engraving "0003069055"
Code: 3069055, Facility: 46, Card: 54399

# scan my pink EM4100 tag with engraving "0008123291"
Code: 8123291, Facility: 123, Card: 62363

# scan my yellow EM4100 tag with engraving "0012459289"
Code: 12459289, Facility: 190, Card: 7449