import time
import busio
import digitalio
import board
from adafruit_tinylora.adafruit_tinylora import TTN, TinyLoRa

spi = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# RFM9x Breakout Pinouts
cs = digitalio.DigitalInOut(board.D5)
irq = digitalio.DigitalInOut(board.D6)

# Feather M0 RFM9x Pinouts
# irq = digitalio.DigitalInOut(board.RFM9X_D0)
# cs = digitalio.DigitalInOut(board.RFM9X_CS)

# TTN Device Address, 4 Bytes, MSB
devaddr = bytearray([0x00, 0x00, 0x00, 0x00])

# TTN Network Key, 16 Bytes, MSB
nwkey = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

# TTN Application Key, 16 Bytess, MSB
app = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

ttn_config = TTN(devaddr, nwkey, app, country='US')

lora = TinyLoRa(spi, cs, irq, ttn_config)

while True:
    data = bytearray(b"\x43\x57\x54\x46")
    print('Sending packet...')
    lora.send_data(data, len(data), lora.frame_counter)
    print('Packet sent!')
    lora.frame_counter += 1
    time.sleep(1)
