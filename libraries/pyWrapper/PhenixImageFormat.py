from enum import IntEnum


class fnxImageFormat(IntEnum):

    FNX_Y800    = 0,   ## Monochrome 8-bit per pixel image format
    FNX_JPEG    = 1,   ## Jpeg compressed image format
    FNX_RGB     = 2,   ## 3 color channels per pixel (Red-Green-Blue ordering). Each channel is coded over 8 bits.
    FNX_BGR     = 3,   ## 3 color channels per pixel (Blue-Green-Red ordering). Each channel is coded over 8 bits.
    FNX_PNG     = 4,   ## PNG compressed image format
    FNX_BMP     = 5,   ## BMP image format
    FNX_RGBA    = 6,   ## 4 color channels per pixel (Red-Green-Blue-Alpha). Each channel is coded over 8 bits.
    FNX_YUYV    = 7,   ## Packed YUV format coded as YUYV for 2 pixels. Each channel is coded over 8 bits.
    FNX_UYVY    = 8,   ## Packed YUV format coded as UYVY for 2 pixels. Each channel is coded over 8 bits.
    FNX_BYR     = 9,   ## Bayer RAW format. Each channel is coded over 8 bits.
    FNX_ARGB    = 10,  ## 4 color channels per pixel (Alpha-Red-Green-Blue). Each channel is coded over 8 bits.
    FNX_BGRA    = 11,  ## 4 color channels per pixel (Blue-Green-Red-Alpha). Each channel is coded over 8 bits.
    FNX_ABGR    = 12,  ## 4 color channels per pixel (Alpha-Blue-Green-Red). Each channel is coded over 8 bits.
    FNX_BYR10   = 13,  ## Bayer RAW format. Each channel is coded over 10 bits.
