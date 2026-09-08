from enum import IntEnum

class fnxSymid (IntEnum):
    FNX_ID_UNKNOWN             = 0
    FNX_ID_DATAMATRIX          = 1
    FNX_ID_CODE39              = 2
    FNX_ID_QRCODE              = 3
    FNX_ID_UPCA                = 4
    FNX_ID_UPCE                = 5
    FNX_ID_EAN13               = 6
    FNX_ID_EAN8                = 7
    FNX_ID_ITF                 = 8
    FNX_ID_CODE128             = 9
    FNX_ID_PDF417              = 10
    FNX_ID_GS1_DATABAR         = 11
    FNX_ID_GS1_DATABAR_EX      = 12
    FNX_ID_GS1_DATABAR_LIMITED = 13
    FNX_ID_AZTEC               = 14
    FNX_ID_GS1_128             = 15
    FNX_ID_GS1_DATAMATRIX      = 16
    FNX_ID_MSI                 = 17
    FNX_ID_CODE32              = 18
    FNX_ID_ITF_14              = 19
    FNX_ID_ISBT128             = 20
    FNX_ID_UPCA_ADDON2         = 21
    FNX_ID_UPCA_ADDON5         = 22
    FNX_ID_UPCE_ADDON2         = 23
    FNX_ID_UPCE_ADDON5         = 24
    FNX_ID_EAN13_ADDON2        = 25
    FNX_ID_EAN13_ADDON5        = 26
    FNX_ID_CODE93              = 27
    FNX_ID_CODABAR             = 28
    FNX_ID_OCR_MRZ             = 100


fnxSymidName = {
    fnxSymid.FNX_ID_UNKNOWN:             "Unknown symbology",
    fnxSymid.FNX_ID_DATAMATRIX:          "Datamatrix",
    fnxSymid.FNX_ID_CODE39:              "Code 39",
    fnxSymid.FNX_ID_QRCODE:              "Qr Code",
    fnxSymid.FNX_ID_UPCA:                "UPC-A",
    fnxSymid.FNX_ID_UPCE:                "UPC-E",
    fnxSymid.FNX_ID_EAN13:               "EAN-13",
    fnxSymid.FNX_ID_EAN8:                "EAN-8",
    fnxSymid.FNX_ID_ITF:                 "Interleave 2 of 5",
    fnxSymid.FNX_ID_CODE128:             "Code 128",
    fnxSymid.FNX_ID_PDF417:              "PDF417",
    fnxSymid.FNX_ID_GS1_DATABAR:         "GS1 Databar",
    fnxSymid.FNX_ID_GS1_DATABAR_EX:      "GS1 Databar Expanded",
    fnxSymid.FNX_ID_GS1_DATABAR_LIMITED: "GS1 Databar Limited",
    fnxSymid.FNX_ID_AZTEC:               "Aztec Code",
    fnxSymid.FNX_ID_GS1_128:             "GS1-128",
    fnxSymid.FNX_ID_GS1_DATAMATRIX:      "GS1 Datamatrix",
    fnxSymid.FNX_ID_MSI:                 "MSI",
    fnxSymid.FNX_ID_CODE32:              "Code 32",
    fnxSymid.FNX_ID_ITF_14:              "ITF-14",
    fnxSymid.FNX_ID_ISBT128:             "ISBT128",
    fnxSymid.FNX_ID_UPCA_ADDON2:         "UPC-A with Addon 2",
    fnxSymid.FNX_ID_UPCA_ADDON5:         "UPC-A with Addon 5",
    fnxSymid.FNX_ID_UPCE_ADDON2:         "UPC-E with Addon 2",
    fnxSymid.FNX_ID_UPCE_ADDON5:         "UPC-E with Addon 5",
    fnxSymid.FNX_ID_EAN13_ADDON2:        "EAN-13 with Addon 2",
    fnxSymid.FNX_ID_EAN13_ADDON5:        "EAN-13 with Addon 5",
    fnxSymid.FNX_ID_CODE93:              "Code 93",
    fnxSymid.FNX_ID_CODABAR:             "Codabar",
    fnxSymid.FNX_ID_OCR_MRZ:             "OCR-MRZ",
}
