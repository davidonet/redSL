import spidev
import time
import signal 
import sys
import subprocess
import random

def signal_handler(signal, frame):
    print 'You pressed Ctrl-C!'
    spi.xfer([0xff,0x0,0x0])
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 0b10
spi.max_speed_hz =100000

def setPattern(c,p):
	spi.xfer2([c,p>>8,p&0xff])			
	
col =[[],[],[],[]]
col[3] = [1,5,9,13,17,21,25,29]
col[2] = [2,6,10,14,18,22,26,30]
col[1] = [3,7,11,15,19,23,27,31]
col[0] = [4,8,12,16,20,24,28,32]


def column(c):
	while True:
		for j in range(16):
			for i in col[c]:
				setPattern(i,1<<j)			
			time.sleep(.3)
		setPattern(0xff,0x0000)

while True:
	for j in range(16):
		for i in range(33):
			setPattern(i,1<<j)	
		time.sleep(.2)
	setPattern(0xff,0x0000)
	time.sleep(.1)