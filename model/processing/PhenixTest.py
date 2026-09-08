#!/usr/bin/env python
# coding: utf-8
import argparse
import platform
import os
import fnmatch

from libraries.pyWrapper.PhenixDecoderManager import fnxDecoderManager
from libraries.pyWrapper.PhenixSettings import fnxSettingTag
from libraries.pyWrapper.PhenixSymid import fnxSymid, fnxSymidName
from libraries.pyWrapper.PhenixStatus import fnxStatus, getStatusMessage

root_dir = str(os.path.abspath(os.curdir))

def GetFilesListFromDirectory(directory, patterns, relative = "", images_list = None):
    if images_list is None:
        images_list = []

    root, dirs, files = next( os.walk(directory) )
    for dir in dirs:
        if dir[0] == ".":
            continue
        new_directory = os.path.join(root, dir)
        new_relative  = os.path.join(relative, dir)
        GetFilesListFromDirectory (new_directory, patterns, new_relative, images_list)

    for file  in files:
        for pattern in patterns:
            if fnmatch.fnmatch(file, pattern):
                images_list.append( os.path.join(directory, file) )
                break

    return images_list



# helper function
def decode_and_print_results(decoder, image_filename: str) -> None:
    #print("\nDecoding %s" % image_filename)
    processing_time, results_list = decoder.ProcessImage(image_filename)
    #print("processing_time: %2.2f ms, %d decode(s)" % (processing_time, len(results_list)))
    for result in results_list:
        #print("  --------------- ")
        #print("  Decoded string: %s" % result['data'].decode('utf-8', 'ignore'))
        #print("  Timestamp: %2.2f" % result['t'])
        #print("  Symbology id: %s" % (fnxSymidName[result['symid']]))
        #print("  Corners: %s" % "-".join(["(%d,%d)" % (x, y) for x, y in result['corners']]))
        if 'optionalData' in result:
            optData = result['optionalData']

            # Example to print all fields
            #for key, value in optData.items():
                #print("  %s: %s" % (key, value))

            ## Example to access particular fields
            # if 'aimId' in optData:
            #    print("  AIM id: %s" %(optData['aimId']) )
            #if 'nModulesHor' in optData:
            #    print("  Number of modules (horizontally): %s" %(optData['nModulesHor']) )
            #if 'nModulesVer' in optData:
                #print("  Number of modules (vertically): %s" %(optData['nModulesVer']) )
    return(results_list)

def Decode(image_or_directory: str, decoder):

    list_images = image_or_directory,

    for image_filename in list_images:
        codeList = decode_and_print_results(decoder, image_filename)
    return(codeList)

