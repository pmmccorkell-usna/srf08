from time import sleep
from machine import Timer, I2C, Pin

DEBUGGING=0
bus=I2C(sda=Pin(21),scl=Pin(22))
#process_timer=Timer(1)
repeat_timer=Timer(2)
distance = 0xff
units='cm'
ADDRESS=112
in_process=0
	
def start(unit='cm'):
	#print('start')
	units=unit
	repeat_timer.init(mode=Timer.PERIODIC,period=70,callback=start_range)
	#start_range()

def stop():
	#print('stop')
	repeat_timer.deinit()
	distance=0xff

def start_range(event=None):
	print('start_range')
	unit_type={
		'cm':b'\x51',
		'in':b'\x50'
	}
	bus.writeto_mem(ADDRESS,0,unit_type[units])
	sleep(0.07)

	print('process')
	# in_process=1

	data=bus.readfrom_mem(ADDRESS,0,8)
	distance=data[2]*0x100 + data[3]
	if (DEBUGGING):
		print(data)
		print("0: "+str(data[0])+", 1: "+str(data[1])+", 2: "+str(data[2])+", 3: "+str(data[3]))
		print("distance: "+str(distance))

	# repeat_timer.init(mode=Timer.ONE_SHOT,period=5,callback=start_range)
	# in_process=0



