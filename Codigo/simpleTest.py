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



print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:

	sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
	print ('Connected to remote API server')
	sim.simxAddStatusbarMessage(clientID,'Funcionando...',sim.simx_opmode_oneshot_wait)
	time.sleep(0.02)

	#Handles
	#Robo
	erro, robo = sim.simxGetObjectHandle(clientID, 'Robotnik_Summit_XL', sim.simx_opmode_blocking)
	#Motores
	[erro, robotBackLeftMotor] = sim.simxGetObjectHandle(clientID, 'joint_back_left_wheel', sim.simx_opmode_blocking)
	[erro, robotBackRightMotor] = sim.simxGetObjectHandle(clientID, 'joint_back_right_wheel', sim.simx_opmode_blocking)
	[erro, robotFrontLeftMotor] = sim.simxGetObjectHandle(clientID, 'joint_front_left_wheel', sim.simx_opmode_blocking)
	[erro, robotFrontRightMotor] = sim.simxGetObjectHandle(clientID, 'joint_front_right_wheel', sim.simx_opmode_blocking)

	sim.simxPauseCommunication(clientID, True)
	sim.simxSetJointTargetVelocity(clientID,robotBackLeftMotor, -5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotBackRightMotor, 5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotFrontLeftMotor, -5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotFrontRightMotor, 5, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(clientID, False)

	time.sleep(1)
	
	sim.simxPauseCommunication(clientID, True)
	sim.simxSetJointTargetVelocity(clientID,robotBackLeftMotor, 5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotBackRightMotor, -5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotFrontLeftMotor, 5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotFrontRightMotor, -5, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(clientID, False)

	time.sleep(1)


	sim.simxPauseCommunication(clientID, True)
	sim.simxSetJointTargetVelocity(clientID,robotBackLeftMotor, -5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotBackRightMotor, 5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotFrontLeftMotor, -5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotFrontRightMotor, 5, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(clientID, False)

	time.sleep(1)

	sim.simxPauseCommunication(clientID, True)
	sim.simxSetJointTargetVelocity(clientID,robotBackLeftMotor, 5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotBackRightMotor, -5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotFrontLeftMotor, 5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotFrontRightMotor, -5, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(clientID, False)

	time.sleep(1)


	sim.simxPauseCommunication(clientID, True)
	sim.simxSetJointTargetVelocity(clientID,robotBackLeftMotor, -5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotBackRightMotor, 5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotFrontLeftMotor, -5, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetVelocity(clientID,robotFrontRightMotor, 5, sim.simx_opmode_oneshot)
	sim.simxPauseCommunication(clientID, False)

	time.sleep(1)

     # Pause simulation
	sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

    # Now close the connection to V-REP:
	sim.simxAddStatusbarMessage(clientID, 'Programa pausado', sim.simx_opmode_blocking )
	sim.simxFinish(clientID)
else:
	print ('Failed connecting to remote API server')
print ('Program ended')
