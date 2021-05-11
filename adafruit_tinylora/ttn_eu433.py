# SPDX-FileCopyrightText: 2018 Brent Rubell for Adafruit Industries
# SPDX-FileCopyrightText: 2021 Thomas Steen Rasmussen
#
# SPDX-License-Identifier: MIT
"""
`ttn_eu433.py`
======================================================
The Things Network Frequency Plans - EU433
* Author(s): Thomas Steen Rasmussen
"""
# 433175000 Hz / 61.035 Hz = 7097157 = 0x6C4B45
TTN_FREQS = {
    0: (0x6C, 0x4B, 0x45),  # 433.175 MHz
    1: (0x6C, 0x58, 0x12),  # 433.375 MHz
    2: (0x6C, 0x64, 0xDE),  # 433.575 MHz
    3: (0x6C, 0x71, 0xAB),  # 433.775 MHz
    4: (0x6C, 0x7E, 0x78),  # 433.975 MHz
    5: (0x6C, 0x8B, 0x45),  # 434.175 MHz
    6: (0x6C, 0x98, 0x12),  # 434.375 MHz
    7: (0x6D, 0xA4, 0xDF),  # 434.575 MHz
}
