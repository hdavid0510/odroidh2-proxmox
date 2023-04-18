#!/usr/bin/env python3

# Copyright (c) 2014-2020 Richard Hull and contributors
# PYTHON_ARGCOMPLETE_OK

import os
import sys
# if os.name != 'posix':
#     sys.exit('{} platform not supported'.format(os.name))

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


def prepare_font():
    global font_size, font_padding, font_path, font_fill, font
    font_fill = "white"
    # font_path, font_size, font_padding = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 10, 1
    font_path, font_size, font_padding = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 10, 1
    font = ImageFont.truetype(font_path, font_size)

def prepare_coord(width, height):
    global padding # constants to allow easy resizing of shapes.
    padding = -2
    global top, bottom
    top = padding
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
        prefix[s] = 1 << (i+1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = (float(n) / prefix[s])
            return f"{value:.1f}{s}"
    return f"{n}B"


def get_cpuusage():
    av1, av2, av3 = os.getloadavg()
    return f"{av1:.2f} {av2:.2f} {av3:.2f}"

def get_uptime():
    uptimerawsec = round(float(subprocess.check_output("cat /proc/uptime | awk '{print $1}'", shell=True).decode("utf-8")))#+60*60*24*100 #test
    uptimed, uptimerawsec = divmod(uptimerawsec, 60*60*24)
    uptimeh, uptimerawsec = divmod(uptimerawsec, 60*60)
    uptimem, uptimerawsec = divmod(uptimerawsec, 60)
    if uptimed == 0:
        return f"{uptimeh:02d}h{uptimem:02d}m"
    else:
        return f"{uptimed}d{uptimeh:02d}h{uptimem:02d}m"

def get_ramusage():
    ram = psutil.virtual_memory()
    return f"{bytes2human(ram.used)}/{bytes2human(ram.total)} {(100-ram.percent):.0f}%"

def get_swapusage():
   return subprocess.check_output("free -m | awk 'NR==3{printf \"%s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'", shell = True).decode("utf-8")

def get_diskusage(dir="/"):
    swap = psutil.disk_usage(dir)
    return f"{bytes2human(swap.used)} {swap.percent:.0f}%"

def get_netusage(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return f"{iface} T{bytes2human(stat.bytes_sent)}, R{bytes2human(stat.bytes_recv)}"

def get_ip():
    return subprocess.check_output("hostname -I | awk '{printf $1}'", shell = True).decode("utf-8")

def get_date(format="%m%d %H:%M:%S"):
    return datetime.now().strftime(format)

def get_temp():
    return f"{psutil.sensors_temperatures()['acpitz'][0].current:0.0f}C"


global pagecount
def stats(device, page=None):
    MAX_PAGE = 4
    COUNT_PER_PAGE = 5
    global pagecount
    if page is int:
        pagecount = page
    else:
        pagecount += 1
        if pagecount >= COUNT_PER_PAGE*MAX_PAGE:
            pagecount = 0
    with canvas(device) as draw:
        draw.text((x, top+(font_size+font_padding)*0), f"{get_date()} {get_uptime()}", font=font, fill=font_fill)
        draw.text((x, top+(font_size+font_padding)*1), f"{get_cpuusage()} {get_temp()}", font=font, fill=font_fill)
        if pagecount < COUNT_PER_PAGE * 1:
            draw.text((x, top+(font_size+font_padding)*2), f"RAM {get_ramusage()}", font=font, fill=font_fill)
            return
        if pagecount < COUNT_PER_PAGE * 2:
            draw.text((x, top+(font_size+font_padding)*2), f"Disk {get_diskusage()}", font=font, fill=font_fill)
            return
        if pagecount < COUNT_PER_PAGE * 3:
            draw.text((x, top+(font_size+font_padding)*2), f"IP {get_ip()}", font=font, fill=font_fill)
            return
        if pagecount < COUNT_PER_PAGE * 4:
          try:
              draw.text((x, top+(font_size+font_padding)*2), get_netusage('vmbr0'), font=font, fill=font_fill)
          except KeyError:
              draw.text((x, top+(font_size+font_padding)*2), "network disconnected", font=font, fill=font_fill)
          return



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
