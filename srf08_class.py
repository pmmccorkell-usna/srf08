from time import sleep
from machine import Timer

class Sonar:

	def __init__(self,BUS,DEBUGGING=0):
		self.bus=BUS
		#self.process_timer=Timer(1)
		self.repeat_timer=Timer(2)
		self.distance = 0xff
		self.units='cm'
		self.ADDRESS=112
		self.in_process=0
	
	def start(self,unit='cm'):
		#print('start')
		self.units=unit
		self.repeat_timer.init(mode=Timer.PERIODIC,period=70,callback=self.start_range)
		#self.start_range()

	def stop(self):
		#print('stop')
		self.repeat_timer.deinit()
		self.process_timer.deinit()
		self.distance=0xff

	def start_range(self,event=None):
		print('start_range')
		unit_type={
			'cm':b'\x51',
			'in':b'\x50'
		}
		self.bus.writeto_mem(self.ADDRESS,0,unit_type[self.units])
		sleep(0.07)
		self.process()

	def process(self):
		print('process')
		# self.in_process=1

		data=self.bus.readfrom_mem(ADDRESS,0,8)
		self.distance=data[2]*0x100 + data[3]
		if (self.DEBUGGING):
			print(data)
			print("0: "+str(data[0])+", 1: "+str(data[1])+", 2: "+str(data[2])+", 3: "+str(data[3]))
			print("distance: "+str(self.distance))

		# self.repeat_timer.init(mode=Timer.ONE_SHOT,period=5,callback=self.start_range)
		# self.in_process=0



