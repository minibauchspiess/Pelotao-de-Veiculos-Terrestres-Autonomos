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

from sim import simxGetInMessageInfo, simxSetVisionSensorImage
import time
from Robot import Robot
import numpy as np
import cv2
import asyncio
import msvcrt
import numpy



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

LIMIAR_DISTANCIA = 1.718624057122607

comando = 's'
comando_lock = asyncio.Lock()

continuar = True
cont_lock = asyncio.Lock()

distancia_atual = 1.718624057122607
distancia_lock = asyncio.Lock()


#Tasks usadas no programa
async def ControleDePrograma():
	global continuar
	global comando

	print("Pressione enter para finalizar o programa")

	done = False
	while(not done):
		if msvcrt.kbhit():
			async with comando_lock:
				comando = msvcrt.getch()
			if ord(comando) == 113: #------------------ q (tecla para sair)
				done = True
		await asyncio.sleep(0.2)
	

	async with cont_lock:
		continuar = False

async def LiderMove(lider):
	global continuar
	async with cont_lock:
		cond = continuar
	while (cond):
		await asyncio.sleep(0.1)
		async with comando_lock:
			com = comando

		if ord(com) == 119: #--------------------------- w (mover para frente)
			lider.MoveFwd(5)
			await asyncio.sleep(0.1)
		if ord(com) == 114: #--------------------------- r (mover para trás)
			lider.MoveRev(5)
			await asyncio.sleep(0.1)
		if ord(com) == 115: #--------------------------- s (comando para parar)
			lider.MoveRev(0)
			await asyncio.sleep(0.5)
		async with cont_lock:
			cond = continuar

async def UpdateArea(seguidor):
	global continuar
	global distancia_atual

	async with cont_lock:
		cond = continuar
	while(cond):
		async with distancia_lock:
			distancia_atual = seguidor.camera.Distance()
			
		await asyncio.sleep(0.03)
		async with cont_lock:
			cond = continuar


async def SeguidorMove(seguidor):
	global continuar
	global distancia_atual

	async with cont_lock:
		cond = continuar

	while(cond):
		async with distancia_lock:
			distancia = distancia_atual
		
		seguidor.MoveFwd(5 * (distancia - LIMIAR_DISTANCIA))
		print("dif distancia: ", round(distancia, 4))
		
		await asyncio.sleep(0.5)

		async with cont_lock:
			cond = continuar

async def ExecThreads(lider, seguidor):
	await asyncio.gather(ControleDePrograma(), LiderMove(lider), UpdateArea(seguidor), SeguidorMove(seguidor))
	
	while(True):
		await asyncio.sleep(1)



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
