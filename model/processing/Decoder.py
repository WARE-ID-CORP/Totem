import os
import time
import traceback
from threading import Thread
from .PhenixTest import *
#import PhenixTest
import cv2
import numpy as np
from datetime import datetime
import threading
import subprocess

class Decoder():
    def __init__(self, config, sorting):
        self.config = config
        #2 cameras
        num_decoders = self.config["scannerOptions"]["numberPhotos"] * 2 
        self.sorting = sorting
        ## Lot mode ##
        self.slice_params_2 = [(5010, 6680)]
        
        self.decoders = []

        self.listBarcodesCam1 = []
        self.listBarcodesCam2 = []

        #initialize decoders
        for _ in range(num_decoders):
            try:
                decoder, decMgr = DecoderInitialization()
                self.decoders.append((decoder, decMgr))
            except Exception as e:
                print(f"Error initializing decoder: {e}")

        #Fork mode Down by default
        self.setDecoder(False)
        
    def setDecoder(self, isForkUp):
        self.decoders_config(self.config["scannerOptions"]["orientation"], self.config["symbology"]["qrcode"], self.config["symbology"]["code128"],
        self.config["symbology"]["code39"], self.config["symbology"]["datamatrix"])


    def close_decoders(self):
        for decoder, decMgr in self.decoders:
            decMgr.destroyDecoder(decoder)

    def decoders_config(self, orientation, qrcode, c128, c39, datamatrix):
        for decoder in self.decoders :
            decoder[0].WriteIntSetting(fnxSettingTag.FNX_PROCESSING_1D_ORIENTATION, orientation)
            decoder[0].WriteIntSetting(fnxSettingTag.FNX_QR_CODE_ENABLE, qrcode)
            decoder[0].WriteIntSetting(fnxSettingTag.FNX_CODE128_ENABLE, c128)
            decoder[0].WriteIntSetting(fnxSettingTag.FNX_GS1_128_ENABLE, c128)
            decoder[0].WriteIntSetting(fnxSettingTag.FNX_CODE128_NANO_SCAN,c128)
            decoder[0].WriteIntSetting(fnxSettingTag.FNX_CODE39_ENABLE, c39)
            decoder[0].WriteIntSetting(fnxSettingTag.FNX_CODE39_NANO_SCAN,c39)
            decoder[0].WriteIntSetting(fnxSettingTag.FNX_DATAMATRIX_ENABLE, datamatrix)
            decoder[0].WriteIntSetting(fnxSettingTag.FNX_GS1_DATAMATRIX_ENABLE, datamatrix)
            #if qrcode==1 or datamatrix==1:
            #    decoder[0].WriteIntSetting(fnxSettingTag.FNX_PROCESSING_2D_LOW_CONTRAST,1)
            #else:
            decoder[0].WriteIntSetting(fnxSettingTag.FNX_PROCESSING_2D_LOW_CONTRAST,0)

    def launchThreadsDecoder(self, buffer, plot, luxBuffer):
        self.dicoCode = {}
        threads = []
        for i in range(len(self.slice_params)):
            thread = Thread(target=self.decode, 
            args=(buffer, i, plot, luxBuffer))

            threads.append(thread)
            thread.start()
            
        for thread in threads:
            thread.join()

    def launchThreadsDecoderCM5(self,listBufferImages, nameCam):
        threads = []
        for i in range(len(listBufferImages)):
            thread = Thread(target=self.decode_cm5_yuv, args=(listBufferImages[i][0], i, nameCam))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def decode_cm5_yuv(self, imageYuv, indice_decoder, nameCam):
        imageYuvGray = cv2.cvtColor(imageYuv, cv2.COLOR_YUV420p2GRAY)

        listcode = Decode(imageYuvGray, self.decoders[indice_decoder][0])

        for codeData in listcode:
            datacode = codeData['data'].decode("utf-8")
            corners = codeData['corners']
            cposx1,cposy1 = int(corners[0][1]), int(corners[0][0])
            cposx2, cposy2  = int(corners[1][1]), int(corners[1][0])
            cposx3, cposy3 = int(corners[2][1]), int(corners[2][0])
            cposx4, cposy4 = int(corners[3][1]), int(corners[3][0])

            len1 = abs(cposx1 - cposx3)
            len2 = abs(cposx2 - cposx4)
            height1 = abs(cposy1 - cposy3)
            height2 = abs(cposy2 - cposy4)

            length = len1 if len1 >= len2 else len2

            height = height1 if height1 >= height2 else height2

            centerx = cposx1 + round(length / 2) if cposx1 < cposx3 else cposx3 + round(length / 2)
            
            offset = 30 #keyCodeData * 835

            centery = cposy1 + round(height / 2) + offset if cposy1 < cposy3 else cposy3 + round(height / 2) + offset 

            decode_time = round(codeData['t'])

            self.sorting.checkIfbarcodeIsValid(datacode, centery, decode_time, height, length, indice_decoder, nameCam, [cposx1, cposx4, cposy1, cposy4])

            if datacode not in self.listBarcodesCam1 and nameCam == "cam1":
                self.listBarcodesCam1.append(datacode)
            elif datacode not in self.listBarcodesCam2 and nameCam == "cam2":
                self.listBarcodesCam2.append(datacode)

    def decode(self, buffer, i, plot, lux):
        #print(buffer.shape)
        self.dicoCode[i] = self.remove_padding(buffer, self.slice_params[i][0], self.slice_params[i][1], self.decoders[i][0], i, plot, lux)

    def convert_yuv_gray(self, bufferYuv):
        return cv2.cvtColor(bufferYuv, cv2.COLOR_YUV420p2GRAY)

    def remove_padding(self, buff, start_x, end_x, decoder, index, plot, lux):
        codeList=[]
        start_time= time.time()
        kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        buff_slice = buff[:, start_x:end_x]
        buff_slice = buff_slice.reshape(buff.shape[0], end_x - start_x)
        buff_slice = np.delete(buff_slice, np.s_[4::5], 1)
        buff_slice = cv2.cvtColor(buff_slice, cv2.COLOR_BayerBG2GRAY)

        if not plot:
            if lux < 50000:
                buff_slice = cv2.convertScaleAbs(buff_slice, alpha=self.scaling_params[index][0], beta=self.scaling_params[index][1])
            else:
                buff_slice = cv2.convertScaleAbs(buff_slice, alpha=self.scaling_params2[index][0], beta=self.scaling_params2[index][1])
            buff_slice = cv2.filter2D(buff_slice, -1, kernel2)
            
            #Write Slice Image
            #datejpeg = datetime.today().strftime("%d%m%Y_%H%M%S")
            #cv2.imwrite("/home/wareid/V120i/images/"+str(index)+"_"+str(datejpeg)+".jpeg", buff_slice, [int(cv2.IMWRITE_JPEG_QUALITY), 20])

            try:
                codeList = Decode(buff_slice, decoder)
            except:
                traceback.print_exc()
        else:
            alphaparam=6
            index1=2
            while index1!=alphaparam:            
                buff_slice1 = cv2.convertScaleAbs(buff_slice, alpha=index1, beta=16)
                buff_slice2 = cv2.filter2D(buff_slice1, -1, kernel2)
                try:
                    codeList1 = Decode(buff_slice2, decoder)
                    codeList=codeList+codeList1
                except:
                    traceback.print_exc()
                index1=index1+1

        return codeList

    def remove_padding9(self, buff):
        try:
            kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
            buff = np.delete(buff, np.s_[4::5], 1)
            buff = cv2.cvtColor(buff, cv2.COLOR_BayerBG2GRAY)
            buff = cv2.convertScaleAbs(buff, alpha=2, beta=16)
            buff = cv2.filter2D(buff, -1, kernel2)
            return buff
        except:
            return buff

    def draw_circle_test(self, buff, center_coordinates):
        color_img = cv2.circle(buff, center_coordinates, 20, (11, 191, 101), -1) 
        return color_img

    def thread_function(self, buffer, start_x, end_x, decoder, codelist_dict, index,plot,lux):
        result = remove_padding(buffer, start_x, end_x, decoder, index, plot, lux)
        codelist_dict[f"codeList{index+1}"] = result

    def calculate_crop_coords(self, x, y, width, height, size=(200, 200)):
        crop_height, crop_width = size

        # Calculate vertical boundaries
        y_start = max(0, y - crop_height // 2)
        # y_end = min(height, y + crop_height // 2)
        y_end = min(height, y_start+crop_height)

        # Calculate horizontal boundaries
        x_start = max(0, x - crop_width // 2)
        # x_end = min(width, x + crop_width // 2)
        x_end = min(width, x_start + crop_width)

        return (x_start, x_end, y_start, y_end)


    def remove_padding_10(self, buff, lux):

        buff_copy = buff.copy()
        buff_copy = np.delete(buff_copy, np.s_[4::5], 1)

        self.slice_params = [(0, 668), (668, 1336), (1336, 2004), (2004, 2672),
                        (2672, 3340), (3340, 4008), (4008, 4676), (4676, 5351)]

        self.scaling_params = [(4, 16),(3, 16),(2, 16),(2, 16),
        (2, 16),(2, 16),(3, 16),(4, 16)]

        self.scaling_params = [(4, 16),(3, 16),(2, 16),(2, 16),
            (2, 16),(2, 16),(3, 16),(4, 16)]

        kernel2 = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

        for i, params in enumerate(slice_params):

            buff_copy[:, params[0]:params[1]] = cv2.cvtColor(buff_copy[:, params[0]:params[1]], cv2.COLOR_BayerBG2GRAY)
            
            if lux < 40000:
                buff_copy[:, params[0]:params[1]] = cv2.convertScaleAbs(buff_copy[:, params[0]:params[1]], alpha=self.scaling_params[i][0], beta=self.scaling_params[i][1])
            else:
                buff_copy[:, params[0]:params[1]] = cv2.convertScaleAbs(buff_copy[:, params[0]:params[1]], alpha=self.scaling_params2[i][0], beta=self.scaling_params2[i][1])
    
        buff_copy = cv2.filter2D(buff_copy, -1, kernel2)

        return buff_copy

    def draw_circle_on_barcode(self, bufferimg1, center_coordinates, IMGname):
        color_img = cv2.cvtColor(bufferimg1, cv2.COLOR_GRAY2BGR)
        if "nobarcodescan" not in IMGname:
            color_img = cv2.circle(color_img, center_coordinates, 50, (11, 191, 101), -1) 
        return color_img

    

