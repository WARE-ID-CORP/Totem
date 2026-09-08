from enum import IntEnum


class fnxSettingTag(IntEnum):

    """
    FNX_CODE39_GROUP = 0x0100
    """

    """
    Enable Code39 decoding.

    Code 39 is a 1D code mainly used in industrial applications.
    https://en.wikipedia.org/wiki/Code_39

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE39_ENABLE = 0x0101

    """
    Enable Code32 decoding.

    Also called Italian Pharmacode, this symbology is a 1D code used in pharmaceutical applications.
    https://github.com/bwipp/postscriptbarcode/wiki/Italian-Pharmacode

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE32_ENABLE = 0x0102

    """
    Enable Nano-scan for Code39.

    See documentation of "Nano-Scan algorithm" for more information.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE39_NANO_SCAN = 0x0110

    """
    Enable transmission of Start and Stop codewords for Code39.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE39_TRANSMIT_START_STOP = 0x0120

    """
    Enable validation of checksum for Code39.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE39_CHECK = 0x0130

    """
    Enable transmission of checksum for Code39.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE39_TRANSMIT_CHECK = 0x0131

    """
    Enable full ASCII mode for Code39.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE39_FULL_ASCII = 0x0140

    """
    Enable Code 39 decoding with damaged codewords (enabling this setting can generate misreads).

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE39_DAMAGED = 0x0150

    """
    Enable partial decoding for Code39.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE39_PARTIAL_DECODING = 0x0160


    """
    FNX_EAN_UPC_GROUP = 0x0200
    """

    """
    Enable EAN13 decoding.

    EAN13 is a 1D code used in retail applications. It is an extension of UPCA and contains 13 digits.
    https://en.wikipedia.org/wiki/International_Article_Number

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_EAN13_ENABLE = 0x0201

    """
    Enable EAN8 decoding.

    EAN8 is a 1D code designed to be used on small packages where an EAN13 barcode would be too large.
    https://en.wikipedia.org/wiki/EAN-8

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_EAN8_ENABLE = 0x0202

    """
    Enable UPCA decoding.

    UPCA is a 1D code used in retail applications. It consists of 12 digits that are uniquely assigned to each trade item.
    https://en.wikipedia.org/wiki/Universal_Product_Code

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_UPCA_ENABLE = 0x0203

    """
    Enable UPCE decoding.

    UPCE is the compressed version of UPCA. It suppresses zeroes to save space.
    https://en.wikipedia.org/wiki/Universal_Product_Code

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_UPCE_ENABLE = 0x0204

    """
    Enable Nano-scan for EAN13, EAN8, UPCA and UPCE.

    See documentation of "Nano-Scan algorithm" for more information.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_EAN_UPC_NANO_SCAN = 0x0210

    """
    Indicate if decoding the EAN13 addon is required.

    Valid input values are:
       * 0 : autodiscriminate (default)
       * 1 : required
    """
    FNX_EAN13_ADDON_REQUIRED = 0x0221

    """
    Indicate if decoding the UPCA addon is required.

    Valid input values are:
       * 0 : autodiscriminate (default)
       * 1 : required
    """
    FNX_UPCA_ADDON_REQUIRED = 0x0223

    """
    Indicate if decoding the UPCE addon is required.

    Valid input values are:
       * 0 : autodiscriminate (default)
       * 1 : required
    """
    FNX_UPCE_ADDON_REQUIRED = 0x0224

    """
    Select the type of addon for EAN13.

    Valid input values are:
       * 0 : none (default)
       * 1 : addon 2
       * 2 : addon 5
       * 3 : addon 2 or addon 5
    """
    FNX_EAN13_ADDON_TYPE = 0x0231

    """
    Select the type of addon for UPCA.

    Valid input values are:
       * 0 : none (default)
       * 1 : addon 2
       * 2 : addon 5
       * 3 : addon 2 or addon 5
    """
    FNX_UPCA_ADDON_TYPE = 0x0233

    """
    Select the type of addon for UPCE.

    Valid input values are:
       * 0 : none (default)
       * 1 : addon 2
       * 2 : addon 5
       * 3 : addon 2 or addon 5
    """
    FNX_UPCE_ADDON_TYPE = 0x0234

    """
    Enable partial decoding for EAN13, EAN8 and UPCA.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_EAN_UPC_PARTIAL_DECODING = 0x0260


    """
    FNX_MSI_GROUP = 0x0300
    """

    """
    Enable MSI decoding.

    MSI (Modified Plessey) is a 1D code mainly used in retail applications.
    https://en.wikipedia.org/wiki/MSI_Barcode

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_MSI_ENABLE = 0x0301

    """
    Enable Nano-scan for MSI.

    See documentation of "Nano-Scan algorithm" for more information.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_MSI_NANO_SCAN = 0x0310

    """
    Select MSI checksum.

    Valid input values are:
       * 1 : check modulo 10 (default)
       * 2 : check modulo 10/10
       * 3 : check modulo 11
       * 4 : check modulo 11/10
    """
    FNX_MSI_CHECK = 0x0330

    """
    Enable transmission of checksum for MSI.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_MSI_TRANSMIT_CHECK = 0x0331


    """
    FNX_ITF_GROUP = 0x0600
    """

    """
    Enable Interleaved 2 of 5 decoding.

    Interleaved 2 of 5 is a 1D code mainly used in industrial applications.
    https://en.wikipedia.org/wiki/Interleaved_2_of_5

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_ITF_ENABLE = 0x0601

    """
    Enable ITF-14 decoding.

    ITF-14 is a standardized version of ITF by GS1. It is designed to mark packages with Global Trade Item Numbers (GTIN).
    https://en.wikipedia.org/wiki/Interleaved_2_of_5

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_ITF_14_ENABLE = 0x0602

    """
    Enable Nano-scan for ITF.

    See documentation of "Nano-Scan algorithm" for more information.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_ITF_NANO_SCAN = 0x0610

    """
    Enable validation of checksum for Interleaved 2 of 5.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_ITF_CHECK = 0x0630

    """
    Enable transmission of checksum for Interleaved 2 of 5.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_ITF_TRANSMIT_CHECK = 0x0631

    """
    Enable short margin for Interleaved 2 of 5.

    Valid input values are:
       * 0 : disable
       * 1 : auto (default)
       * 2 : allowed
    """
    FNX_ITF_SHORT_MARGIN = 0x0670


    """
    FNX_CODE128_GROUP = 0x0700
    """

    """
    Enable Code 128 decoding.

    Code 128 is a 1D code mainly used in industrial applications.
    https://en.wikipedia.org/wiki/Code_128

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE128_ENABLE = 0x0701

    """
    Enable GS1-128 decoding.

    Formerly known as UCC/EAN-128, it is a subset of Code 128 used in shipping and packaging industries as a product identification code for containers and pallets.
    https://en.wikipedia.org/wiki/Code_128

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_GS1_128_ENABLE = 0x0702

    """
    Enable ISBT 128 decoding.

    ISBT 128 is based on Code 128. It is used to identify medical products of human origin.
    https://en.wikipedia.org/wiki/ISBT_128

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_ISBT128_ENABLE = 0x0703

    """
    Enable ISBT 128 concatenation.

    Valid input values are:
       * 0 : disable (default)
       * 1 : auto
       * 2 : required
    """
    FNX_ISBT128_CONCATENATION = 0x0740

    """
    Enable Nano-scan for Code 128 and GS1-128.

    See documentation of "Nano-Scan algorithm" for more information.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE128_NANO_SCAN = 0x0710

    """
    Enable Code 128 and GS1-128 decoding with a damaged start or stop.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE128_DAMAGED_START_STOP = 0x0750

    """
    Enable partial decoding for Code 128 and GS1-128.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE128_PARTIAL_DECODING = 0x0760


    """
    FNX_GS1_DATABAR_GROUP = 0x0800
    """

    """
    Enable GS1-Databar decoding.

    GS1 Databar is a 1D/stacked code mainly used in retail applications.
    https://www.gs1.org/standards/barcodes/databar

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_GS1_DATABAR_ENABLE = 0x0801

    """
    Enable GS1-Databar Expanded decoding.

    GS1 DataBar Expanded is a 1D/stacked code designed for applications that require data to be encoded in addition to Global Trade Item Number (GTIN) or Global Coupon Number (GCN)
    https://www.gs1.org/standards/barcodes/databar

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_GS1_DATABAR_EX_ENABLE = 0x0802

    """
    Enable GS1-Databar Limited decoding.

    GS1 Databar Limited is a 1D code used to encode GTIN-14, designed for applications where space is extremely limited.
    https://github.com/bwipp/postscriptbarcode/wiki/GS1-DataBar-Limited

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_GS1_DATABAR_LIMITED_ENABLE = 0x0803


    """
    FNX_CODE93_GROUP = 0x0900
    """

    """
    Enable Code 93 decoding.

    Code 93 is a 1D code designed to provide a higher density and data security enhancement to Code 39.
    https://en.wikipedia.org/wiki/Code_93

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODE93_ENABLE = 0x0901


    """
    FNX_CODABAR_GROUP = 0x1000
    """

    """
    Enable Codabar decoding.

    Codabar is a 1D code designed to be accurately read even when printed on dot-matrix printers.
    https://en.wikipedia.org/wiki/Codabar

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODABAR_ENABLE = 0x1001

    """
    Enable transmission of Start and Stop codewords for Codabar.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODABAR_TRANSMIT_START_STOP = 0x1020

    """
    Enable validation of checksum for Codabar.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODABAR_CHECK = 0x1030

    """
    Enable transmission of checksum for Codabar.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_CODABAR_TRANSMIT_CHECK = 0x1031


    """
    FNX_DATAMATRIX_GROUP = 0x2000
    """

    """
    Enable Datamatrix decoding.

    Datamatrix is a 2D code mainly used in industrial applications.
    https://en.wikipedia.org/wiki/Data_Matrix

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_DATAMATRIX_ENABLE = 0x2001

    """
    Enable GS1-Datamatrix decoding.

    GS1-Datamatrix is a Datamatrix that contains data structured according to the rules of the GS1 System.
    https://www.gs1.org/standards/gs1-datamatrix-guideline/25

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_GS1_DATAMATRIX_ENABLE = 0x2002

    """
    Enable Damaged datamatrix decoding.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_DATAMATRIX_DAMAGED = 0x2010


    """
    FNX_QR_CODE_GROUP = 0x2100
    """

    """
    Enable QR Code decoding.

    QR Code is a 2D code most often used for consumer applications.
    https://en.wikipedia.org/wiki/QR_code

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_QR_CODE_ENABLE = 0x2101


    """
    FNX_PDF417_GROUP = 0x2200
    """

    """
    Enable PDF417 decoding.

    PDF417 is a stacked symbology that can be read using a 1D reader.
    https://en.wikipedia.org/wiki/PDF417

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_PDF417_ENABLE = 0x2201


    """
    FNX_AZTEC_GROUP = 0x2300
    """

    """
    Enable Aztec decoding.

    Aztec is a 2D code mainly used for tickets.
    https://en.wikipedia.org/wiki/Aztec_Code

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_AZTEC_ENABLE = 0x2301


    """
    FNX_MRZ_GROUP = 0x4000
    """

    """
    Enable MRZ OCR decoding.

    MRZ is a machine-readable zone of text on identity documents (passports specifically).
    https://en.wikipedia.org/wiki/Machine-readable_passport

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_MRZ_ENABLE = 0x4001


    """
    FNX_OPERATING_GROUP = 0x8000
    """

    """
    Enable multithreaded decoding.

    See documentation of "Multi-thread support" for more information.

    Valid input values are:
       * 0 : disable
       * 1 : enable (default)
    """
    FNX_OPERATING_MULTI_THREAD = 0x8001

    """
    Enable multi-scale decoding.

    See documentation of "Multi-scale analysis" for more information.

    Valid input values are:
       * 0 : disable
       * 1 : enable (default)
    """
    FNX_OPERATING_N_MULTI_SCALE_ENABLE = 0x8002

    """
    Set number of scales used in multi-scale decoding.

    See documentation of "Multi-scale analysis" for more information.

    Valid input values are:
       * 2 : 2 scales (default)
       * 3 : 3 scales
    """
    FNX_OPERATING_N_MULTI_SCALE = 0x8003

    """
    Enable automatic termination of the decoding process after N reading success per image.

    See documentation of "Stopping the decoder after N decodes or timeout" for more information.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_OPERATING_N_CODES_EXPECTED_ENABLE = 0x8005

    """
    Set the number of barcode N to be decoded per image for the decoding process to terminate.

    See documentation of "Stopping the decoder after N decodes or timeout" for more information.
    """
    FNX_OPERATING_N_CODES_EXPECTED = 0x8006

    """
    Enable automatic termination of the decoding process after timeout.

    See documentation of "Stopping the decoder after N decodes or timeout" for more information.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_OPERATING_TIME_OUT_ENABLE = 0x8007

    """
    Set the timeout value in milliseconds for the decoding process to terminate after timeout.

    See documentation of "Stopping the decoder after N decodes or timeout" for more information.
    """
    FNX_OPERATING_TIME_OUT = 0x8008

    """
    Enable CUDA optimization for NVIDIA GPUs.

    See documentation of "CUDA optimizations" for more information.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_OPERATING_CUDA_ENABLE = 0x8009


    """
    FNX_PROCESSING_1D_GROUP = 0x8100
    """

    """
    Enable search for 1D high density codes. Enabling this option favours the detection of small and dense 1D barcodes at the expense of very large ones.

    See documentation of "1D High density" for more information.

    Valid input values are:
       * 0 : disable
       * 1 : enable (default)
    """
    FNX_PROCESSING_1D_HIGH_DENSITY = 0x8102

    """
    Enable additional processing for improving 1D damaged codes reading at the expense of decoding time.

    Valid input values are:
       * 0 : disable
       * 1 : mild (default)
       * 2 : aggressive
    """
    FNX_PROCESSING_1D_DAMAGED = 0x8103

    """
    Set search direction of 1D barcodes in the image to reduce decoding time.

    See documentation of "1D Orientation" for more information.

    Valid input values are:
       * 0 : any directions (default)
       * 1 : horizontal +/- 45°
       * 2 : vertical +/- 45°
    """
    FNX_PROCESSING_1D_ORIENTATION = 0x8104

    """
    Enable detection 1D barcodes with very low contrast at the expense of decoding time.

    See documentation of "1D Low contrast" for more information.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_PROCESSING_1D_LOW_CONTRAST = 0x8105

    """
    Optimize scanning direction in case of high perspective. Enabling this setting increase decoding time.

    Valid input values are:
       * 0 : standard algorithm
       * 1 : improved algorithm (default)
    """
    FNX_PROCESSING_1D_PERSPECTIVE = 0x8106

    """
    Enable search for very low height 1D barcodes. As this feature is very CPU intensive, it should only be enabled if it is really needed.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_PROCESSING_1D_LOW_HEIGHT = 0x8107


    """
    FNX_PROCESSING_2D_GROUP = 0x8200
    """

    """
    Enable extensive search for large number of 2D barcodes. Enabling this settings to decode several hundred 2D barcodes in large images.

    Valid input values are:
       * 0 : disable (default)
       * 1 : enable
    """
    FNX_PROCESSING_2D_EXTENSIVE_SEARCH = 0x8201

    """
    Enable detection 2D barcodes with very low contrast at the expense of decoding time. Valid input values are:

       * 0 : disable (default)
       * 1 : enable
    """
    FNX_PROCESSING_2D_LOW_CONTRAST = 0x8202


    """
    FNX_DECODER_INFO_GROUP = 0xFF00
    """

    """
    Return the date of the decoder build as a C string (Read only setting).

    """
    FNX_DECODER_BUILD_DATE = 0xFF01

    """
    Return the maximum number of decoder instances that can be created simultaneously, see fnxCreateDecoder API function (Read only setting).

    """
    FNX_DECODER_N_MAX_INSTANCES = 0xFF02

    """
    Return the scan mode (Read only setting).

    Returned values can be:
       * 0 : Item-Scan (single barcode scans)
       * 1 : Multi-Scan (up to 5 codes per image)
       * 2 : Maxi-Scan (unlimited codes per image)
    """
    FNX_DECODER_SCAN_MODE = 0xFF03

    """
    Return the CUDA capabilities as a C string (Read only setting).

    Returned strings can be:
       * "Not supported" : CUDA algorithms are not built in the decoder library
       * "No device found" : No supported NVidia GPU has been found
       * "Xavier", "Volta" ... : Name of the CUDA architecture
    """
    FNX_DECODER_CUDA_CAPABILITIES = 0xFF10

