# Make sure to have the server side running in CoppeliaSim: 
# in a child script of a CoppeliaSim scene, add following command
# to be executed just once, at simulation start:
#
# simRemoteApi.start(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

try:
	import sim
except:
	print ('--------------------------------------------------------------')
	print ('"sim.py" could not be imported. This means very probably that')
	print ('either "sim.py" or the remoteApi library could not be found.')
	print ('Make sure both are in the same folder as this file,')
	print ('or appropriately adjust the file "sim.py"')
	print ('--------------------------------------------------------------')
	print ('')

import time
from Robot import Robot
import numpy as np
import cv2



ROBOT = 'Robotnik_Summit_XL'
WHEEL_BL = 'joint_back_left_wheel'
WHEEL_BR = 'joint_back_right_wheel'
WHEEL_FL = 'joint_front_left_wheel'
WHEEL_FR = 'joint_front_right_wheel'

def getImage(clientID, _camera):
	errol = 1

	while(errol != sim.simx_return_ok):
		errol, res, image = sim.simxGetVisionSensorImage(clientID, _camera, 0, sim.simx_opmode_buffer)
		time.sleep(0.005)
	nres = [res[0]-int(res[0]/3),res[1]]
	img = np.array(image, dtype=np.uint8)		# Como é recebido uma string, precisa reformatar
	img = np.reshape(img, (res[0], res[1], 3))	# Pro CV2, (y, x, [B,R,G])
	img = np.flip(img, 0)						# Por algum motivo vem de ponta cabeça
	img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)	# Transforma o RGB recebido em BGR pro CV2
	img = img[0:res[0]-(int(res[0]/3)), 0:res[1]]

	return img



print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:

	sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
	print ('Connected to remote API server')
	sim.simxAddStatusbarMessage(clientID,'Funcionando...',sim.simx_opmode_oneshot_wait)
	time.sleep(0.02)


	robot = Robot(clientID, ROBOT, WHEEL_BL, WHEEL_BR, WHEEL_FL, WHEEL_FR, 'Vision_sensor')

	robot.camera.ShowInWindow(robot.camera.GetImage())

	robot.MoveLeft(30, 0.6)


	time.sleep(3)

     # Pause simulation
	sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

    # Now close the connection to V-REP:
	sim.simxAddStatusbarMessage(clientID, 'Programa pausado', sim.simx_opmode_blocking )
	sim.simxFinish(clientID)
else:
	print ('Failed connecting to remote API server')
print ('Program ended')
