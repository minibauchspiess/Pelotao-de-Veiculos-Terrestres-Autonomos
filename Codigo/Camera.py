import sim
import time
import numpy as np
import numpy
import cv2
import asyncio

class Camera:
    def __init__(self, clientID, cam_name):
        self.clientID = clientID

        erro, self.camera_hand = sim.simxGetObjectHandle(clientID, cam_name, sim.simx_opmode_oneshot_wait)
        # Start the Stream
        erro, res, image = sim.simxGetVisionSensorImage(clientID, self.camera_hand, 0, sim.simx_opmode_streaming)

    def GetImage(self):
        errol = 1

        while(errol != sim.simx_return_ok):
            errol, res, image = sim.simxGetVisionSensorImage(self.clientID, self.camera_hand, 0, sim.simx_opmode_buffer)
            time.sleep(0.005)
        nres = [res[0]-int(res[0]/3),res[1]]
        img = np.array(image, dtype=np.uint8)		# Como é recebido uma string, precisa reformatar
        img = np.reshape(img, (res[0], res[1], 3))	# Pro CV2, (y, x, [B,R,G])
        img = np.flip(img, 0)						# Por algum motivo vem de ponta cabeça
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)	# Transforma o RGB recebido em BGR pro CV2
        img = img[0:res[0]-(int(res[0]/3)), 0:res[1]]

        return img

    def ShowInWindow(self, img, winName='image'):
        cv2.namedWindow(winName, cv2.WINDOW_NORMAL)
        cv2.imshow(winName,img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    #AreaSize retorna a area (ou um valor relacionado) do quadrado visto na imagem    
    def AreaSize(self):

        img = self.GetImage()
        
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        lowerRed = numpy.array([120, 200, 190])
        upRed = numpy.array([150, 220, 210])

        mask = cv2.inRange(lab, lowerRed, upRed)
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cnt = contours[0]
        m = cv2.moments(cnt)
        cx = int(m['m10']/m['m00'])
        cy = int(m['m01']/m['m00'])
        area= cv2.contourArea(cnt)
        
        return area

