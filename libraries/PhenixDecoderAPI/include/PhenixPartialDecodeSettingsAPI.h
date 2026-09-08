///
/// \file PhenixPartialDecodeSettingsAPI.h
/// \brief This header file defines SettingTag enumeration
///

#ifndef PHENIX_PARTIAL_DECODE_SETTINGS_API_H
#define PHENIX_PARTIAL_DECODE_SETTINGS_API_H

#include "PhenixSettingsAPI.h"

    // -------------------------------------------------------
    //  Settings definition
    // -------------------------------------------------------

    ///
    /// \brief Specific settings for partial decoding
    ///
    #define FNX_CODE39_PARTIAL_DECODING  (fnxSettingTag)0x0160    ///< Enable partial decoding for Code39.\n Valid input values are: <ul><li>0 : disable (default)</li><li>1 : enable</li></ul>
    #define FNX_EAN_UPC_PARTIAL_DECODING (fnxSettingTag)0x0260    ///< Enable partial decoding for EAN13, EAN8 and UPCA.\n Valid input values are: <ul><li>0 : disable (default)</li><li>1 : enable</li></ul>
    #define FNX_CODE128_PARTIAL_DECODING (fnxSettingTag)0x0760    ///< Enable partial decoding for Code 128 and GS1-128.\n Valid input values are: <ul><li>0 : disable (default)</li><li>1 : enable</li></ul>

#endif
