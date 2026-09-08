import traceback
import re
import configparser
import logging
from time import sleep
import cv2
import os
from datetime import datetime
import subprocess

class Sorting():
    def __init__(self, config):
        self.config = config
        self.dicoPriority = { "cam1": {}, "cam2": {} }
        self.dicoInfoCodeSent = {}
        self.alreadyRead = ""
        self.dicoReject = {}

    def resetDicoPriority(self):
        self.dicoPriority = { "cam1": {}, "cam2": {} }
        for priority in self.config["codeFiltersPriority"]:
            self.dicoPriority["cam1"][priority] = []
            self.dicoPriority["cam2"][priority] = []
        
        self.dicoReject = { "cam1": {}, "cam2": {} }
        for priority in self.config["codeFiltersPriority"]:
            self.dicoReject["cam1"][priority] = {}
            self.dicoReject["cam2"][priority] = {}

    def transformFormatToRegex(self, formatCodePos):
        regex = "^"
        cpt=0
        for char in formatCodePos:
            if char == "X":
                cpt+=1
            else:
                regex+="[a-zA-Z0-9]{"+str(cpt)+"}"
                cpt=0
                regex+=char
        if cpt>0:
            regex+="[a-zA-Z0-9]{"+str(cpt)+"}$"
        return regex



    def regexMatchDatacode(self, barcode, listRegex, start):
            for regex in listRegex:
                if regex == "ALL":
                    return True
                if start:
                    regex = "^"+regex+".*"
                else:
                    regex = ".*"+regex+"$"
                if re.search(regex, barcode) != None:
                    return True
            return False

    def rejectBarcodeStartSame(self, barcode, sizeReject, dicoProrityCam):
        for dicoCode in dicoProrityCam:
            if sizeReject <= len(dicoCode["code"]) and dicoCode["code"][:sizeReject] == barcode:
                return True
        return False

    def checkIfbarcodeIsValid(self, barcode, centery, decode_time, height, length, numberImage, nameCam, coords):
        dicoCode = self.config["codeFiltersPriority"] 
        for priority in dicoCode:
            listRegexStart = dicoCode[priority]["dataCodeStartByChar"].split(",")
            if not self.regexMatchDatacode(barcode, listRegexStart, True):
                if "startChar" not in self.dicoReject[nameCam][priority]:
                    self.dicoReject[nameCam][priority]["startChar"] = [barcode]
                elif barcode not in self.dicoReject[nameCam][priority]["startChar"]:
                    self.dicoReject[nameCam][priority]["startChar"].append(barcode)
                continue
            
            if int(dicoCode[priority]["minimumLengthOfDataCodeInCm"]) != -1 and (height/length) < 0.7 and length < (int(dicoCode[priority]["minimumLengthOfDataCodeInCm"]) * 40):
                if "rejectSizeLength" not in self.dicoReject[nameCam][priority]:
                    self.dicoReject[nameCam][priority]["rejectSizeLength"] = [(barcode, length)]
                elif (barcode, length) not in self.dicoReject[nameCam][priority]["rejectSizeLength"]:
                    self.dicoReject[nameCam][priority]["rejectSizeLength"].append((barcode, length))
                continue

            if len(barcode) != int(dicoCode[priority]["numberCharOfDataCode"]) and int(dicoCode[priority]["numberCharOfDataCode"]) != -1:
                if "rejectNumberChar" not in self.dicoReject[nameCam][priority]:
                    self.dicoReject[nameCam][priority]["rejectNumberChar"] = [(barcode, len(barcode))]
                elif (barcode, len(barcode)) not in self.dicoReject[nameCam][priority]["rejectNumberChar"]:
                    self.dicoReject[nameCam][priority]["rejectNumberChar"].append((barcode, len(barcode)))
                continue

            sizeToRejectSameBarcode = int(dicoCode[priority]["sizeToRejectSameBarcode"])
            if sizeToRejectSameBarcode != -1 and priority in self.dicoPriority and self.rejectBarcodeStartSame(barcode[:sizeToRejectSameBarcode], sizeToRejectSameBarcode, self.dicoPriority[priority]):
                if "sizeToRejectSameBarcode" not in self.dicoReject[nameCam][priority]:
                    self.dicoReject[nameCam][priority]["sizeToRejectSameBarcode"] = [barcode]
                elif barcode not in self.dicoReject[nameCam][priority]["sizeToRejectSameBarcode"]:
                    self.dicoReject[nameCam][priority]["sizeToRejectSameBarcode"].append(barcode)
                continue

            self.dicoPriority[nameCam][priority].append({"code": barcode, "decode_time": decode_time, "centery": centery, "numberImage": numberImage, "x0": coords[0], "x1": coords[1],
            "y0": coords[2], "y1": coords[3]})

    def filterSendCodeByPriority(self):
        self.dicoInfoCodeSent = {}
        self.hasSentAlreadyRead = False

        orderDownToUp = None
        if self.config["scannerOptions"]["codeDirection"] == "DOWN":
            orderDownToUp=False

        if self.config["scannerOptions"]["codeDirection"] == "UP":
            orderDownToUp=True

        if orderDownToUp is not None:
            for cam in self.dicoPriority:
                for priority in self.dicoPriority[cam]:
                    self.dicoPriority[cam][priority] = sorted(self.dicoPriority[cam][priority], key=lambda item: item['centery'], reverse=orderDownToUp)
        
            logging.info('Fsv4 - Sorting - ' + str(self.dicoPriority))

            numberCodeToSend = int(self.config["scannerOptions"]["numberCodeToSend"])

            datacodeSentByPriority = {}
            for priority in self.config["codeFiltersPriority"]:
                datacodeSentByPriority[priority] = []

            if orderDownToUp:
                listCam = ["cam1", "cam2"]
            else:
                listCam = ["cam2", "cam1"]

            datacodeSent = 0
            for priority in self.config["codeFiltersPriority"]:
                for cam in listCam:
                    for codepriority in self.dicoPriority[cam][priority]:
                        datacode = codepriority["code"]
                        if datacode not in datacodeSentByPriority[priority]:
                            logging.info('Fsv4 - Sorting - Eth Automate - Send code '+datacode+' Priority '+priority)
                            numberCharToSend = self.config["codeFiltersPriority"][priority]["numberCharToSend"]
                            if datacodeSent == 0:
                                if self.config["scannerOptions"]["alreadyRead"] == 1 and datacode == self.alreadyRead:
                                    logging.info('Fsv4 - Sorting - Eth Automate - Already read code '+datacode)
                                    # self.xbee.nbCodeScanned+=1
                                    # self.xbee.sendData("alread")
                                    self.alreadyRead = ""
                                    self.hasSentAlreadyRead = True
                                    return
                                self.alreadyRead = datacode
                            #self.xbee.nbCodeScanned+=1
                            #self.xbee.sendData(datacode[:numberCharToSend])
                            if numberCodeToSend > 1:
                                sleep(self.config["scannerOptions"]["time2code"])
                            datacodeSent += 1
                            if priority not in self.dicoInfoCodeSent:
                                self.dicoInfoCodeSent[priority] = codepriority
                            datacodeSentByPriority[priority].append(datacode)
                        if datacodeSent >= numberCodeToSend:
                            return
                    
                    #code priority seen, so stop (pass to next code priority only if current code priority not detected)
                    if len(datacodeSentByPriority[priority]) > 0:
                        break
        else:
            logging.error('Fsv4 - Sorting - Error Config Code Direction')

        # if datacodeSent == 0:
        #     self.xbee.sendData("noscan")