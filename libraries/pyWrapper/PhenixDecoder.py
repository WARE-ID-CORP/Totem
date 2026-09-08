import ctypes
import PIL.Image
import numpy as np
import time
import copy
import json
from typing import Callable, Tuple, List, Dict

from .PhenixStatus import fnxStatus, getStatusMessage
from .PhenixImageFormat import fnxImageFormat
from .PhenixSymid                import fnxSymid
from .PhenixPartialSymid         import fnxPartialSymid
from .PhenixPartialDecodeTypes   import fnxPartialDecodeType



class fnxPoint(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int) ]


class fnxImage(ctypes.Structure):
    _fields_ = [("data",     ctypes.POINTER(ctypes.c_char)),
                ("width",    ctypes.c_uint),
                ("height",   ctypes.c_uint),
                ("stride",   ctypes.c_uint),
                ("nb_bytes", ctypes.c_uint),
                ("format",   ctypes.c_int),
                ("aimer",    fnxPoint) ]


class fnxResult(ctypes.Structure):
    _fields_ = [("data",    ctypes.POINTER(ctypes.c_char)),
                ("length",  ctypes.c_uint),
                ("symid",   ctypes.c_int),
                ("format",  ctypes.c_uint),
                ("corners", fnxPoint * 4) ]


class fnxPartialMessage(ctypes.Structure):
    _fields_ = [("data",           ctypes.POINTER(ctypes.c_char)),
                ("dataLength",     ctypes.c_uint),
                ("format",         ctypes.c_uint) ]


class fnxPartialResult(ctypes.Structure):
    _fields_ = [("partialDecodeType",  ctypes.c_int),
                ("barcodeScore",       ctypes.c_uint),
                ("nbCodeword",         ctypes.c_uint),
                ("codewords",          ctypes.POINTER(ctypes.c_ubyte)),
                ("codewordScores",     ctypes.POINTER(ctypes.c_ubyte)),
                ("partialSymid",       ctypes.c_int),
                ("nbPossibleMessages", ctypes.c_uint),
                ("possibleMessages",   ctypes.POINTER(fnxPartialMessage)),
                ("corners",           fnxPoint * 4) ]


