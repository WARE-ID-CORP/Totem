from libcamera import controls
from picamera2 import Picamera2
import logging
from datetime import datetime
from ..Lum import Lum
import numpy as np
from time import sleep,time
import os
import subprocess
import cv2

class Camera():
    def __init__(self, camNumber, config):
        self.config = config
        self.camNumber = camNumber
        try:
            if self.camNumber == 1:
                self.camOk = self.subprocess_cmd("sudo i2cdetect -y 0 | grep UU | wc -l")[0]

            if self.camNumber == 0:
                self.camOk = self.subprocess_cmd("sudo i2cdetect -y 10 | grep UU | wc -l")[0]

            self.camOk = int(self.camOk)

            if not self.camOk:
                logging.error("CAMERA "+str(self.camNumber)+"/"+("B" if self.camNumber else "A")+" NOT DETECTED")
                self.run = False
                return

            self.picam2 = Picamera2(self.camNumber)
            print(self.picam2.sensor_resolution)
            self.preview_config = self.picam2.create_preview_configuration({"format": "YUV420","size": (self.picam2.sensor_resolution)})
            self.picam2.configure(self.preview_config)
            focusCam = self.config["scannerOptions"]["focusCam1"] if self.camNumber == 0 else self.config["scannerOptions"]["focusCam2"]

            exposureTime = 600 if self.camNumber == 0 else 1000
            self.picam2.set_controls({
                "AeEnable": False,
                "AfMode":controls.AfModeEnum.Manual,
                "ExposureTime": exposureTime,
                "AwbEnable": False,
                "AnalogueGain": 5,            
                "NoiseReductionMode": controls.draft.NoiseReductionModeEnum.Fast,
                "Saturation": 1.1,
                "LensPosition": (focusCam/100),
                "Contrast": 1.2,
                "Sharpness": 1.6,
                "Brightness":0.2
            })

            sleep(2)
            self.picam2.start()
            self.run = True
            self.listBufferImages = []
        except Exception as e:
            print("ERROR CAMERA "+str(self.camNumber)+"/"+("B" if self.camNumber else "A")+" :", e)
            self.run = False


    def subprocess_cmd(self, command):
        process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
        proc_stdout = process.communicate()[0].strip()
        return proc_stdout.decode().split('\n')

    def startCapture(self):
        cpt = 0
        timeStart = time()
        while self.run:
            cpt+=1
            buffer = self.picam2.capture_array() #"raw"
            self.metadata = self.picam2.capture_metadata()
            self.listBufferImages.append((buffer, self.metadata["Lux"]))
            #print("has capture image")
        timeSpend = time() - timeStart
        print("frames ", cpt)
        print("time spend ", timeSpend)
        print("frame rate : ", cpt/timeSpend)
        print("end capture")

    def brightness(self, img):
        lux = np.average(img[0:img.shape[0],0:img.shape[1]])
        print(lux)
        return lux

    def close(self):
        self.picam2.stop()
        self.picam2.close()


    def writeImagesCodePos(self, datacodeSentByPriority):
        cpt=0
        hostname = self.subprocess_cmd("hostname")[0][:-1]+"A"
        date = datetime.today().strftime("%d%m%Y_%H%M%S")
        for priority in datacodeSentByPriority:
            code = datacodeSentByPriority[priority]["code"]
            lux = self.listBufferImages[cpt][1]
            if lux < self.config.minLuxToSaveImg:
                logging.info("FSv4 - Camera - Lux value too min to save Image %s/%s", lux, self.config.minLuxToSaveImg)
                continue
            
            imageYuvGray = cv2.cvtColor(self.listBufferImages[cpt][0], cv2.COLOR_YUV2GRAY_NV21)
            imageGrayRgb  = cv2.cvtColor(imageYuvGray, cv2.COLOR_GRAY2RGB)
            cv2.rectangle(imageGrayRgb, (3000, 0), (5341, 4012), (0, 255, 0), 4)
            cv2.putText(imageGrayRgb, "zoneToDecode", (3000+20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 2)
            filename = os.path.join("/home/wareid/FSV4/images/","C"+code+"_"+hostname+"_"+date+".jpeg")
            cv2.imwrite(filename, imageGrayRgb, [cv2.IMWRITE_JPEG_QUALITY, 20])
            cpt+=1
        if cpt == 0:
            imageYuvGray = cv2.cvtColor(self.listBufferImages[0][0], cv2.COLOR_YUV2GRAY_NV21)
            imageGrayRgb  = cv2.cvtColor(imageYuvGray, cv2.COLOR_GRAY2RGB)
            cv2.rectangle(imageGrayRgb, (3000, 0), (5341, 4012), (0, 255, 0), 4)
            cv2.putText(imageGrayRgb, "zoneToDecode", (3000+20, 60), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 2)
            filename = os.path.join("/home/wareid/FSV4/images/","nocodelocation_"+hostname+"_"+date+".jpeg")
            cv2.imwrite(filename, imageGrayRgb, [cv2.IMWRITE_JPEG_QUALITY, 20])

    def writeImages(self, datacodeSentByPriority, dicoRails):
        cpt=0
        for priority in datacodeSentByPriority:
            x0, y0, x1, y1 = datacodeSentByPriority[priority]["x0"],datacodeSentByPriority[priority]["y0"],datacodeSentByPriority[priority]["x1"],datacodeSentByPriority[priority]["y1"]
            code = datacodeSentByPriority[priority]["code"]
            lux = self.listBufferImages[0][1]
            if lux < self.config.minLuxToSaveImg:
                logging.info("FSv4 - Camera - Lux value too min to save Image %s/%s", lux, self.config.minLuxToSaveImg)
                continue

            imageYuvGray = cv2.cvtColor(self.listBufferImages[0][0], cv2.COLOR_YUV2GRAY_NV21)
            imageGrayRgb  = cv2.cvtColor(imageYuvGray, cv2.COLOR_GRAY2RGB)
            if self.camNumber == datacodeSentByPriority[priority]["cam"]:
                cv2.rectangle(imageGrayRgb, (x0, y0), (x1, y1), (0, 255, 0), 2)
                cv2.putText(imageGrayRgb, code, (x0 + 10, y0 + 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)

            if len(dicoRails)>0:
                x0, y0, x1, y1 = dicoRails[0]["x0"],dicoRails[0]["y0"],dicoRails[0]["x1"],dicoRails[0]["y1"]
                cv2.rectangle(imageGrayRgb, (x0, y0), (x1, y1), (0, 255, 0), 2)
                cv2.putText(imageGrayRgb, "FORKUP_RAIL", (x0 + 10, y0 + 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                   
            hostname = self.subprocess_cmd("hostname")[0][:-1]
            hostname+= "A" if self.camNumber == 0 else "B"
            date = datetime.today().strftime("%d%m%Y_%H%M%S")
            filename = os.path.join("/home/wareid/FSV4/images/",code+"_"+hostname+"_"+date+".jpeg")
            cv2.imwrite(filename, imageGrayRgb, [cv2.IMWRITE_JPEG_QUALITY, 20])
            cpt+=1
        if cpt == 0:
            imageYuvGray = cv2.cvtColor(self.listBufferImages[0][0], cv2.COLOR_YUV2GRAY_NV21)
            hostname = self.subprocess_cmd("hostname")[0][:-1]
            hostname+= "A" if self.camNumber == 0 else "B"
            date = datetime.today().strftime("%d%m%Y_%H%M%S")
            filename = os.path.join("/home/wareid/FSV4/images/","nobarcodescan_"+hostname+"_"+date+".jpeg")
            cv2.imwrite(filename, imageYuvGray, [cv2.IMWRITE_JPEG_QUALITY, 20])

    def brightness(self, img):
        lux = np.average(img[0:img.shape[0],0:img.shape[1]])
        print(lux)
        return lux

    def takePicture(self):
        buffer = self.picam2.capture_array() #"raw"
        lux = self.brightness(buffer)
        #self.metadata = self.picam2.capture_metadata()
        #self.metadata["Lux"]
        self.listBufferImages.append([buffer, lux]) 

    def getPicture(self):
        return self.picam2.capture_array()
