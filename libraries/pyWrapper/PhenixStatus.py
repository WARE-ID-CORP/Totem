from enum import IntEnum


class fnxStatus(IntEnum):
    FNX_SUCCESS                       = 0       ## Function call succeeded
    FNX_INVALID_HANDLE                = 1       ## An invalid decoder handle was passed to the function
    FNX_MEMORY_ALLOCATION_ERROR       = 3       ## Decoder was not able to allocate memory
    FNX_UNSUPPORTED                   = 4       ## The function is not supported in this version
    FNX_SETTING_TAG_UNKNOWN           = 5       ## Provided SettingTag is not valid
    FNX_SETTING_VALUE_INVALID         = 6       ## Provided value associated with this SettingTag is not valid
    FNX_IMAGE_FORMAT_NOT_SUPPORTED    = 7       ## Input image format is not supported
    FNX_IMAGE_SIZE_NOT_SUPPORTED      = 8       ## Image size is too small (< 48 pixels)
    FNX_SETTING_TAG_NOT_LICENSED      = 9       ## Provided SettingTag is not licensed
    FNX_INVALID_CONTEXT               = 10      ## Function call is invalid in current context
    FNX_LICENSE_ACTIVATION_FAILED     = 1001    ## The license activation failed
    FNX_LICENSE_EXPIRED               = 1020    ## The license has expired or system time has been tampered
    FNX_LICENSE_SUSPENDED             = 1021    ## The license has been suspended
    FNX_LICENSE_GRACE_PERIOD_OVER     = 1022    ## The grace period for server sync is over
    FNX_INVALID_FILE_PATH             = 1040    ## Invalid file path
    FNX_FILE_PERMISSION               = 1045    ## No permission to write to file.
    FNX_LICENSE_TIME_ERROR            = 1047    ## The system time and the network time are different
    FNX_LICENSE_NETWORK_ERROR         = 1048    ## The connection to the server failed due to network error
    FNX_LICENSE_REVOKED               = 1053    ## The license has been revoked
    FNX_LICENSE_INVALID_KEY           = 1054    ## The license key is invalid
    FNX_LICENSE_INVALID_TYPE          = 1055    ## Invalid license type. Make sure floating license is not being used
    FNX_LICENSE_ACTIVATION_LIMIT      = 1058    ## The license has reached its allowed activations limit
    FNX_LICENSE_ACTIVATION_NOT_FOUND  = 1059    ## The license activation was deleted on the server
    FNX_LICENSE_DEACTIVATION_LIMIT    = 1060    ## The license has reached it's allowed deactivations limit
    FNX_LICENSE_MACHINE_FINGERPRINT   = 1063    ## The device fingerprint has changed
    FNX_LICENSE_TIME_MODIFIED         = 1069    ## The system time has been tampered (backdated)
    FNX_LICENSE_RELEASE_VERSION_ERROR = 1077    ## The release version is not allowed
    FNX_LICENSE_VM_ERROR              = 1080    ## Running in VM: please contact us at support@viziotix.com
    FNX_LICENSE_COUNTRY_ERROR         = 1081    ## Country is not allowed
    FNX_LICENSE_IP_ERROR              = 1082    ## IP address is not allowed
    FNX_LICENSE_CONTAINER_ERROR       = 1083    ## Running in container: please contact us at support@viziotix.com
    FNX_LICENSE_SERVER_ERROR          = 1091    ## Server error
    FNX_PA_APPLICATION_NAME_ERROR     = 1401    ## Post activation error: Application name error
    FNX_PA_RELEASE_VERSION_ERROR      = 1402    ## Post activation error: The release version is not allowed
    FNX_PA_PLATFORM_ERROR             = 1403    ## Post activation error: The platform is not allowed
    FNX_OP_LICENSE_ACTIVATION_FAILED  = 1501    ## The on-premise license activation failed
    FNX_OP_LICENSE_INVALID_URL        = 1542    ## Missing or invalid on-premise server url
    FNX_OP_LICENSE_TIME_ERROR         = 1543    ## The on-premise system time and the network time are different
    FNX_OP_LICENSE_NETWORK_ERROR      = 1544    ## The connection to the on-premise server failed due to network error
    FNX_OP_LICENSE_NOT_FOUND          = 1547    ## The on-premise license does not exist on server or has already expired (the request to refresh the license is delayed)
    FNX_OP_LICENSE_EXPIRED_INET       = 1548    ## The on-premise license lease has expired due to network error (the request to refresh the license fails due to network error)
    FNX_OP_LICENSE_ACTIVATION_LIMIT   = 1549    ## The on-premise license has reached its allowed activations limit
    FNX_OP_LICENSE_SERVER_ERROR       = 1571    ## On-premise server error
    FNX_OP_LICENSE_TIME_MODIFIED      = 1572    ## The on-premise server system time has been tampered (backdated)
    FNX_OP_LICENSE_NOT_ACTIVATED      = 1573    ## The on-premise server has not been activated using a license key
    FNX_OP_LICENSE_EXPIRED            = 1574    ## The on-premise server license has expired
    FNX_OP_LICENSE_SUSPENDED          = 1575    ## The on-premise server license has been suspended
    FNX_OP_LICENSE_GRACE_PERIOD_OVER  = 1576    ## The on-premise server grace period for server sync is over