class fnxDecoder:
    m_Handle = 0

    def __init__(self, decoder_lib):
        self.decoder_lib = decoder_lib
        
        try:
            self.m_Handle = self.decoder_lib.fnxCreateDecoder()
        except:
            raise RuntimeError('Error: exception in fnxCreateDecoder')

        if self.m_Handle == 0:
            raise RuntimeError('Error: fnxCreateDecoder returned no handle')

        self._SetResultCallback()
        self._SetPartialResultCallback()


    def __del__(self):
        if self.m_Handle:
            try:
                status = self.decoder_lib.fnxDestroyDecoder(self.m_Handle)
            except:
                raise RuntimeError('Error: exception in fnxDestroyDecoder')
            if status != 0:
                print('Warning fnxDestroyDecoder: %s' % getStatusMessage(status))


    def ReadIntSetting(self, settingTag) -> int:
        value = ctypes.c_int(0)
        try:
            status = self.decoder_lib.fnxReadIntSetting(self.m_Handle, settingTag, ctypes.pointer(value))
        except:
            raise RuntimeError('Error: exception in fnxReadIntSetting')
            
        if status != 0:
            print('Warning fnxReadIntSetting(%s): %s' % (hex(settingTag), getStatusMessage(status)))

        return value.value


    def WriteIntSetting(self, settingTag: int, settingValue: int)-> None:
        try:
            status = self.decoder_lib.fnxWriteIntSetting(self.m_Handle, settingTag, settingValue)
        except:
            raise RuntimeError('Error: exception in fnxWriteIntSetting')

        if status != 0:
            print('Warning fnxWriteIntSetting(%s): %s' % (hex(settingTag), getStatusMessage(status)))


    def _ResultCallbackMaker(self) -> Callable[[fnxResult, int], int]:
        def result_callback(result: fnxResult, caller: int) -> int:
            t_ms = (time.perf_counter() - self.t_start) * 1000
            resultOut = {'data':    copy.deepcopy(result[0].data[0:result[0].length]),
                         'length':  copy.deepcopy(result[0].length),
                         'symid':   copy.deepcopy(fnxSymid(result[0].symid)),
                         'format':  copy.deepcopy(result[0].format),
                         'corners': [(corner.x, corner.y) for corner in result[0].corners],
                         't':       copy.deepcopy(t_ms),
                     }
            
            try:
                optionalDataLength = ctypes.c_int()
                optionalDataBuffer = ctypes.POINTER(ctypes.c_char)()
                self.decoder_lib.fnxGetOptionalData(0, ctypes.byref(optionalDataBuffer), ctypes.byref(optionalDataLength))
                            
                resultOut['optionalData'] = json.loads(optionalDataBuffer[0:optionalDataLength.value])
            except:
                pass

            self.results.append(resultOut)
            return 0
        return result_callback


    def _SetResultCallback(self) -> None:
        RESULT_CALLBACK_TYPE  = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(fnxResult), ctypes.c_void_p)
        result_callback       = self._ResultCallbackMaker()
        self._result_callback = RESULT_CALLBACK_TYPE( result_callback )

        try:
            status = self.decoder_lib.fnxSetResultCallback(self.m_Handle, self._result_callback, 0)
        except:
            raise RuntimeError('Error: exception in fnxSetResultCallback')

        if status != 0:
            raise RuntimeError('Error fnxSetResultCallback: %s' % getStatusMessage(status))


    def _PartialResultCallbackMaker(self) -> Callable[[fnxPartialResult, int], int]:
        def partial_result_callback(partialResult: fnxPartialResult, caller: int) -> int:
            t_ms = (time.perf_counter() - self.t_start) * 1000
            resultOut = {'partialDecodeType': copy.deepcopy(fnxPartialDecodeType(partialResult[0].partialDecodeType)),
                         'barcodeScore':      copy.deepcopy(partialResult[0].barcodeScore),
                         'nbCodeword':        copy.deepcopy(partialResult[0].nbCodeword),
                         'codewords':         copy.deepcopy(partialResult[0].codewords[0:partialResult[0].nbCodeword]),
                         'codewordScores':    copy.deepcopy(partialResult[0].codewordScores[0:partialResult[0].nbCodeword]),
                         'partialSymid':      copy.deepcopy(fnxPartialSymid(partialResult[0].partialSymid)),
                         'possibleMessages':  [],
                         'corners':           [(corner.x, corner.y) for corner in partialResult[0].corners],
                         't':                 copy.deepcopy(t_ms),
                     }
                     
            for i in range(partialResult[0].nbPossibleMessages):
                possibleMessages = partialResult[0].possibleMessages[i]
                partialMessage = {'data':         copy.deepcopy(possibleMessages.data[0:possibleMessages.dataLength]),
                                  'dataLength':   copy.deepcopy(possibleMessages.dataLength),
                                  'format':       copy.deepcopy(possibleMessages.format) }
                resultOut['possibleMessages'].append(partialMessage)
                
            self.partialResults.append(resultOut)
            return 0
        return partial_result_callback


    def _SetPartialResultCallback(self) -> None:
        PARTIAL_RESULT_CALLBACK_TYPE  = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(fnxPartialResult), ctypes.c_void_p)
        partial_result_callback       = self._PartialResultCallbackMaker()
        self._partial_result_callback = PARTIAL_RESULT_CALLBACK_TYPE( partial_result_callback )

        status = 0
        try:
            status = self.decoder_lib.fnxSetPartialResultCallback(self.m_Handle, self._partial_result_callback, 0)
        except AttributeError as err:
            print('Warning: ', err)
            pass
        except:
            raise RuntimeError('Error: exception in fnxSetPartialResultCallback')

        if status != 0:
            raise RuntimeError('Error SetPartialResultCallback: %s' % getStatusMessage(status))


    def _FillImageStruct(self, image_prm) -> fnxImage:
        try:
            if type(image_prm) == np.ndarray:
                h, w = image_prm.shape
                img_c_array   = ctypes.create_string_buffer(image_prm.tostring())
                stride = w
                imageFormat = fnxImageFormat.FNX_Y800
            else:
                if type(image_prm) == PIL.Image.Image:
                    if image_prm.getbands() != ('L',):
                        image = image_prm.convert("L")
                    else:
                        image = image_prm
                elif type(image_prm) == str:
                    image = PIL.Image.open(image_prm)
                    # workaround PIL issue for loading 32-bit signed integer pixels PNG images
                    if image.mode == "I":
                        table = [ i/256 for i in range(65536) ]
                        image = image.point(table, 'L')
                    else:
                        # comment the following line if you want to send images as color images to the decoder
                        image = image.convert('L')
                        pass
                w, h = image.size
                img_buffer    = image.tobytes(encoder_name='raw')
                img_c_array   = ctypes.create_string_buffer(img_buffer)
                
                if image.mode == "L":
                    stride = w
                    imageFormat = fnxImageFormat.FNX_Y800
                elif image.mode == "I":
                    stride = w
                    imageFormat = fnxImageFormat.FNX_Y800
                elif image.mode == "P":
                    stride = w
                    imageFormat = fnxImageFormat.FNX_Y800
                elif image.mode == "RGB":
                    stride = w * 3
                    imageFormat = fnxImageFormat.FNX_RGB
                elif image.mode == "RGBA":
                    stride = w * 4
                    imageFormat = fnxImageFormat.FNX_RGBA
                else:
                    raise RuntimeError("Conversion missing for Pillow mode '%s'" % image.mode)
        except:
            raise RuntimeError("Error with image_prm")

        return fnxImage(img_c_array, w, h, stride, 0, imageFormat, fnxPoint(w // 2, h // 2))


    def ProcessImageWithPartial(self, image_prm) -> Tuple[int, List[Dict], List[Dict]]:
        image_struct = self._FillImageStruct(image_prm)

        self.results = []
        self.partialResults = []
        try:
            self.t_start = time.perf_counter()
            status = self.decoder_lib.fnxProcessImage(self.m_Handle, ctypes.byref(image_struct))
            processing_time_ms = (time.perf_counter() - self.t_start) * 1000
        except:
            raise RuntimeError('Error: exception in fnxProcessImage')

        if status:
            print('Warning fnxProcessImage: %s' % getStatusMessage(status))
            
        return processing_time_ms, copy.deepcopy(self.results), copy.deepcopy(self.partialResults)


    def ProcessImage(self, image_prm) -> Tuple[int, List[Dict]]:
    
        processing_time_ms, results, _ = self.ProcessImageWithPartial(image_prm)       
        
        return processing_time_ms, results
