from smbus2 import SMBus
from time import sleep

bus = SMBus(1)
SLAVE_ADDRESS = 0x04

def request_reading():
    reading = bus.read_i2c_block_data(i2c_addr=SLAVE_ADDRESS, register=0x00, length=2)
    print(reading[0] * 256 + reading[1])

while True:
    request_reading()
    sleep(0.25)
