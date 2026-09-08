from enum import IntEnum

class fnxPartialSymid (IntEnum):
    FNX_ID_PARTIAL_UNKNOWN    = 1000
    FNX_ID_PARTIAL_CODE39     = 1001
    FNX_ID_PARTIAL_EAN13_UPCA = 1002
    FNX_ID_PARTIAL_EAN8       = 1003
    FNX_ID_PARTIAL_CODE128    = 1004


fnxPartialSymidName = {
    fnxPartialSymid.FNX_ID_PARTIAL_UNKNOWN:    "Unknown symbology",
    fnxPartialSymid.FNX_ID_PARTIAL_CODE39:     "Partial Code 39",
    fnxPartialSymid.FNX_ID_PARTIAL_EAN13_UPCA: "Partial EAN-13/UPC-A",
    fnxPartialSymid.FNX_ID_PARTIAL_EAN8:       "Partial EAN-8",
    fnxPartialSymid.FNX_ID_PARTIAL_CODE128:    "Partial Code 128/GS1-128",
}
