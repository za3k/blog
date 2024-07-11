---
author: admin
categories:
- Technical
date: 2017-07-02 20:41:58-07:00
markup: html
source: wordpress
tags:
- arch linux
- arduino
- hardware
- linux
- microcontroller
- pro trinket
- software
title: Getting the Adafruit Pro Trinket 3.3V to work in Arch Linux
updated: 2017-07-02 20:41:58-07:00
wordpress_id: 410
wordpress_slug: getting-the-adafruit-pro-trinket-3-3v-to-work-in-arch-linux
---
I’m on Linux, and here’s what I did to get the **Adafruit Pro Trinket** (3.3V version) to work. I think most of this should work for other Adafruit boards as well. I’m on **Arch Linux**, but other distros will be similar, just find the right paths for everything. Your version of udev may vary on older distros especially.

1.  Install the Arduino IDE. If you want to install the [adafruit version][1], be my guest. It should work out of the box, minus the udev rule below. I have multiple microprocessors I want to support, so this wasn’t an option for me.
2.  Copy the hardware profiles to your Arduino install. `pacman -Ql arduino` shows me that I should be installing to **/usr/share/aduino**.  You can find the files you need at their [source][2] (copy the entire folder) or the same thing is packaged inside of the [IDE installs][3].
    
    cp adafruit-git /usr/share/arduino/adafruit
    
3.  Re-configure “ATtiny85” to work with *avrdude*. On arch, `pacman -Ql arduino | grep "avrdude.conf` says I should edit **/usr/share/arduino/hardware/tools/avr/etc/avrdude.conf**. Paste [this revised “t85” section][4] into avrdude.conf ([credit][5] to the author)
4.  Install a [udev][6] rule so you can program the Trinket Pro as yourself (and not as root).
    
    \# /etc/udev/rules.d/adafruit-usbtiny.rules
    SUBSYSTEM=="usb", ATTR{product}=="USBtiny", ATTR{idProduct}=="0c9f", ATTRS{idVendor}=="1781", MODE="0660", GROUP="arduino"
    
5.  Add yourself as an *arduino* group user so you can program the device with `usermod -G arduino -a <username>`. [Reload the udev rules][7] and log in again to refresh the groups you’re in. Close and re-open the Arduino IDE if you have it open to refresh the hardware rules.
6.  You should be good to go! If you’re having trouble, start by making sure you can see the correct hardware, and that *avrdude* can recognize and program your device with simple test programs from the command link. The source links have some good specific suggestions.

Sources:  
[http://www.bacspc.com/2015/07/28/arch-linux-and-trinket/][8]  
[http://andijcr.github.io/blog/2014/07/31/notes-on-trinket-on-ubuntu-14.04/][9]

[1]: https://learn.adafruit.com/adafruit-arduino-ide-setup/linux-setup
[2]: https://github.com/adafruit/Adafruit_Arduino_Boards
[3]: https://learn.adafruit.com/adafruit-arduino-ide-setup/linux-setup
[4]: https://gist.github.com/andijcr/f4a660fde4035fb0a3aa
[5]: http://andijcr.github.io/blog/2014/07/31/notes-on-trinket-on-ubuntu-14.04/
[6]: https://wiki.archlinux.org/index.php/udev
[7]: https://wiki.archlinux.org/index.php/udev#Loading_new_rules
[8]: http://www.bacspc.com/2015/07/28/arch-linux-and-trinket/
[9]: http://andijcr.github.io/blog/2014/07/31/notes-on-trinket-on-ubuntu-14.04/
