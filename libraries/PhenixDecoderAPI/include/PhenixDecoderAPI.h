///
/// \file PhenixDecoderAPI.h
/// \brief This header file defines API functions and data structures
///

#ifndef PHENIX_DECODER_API_H
#define PHENIX_DECODER_API_H

#include "PhenixSettingsAPI.h"

/// \cond
#if !defined(PHENIX_STATIC_LIB) && !defined(PHENIX_SHARED_LIB)
   #define PHENIX_SHARED_LIB  1
#endif
/// \endcond
/// 
#if defined(__ANDROID__)
    #define PHENIX_API
#elif defined(__GNUC__)
    #if PHENIX_SHARED_LIB
        #define PHENIX_API   __attribute__((visibility("default")))
    #else
        #define PHENIX_API
    #endif  // PHENIX_SHARED_LIB
#elif defined(_MSC_VER)
    #if PHENIX_SHARED_LIB
        #ifdef PHENIX_API_EXPORTS
            #define PHENIX_API   __declspec(dllexport)
        #else
            #define PHENIX_API   __declspec(dllimport)
        #endif
    #else
        #define PHENIX_API
    #endif  // PHENIX_SHARED_LIB
#endif  // __GNUC__

#ifdef __cplusplus
#ifndef EMSCRIPTEN
extern "C" {
#endif
#endif  // __cplusplus

    // -----------------------------------------------------
    //  Data types definition
    // -------------------------------------------------------

    ///
    /// \brief Status definition
    ///
    typedef enum fnxStatus
    {
        FNX_SUCCESS                       = 0,      ///< Function call succeeded
        FNX_INVALID_HANDLE                = 1,      ///< An invalid decoder handle was passed to the function
        FNX_MEMORY_ALLOCATION_ERROR       = 3,      ///< Decoder was not able to allocate memory
        FNX_UNSUPPORTED                   = 4,      ///< The function is not supported in this version
        FNX_SETTING_TAG_UNKNOWN           = 5,      ///< Provided SettingTag is not valid
        FNX_SETTING_VALUE_INVALID         = 6,      ///< Provided value associated with this SettingTag is not valid
        FNX_IMAGE_FORMAT_NOT_SUPPORTED    = 7,      ///< Input image format is not supported
        FNX_IMAGE_SIZE_NOT_SUPPORTED      = 8,      ///< Image size is too small (< 48 pixels)
        FNX_SETTING_TAG_NOT_LICENSED      = 9,      ///< Provided SettingTag is not licensed
        FNX_INVALID_CONTEXT               = 10,     ///< Function call is invalid in current context
        FNX_LICENSE_ACTIVATION_FAILED     = 1001,   ///< The license activation failed
        FNX_LICENSE_EXPIRED               = 1020,   ///< The license has expired or system time has been tampered
        FNX_LICENSE_SUSPENDED             = 1021,   ///< The license has been suspended
        FNX_LICENSE_GRACE_PERIOD_OVER     = 1022,   ///< The grace period for server sync is over
        FNX_INVALID_FILE_PATH             = 1040,   ///< Invalid file path
        FNX_FILE_PERMISSION               = 1045,   ///< No permission to write to file.
        FNX_LICENSE_TIME_ERROR            = 1047,   ///< The system time and the network time are different
        FNX_LICENSE_NETWORK_ERROR         = 1048,   ///< The connection to the server failed due to network error
        FNX_LICENSE_REVOKED               = 1053,   ///< The license has been revoked
        FNX_LICENSE_INVALID_KEY           = 1054,   ///< The license key is invalid
        FNX_LICENSE_INVALID_TYPE          = 1055,   ///< Invalid license type. Make sure floating license is not being used
        FNX_LICENSE_ACTIVATION_LIMIT      = 1058,   ///< The license has reached its allowed activations limit
        FNX_LICENSE_ACTIVATION_NOT_FOUND  = 1059,   ///< The license activation was deleted on the server
        FNX_LICENSE_DEACTIVATION_LIMIT    = 1060,   ///< The license has reached it's allowed deactivations limit
        FNX_LICENSE_MACHINE_FINGERPRINT   = 1063,   ///< The device fingerprint has changed
        FNX_LICENSE_TIME_MODIFIED         = 1069,   ///< The system time has been tampered (backdated)
        FNX_LICENSE_RELEASE_VERSION_ERROR = 1077,   ///< The release version is not allowed
        FNX_LICENSE_VM_ERROR              = 1080,   ///< Running in VM: please contact us at support@viziotix.com
        FNX_LICENSE_COUNTRY_ERROR         = 1081,   ///< Country is not allowed
        FNX_LICENSE_IP_ERROR              = 1082,   ///< IP address is not allowed
        FNX_LICENSE_CONTAINER_ERROR       = 1083,   ///< Running in container: please contact us at support@viziotix.com
        FNX_LICENSE_SERVER_ERROR          = 1091,   ///< Server error
        FNX_PA_APPLICATION_NAME_ERROR     = 1401,   ///< Post activation error: Application name error
        FNX_PA_RELEASE_VERSION_ERROR      = 1402,   ///< Post activation error: The release version is not allowed
        FNX_PA_PLATFORM_ERROR             = 1403,   ///< Post activation error: The platform is not allowed
        FNX_OP_LICENSE_ACTIVATION_FAILED  = 1501,   ///< The on-premise license activation failed
        FNX_OP_LICENSE_INVALID_URL        = 1542,   ///< Missing or invalid on-premise server url
        FNX_OP_LICENSE_TIME_ERROR         = 1543,   ///< The on-premise system time and the network time are different
        FNX_OP_LICENSE_NETWORK_ERROR      = 1544,   ///< The connection to the on-premise server failed due to network error
        FNX_OP_LICENSE_NOT_FOUND          = 1547,   ///< The on-premise license does not exist on server or has already expired (the request to refresh the license is delayed)
        FNX_OP_LICENSE_EXPIRED_INET       = 1548,   ///< The on-premise license lease has expired due to network error (the request to refresh the license fails due to network error)
        FNX_OP_LICENSE_ACTIVATION_LIMIT   = 1549,   ///< The on-premise license has reached its allowed activations limit
        FNX_OP_LICENSE_SERVER_ERROR       = 1571,   ///< On-premise server error
        FNX_OP_LICENSE_TIME_MODIFIED      = 1572,   ///< The on-premise server system time has been tampered (backdated)
        FNX_OP_LICENSE_NOT_ACTIVATED      = 1573,   ///< The on-premise server has not been activated using a license key
        FNX_OP_LICENSE_EXPIRED            = 1574,   ///< The on-premise server license has expired
        FNX_OP_LICENSE_SUSPENDED          = 1575,   ///< The on-premise server license has been suspended
        FNX_OP_LICENSE_GRACE_PERIOD_OVER  = 1576,   ///< The on-premise server grace period for server sync is over
    } fnxStatus;

    ///
    /// \brief Symbologies Identifiers definition
    ///
    typedef enum fnxSymid
    {
        FNX_ID_UNKNOWN             = 0,           ///< Unknown symbology
        FNX_ID_DATAMATRIX          = 1,           ///< Datamatrix symbology identifier
        FNX_ID_CODE39              = 2,           ///< Code 39 symbology identifier
        FNX_ID_QRCODE              = 3,           ///< Qr Code symbology identifier
        FNX_ID_UPCA                = 4,           ///< UPC-A symbology identifier
        FNX_ID_UPCE                = 5,           ///< UPC-E symbology identifier
        FNX_ID_EAN13               = 6,           ///< EAN-13 symbology identifier
        FNX_ID_EAN8                = 7,           ///< EAN-8 symbology identifier
        FNX_ID_ITF                 = 8,           ///< Interleave 2 of 5 symbology identifier
        FNX_ID_CODE128             = 9,           ///< Code 128 symbology identifier
        FNX_ID_PDF417              = 10,          ///< PDF417 symbology identifier
        FNX_ID_GS1_DATABAR         = 11,          ///< GS1 Databar symbology identifier
        FNX_ID_GS1_DATABAR_EX      = 12,          ///< GS1 Databar Expanded symbology identifier
        FNX_ID_GS1_DATABAR_LIMITED = 13,          ///< GS1 Databar Limited symbology identifier
        FNX_ID_AZTEC               = 14,          ///< Aztec Code symbology identifier
        FNX_ID_GS1_128             = 15,          ///< GS1-128 symbology identifier
        FNX_ID_GS1_DATAMATRIX      = 16,          ///< GS1 Datamatrix symbology identifier
        FNX_ID_MSI                 = 17,          ///< MSI symbology identifier
        FNX_ID_CODE32              = 18,          ///< Code 32 symbology identifier
        FNX_ID_ITF_14              = 19,          ///< ITF-14 symbology identifier
        FNX_ID_ISBT128             = 20,          ///< ISBT128 symbology identifier
        FNX_ID_UPCA_ADDON2         = 21,          ///< UPC-A with Addon 2 symbology identifier
        FNX_ID_UPCA_ADDON5         = 22,          ///< UPC-A with Addon 5 symbology identifier
        FNX_ID_UPCE_ADDON2         = 23,          ///< UPC-E with Addon 2 symbology identifier
        FNX_ID_UPCE_ADDON5         = 24,          ///< UPC-E with Addon 5 symbology identifier
        FNX_ID_EAN13_ADDON2        = 25,          ///< EAN-13 with Addon 2 symbology identifier
        FNX_ID_EAN13_ADDON5        = 26,          ///< EAN-13 with Addon 5 symbology identifier
        FNX_ID_CODE93              = 27,          ///< Code 93 symbology identifier
        FNX_ID_CODABAR             = 28,          ///< Codabar symbology identifier
        FNX_ID_OCR_MRZ             = 100,         ///< OCR-MRZ symbology identifier
    } fnxSymid;

    ///
    /// \brief Image format definition
    ///
    typedef enum fnxImageFormat
    {
        FNX_Y800  = 0,   ///< Monochrome 8-bit per pixel image format
        FNX_JPEG  = 1,   ///< Jpeg compressed image format
        FNX_RGB   = 2,   ///< 3 color channels per pixel (Red-Green-Blue ordering). Each channel is coded over 8 bits.
        FNX_BGR   = 3,   ///< 3 color channels per pixel (Blue-Green-Red ordering). Each channel is coded over 8 bits.
        FNX_PNG   = 4,   ///< PNG compressed image format
        FNX_BMP   = 5,   ///< BMP image format
        FNX_RGBA  = 6,   ///< 4 color channels per pixel (Red-Green-Blue-Alpha). Each channel is coded over 8 bits.
        FNX_YUYV  = 7,   ///< Packed YUV format coded as YUYV for 2 pixels. Each channel is coded over 8 bits.
        FNX_UYVY  = 8,   ///< Packed YUV format coded as UYVY for 2 pixels. Each channel is coded over 8 bits.
        FNX_BYR   = 9,   ///< Bayer RAW format. Each channel is coded over 8 bits.
        FNX_ARGB  = 10,  ///< 4 color channels per pixel (Alpha-Red-Green-Blue). Each channel is coded over 8 bits.
        FNX_BGRA  = 11,  ///< 4 color channels per pixel (Blue-Green-Red-Alpha). Each channel is coded over 8 bits.
        FNX_ABGR  = 12,  ///< 4 color channels per pixel (Alpha-Blue-Green-Red). Each channel is coded over 8 bits.
        FNX_BYR10 = 13,  ///< Bayer RAW format. Each channel is coded over 10 bits.

    } fnxImageFormat;

    ///
    /// \brief 2D Point definition
    ///
    typedef struct fnxPoint
    {
        int   x;    ///< x coordinate of this point
        int   y;    ///< y coordinate of this point

    } fnxPoint;

    ///
    /// \brief Image definition
    ///
    typedef struct fnxImage
    {
        unsigned char* data;                ///<  Pointer to image byte data
        unsigned int   width;               ///<  Width of image in pixels
        unsigned int   height;              ///<  Height of image in pixels
        unsigned int   stride;              ///<  Stride of image in bytes
        unsigned int   nb_bytes;            ///<  number of bytes in data buffer (setting this field is mandatory with Image format FNX_JPEG, FNX_PNG and FNX_BMP) 
        fnxImageFormat format;              ///<  Image format
        fnxPoint       aimer;               ///<  Aiming position in image (not used at the moment)

    } fnxImage;

    ///
    /// \brief Decoding result 
    ///
    typedef struct fnxResult
    {
        const char*     data;                ///<  Pointer to output string data       
        unsigned int    length;              ///<  Length of output string in bytes     
        fnxSymid        symid;               ///<  Symbology identifier
        unsigned int    format;              ///<  Format of output data 
        fnxPoint        corners[4];          ///<  Coordinates of decoded code frame

    } fnxResult;

    // -------------------------------------------------------
    //  API function definitions
    // -------------------------------------------------------

    ///
    /// \brief Get the library version number
    /// 
    /// \return null terminated string that contains the library version number.
    /// 
    PHENIX_API const char* fnxGetLibraryVersion(void);

    ///
    /// \brief Initialize decoder library internal state and verify status of license activation
    /// 
    /// This function must be called prior to any other decoder library functions except GetLibraryVersion
    /// 
    /// \return status code
    ///
    PHENIX_API fnxStatus   fnxInitializeLibrary(void);

    ///
    /// \brief Deinitialize decoder library
    /// 
    /// This function can be called to drop hosted-floating or on-premise-floating licenses
    /// 
    /// \return status code
    ///
    PHENIX_API fnxStatus   fnxDeinitializeLibrary(void);

    ///
    /// \brief Activate license
    /// 
    ///  This function must be called when initializing library returns a license activation error
    /// 
    /// \param  activation_key  null terminated string containing license activation key
    /// \return status code
    /// 
    PHENIX_API fnxStatus   fnxActivateLicense(const char* activation_key);

    ///
    /// \brief Create a new decoder
    /// 
    /// \return     handle of the newly created decoder larger than zero if success, zero if failed. 
    /// 
    PHENIX_API int         fnxCreateDecoder();

    ///
    /// \brief Destroy a decoder
    /// 
    /// \param handle   handle of the decoder to be destroyed
    /// \return status code
    /// 
    PHENIX_API fnxStatus   fnxDestroyDecoder(int handle);


    /// \brief Definition of the result callback
    /// 
    /// The result callback is called by a decoder when decoding is successful to transmit result output.
    /// When used in a object-oriented programming context, caller parameter must points to the object that hold the callback method. 
    /// Caller parameter is null otherwise.
    /// 
    /// \param result   decoder result  
    /// \param callerContext   caller specific data passed to the fnxSetResultCallback function
    /// 
    typedef int           (*fnxResultCallbackPtr)    (const fnxResult* result, void* callerContext); 


    /// \brief Set the result callback
    /// 
    /// \param handle   handle of the decoder
    /// \param resultCallback callback function   
    /// \param callerContext caller specific data to retrieve when the callback function is called (i.e. it can be used to pass the pointer to the caller object, or the handle of the decoder ...)
    /// \return status code
    /// 
    PHENIX_API fnxStatus   fnxSetResultCallback(int handle, fnxResultCallbackPtr resultCallback, void* callerContext);


    /// \brief Process image to be decoded
    /// 
    /// \param handle   handle of the decoder
    /// \param pImage   pointer to image to be decoded
    /// \return status code
    /// 
    PHENIX_API fnxStatus   fnxProcessImage(int handle, fnxImage* pImage);


    /// \brief Stop current decode process
    /// 
    /// \param handle   handle of the decoder
    /// \return status code
    /// 
    PHENIX_API fnxStatus   fnxStopProcessing(int handle);


    /// \brief Read integer settings
    /// 
    /// \param handle         handle of the decoder
    /// \param setting_tag    tag identifier of the setting 
    /// \param setting_value  output value of the setting 
    /// \return status code
    /// 
    PHENIX_API fnxStatus   fnxReadIntSetting(int handle, fnxSettingTag setting_tag, int* setting_value);


    /// \brief Write integer value of a setting
    /// 
    /// \param handle         handle of the decoder
    /// \param setting_tag    tag identifier of the setting 
    /// \param setting_value  value of the setting
    /// \return status code
    /// 
    PHENIX_API fnxStatus   fnxWriteIntSetting(int handle, fnxSettingTag setting_tag, int setting_value);


    /// \brief Read string value of a setting
    /// 
    /// \param handle               handle of the decoder
    /// \param setting_tag          tag identifier of the setting 
    /// \param buffer               output content buffer of the setting
    /// \param n_bytes_in_buffer    output number of bytes in content buffer
    /// \return status code   
    /// 
    PHENIX_API fnxStatus   fnxReadBufferSetting(int handle, fnxSettingTag setting_tag, unsigned char** buffer, int* n_bytes_in_buffer);


    /// \brief Write string value of a setting
    /// 
    /// \param handle               handle of the decoder
    /// \param setting_tag          tag identifier of the setting 
    /// \param buffer               input content buffer of the setting 
    /// \param n_bytes_in_buffer    input number of bytes in content buffer
    /// \return status code   
    ///
    PHENIX_API fnxStatus   fnxWriteBufferSetting(int handle, fnxSettingTag setting_tag, unsigned char* buffer, int n_bytes_in_buffer);


    /// \brief Get optional data during result callback
    /// 
    /// \param reserved             reserved value, should be set to 0
    /// \param buffer               output content C string of optional data in Json format
    /// \param n_bytes_in_buffer    output number of bytes in content buffer 
    /// \return status code   
    ///
    PHENIX_API fnxStatus   fnxGetOptionalData(int reserved, const char** buffer, int* n_bytes_in_buffer);


    ///
    /// \brief Offline Activation Request
    /// 
    ///  This function must be called when an offline activation is required.
    /// 
    /// \param  activation_key  null terminated string containing license activation key
    /// \param  filepath        null terminated string to the path where the request file will be written
    /// \return status code
    /// 
    PHENIX_API fnxStatus   fnxOfflineActivationRequest(const char* activation_key, const char * filepath);
    
    
    ///
    /// \brief Activate License Offline
    /// 
    ///  This function must be called when an offline activation is required.
    /// 
    /// \param  filepath         null terminated string with the full pathname of the offline activation file
    /// \return status code
    /// 
    PHENIX_API fnxStatus   fnxOfflineActivateLicense(const char* filepath);


#ifdef __cplusplus
#ifndef EMSCRIPTEN
}  // extern "C"
#endif
#endif /* __cplusplus */


#endif  // PHENIX_DECODER_API_H