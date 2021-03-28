from time import sleep
from machine import Timer

class Sonar:

	def __init__(self,BUS,debug=0):
		self.DEBUGGING=debug
		self.bus=BUS
		self.repeat_timer = Timer(2)
		self.distance = 0xffff
		self.units = b'\x51'	# cm default
		self.ADDRESS = 112
	
	def start(self,unit='cm'):
		unit_type={
			'in':b'\x50',
			'cm':b'\x51'
		}
		self.units=unit_type[unit]
		self.write_range()
		sleep(0.1)
		self.repeat_timer.init(mode=Timer.PERIODIC,freq=10,callback=self.get_range)

	def stop(self):
		self.repeat_timer.deinit()
		self.process_timer.deinit()
		self.distance=0xffff

	def get_range(self,event=None):
		self.distance=self.read_range()
		#sleep(0.0001)
		self.write_range()

	def read_range(self):
		data = self.bus.readfrom_mem(self.ADDRESS,2,2)
		if (self.DEBUGGING):
			print(data)
			print("0: "+str(data[0])+", 1: "+str(data[1])+", 2: "+str(data[2])+", 3: "+str(data[3]))
			print("distance: "+str(self.distance))
		return data[0]*0x100 + data[1]

	def write_range(self):
		self.bus.writeto_mem(self.ADDRESS,0,self.units)

