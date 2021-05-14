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
import matplotlib.pyplot as plt


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
P = 10	#Proporcional do controle de velocidade do seguidor
PERIODO_CONTROL = 0.8
PERIODO_LIDER = 0.7
PERIODO_CAP_IMAGE = 0.6
PERIODO_READ_IMAGE = 0.6
PERIODO_GET_DIST = 0.6
PERIODO_SEGUIDOR = 0.6

TEMPO_READ_IMG = 0.03

#Variaveis globais
comando = 's'
continuar = True
distancia_atual = 1.718624057122607
pureImg = 0
res = 0
cvImg = 0

#Controles de tempo
ctrlStartTime = time.time()
ctrlSimStartTime = 0
liderStartTime = time.time()
liderSimStartTime = 0
captImgStartTime = time.time()
captImgSimStartTime = 0
readImgStartTime = time.time()
readImgSimStartTime = 0
getDistStartTime = time.time()
getDistSimStartTime = 0
seguidorStartTime = time.time()
seguidorSimStartTime = 0

ctrlRespTime = []
liderRespTime = []
captImgRespTime = []
readImgRespTime = []
getDistRespTime = []
seguidorRespTime = []


#Tasks usadas no programa
async def ControleDePrograma():
	global continuar
	global comando
	#print("Entrei no controle")
	if msvcrt.kbhit():
		comando = msvcrt.getch()
	await asyncio.sleep(0.000001)
	if ord(comando) == 113: #------------------ q (tecla para sair)
		continuar = False
	ctrlRespTime.append(time.time()-ctrlStartTime)

async def CallControleDePrograma(task, period, start, startSim):
	global ctrlStartTime
	global ctrlSimStartTime
	#simTimeNow = time.time()	#Mudar esse time.time() pra forma de pegar o tempo da simulacao
	if((startSim-ctrlSimStartTime)>period)and(task.done()):
		ctrlStartTime = start
		ctrlSimStartTime = startSim
		task = asyncio.create_task(ControleDePrograma())
	else:
		await asyncio.sleep(0.000001)


async def LiderMove(lider):
	global comando
	#print("Entrei no lider")
	if ord(comando) == 119: #--------------------------- w (mover para frente)
		lider.MoveFwd(5)
	await asyncio.sleep(0.000001)
	if ord(comando) == 114: #--------------------------- r (mover para trás)
		lider.MoveRev(5)
	await asyncio.sleep(0.000001)
	if ord(comando) == 115: #--------------------------- s (comando para parar)
		lider.MoveRev(0)
	liderRespTime.append(time.time()-liderStartTime)

async def CallLiderMove(task, period, start, startSim, lider):
	global liderStartTime
	global liderSimStartTime
	if((startSim-liderSimStartTime)>period)and(task.done()):
		liderStartTime = start
		liderSimStartTime = startSim
		task = asyncio.create_task(LiderMove(lider))
	else:
		await asyncio.sleep(0.000001)


async def CapturaImagem(seguidor):
	global imagemPura
	global res
	#print("Entrei na captura")
	[pureImg, res] = seguidor.camera.CaptureImage(30)
	captImgRespTime.append(time.time()-captImgStartTime)

async def CallCapturaImagem(task, period, start, startSim, seguidor):
	global captImgStartTime
	global captImgSimStartTime
	if((startSim-captImgSimStartTime)>period)and(task.done()):
		captImgStartTime = start
		captImgSimStartTime = startSim
		task = asyncio.create_task(CapturaImagem(seguidor))
	else:
		await asyncio.sleep(0.000001)


async def ReadImg(seguidor):
	global pureImg
	global res
	#print("Entrei no read")
	cvImg = seguidor.camera.ReadImage(pureImg, res, TEMPO_READ_IMG)
	readImgRespTime.append(time.time()-readImgStartTime)

async def CallReadImg(task, period, start, startSim, seguidor):
	global readImgStartTime
	global readImgSimStartTime
	if((startSim-readImgSimStartTime)>period)and(task.done()):
		readImgStartTime = start
		readImgSimStartTime = startSim
		task = asyncio.create_task(ReadImg(seguidor))
	else:
		await asyncio.sleep(0.000001)


async def GetDistance(seguidor):
	global cvImg
	global distancia_atual
	#print("Entrei no get distance")

	distancia_atual = seguidor.camera.Distance()
	getDistRespTime.append(time.time()-getDistStartTime)

async def CallGetDistance(task, period, start, startSim, seguidor):
	global getDistStartTime
	global getDistSimStartTime
	if((startSim-getDistSimStartTime)>period)and(task.done()):
		getDistStartTime = start
		getDistSimStartTime = startSim
		task = asyncio.create_task(GetDistance(seguidor))
	else:
		await asyncio.sleep(0.000001)


