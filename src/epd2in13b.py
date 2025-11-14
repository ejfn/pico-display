# *****************************************************************************
# * | File        :	  epd2in13b.py
# * | Author      :   Waveshare team
# * | Function    :   Electronic paper driver
# * | Info        :
# *----------------
# * | This version:   V1.0
# * | Date        :   2021-03-16
# # | Info        :   python demo
# -----------------------------------------------------------------------------
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documnetation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to  whom the Software is
# furished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS OR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#

from machine import Pin, SPI
import framebuf
import utime


EPD_WIDTH       = 104
EPD_HEIGHT      = 212

RST_PIN         = 12
DC_PIN          = 8
CS_PIN          = 9
BUSY_PIN        = 13

class EPD_2in13_B:
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)

        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)


        self.buffer_black = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        self.imageblack = framebuf.FrameBuffer(self.buffer_black, self.width, self.height, framebuf.MONO_HLSB)
        self.imagered = framebuf.FrameBuffer(self.buffer_red, self.width, self.height, framebuf.MONO_HLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    # Hardware reset
    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)


    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)

    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        print("e-Paper busy")
        while(self.digital_read(self.busy_pin) == 1):      # 0: idle, 1: busy
            self.delay_ms(10)
        print("e-Paper busy release")

    def TurnOnDisplay(self):
        self.send_command(0x12)
        self.delay_ms(100)
        self.ReadBusy()

    def init(self):
        self.reset()

        self.send_command(0x04)
        self.ReadBusy()

        self.send_command(0x00)
        self.send_data(0x0f)
        self.send_data(0x89)

        self.send_command(0x61)
        self.send_data(0x68)
        self.send_data(0x00)
        self.send_data(0xD4)

        self.send_command(0x50)
        self.send_data(0x77)

    def display(self):
        self.send_command(0x10)
        self.send_data1(self.buffer_black)

        self.send_command(0x13)
        self.send_data1(self.buffer_red)

        self.TurnOnDisplay()

    def display_mono_fast(self):
        """Fast monochrome display - black/white only, minimal flashing"""
        # Only send black channel data
        self.send_command(0x10)
        self.send_data1(self.buffer_black)

        # Send white to red channel (disables red)
        self.send_command(0x13)
        self.send_data1([0xFF] * len(self.buffer_red))

        # Fast refresh
        self.TurnOnDisplay()


    def Clear(self, colorblack, colorred):
        self.send_command(0x10)
        self.send_data1([colorred] * self.height * int(self.width / 8))

        self.send_command(0x13)
        self.send_data1([colorred] * self.height * int(self.width / 8))

        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0X50)
        self.send_data(0xf7)
        self.send_command(0X02)
        self.ReadBusy()
        self.send_command(0x07) # DEEP_SLEEP
        self.send_data(0xA5) # check code

        self.delay_ms(2000)
        self.module_exit()


class EPD_2in13_B_Landscape:
    """Landscape orientation (212 x 104) - just rotates the portrait display"""
    def __init__(self):
        self.reset_pin = Pin(RST_PIN, Pin.OUT)
        self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
        self.cs_pin = Pin(CS_PIN, Pin.OUT)
        # Swap dimensions for landscape
        self.width = EPD_HEIGHT  # 212 (wide)
        self.height = EPD_WIDTH  # 104 (tall)

        self.spi = SPI(1)
        self.spi.init(baudrate=4000_000)
        self.dc_pin = Pin(DC_PIN, Pin.OUT)

        self.buffer_black = bytearray(self.height * self.width // 8)
        self.buffer_red = bytearray(self.height * self.width // 8)
        # Use MONO_HLSB (same as portrait)
        self.imageblack = framebuf.FrameBuffer(self.buffer_black, self.width, self.height, framebuf.MONO_HLSB)
        self.imagered = framebuf.FrameBuffer(self.buffer_red, self.width, self.height, framebuf.MONO_HLSB)
        self.init()

    def digital_write(self, pin, value):
        pin.value(value)

    def digital_read(self, pin):
        return pin.value()

    def delay_ms(self, delaytime):
        utime.sleep(delaytime / 1000.0)

    def spi_writebyte(self, data):
        self.spi.write(bytearray(data))

    def module_exit(self):
        self.digital_write(self.reset_pin, 0)

    def reset(self):
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)
        self.digital_write(self.reset_pin, 0)
        self.delay_ms(2)
        self.digital_write(self.reset_pin, 1)
        self.delay_ms(50)

    def send_command(self, command):
        self.digital_write(self.dc_pin, 0)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([command])
        self.digital_write(self.cs_pin, 1)

    def send_data(self, data):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi_writebyte([data])
        self.digital_write(self.cs_pin, 1)

    def send_data1(self, buf):
        self.digital_write(self.dc_pin, 1)
        self.digital_write(self.cs_pin, 0)
        self.spi.write(bytearray(buf))
        self.digital_write(self.cs_pin, 1)

    def ReadBusy(self):
        print("e-Paper busy")
        while(self.digital_read(self.busy_pin) == 1):
            self.delay_ms(10)
        print("e-Paper busy release")

    def TurnOnDisplay(self):
        self.send_command(0x12)
        self.delay_ms(100)
        self.ReadBusy()

    def init(self):
        self.reset()
        self.send_command(0x04)
        self.ReadBusy()
        self.send_command(0x00)
        self.send_data(0x0f)
        self.send_data(0x89)
        self.send_command(0x61)
        self.send_data(0x68)
        self.send_data(0x00)
        self.send_data(0xD4)
        # Data entry mode 0x07 for landscape
        self.send_command(0x11)
        self.send_data(0x07)
        self.send_command(0x50)
        self.send_data(0x77)

    def display(self):
        # Send data directly (no transformation needed with HLSB)
        self.send_command(0x10)
        self.send_data1(self.buffer_black)
        self.send_command(0x13)
        self.send_data1(self.buffer_red)
        self.TurnOnDisplay()

    def sleep(self):
        self.send_command(0X50)
        self.send_data(0xf7)
        self.send_command(0X02)
        self.ReadBusy()
        self.send_command(0x07)
        self.send_data(0xA5)
        self.delay_ms(2000)
        self.module_exit()