def DecoderInitialization():
    # Decoder library initialization
    license_key = "A26DF1-ACDB3B-43CEBC-D6D371-E3C671-CAF1D1"
    decMgr = fnxDecoderManager("/home/wareid/Totem/libraries/PhenixDecoderAPI/lib/Linux/aarch64-linux-gnu/libPhenixDecoder.so")
    # print("Library path:    ", root_dir+ "/PhenixDecoderAPI/lib/Linux/aarch64-linux-gnu/libPhenixDecoder.so")
    # print("Library version: ", ', '.join(decMgr.getLibraryVersion().split("\n")))
    force_license_key = False

    status = decMgr.initializeLibrary()
    if status != fnxStatus.FNX_SUCCESS.value:
        print("Warning (initializeLibrary): %s" % getStatusMessage(status))

    if (status != fnxStatus.FNX_SUCCESS.value) or force_license_key:
        if len(license_key):
            status = decMgr.activateLicense(license_key)
            if status != fnxStatus.FNX_SUCCESS.value:
                print("Error (activateLicense): %s" % getStatusMessage(status))
                return
        else:
            print("Error: License key is missing")
            return

    print("License validated")


    # Decoder creation and initialization
    decoder = decMgr.createDecoder()

    # activate some symbologies and settings
    decoder.WriteIntSetting(fnxSettingTag.FNX_CODE39_ENABLE,                  0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_CODE39_NANO_SCAN,               0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_EAN13_ENABLE,                   0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_EAN8_ENABLE,                    0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_UPCA_ENABLE,                    0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_UPCE_ENABLE,                    0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_EAN_UPC_NANO_SCAN,              0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_CODE128_ENABLE,                 1)
    decoder.WriteIntSetting(fnxSettingTag.FNX_GS1_128_ENABLE,                 1)
    decoder.WriteIntSetting(fnxSettingTag.FNX_CODE128_NANO_SCAN,              1)
    decoder.WriteIntSetting(fnxSettingTag.FNX_DATAMATRIX_ENABLE,              0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_GS1_DATAMATRIX_ENABLE,          0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_QR_CODE_ENABLE,                 0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_PROCESSING_1D_LOW_CONTRAST,     1)
    decoder.WriteIntSetting(fnxSettingTag.FNX_PROCESSING_1D_PERSPECTIVE,      0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_PROCESSING_1D_HIGH_DENSITY,     1)
    decoder.WriteIntSetting(fnxSettingTag.FNX_PROCESSING_1D_ORIENTATION,      2)
    decoder.WriteIntSetting(fnxSettingTag.FNX_PROCESSING_1D_DAMAGED,          2)
    decoder.WriteIntSetting(fnxSettingTag.FNX_CODE128_DAMAGED_START_STOP,     1)
    decoder.WriteIntSetting(fnxSettingTag.FNX_PROCESSING_1D_LOW_HEIGHT,       0)
    decoder.WriteIntSetting(fnxSettingTag.FNX_OPERATING_MULTI_THREAD,         1)
    decoder.WriteIntSetting(fnxSettingTag.FNX_OPERATING_N_MULTI_SCALE_ENABLE, 1)
    decoder.WriteIntSetting(fnxSettingTag.FNX_OPERATING_N_MULTI_SCALE,        3)
    decoder.WriteIntSetting(fnxSettingTag.FNX_OPERATING_TIME_OUT_ENABLE,      0)
    #decoder.WriteIntSetting(fnxSettingTag.FNX_PROCESSING_2D_LOW_CONTRAST,     1)
    ####

    # activate partial decode
    #decoder.WriteIntSetting(fnxSettingTag.FNX_CODE128_PARTIAL_DECODING,       1)
    #decoder.WriteIntSetting(fnxSettingTag.FNX_EAN_UPC_PARTIAL_DECODING,       1)
    #decoder.WriteIntSetting(fnxSettingTag.FNX_CODE39_PARTIAL_DECODING,        1)

    return(decoder,decMgr)

def DecoderClose(decoder,decMgr):
    decMgr.destroyDecoder(decoder)

if __name__ == '__main__':

    if  platform.system() == "Linux":
        decoder_filename = "libPhenixDecoder.so"
        platform_target = "%s-linux-gnu" % platform.machine()
    elif platform.system() == "Darwin":
        decoder_filename = "libPhenixDecoder.dylib"
        platform_target = "%s" % platform.machine()
    else:
        decoder_filename = "PhenixDecoder.dll"
        if platform.machine().endswith('64'):
            platform_target = "x64"
        else:
            platform_target = "Win32"

    default_decoder_path = "%s/../PhenixDecoderAPI/lib/%s/%s/%s" %(os.path.dirname(os.path.abspath(__file__)), platform.system(), platform_target, decoder_filename)

    parser = argparse.ArgumentParser(description='PhenixDecoder test.')

    parser.add_argument('-d', '--decoder_path', help = 'pathname of the decoder library', default = default_decoder_path)
    parser.add_argument('-k', '--license_key', help = 'license key', default='')
    parser.add_argument('-f', '--force_license_key', help = 'force (overwrite) license key', action='store_true')
    parser.add_argument('-i', '--image_or_directory', help = 'image/directory to decode', required = True)

    args = parser.parse_args()

    main(args.decoder_path, args.image_or_directory, args.license_key, args.force_license_key)