'''
async def UpdateArea(seguidor):
	global distancia_atual
	distancia_atual = seguidor.camera.Distance()
	updtAreaRespTime.append(time.time()-updtAreaStartTime)

async def CallUpdateArea(task, period, start, startSim, seguidor):
	global updtAreaStartTime
	global updtAreaSimStartTime
	#simTimeNow = time.time()	#Mudar esse time.time() pra forma de pegar o tempo da simulacao
	if((startSim-updtAreaSimStartTime)>period)and(task.done()):
		updtAreaStartTime = start
		updtAreaSimStartTime = startSim
		task = asyncio.create_task(UpdateArea(seguidor))
	else:
		await asyncio.sleep(0.000001)
'''

async def SeguidorMove(seguidor):
	global distancia_atual
	#print("Entrei no seguidor")
	seguidor.MoveFwd(P * (distancia_atual - LIMIAR_DISTANCIA))
	seguidorRespTime.append(time.time()-seguidorStartTime)

async def CallSeguidorMove(task, period, start, startSim, seguidor):
	global seguidorStartTime
	global seguidorSimStartTime
	#simTimeNow = time.time()	#Mudar esse time.time() pra forma de pegar o tempo da simulacao
	if((startSim-seguidorSimStartTime)>period)and(task.done()):
		seguidorStartTime = start
		seguidorSimStartTime = startSim
		task = asyncio.create_task(SeguidorMove(seguidor))
	else:
		await asyncio.sleep(0.000001)


async def ExecThreads(lider, seguidor):
	taskCtrl = asyncio.create_task(ControleDePrograma())
	taskLider = asyncio.create_task(LiderMove(lider))
	#taskcaptImg = asyncio.create_task(CapturaImagem(seguidor))
	#await asyncio.sleep(4)
	#taskReadImg = asyncio.create_task(ReadImg(seguidor))
	#await asyncio.sleep(4)
	taskGetDist = asyncio.create_task(GetDistance(seguidor))
	#await asyncio.sleep(4)
	#taskUpdtArea = asyncio.create_task(UpdateArea(seguidor))
	taskSeguidor = asyncio.create_task(SeguidorMove(seguidor))
	await asyncio.sleep(0.000001)

	while continuar:
		sim.simxAddStatusbarMessage(clientID,'pegando T',sim.simx_opmode_oneshot_wait)
		simTime = sim.simxGetLastCmdTime(clientID)/100
		await CallControleDePrograma(taskCtrl, 0.1, time.time(), simTime)

		sim.simxAddStatusbarMessage(clientID,'pegando T',sim.simx_opmode_oneshot_wait)
		simTime = sim.simxGetLastCmdTime(clientID)/100
		await CallLiderMove(taskLider, 0.1, time.time(), simTime, lider)

		#sim.simxAddStatusbarMessage(clientID,'pegando T',sim.simx_opmode_oneshot_wait)
		#simTime = sim.simxGetLastCmdTime(clientID)/100
		#await CallCapturaImagem(taskcaptImg, PERIODO_CAP_IMAGE, time.time(), simTime, seguidor)

		#sim.simxAddStatusbarMessage(clientID,'pegando T',sim.simx_opmode_oneshot_wait)
		#simTime = sim.simxGetLastCmdTime(clientID)/100
		#await CallReadImg(taskReadImg, PERIODO_READ_IMAGE, time.time(), simTime, seguidor)

		sim.simxAddStatusbarMessage(clientID,'pegando T',sim.simx_opmode_oneshot_wait)
		simTime = sim.simxGetLastCmdTime(clientID)/100
		await CallGetDistance(taskGetDist, PERIODO_GET_DIST, time.time(), simTime, seguidor)

		#await CallUpdateArea(taskUpdtArea, 0.1, time.time(), simTime, seguidor)
		sim.simxAddStatusbarMessage(clientID,'pegando T',sim.simx_opmode_oneshot_wait)
		simTime = sim.simxGetLastCmdTime(clientID)/100
		await CallSeguidorMove(taskSeguidor, 0.1, time.time(), simTime, seguidor)

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
	plt.hist(ctrlRespTime)
	print(ctrlRespTime)


    # Pause simulation
	sim.simxPauseSimulation(clientID,sim.simx_opmode_oneshot_wait)

    # Now close the connection to V-REP:
	sim.simxAddStatusbarMessage(clientID, 'Programa pausado', sim.simx_opmode_blocking )
	sim.simxFinish(clientID)
else:
	print ('Failed connecting to remote API server')
print ('Program ended')
