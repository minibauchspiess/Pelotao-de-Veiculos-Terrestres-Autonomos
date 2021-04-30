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
import asyncio
import msvcrt



SEGUIDOR = 'Seguidor'
SEG_WHEEL_BL = 'seg_bl_wheel'
SEG_WHEEL_BR = 'seg_br_wheel'
SEG_WHEEL_FL = 'seg_fl_wheel'
SEG_WHEEL_FR = 'seg_fr_wheel'
SEG_CAMERA = 'cam'

LIDER = 'Lider'
LID_WHEEL_BL = 'lid_bl_wheel'
LID_WHEEL_BR = 'lid_br_wheel'
LID_WHEEL_FL = 'lid_fl_wheel'
LID_WHEEL_FR = 'lid_fr_wheel'

LIMIAR_AREA = 2


continuar = True
cont_lock = asyncio.Lock()

area_atual = 3
area_lock = asyncio.Lock()


#Tasks usadas no programa
async def ControleDePrograma():
	global continuar

	print("Pressione enter para finalizar o programa")

	done = False
	while(not done):
		if msvcrt.kbhit():
			done = True
		await asyncio.sleep(0.2)
	

	async with cont_lock:
		continuar = False

async def LiderMove(lider):
	global continuar
	async with cont_lock:
		cond = continuar
	while (cond):
		lider.MoveFwd(10)
		await asyncio.sleep(2)
		lider.MoveRev(10)
		await asyncio.sleep(2)

		async with cont_lock:
			cond = continuar

async def UpdateArea(seguidor):
	global continuar
	global area_atual

	async with cont_lock:
		cond = continuar
	while(cond):
		async with area_lock:
			area_atual = seguidor.camera.AreaSize()
			print(area_atual)
		await asyncio.sleep(0.5)
		async with cont_lock:
			cond = continuar


async def SeguidorMove(seguidor):
	global continuar
	global area_atual

	async with cont_lock:
		cond = continuar

	while(cond):
		async with area_lock:
			area = area_atual
		
		if(area<LIMIAR_AREA):
			seguidor.MoveFwd(10)
		else:
			seguidor.MoveRev(10)
		
		await asyncio.sleep(0.5)

		async with cont_lock:
			cond = continuar

async def ExecThreads(lider, seguidor):
	await asyncio.gather(ControleDePrograma(), LiderMove(lider), UpdateArea(seguidor), SeguidorMove(seguidor))



print ('Program started')
sim.simxFinish(-1) # just in case, close all opened connections
clientID=sim.simxStart('127.0.0.1',19999,True,True,5000,5) # Connect to CoppeliaSim
if clientID!=-1:

	sim.simxStartSimulation(clientID, sim.simx_opmode_oneshot_wait)
	print ('Connected to remote API server')
	sim.simxAddStatusbarMessage(clientID,'Funcionando...',sim.simx_opmode_oneshot_wait)
	time.sleep(0.02)


	seguidor = Robot(clientID, SEGUIDOR, SEG_WHEEL_BL, SEG_WHEEL_BR, SEG_WHEEL_FL, SEG_WHEEL_FR, SEG_CAMERA)
	lider = Robot(clientID, LIDER, LID_WHEEL_BL, LID_WHEEL_BR, LID_WHEEL_FL, LID_WHEEL_FR)


	asyncio.run(ExecThreads(lider, seguidor))


    # Pause simulation
	sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

    # Now close the connection to V-REP:
	sim.simxAddStatusbarMessage(clientID, 'Programa pausado', sim.simx_opmode_blocking )
	sim.simxFinish(clientID)
else:
	print ('Failed connecting to remote API server')
print ('Program ended')
