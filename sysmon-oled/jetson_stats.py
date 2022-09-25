#!/usr/bin/python3
# This programm was slightly changed to run on a NVIDIA Jetson Nano
# by Ingmar Stapel
# Homepage: www.custom-build-robots.com
# Date: 20191201
#  
# Copyright (c) 2017 Adafruit Industries
# Author: Tony DiCola & James DeVito
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import time
import board
import busio
import digitalio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import subprocess



print("Acquiring I2C OLED module")
oled_reset = digitalio.DigitalInOut(board.D4)
i2c = busio.I2C(board.SCL_1, board.SDA_1)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=oled_reset)



print("Initializing display")

oled.fill(0)
oled.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
image = Image.new('1', (oled.width, oled.height))



print("Preparing buffer")

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)

# constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = oled.height - padding

# Move left to right keeping track of the current x position for drawing shapes.
x = 0



print("Loading font")

# Load default font
FONT_SIZE=10
font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', size=FONT_SIZE);



print("Fetching system info and beginning update")

while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0,0,oled.width, oled.height), outline=0, fill=0)

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    IP       = subprocess.check_output("hostname -I", shell = True )
    CPU      = subprocess.check_output("top -bn1 | grep load | awk '{printf \"CPU %.2f\", $(NF-2)}'", shell = True )
    MemUsage = subprocess.check_output("free -m | awk 'NR==2{printf \"RAM %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'", shell = True )
    SwapUsage= subprocess.check_output("free -m | awk 'NR==3{printf \"SWP %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'", shell = True )
    Disk     = subprocess.check_output("df -h | awk '$NF==\"/\"{printf \"DSK: %d/%dGB %s\", $3,$2,$5}'", shell = True )
    Date     = subprocess.check_output("date", shell = True )

    # Write lines of text.
    draw.text((x, top+FONT_SIZE*0), str(Date.decode('utf-8')),      font=font, fill=255)
    draw.text((x, top+FONT_SIZE*1), str(IP.decode('utf-8')),        font=font, fill=255)
    draw.text((x, top+FONT_SIZE*2), str(CPU.decode('utf-8')),       font=font, fill=255)
    draw.text((x, top+FONT_SIZE*3), str(MemUsage.decode('utf-8')),  font=font, fill=255)
    draw.text((x, top+FONT_SIZE*4), str(SwapUsage.decode('utf-8')), font=font, fill=255)
    draw.text((x, top+FONT_SIZE*5), str(Disk.decode('utf-8')),      font=font, fill=255)

    # Display image.
    oled.image(image)
    # oled.display()
    # time.sleep(.1)
    oled.show()

