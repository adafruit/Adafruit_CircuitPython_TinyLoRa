# AES-Python, Copyright (C) 2012 Bo Zhu http://about.bozhu.me
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# Modified by Brent Rubell for Adafruit Industries
"""
`adafruit_tinylora_encryption.py`
======================================================
Required tinyLoRA Encryption Methods for AES and
Message Integrity checks.
* Author(s): adafruit
"""
# from http://cs.ucsb.edu/~koc/cs178/projects/JT/aes.c
def xtime(col):
    """xtime impl. for _mix_single_column()
    """
    return (((col << 1) ^ 0x1B) & 0xFF) if (col & 0x80) else (col << 1)

# AES S-box
S_BOX = [
    [0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
     0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76],
    [0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
     0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0],
    [0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
     0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15],
    [0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
     0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75],
    [0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
     0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84],
    [0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
     0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF],
    [0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
     0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8],
    [0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
     0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2],
    [0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
     0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73],
    [0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
     0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB],
    [0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
     0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79],
    [0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
     0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08],
    [0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
     0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A],
    [0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
     0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E],
    [0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
     0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF],
    [0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
     0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16]]


class AES():
    """TinyLoRA AES Implementation
    Functions in this implementation are from and/or derived from AES-Python
    (https://github.com/bozhu/AES-Python) and TinyLoRa ()
    """

    def __init__(self, device_address, app_key, network_key, frame_counter):
        self._app_key = app_key
        self._device_address = device_address
        self._network_key = network_key
        self.frame_counter = frame_counter

    def encrypt(self, aes_data):
        """Performs AES Encryption routine with data.
        :param bytearray data: Data to-be encrypted.
        """
        self.encrypt_payload(aes_data)
        return aes_data

    def encrypt_payload(self, data):
        """Encrypts data payload.
        :param bytearray data: Data to-be-encrypted.
        """
        block_a = bytearray(16)
        # calculate required number of blocks
        num_blocks = len(data) // 16
        incomplete_block_size = len(data) % 16
        if incomplete_block_size != 0:
            num_blocks += 1
        # k = data ptr
        k = 0
        i = 1
        while i <= 1:
            block_a[0] = 0x01
            block_a[1] = 0x00
            block_a[2] = 0x00
            block_a[3] = 0x00
            block_a[4] = 0x00
            block_a[5] = 0x00
            # block from device_address, MSB first
            block_a[6] = self._device_address[3]
            block_a[7] = self._device_address[2]
            block_a[8] = self._device_address[1]
            block_a[9] = self._device_address[0]
            # block from frame counter
            block_a[10] = (self.frame_counter & 0x00FF)
            block_a[11] = ((self.frame_counter >> 8) & 0x00FF)
            block_a[12] = 0x00
            block_a[13] = 0x00
            block_a[14] = 0x00
            block_a[15] = i
            # calculate S
            self._aes_encrypt(block_a, self._app_key)
            # check for last block
            if i != num_blocks:
                for j in range(16):
                    data[k] ^= block_a[j]
                    k += 1
            else:
                if incomplete_block_size == 0:
                    incomplete_block_size = 16
                for j in range(incomplete_block_size):
                    data[k] ^= block_a[j]
                    k += 1
            i += 1

    def _aes_encrypt(self, data, key):
        """Performs 9 rounds of AES encryption on data per TinyLoRa spec.
        NOTE: This is not an accurate aes_encrypt impl., tinylora performs
        an additional key calculation after 9 rounds.
        :param bytearray data: Data array.
        :param bytearray key: Round Key Array.
        """
        state = [['0', '0', '0', '0'],
                 ['0', '0', '0', '0'],
                 ['0', '0', '0', '0'],
                 ['0', '0', '0', '0']]
        # Copy Data to State Array for manipulation
        for col in range(4):
            for row in range(4):
                state[col][row] = data[row + (col << 2)]
        # copy key to round_key
        round_key = bytearray(16)
        for i in range(16):
            round_key[i] = key[i]
        self._aes_add_round_key(round_key, state)
        # encrypt data 9x
        for round_nums in range(1, 10):
            self._round_encrypt(state, round_key, round_nums)
        self._aes_sub_bytes(state)
        self._aes_shift_rows(state)
        self._aes_calculate_key(10, round_key)
        self._aes_add_round_key(round_key, state)
        for row in range(4):
            for col in range(4):
                data[col + (row << 2)] = state[row][col]

    def _round_encrypt(self, state, key, num_round):
        """Performs one round of AES.
        :param bytearray state: State array.
        :param bytearray key: Round key array.
        :param int round: AES round number.
        """
        self._aes_sub_bytes(state)
        self._aes_shift_rows(state)
        self._aes_mix_columns(state)
        self._aes_calculate_key(num_round, key)
        self._aes_add_round_key(key, state)

    def _aes_calculate_key(self, num_round, round_key):
        """Performs round key calculation per TinyLoRa's spec.
        :param int num_round: Round number
        :param bytearray round_key: Round key array.
        """
        tmp_arr = bytearray(4)
        round_const = 0x01
        # add round_const calculation
        while num_round != 1:
            b = round_const & 0x80
            round_const <<= 1
            round_const &= 0xff
            if b == 0x80:
                round_const ^= 0x1b
            num_round -= 1
        # Calculate first temp
        tmp_arr[0] = self._aes_sub_byte(round_key[12 + 1])
        tmp_arr[1] = self._aes_sub_byte(round_key[12 + 2])
        tmp_arr[2] = self._aes_sub_byte(round_key[12 + 3])
        tmp_arr[3] = self._aes_sub_byte(round_key[12 + 0])
        # XOR tmp_arr[0] wth round_const first
        tmp_arr[0] ^= round_const
        # then calculate new round key
        for i in range(4):
            for j in range(4):
                round_key[j + (i << 2)] ^= tmp_arr[j]
                tmp_arr[j] = round_key[j + (i << 2)]

    @staticmethod
    def _aes_add_round_key(round_key, state):
        """AES AddRoundKey Step: Round_Key combined with the state.
        :param bytearray round_key: Subkey for each round.
        :param bytearray state: State array.
        """
        for col in range(4):
            for row in range(4):
                state[col][row] ^= round_key[row + (col << 2)]

    @staticmethod
    def _aes_sub_byte(sub_byte):
        """Sub-Byte Step: Used for returning specific byte
        from the AES S_BOX.
        :param byte sub_byte: byte to be replaced with S_BOX byte.
        """
        row = ((sub_byte >> 4) & 0x0F)
        col = ((sub_byte >> 0) & 0x0F)
        return S_BOX[row][col]

    def _aes_sub_bytes(self, state):
        """AES SubBytes Step: Replace state arr. bytes w/sub-byte from S_BOX
        :param bytearray s: State array.
        """
        for col in range(4):
            for row in range(4):
                state[row][col] = self._aes_sub_byte(state[row][col])

    @staticmethod
    def _mix_single_column(col):
        """Mixes individual columns with state array
        :param bytearray col: Column from statearray
        """
        temp = col[0] ^ col[1] ^ col[2] ^ col[3]
        col_zero = col[0]
        col[0] ^= temp ^ xtime(col[0] ^ col[1])
        col[1] ^= temp ^ xtime(col[1] ^ col[2])
        col[2] ^= temp ^ xtime(col[2] ^ col[3])
        col[3] ^= temp ^ xtime(col[3] ^ col_zero)

    def _aes_mix_columns(self, state):
        """AES MixColumns Step: Multiplies each column of the state array with xtime.
        :param bytearray state: State array.
        """
        for i in range(4):
            self._mix_single_column(state[i])

    @staticmethod
    def _aes_shift_rows(arr):
        """AES ShiftRows Step: State array's bytes shifted to the left.
        :param bytearray state: State array.
        """
        arr[0][1], arr[1][1], arr[2][1], arr[3][1] = arr[1][1], arr[2][1], arr[3][1], arr[0][1]
        arr[0][2], arr[1][2], arr[2][2], arr[3][2] = arr[2][2], arr[3][2], arr[0][2], arr[1][2]
        arr[0][3], arr[1][3], arr[2][3], arr[3][3] = arr[3][3], arr[0][3], arr[1][3], arr[2][3]

    def calculate_mic(self, lora_packet, lora_packet_length, mic):
        """Calculates the validity of data messages, generates a message integrity check bytearray.
        """
        block_b = bytearray(16)
        key_k1 = bytearray(16)
        key_k2 = bytearray(16)
        old_data = bytearray(16)
        new_data = bytearray(16)
        block_b[0] = 0x49
        block_b[6] = self._device_address[3]
        block_b[7] = self._device_address[2]
        block_b[8] = self._device_address[1]
        block_b[9] = self._device_address[0]
        block_b[10] = (self.frame_counter & 0x00FF)
        block_b[11] = ((self.frame_counter >> 8) & 0x00FF)
        block_b[15] = lora_packet_length
        # calculate num. of blocks and blocksz of last block
        num_blocks = lora_packet_length // 16
        incomplete_block_size = lora_packet_length % 16
        if incomplete_block_size != 0:
            num_blocks += 1
        # generate keys
        self._mic_generate_keys(key_k1, key_k2)
        # aes encryption on block_b
        self._aes_encrypt(block_b, self._network_key)
        # copy block_b to old_data
        for i in range(16):
            old_data[i] = block_b[i]
        block_counter = 1
        # calculate until n-1 packet blocks
        while block_counter < num_blocks:
            # copy data into array
            k = 0  # ptr
            for i in range(16):
                new_data[k] = lora_packet[i]
                k += 1
            # XOR new_data with old_data
            self._xor_data(new_data, old_data)
            # aes encrypt new_data
            self._aes_encrypt(new_data, self._network_key)
            # copy new_data to old_data
            for i in range(16):
                old_data[i] = new_data[i]
            # increase block_counter
            block_counter = block_counter + 1
        # perform calculation on last block
        if incomplete_block_size == 0:
            for i in range(16):
                new_data[i] = lora_packet[i]
            # xor with key 1
            self._xor_data(new_data, key_k1)
            # xor with old data
            self._xor_data(new_data, old_data)
            # aes routine
            self._aes_encrypt(new_data, self._network_key)
        else:
            # copy the remaining data
            k = 0  # ptr
            for i in range(16):
                if i < incomplete_block_size:
                    new_data[k] = lora_packet[i]
                    k += 1
                if i == incomplete_block_size:
                    new_data[i] = 0x80
                if i > incomplete_block_size:
                    new_data[i] = 0x00
            # perform xor with key 2
            self._xor_data(new_data, key_k2)
            # perform xor with old data
            self._xor_data(new_data, old_data)
            self._aes_encrypt(new_data, self._network_key)
        # load MIC[] with data
        mic[0] = new_data[0]
        mic[1] = new_data[1]
        mic[2] = new_data[2]
        mic[3] = new_data[3]
        # return message integrity check array to calling method
        return mic

    def _mic_generate_keys(self, key_1, key_2):
        # encrypt the 0's in k1 with network key
        self._aes_encrypt(key_1, self._network_key)
        # perform gen_key on key_1
        # check if key_1's msb is 1
        if (key_1[0] & 0x80) == 0x80:
            msb_key = 1
        else:
            msb_key = 0
        # shift k1 left 1b
        self._shift_left(key_1)
        # check if msb is 1
        if msb_key == 1:
            key_1[15] = key_1[15] ^ 0x87
        # perform gen_key on key_2
        # copy key_1 to key_2
        for i in range(16):
            key_2[i] = key_1[i]
        if (key_2[0] & 0x80) == 0x80:
            msb_key = 1
        else:
            msb_key = 0
        self._shift_left(key_2)
        # check if msb is 1
        if msb_key == 1:
            key_2[15] = key_2[15] ^ 0x87

    @staticmethod
    def _shift_left(data):
        """ Shifts data bytearray left by 1
        """
        for i in range(16):
            if i < 15:
                if (data[i + 1] & 0x80) == 0x80:
                    overflow = 1
                else:
                    overflow = 0
            else:
                overflow = 0
            # shift 1b left
            data[i] = ((data[i] << 1) + overflow)&0xff

    @staticmethod
    def _xor_data(new_data, old_data):
        """ XOR two data arrays
        :param bytearray new_data: Calculated data.
        :param bytearray old_data: data to be xor'd.
        """
        for i in range(16):
            new_data[i] = new_data[i] ^ old_data[i]
