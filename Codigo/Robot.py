import sim
from Camera import Camera
import asyncio

class Robot:
    def __init__(self, clientID, robot_name, wheel_bl_name, wheel_br_name, wheel_fl_name, wheel_fr_name, cam_name):

        self.clientID = clientID
        #Handles
        #Robo
        erro, self.robot_hand = sim.simxGetObjectHandle(self.clientID, robot_name, sim.simx_opmode_blocking)
        #Motores
        [erro, self.wheel_bl_hand] = sim.simxGetObjectHandle(self.clientID, wheel_bl_name, sim.simx_opmode_blocking)
        [erro, self.wheel_br_hand] = sim.simxGetObjectHandle(self.clientID, wheel_br_name, sim.simx_opmode_blocking)
        [erro, self.wheel_fl_hand] = sim.simxGetObjectHandle(self.clientID, wheel_fl_name, sim.simx_opmode_blocking)
        [erro, self.wheel_fr_hand] = sim.simxGetObjectHandle(self.clientID, wheel_fr_name, sim.simx_opmode_blocking)
        #Sensores
        self.camera = Camera(self.clientID, cam_name)
        

    #Funcao para andar para a frente, com velocidade v
    def MoveFwd(self, v):
        sim.simxPauseCommunication(self.clientID, True)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_bl_hand, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_br_hand, -v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_fl_hand, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_fr_hand, -v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(self.clientID, False)
    
    #Funcao para andar para tras, com velocidade v
    def MoveRev(self, v):
        sim.simxPauseCommunication(self.clientID, True)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_bl_hand, -v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_br_hand, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_fl_hand, -v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_fr_hand, v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(self.clientID, False)

    #Funcao para andar girando para a esquerda
    #Velocidade das rodas da direita ficam em v, da esquerda ficam em turnCoef*v, sendo 0<=turnCoef<1
    def MoveLeft(self, v, turnCoef):
        sim.simxPauseCommunication(self.clientID, True)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_bl_hand, turnCoef*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_br_hand, -v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_fl_hand, turnCoef*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_fr_hand, -v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(self.clientID, False)
    
    #Funcao para andar girando para a direita
    #Velocidade das rodas da esquerda ficam em v, da direita ficam em turnCoef*v, sendo 0<=turnCoef<1
    def MoveRight(self, v, turnCoef):
        sim.simxPauseCommunication(self.clientID, True)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_bl_hand, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_br_hand, -turnCoef*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_fl_hand, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.wheel_fr_hand, -turnCoef*v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(self.clientID, False)
