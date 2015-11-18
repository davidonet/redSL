#!/usr/bin/env python2


from liblo import *
import sys
import spidev

class MyServer(ServerThread):
	def __init__(self):
		ServerThread.__init__(self, 1234)
		self.spi = spidev.SpiDev()
		self.spi.open(0,0)
		self.spi.mode = 0b10
		self.spi.max_speed_hz =100000

	def setPattern(self,c,p):
		self.spi.xfer([c,p>>8,p&0xff])		

	@make_method('/set', 'ii')
	def foo_callback(self, path, args):
		a,p = args
		print "received",a,p
		self.setPattern(a,p)


try:
	server = MyServer()
except ServerError, err:
	print str(err)
	sys.exit()

server.start()

while True:
	sleep(10)
	
