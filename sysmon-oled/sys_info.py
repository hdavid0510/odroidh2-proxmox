#!/usr/bin/env python

# Copyright (c) 2014-2020 Richard Hull and contributors
# PYTHON_ARGCOMPLETE_OK

"""
Display basic system information.

Needs psutil (+ dependencies) installed::

  $ sudo apt-get install python-dev
  $ sudo -H pip install psutil
"""

import os
import sys
if os.name != 'posix':
    sys.exit('{} platform not supported'.format(os.name))

import time
import subprocess
from pathlib import Path
from datetime import datetime
from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont
try:
    import psutil
except ImportError:
    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
    sys.exit()


global font_size, font_padding, font_path, font_fill, font
def prepare_font():
    global font_size
    font_size = 12
    global font_padding
    font_padding = 0
    global font_fill
    font_fill = 255
    global font_path
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
    # font_path = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    global font
    font = ImageFont.truetype(font_path, font_size)

global top, bottom, x
def prepare_coord(width, height):
    global padding # constants to allow easy resizing of shapes.
    padding = -2
    global top
    top = padding
    global bottom
    bottom = height - padding
    global x # Move left to right keeping track of the current x position for drawing shapes.
    x = 0

def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return f"{value}{s}"
    return f"{n}B"


def get_cpuusage(debug=False):
    av1, av2, av3 = os.getloadavg()
    usage = f"CPU  {av1:.2f} {av2:.2f} {av3:.2f}"
    if debug:
        print(usage)
    return usage
# def get_cpuusage():
#     usage = subprocess.check_output("top -bn1 | grep load | awk '{printf \"CPU %.2f\", $(NF-2)}'", shell = True )
#     return str(usage.decode('utf-8'))

def get_uptime(debug=False):
    uptime = f"Up {str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0]}"
    if debug:
        print(uptime)
    return uptime

# def get_ramusage():
#     usage = psutil.virtual_memory()
#     return "Mem %s %.0f%%" % (bytes2human(usage.used), 100 - usage.percent)
def get_ramusage(debug=False):
    usage = subprocess.check_output("free -m | awk 'NR==2{printf \"MEM  %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'", shell = True ).decode('utf-8')
    if debug:
        print(str(usage.decode('utf-8')))
    return usage

def get_swapusage(debug=False):
    usage = subprocess.check_output("free -m | awk 'NR==3{printf \"Swap %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'", shell = True).decode('utf-8')
    if debug:
        print(usage)
    return usage

# def get_diskusage(dir):
#     usage = psutil.get_diskusage(dir)
#     return "SD  %s %.0f%%" % (bytes2human(usage.used), usage.percent)
def get_diskusage(debug=False):
    usage = subprocess.check_output("df -h | awk '$NF==\"/\"{printf \"Disk %d/%dGB %s\", $3,$2,$5}'", shell = True ).decode('utf-8')
    if debug:
        print(usage)
    return usage

def get_netusage(iface, debug=False):
    stat = psutil.net_io_counters(pernic=True)[iface]
    usage = f"{iface} Tx{bytes2human(stat.bytes_sent)}, Rx{bytes2human(stat.bytes_recv)}"
    if debug:
        print(usage)
    return usage

def get_ip(debug=False):
    ip = subprocess.check_output("hostname -I", shell = True ).decode('utf-8')
    if debug:
        print(ip)
    return ip

def get_date(debug=False):
    date = subprocess.check_output("date", shell = True ).decode('utf-8')
    if debug:
        print(date)
    return date

def get_temp(debug=False):
    temp = f"{psutil.sensors_temperatures()['acpitz'][0].current}℃"
    if debug:
        print(temp)
    return temp


global pagecount
def stats(device, page=None):
    global pagecount
    if page is int:
        pagecount = page
    else:
        pagecount += 1
        if pagecount >= 10:
            pagecount = 0
    with canvas(device) as draw:
        draw.text((x, top+(font_size+font_padding)*0), get_date(), font=font, fill=font_fill)
        draw.text((x, top+(font_size+font_padding)*1), get_cpuusage()+"\t"+get_temp(), font=font, fill=font_fill)
        draw.text((x, top+(font_size+font_padding)*2), get_ramusage(), font=font, fill=font_fill)
        # if 0 <= pagecount and pagecount < 5:
        #     draw.text((x, top+(font_size+font_padding)*2), get_ramusage(), font=font, fill=font_fill)
        #     return
        # if 5 <= pagecount and pagecount < 10:
        #     #draw.text((x, top+(font_size+font_padding)*1), get_diskusage(), font=font, fill=font_fill)
        try:
            draw.text((x, top+(font_size+font_padding)*3), get_netusage('vmbr0'), font=font, fill=font_fill)
        except KeyError:
            # no wifi enabled/available
            pass
        #     return


def main():
    prepare_font()
    prepare_coord(device.width, device.height)
    global pagecount
    pagecount = 0
    while True:
        stats(device)
        time.sleep(1)


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
