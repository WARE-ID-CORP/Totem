from model.Lum import Lum
#from model.Rtc import Rtc
from model.processing.Decoder import Decoder
from model.processing.Sorting import Sorting
from model.camera.Camera import Camera
from model.Server import Server
from libcamera import controls
from picamera2 import Picamera2
from helpers.Conf import Conf
import os
import logging
from threading import Thread
from datetime import *
import cv2
from time import time,sleep
import subprocess
import sys

class Totem():
    def __init__(self):
        os.environ["OPENBLAS_NUM_THREADS"] = "24"

        self.path = "/home/wareid/Totem/"
        self.conf = Conf(self.path)
        self.config = self.conf.config

        self.createLogFile()

        logging.info('--------------------------------------------------------------------------')

        logging.info('Program Totem - Start : HENESSY')

        logging.info('Initialize Camera...')

        #self.ForkIsUp = False
        self.hasStartFlash = False


        self.ethHost = "192.168.1.98"
        self.ethPort = 8080

        # self.ethHost = "10.56.34.21"
        # self.ethPort = 2004
        self.run = True

        self.server = Server(self.ethHost, self.ethPort)

        self.threadEthernet = Thread(target=self.server.serverEthernet, args=[])
        self.threadEthernet.start()

        logging.info('Camera 1 Setup...')

        self.camera1 = Camera(0, self.config)

        #logging.info('Camera 2 Setup...')

        self.camera2 = Camera(1, self.config)

        #self.lum = Lum()
        #self.lum.stopFlash()
        self.sorting = Sorting(self.config, self.server)

        self.sorting.resetDicoPriority()

        self.decoder = Decoder(self.config, self.sorting)

        self.canDecode = False
        self.lum = Lum()

        # self.ethHost = "10.56.34.21"
        # self.ethPort = 2004  # The port used by the server
        


        #self.progIsReady = False

        #self.cell.readCell()

        self.timeStartFlash = time() + 10000000

        self.isReady = False

        self.hasStart = False

        self.main()

    def createLogFile(self):
        print("create new log file")
        self.currentTodayDate = str(date.today())
        log = logging.getLogger()  # root logger
        for hdlr in log.handlers[:]:  # remove all old handlers
            log.removeHandler(hdlr)
        logging.basicConfig(level=logging.INFO,
            filename=self.path+"logs/"+self.currentTodayDate+ "_HENNESSY_Totem.log",
            filemode="a",
            format='%(asctime)s - %(levelname)s - %(message)s')

    def checkNoBarcodeScanned(self, dico):
        for key in dico:
            if len(dico[key]) != 0:
                return False
        return True

    def checkIfRestart(self):
        cptTakePhoto = 0
        while True:
            if self.hasStartFlash:
                sleep(1)
                cptTakePhoto += 1
            else:
                cptTakePhoto = 0

            if cptTakePhoto > 5:
                self.lum.stopFlash()
                logging.info('Main - Flash is stayed activated 5 seconds, restart program')
                self.restart()
            sleep(0.2)

    def subprocess_cmd(self, command):
        process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        return proc_stdout.decode().split('\n')

    def restart(self):
        logging.info('Program - Restart')
        self.decoder.close_decoders()
        #os.system("sudo pkill -f 'V120c.py'")
        os.system("sudo python3 "+self.path+"restart.py")

    def checkDateConfig(self, configFile):
        command = "ls -l "+self.path+configFile+" | awk '{print $6 $7 $8}'"
        return self.subprocess_cmd(command)[0]

    def main(self):
        #self.threadCapture = Thread(target=self.camera.startCapture, args=[])
        self.codeAlreadyRead = ""
        listcodePriority1 = []
        numberOfImageCapture = 0

        timeCheckConfigFiles = time()

        timeTriggerFlash = time()
        self.dateConfig = self.checkDateConfig("Config.json")

        # if not self.cell.cellIsOk():
        #     logging.info('------------- /!\ ERROR CELLULE HS /!\ ------------------------------')
        #     return
        logging.info('Main - System READY')
        lastDistance = 0
        while self.run:
            if self.server.isReady and not self.hasStart:
                self.hasStart = True
                self.lum.progStart()

            if self.server.isReady and self.server.triggered and not self.hasStartFlash:
                self.server.totemIsReady = False
                self.hasStartFlash = True
                self.lum.startFlash()
                sleep(0.4)
                timeTriggerFlash = time()

            if time() - timeCheckConfigFiles > 10:
                if self.currentTodayDate != str(date.today()):
                    self.createLogFile()
                timeCheckConfigFiles = time()
                dateConfig = self.checkDateConfig("Config.json")
                if dateConfig != self.dateConfig:
                    logging.info('Config.json has changed')
                    self.restart()
                #self.rtc.update_time()

            # if not self.progIsReady:
            #     self.lum.progStart()
            #     self.progIsReady = True

            # if not self.hasStartFlash:
            #     self.lum.startFlash()
            #     sleep(0.4)
            #     self.hasStartFlash = True
            #     logging.info('Main - Start Flash')
            #     self.timeStartFlash = time()

            if self.hasStartFlash:
                logging.info("Main - Try Capture Image...")
                self.camera1.takePicture()
                self.camera2.takePicture()
                numberOfImageCapture+=2
                logging.info('Main - Capture Picture '+str(numberOfImageCapture))
                sleep(self.config["scannerOptions"]["delayBetweenImages"])

            if numberOfImageCapture > (self.config["scannerOptions"]["numberPhotos"]*2-1):
                sleep(0.4)
                self.lum.stopFlash()
                numberOfImageCapture = 0
                self.hasStartFlash = False
                timeTriggerFlash = time()
                logging.info("Main - Stop Flash/Stop Capture")

                #self.lum.stopFlash()

                processTime = time()

                #modePlot = self.config.codePosEnable
                
                self.decoder.launchThreadsDecoderCM5(self.camera1.listBufferImages, "cam1")

                self.decoder.launchThreadsDecoderCM5(self.camera2.listBufferImages, "cam2")

                temperatures = self.subprocess_cmd("sensors | grep ° | awk '{print $2}'")
                logging.info('V120c - Temperature - cpu_thermal-virtual-0 - '+temperatures[0])
                logging.info('V120c - Temperature - rp1_adc-isa-0000 - '+temperatures[1])

                decodeTime = round((time() - processTime), 2)
                logging.info('Totem - Time to decode: %s', decodeTime)
                
                logging.info('Totem - CAM1 - datacodes decoded: %s', self.decoder.listBarcodesCam1)
                logging.info('Totem - CAM2 - datacodes decoded: %s', self.decoder.listBarcodesCam2)

                self.sorting.filterSendCodeByPriority()

                for i in range(len(self.camera1.listBufferImages)):
                    imageYuvGray = cv2.cvtColor(self.camera1.listBufferImages[i][0], cv2.COLOR_YUV2GRAY_NV21)
                    hostname = self.subprocess_cmd("hostname")[0]
                    datePhoto = datetime.today().strftime("%d%m%Y_%H%M%S")
                    filename = os.path.join("/home/wareid/Totem/images/","CAM1_"+str(i)+"_"+hostname+"_"+datePhoto+".jpeg")
                    cv2.imwrite(filename, imageYuvGray, [cv2.IMWRITE_JPEG_QUALITY, 20])

                for i in range(len(self.camera2.listBufferImages)):
                    imageYuvGray = cv2.cvtColor(self.camera2.listBufferImages[i][0], cv2.COLOR_YUV2GRAY_NV21)
                    hostname = self.subprocess_cmd("hostname")[0]
                    datePhoto = datetime.today().strftime("%d%m%Y_%H%M%S")
                    filename = os.path.join("/home/wareid/Totem/images/","CAM2_"+str(i)+hostname+"_"+datePhoto+".jpeg")
                    cv2.imwrite(filename, imageYuvGray, [cv2.IMWRITE_JPEG_QUALITY, 20])

                self.camera1.listBufferImages.clear()
                self.camera2.listBufferImages.clear()

                self.server.totemIsReady = True
                self.server.triggered = False
            
    def writeImageAndLogs(self, yuvImage, lux, listBarcode, codeToSend, codeReal, numberCharToSend, dicoInfos, decodeTime):
        nameImage = ""

        if numberCharToSend != -1:
            codeToSend = codeToSend[:numberCharToSend]

        if codeToSend != self.codeAlreadyRead:
            self.xbee.sendData(codeToSend)
            nameImage = codeToSend
            if self.config.AlreadyRead:
                self.codeAlreadyRead = codeToSend
        else:
            nameImage = "alreadyRead"
            self.xbee.sendData("alread")
            logging.info('V120i - Image - Already Read')

        logging.info('V120i - Image - codeposi - Y: %s', dicoInfos[codeReal]["centery"])
        logging.info('V120i - Image - codeposi - X: %s', dicoInfos[codeReal]["centerx"])
        logging.info('V120i - Image - codelength: %s', dicoInfos[codeReal]["length"])
        logging.info('V120i - Image - codeheight: %s', dicoInfos[codeReal]["height"])
        logging.info('V120i - Image - timedecode: %s', dicoInfos[codeReal]["decode_time"])

        #imgToDecode = self.decoder.draw_circle_test(imgToDecode, (dicoInfos[code]["centerx"], dicoInfos[code]["centery"]))
        datejpeg = datetime.datetime.today().strftime("%d%m%Y_%H%M%S")

        for i in range(len(self.camera.listBufferImages)):
            logging.info('V120i - Image '+str(i)+' - lux: %s - FocusFoM: %s', self.camera.listBufferImages[i][1], self.config.focusCAM)
            imgToDecode = self.decoder.convert_yuv_gray(self.camera.listBufferImages[i][0])
            cv2.imwrite("/home/wareid/V120i/images/"+str(i)+"_"+str(nameImage)+"_"+self.config.freescanName+"_"+str(datejpeg)+".jpeg", imgToDecode, [int(cv2.IMWRITE_JPEG_QUALITY), 20])

        self.camera.listBufferImages.clear()
totem = Totem()
