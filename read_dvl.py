# connect device to pc/rpi
# sudo chmod 777 /dev/ttyUSB0
# pip / pip3 install -e . 
# pip / pip3 install crcmod pyserial
# sudo chmod +x+rw read_dvl.py (or *)
######################################
# requirements: python3, pip3, packages above

from wldvl import WlDVL as DVL 
import asyncio
import numpy as np
from time import sleep
import socket

def connectDVL():
	dvl = DVL("/dev/ttyUSB0")
	return dvl

def connectTCP(ip="127.0.0.1", port=16716):
	connection = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	connection.connect((ip,port))
	print("Connected!")
	return connection

async def main():

	timestep = 0.05
	recnum = 1
	sndnum = 7
	#recMsg = np.zeros(recnum)
	sndMsg = np.zeros(sndnum)

	dvl 	= connectDVL()
	iTCP 	= connectTCP()

	while True:
		
		
		await asyncio.sleep(timestep)
		
		dvl_data = dvl.read()
		
		sndMsg = -np.ones(sndnum)
		
		try:
			if dvl_data:
				print("Data is valid!")
				if dvl_data['time'] < 200: 			# if data is not older than 200 ms
					sndMsg[0] = dvl_data['time']
					sndMsg[1] = dvl_data['vx']
					sndMsg[2] = dvl_data['vy']
					sndMsg[3] = dvl_data['vz']
					sndMsg[4] = dvl_data['fom']
					sndMsg[5] = dvl_data['altitude']
					sndMsg[6] = dvl_data['valid']
			else:
				print("Data not valid")

			if 1:
				print("Time since last report (ms):", dvl_data['time'])
				print("Velocity:", dvl_data['vx'], dvl_data['vy'], dvl_data['vz'])
				print("Velocity accuracy:", dvl_data['fom'])
				print("Altitude:", dvl_data['altitude'])
				print("Measurement valid:", dvl_data['valid'])
				print(sndMsg)
				#print("------------------")
		except Exception as e:
			pass#print("Error:", e)

		try: 
			iTCP.sendall(sndMsg)
			print("Data sent!")
		except Exception as e:
			print("TCP Error:", e)

		

if __name__ == "__main__":
	asyncio.run(main())