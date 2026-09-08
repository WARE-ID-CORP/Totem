///
/// \file PhenixPartialDecodeAPI.h
/// \brief This header file defines API functions and data structures for partial decoding
///

#ifndef PHENIX_PARTIAL_DECODE_API_H
#define PHENIX_PARTIAL_DECODE_API_H

#include "PhenixDecoderAPI.h"

#ifdef __cplusplus
extern "C" {
#endif  // __cplusplus

    // -------------------------------------------------------
    //  Data types definition
    // -------------------------------------------------------

    ///
    /// \brief Symbologies Identifiers definition
    ///
    typedef enum fnxPartialSymid
    {
        FNX_ID_PARTIAL_UNKNOWN    = 1000,  ///< Unknown symbology
        FNX_ID_PARTIAL_CODE39     = 1001,  ///< Partial Code 39 symbology identifier
        FNX_ID_PARTIAL_EAN13_UPCA = 1002,  ///< Partial EAN-13/UPC-A symbology identifier
        FNX_ID_PARTIAL_EAN8       = 1003,  ///< Partial EAN-8 symbology identifier
        FNX_ID_PARTIAL_CODE128    = 1004,  ///< Partial Code 128/GS1-128 symbology identifier
    } fnxPartialSymid;

    ///
    /// \brief Partial decode type
    ///
    typedef enum fnxPartialDecodeType
    {
        FNX_DECODED_FROM_START = 0,  ///< Partial decode from barcode start
        FNX_DECODED_FROM_STOP  = 1,  ///< Partial decode from barcode stop
        FNX_FULL_BARCODE       = 2,  ///< Full barcode with some missing or bad codewords
    } fnxPartialDecodeType;

    ///
    /// \brief Partial decoded message 
    ///
    typedef struct fnxPartialMessage
    {
        const char*            data;                ///<  Pointer to output string data
        unsigned int           dataLength;          ///<  Length of output string in bytes
        unsigned int           format;              ///<  Format of output data

    } fnxPartialMessage;

    ///
    /// \brief Partial decoding result 
    ///
    typedef struct fnxPartialResult
    {
        fnxPartialDecodeType   partialDecodeType;   ///<  Partial decode type
        unsigned int           barcodeScore;        ///<  Partial barcode decoding score
        unsigned int           nbCodewords;         ///<  Number of codewords
        const unsigned char*   codewords;           ///<  Pointer to output codewords
        const unsigned char*   codewordScores;      ///<  Pointer to output codeword scores
        fnxPartialSymid        partialSymid;        ///<  fnxPartialSymid symbology identifier
        unsigned int           nbPossibleMessages;  ///<  Number of possible partial messages          
        fnxPartialMessage*     possibleMessages;    ///<  Pointer to an array of partial messages
        fnxPoint               corners[4];          ///<  Coordinates of decoded code frame

    } fnxPartialResult;

    // -------------------------------------------------------
    //  API function definitions
    // -------------------------------------------------------

    /// \brief Definition of the partial result callback
    /// 
    /// The partial result callback is called by a decoder when a barcode has been partially decoded.
    /// When used in a object-oriented programming context, caller parameter must points to the object that hold the callback method. 
    /// Caller parameter is null otherwise.
    /// 
    /// \param result   partial decoder result  
    /// \param callerContext   caller specific data passed to the fnxSetResultCallback function
    /// 
    typedef int           (*fnxPartialResultCallbackPtr)    (const fnxPartialResult* result, void* callerContext);


    /// \brief Set the partial result callback
    /// 
    /// \param handle   handle of the decoder
    /// \param partialResultCallback callback function   
    /// \param callerContext caller specific data to retrieve when the callback function is called (i.e. it can be used to pass the pointer to the caller object, or the handle of the decoder ...)
    /// \return status code
    /// 
    PHENIX_API fnxStatus   fnxSetPartialResultCallback(int handle, fnxPartialResultCallbackPtr partialResultCallback, void* callerContext);


#ifdef __cplusplus
}  // extern "C"
#endif /* __cplusplus */


#endif  // PHENIX_PARTIAL_DECODE_API_H