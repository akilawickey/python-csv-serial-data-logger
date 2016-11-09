#######################################TEAM VEGA##################################################


import csv
import serial
# import XBee
from time import sleep
from datetime import datetime
import serial.tools.list_ports
import thread
import time
#----------------------------------------------------------------------

global ser_can,ser_batt

def csv_writer(data, path):

    """

    Write data to a CSV file path

    """

    with open(path, "a") as csv_file:

        writer = csv.writer(csv_file,delimiter=',')

        

        writer.writerow(data)


def read_battery():

	global data_raw

	data_raw = ser_batt.readline()
	#data_raw = '#0,0,0,0,3,4,5,1,2,4,34,23,43,32,65,23,34,23,43,32  #1,4345,4645,6755,3456,4334,3453,1234,4355,3423,4356,7567,3245,5467,3245,3425,23445,23445,2345,4325,3454,3453,5344,5435,3455,3455,3456,2345,2445,2345,23445,2455,2344,3455,4566,3455,34544,4535,3455,3244,2344,5464,2344,5345,2342,43455,23445,2344,5345,2344,4353'
    	print(data_raw)

def read_can():        

	global data_raw2
	data_raw2= ser_can.readline()
	#data_raw2 = "#ID: BB  Data: 23 45 34 23 45 23 45 23"
    	print(data_raw2)

# def send_Xbee():        

# 	new_str_wait = '#' +time + '#' + data_raw + data_raw2 + ']]]]]]]]]]'
# 	# time.sleep(1)
# 	ser2.write(new_str_wait)
# 	print(new_str_wait)

# 	ser2.write('\n')
# 	ser_batt.flushInput()
# 	ser_batt.flushOutput()
# 	ser_can.flushInput()
# 	ser_can.flushOutput()
	# ser2.flushInput()
	# ser2.flushOutput()

	#time.sleep(0.5)
	#ser2.write('###' +time + '#' + str(data_raw2) + ']]]]]]]')


	
#----------------------------------------------------------------------

if __name__ == "__main__":

	XBEE = ""
	BATTERY = ""
	CAN = ""


	try:

		########################## Configure USB ports #################################

		list1 = serial.tools.list_ports.comports()
		Xbee = "USB VID:PID=0403:6001 SNR=AH03I7PP"
		battery_cable = "USB VID:PID=0403:6001 SNR=A50285BI"
		CAN_pid_vid = "USB VID:PID=1a86:7523"


		#print(list(serial.tools.list_ports.comports()))s
		for a in range(0,len(list1) ):
		    #if(list1[a][0] ==  "/dev/ttyUSB0"):
		 if(list1[a][2] == CAN_pid_vid):	
		  CAN = list1[a][0]
				
		 if(Xbee == list1[a][2]):
		  XBEE = list1[a][0]

		 if(battery_cable == list1[a][2]):
		  BATTERY = list1[a][0]

		##################################################################################				
	
		ser_batt = serial.Serial('/dev/ttyUSB1', 9600, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		ser_batt.flushInput()
		ser_batt.flushOutput()

		ser_can = serial.Serial('/dev/ttyUSB0', 115200, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		ser_can.flushInput()
		ser_can.flushOutput()

		#ser2 = serial.Serial(XBEE, 115200, timeout=2, xonxoff=False, rtscts=False, dsrdtr=False) #Tried with and without the last 3 parameters, and also at 1Mbps, same happens.
		#ser2.flushInput()
		#ser2.flushOutput()

		
		#xbee = XBee.XBee("/dev/ttyUSB0") 
		

		while True:
		  # thread.start_new_thread(read_battery,())	
		  # read_can()	
		  read_battery()
		  read_can()

		  print("VEGA logging data ...")
		  time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")	
		  # if count == 5:
		  # ent = xbee.SendStr(data_raw.split(','))

		  #send_Xbee()
		  #thread.start_new_thread(send_Xbee)
		  

		  # print("sent!!!")
		  csv_write_battery = time + str(data_raw)	
		  csv_write_can = time + str(data_raw2)	

		  csv_writer(csv_write_battery.split(','), "battery.csv")
		  csv_writer(csv_write_can.split(','), "can.csv")

			  # count = 0	
	except KeyboardInterrupt:

		print "closing ports"
        ser_batt.close()
        ser_can.close()
