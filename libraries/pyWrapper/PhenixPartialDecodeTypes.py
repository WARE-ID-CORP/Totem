from enum import IntEnum

class fnxPartialDecodeType (IntEnum):
    FNX_DECODED_FROM_START      = 0
    FNX_DECODED_FROM_STOP       = 1
    FNX_FULL_BARCODE            = 2


fnxPartialDecodeTypeName = {
    fnxPartialDecodeType.FNX_DECODED_FROM_START:  "start",
    fnxPartialDecodeType.FNX_DECODED_FROM_STOP:   "stop",
    fnxPartialDecodeType.FNX_FULL_BARCODE:        "full barcode",
}