fnxStatusMessages = {
    fnxStatus.FNX_SUCCESS                       : "Function call succeeded",
    fnxStatus.FNX_INVALID_HANDLE                : "An invalid decoder handle was passed to the function",
    fnxStatus.FNX_MEMORY_ALLOCATION_ERROR       : "Decoder was not able to allocate memory",
    fnxStatus.FNX_UNSUPPORTED                   : "The function is not supported in this version",
    fnxStatus.FNX_SETTING_TAG_UNKNOWN           : "Provided SettingTag is not valid",
    fnxStatus.FNX_SETTING_VALUE_INVALID         : "Provided value associated with this SettingTag is not valid",
    fnxStatus.FNX_IMAGE_FORMAT_NOT_SUPPORTED    : "Input image format is not supported",
    fnxStatus.FNX_IMAGE_SIZE_NOT_SUPPORTED      : "Image size is too small (< 48 pixels)",
    fnxStatus.FNX_SETTING_TAG_NOT_LICENSED      : "Provided SettingTag is not licensed",
    fnxStatus.FNX_INVALID_CONTEXT               : "Function call is invalid in current context",
    fnxStatus.FNX_LICENSE_ACTIVATION_FAILED     : "The license activation failed",
    fnxStatus.FNX_LICENSE_EXPIRED               : "The license has expired or system time has been tampered",
    fnxStatus.FNX_LICENSE_SUSPENDED             : "The license has been suspended",
    fnxStatus.FNX_LICENSE_GRACE_PERIOD_OVER     : "The grace period for server sync is over",
    fnxStatus.FNX_INVALID_FILE_PATH             : "Invalid file path",
    fnxStatus.FNX_FILE_PERMISSION               : "No permission to write to file.",
    fnxStatus.FNX_LICENSE_TIME_ERROR            : "The system time and the network time are different",
    fnxStatus.FNX_LICENSE_NETWORK_ERROR         : "The connection to the server failed due to network error",
    fnxStatus.FNX_LICENSE_REVOKED               : "The license has been revoked",
    fnxStatus.FNX_LICENSE_INVALID_KEY           : "The license key is invalid",
    fnxStatus.FNX_LICENSE_INVALID_TYPE          : "Invalid license type. Make sure floating license is not being used",
    fnxStatus.FNX_LICENSE_ACTIVATION_LIMIT      : "The license has reached its allowed activations limit",
    fnxStatus.FNX_LICENSE_ACTIVATION_NOT_FOUND  : "The license activation was deleted on the server",
    fnxStatus.FNX_LICENSE_DEACTIVATION_LIMIT    : "The license has reached it's allowed deactivations limit",
    fnxStatus.FNX_LICENSE_MACHINE_FINGERPRINT   : "The device fingerprint has changed",
    fnxStatus.FNX_LICENSE_TIME_MODIFIED         : "The system time has been tampered (backdated)",
    fnxStatus.FNX_LICENSE_RELEASE_VERSION_ERROR : "The release version is not allowed",
    fnxStatus.FNX_LICENSE_VM_ERROR              : "Running in VM: please contact us at support@viziotix.com",
    fnxStatus.FNX_LICENSE_COUNTRY_ERROR         : "Country is not allowed",
    fnxStatus.FNX_LICENSE_IP_ERROR              : "IP address is not allowed",
    fnxStatus.FNX_LICENSE_CONTAINER_ERROR       : "Running in container: please contact us at support@viziotix.com",
    fnxStatus.FNX_LICENSE_SERVER_ERROR          : "Server error",
    fnxStatus.FNX_PA_APPLICATION_NAME_ERROR     : "Post activation error: Application name error",
    fnxStatus.FNX_PA_RELEASE_VERSION_ERROR      : "Post activation error: The release version is not allowed",
    fnxStatus.FNX_PA_PLATFORM_ERROR             : "Post activation error: The platform is not allowed",
    fnxStatus.FNX_OP_LICENSE_ACTIVATION_FAILED  : "The on-premise license activation failed",
    fnxStatus.FNX_OP_LICENSE_INVALID_URL        : "Missing or invalid on-premise server url",
    fnxStatus.FNX_OP_LICENSE_TIME_ERROR         : "The on-premise system time and the network time are different",
    fnxStatus.FNX_OP_LICENSE_NETWORK_ERROR      : "The connection to the on-premise server failed due to network error",
    fnxStatus.FNX_OP_LICENSE_NOT_FOUND          : "The on-premise license does not exist on server or has already expired (the request to refresh the license is delayed)",
    fnxStatus.FNX_OP_LICENSE_EXPIRED_INET       : "The on-premise license lease has expired due to network error (the request to refresh the license fails due to network error)",
    fnxStatus.FNX_OP_LICENSE_ACTIVATION_LIMIT   : "The on-premise license has reached its allowed activations limit",
    fnxStatus.FNX_OP_LICENSE_SERVER_ERROR       : "On-premise server error",
    fnxStatus.FNX_OP_LICENSE_TIME_MODIFIED      : "The on-premise server system time has been tampered (backdated)",
    fnxStatus.FNX_OP_LICENSE_NOT_ACTIVATED      : "The on-premise server has not been activated using a license key",
    fnxStatus.FNX_OP_LICENSE_EXPIRED            : "The on-premise server license has expired",
    fnxStatus.FNX_OP_LICENSE_SUSPENDED          : "The on-premise server license has been suspended",
    fnxStatus.FNX_OP_LICENSE_GRACE_PERIOD_OVER  : "The on-premise server grace period for server sync is over",
}


def getStatusMessage(status: fnxStatus)-> str:
    try:
        return fnxStatusMessages[status]
    except:
        return  "fnxStatus code %d, Please contact us at support@viziotix.com" % int(status)
