import sim

class Robot:
    def __init__(self, clientID, robot_name, wheel_bl_name, wheel_br_name, wheel_fl_name, wheel_fr_name):

        self.clientID = clientID
        #Handles
        #Robo
        erro, self.robot = sim.simxGetObjectHandle(self.clientID, robot_name, sim.simx_opmode_blocking)
        #Motores
        [erro, self.robotBackLeftMotor] = sim.simxGetObjectHandle(self.clientID, wheel_bl_name, sim.simx_opmode_blocking)
        [erro, self.robotBackRightMotor] = sim.simxGetObjectHandle(self.clientID, wheel_br_name, sim.simx_opmode_blocking)
        [erro, self.robotFrontLeftMotor] = sim.simxGetObjectHandle(self.clientID, wheel_fl_name, sim.simx_opmode_blocking)
        [erro, self.robotFrontRightMotor] = sim.simxGetObjectHandle(self.clientID, wheel_fr_name, sim.simx_opmode_blocking)
        #Sensores
        

    #Funcao para andar para a frente, com velocidade v
    def MoveFwd(self, v):
        sim.simxPauseCommunication(self.clientID, True)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotBackLeftMotor, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotBackRightMotor, -v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotFrontLeftMotor, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotFrontRightMotor, -v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(self.clientID, False)
    
    #Funcao para andar para tras, com velocidade v
    def MoveRev(self, v):
        sim.simxPauseCommunication(self.clientID, True)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotBackLeftMotor, -v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotBackRightMotor, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotFrontLeftMotor, -v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotFrontRightMotor, v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(self.clientID, False)

    #Funcao para andar girando para a esquerda
    #Velocidade das rodas da direita ficam em v, da esquerda ficam em turnCoef*v, sendo 0<=turnCoef<1
    def MoveLeft(self, v, turnCoef):
        sim.simxPauseCommunication(self.clientID, True)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotBackLeftMotor, turnCoef*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotBackRightMotor, -v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotFrontLeftMotor, turnCoef*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotFrontRightMotor, -v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(self.clientID, False)
    
    #Funcao para andar girando para a direita
    #Velocidade das rodas da esquerda ficam em v, da direita ficam em turnCoef*v, sendo 0<=turnCoef<1
    def MoveRight(self, v, turnCoef):
        sim.simxPauseCommunication(self.clientID, True)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotBackLeftMotor, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotBackRightMotor, -turnCoef*v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotFrontLeftMotor, v, sim.simx_opmode_oneshot)
        sim.simxSetJointTargetVelocity(self.clientID,self.robotFrontRightMotor, -turnCoef*v, sim.simx_opmode_oneshot)
        sim.simxPauseCommunication(self.clientID, False)
