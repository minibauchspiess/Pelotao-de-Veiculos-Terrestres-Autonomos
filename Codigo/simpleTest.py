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
from statistics import mean


#Informacoes dos veiculos
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

#Valores fixos
LIMIAR_DISTANCIA = 1.718624057122607

#Variaveis globais
comando = 's'
continuar = True
distancia_atual = 1.718624057122607

#Controles de tempo
ctrlStartTime = time.time()
liderStartTime = time.time()
updtAreaStartTime = time.time()
seguidorStartTime = time.time()

ctrlRespTime = []
liderRespTime = []
updtAreaRespTime = []
seguidorRespTime = []


#Tasks usadas no programa
async def ControleDePrograma():
	global continuar
	global comando
	if msvcrt.kbhit():
		comando = msvcrt.getch()
	await asyncio.sleep(0.000001)
	if ord(comando) == 113: #------------------ q (tecla para sair)
		continuar = False
	ctrlRespTime.append(time.time()-ctrlStartTime)

async def CallControleDePrograma(task, period, start):
    global ctrlStartTime
    if((time.time()-ctrlStartTime)>period)and(task.done()):
        ctrlStartTime = start
        task = asyncio.create_task(ControleDePrograma())
    else:
        await asyncio.sleep(0.000001)

async def LiderMove(lider):
	global comando
	if ord(comando) == 119: #--------------------------- w (mover para frente)
		lider.MoveFwd(5)
	await asyncio.sleep(0.000001)
	if ord(comando) == 114: #--------------------------- r (mover para trás)
		lider.MoveRev(5)
	await asyncio.sleep(0.000001)
	if ord(comando) == 115: #--------------------------- s (comando para parar)
		lider.MoveRev(0)
	liderRespTime.append(time.time()-liderStartTime)

async def CallLiderMove(task, period, start, lider):
    global liderStartTime
    if((time.time()-liderStartTime)>period)and(task.done()):
        liderStartTime = start
        task = asyncio.create_task(LiderMove(lider))
    else:
        await asyncio.sleep(0.000001)

async def UpdateArea(seguidor):
	global distancia_atual
	distancia_atual = seguidor.camera.Distance()
	updtAreaRespTime.append(time.time()-updtAreaStartTime)

async def CallUpdateArea(task, period, start, seguidor):
    global updtAreaStartTime
    if((time.time()-updtAreaStartTime)>period)and(task.done()):
        updtAreaStartTime = start
        task = asyncio.create_task(UpdateArea(seguidor))
    else:
        await asyncio.sleep(0.000001)

async def SeguidorMove(seguidor):
	global distancia_atual
	seguidor.MoveFwd(5 * (distancia_atual - LIMIAR_DISTANCIA))
	seguidorRespTime.append(time.time()-seguidorStartTime)

async def CallSeguidorMove(task, period, start, seguidor):
    global seguidorStartTime
    if((time.time()-seguidorStartTime)>period)and(task.done()):
        seguidorStartTime = start
        task = asyncio.create_task(SeguidorMove(seguidor))
    else:
        await asyncio.sleep(0.000001)


async def ExecThreads(lider, seguidor):
	taskCtrl = asyncio.create_task(ControleDePrograma())
	taskLider = asyncio.create_task(LiderMove(lider))
	taskUpdtArea = asyncio.create_task(UpdateArea(seguidor))
	taskSeguidor = asyncio.create_task(SeguidorMove(seguidor))

	while continuar:
		await CallControleDePrograma(taskCtrl, 0.1, time.time())
		await CallLiderMove(taskLider, 0.1, time.time(), lider)
		await CallUpdateArea(taskUpdtArea, 0.1, time.time(), seguidor)
		await CallSeguidorMove(taskSeguidor, 0.1, time.time(), seguidor)
		await asyncio.sleep(0.000001)




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
