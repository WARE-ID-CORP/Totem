import os.path
import ctypes
from .PhenixDecoder import fnxDecoder
from .PhenixStatus  import fnxStatus




class fnxDecoderManager:

    def __init__(self, library_path : str):
        if not os.path.isfile(library_path):
            raise RuntimeError ("Library file '%s' not found!" % library_path)
    
        self.decoder_lib = ctypes.CDLL(library_path)


    def initializeLibrary(self) -> int:
        status = self.decoder_lib.fnxInitializeLibrary()
        return status


    def deinitializeLibrary(self) -> int:
        status = 0
        try:
            status = self.decoder_lib.fnxDeinitializeLibrary()
        except:
            pass
        return status


    def getLibraryVersion(self) -> str:
        self.decoder_lib.fnxGetLibraryVersion.restype = ctypes.c_char_p
        return self.decoder_lib.fnxGetLibraryVersion().decode('utf-8')


    def activateLicense(self, key: str) -> int:
        status = self.decoder_lib.fnxActivateLicense(ctypes.c_char_p(key.encode('utf-8')))
        return status


    def createDecoder(self) -> fnxDecoder:
        decoder = fnxDecoder(self.decoder_lib);
        if decoder.m_Handle == 0:
            # something went wrong inside decoder library, exit on error
            del decoder;
            raise RuntimeError ("createDecoder failed")

        return decoder;


    def destroyDecoder(self, decoder: fnxDecoder):
        del decoder


    def offlineActivationRequest(self, key: str, filepath: str) -> int:
        status = self.decoder_lib.fnxOfflineActivationRequest(ctypes.c_char_p(key.encode('utf-8')), ctypes.c_char_p(filepath.encode('utf-8')))
        return status


    def offlineActivateLicense(self, filepath: str) -> int:
        status = self.decoder_lib.fnxOfflineActivateLicense(ctypes.c_char_p(filepath.encode('utf-8')))
        return status

