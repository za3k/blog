---
author: admin
categories:
- Technical
date: 2026-01-14
tags:
- hardware
- linux
title: DDRPad.com dance pad under Linux
---

I had quite a struggle getting [this pad](https://ddrpad.com/products/stepmania-soft-pad-1) working under linux. Here's how I did it on USB.

First, get rid of the built-in `xpad` module, which doesn't work.

    sudo modprobe -r xpad
    echo "blacklist xpad" | sudo tee /etc/modprobe.d/xpad.conf

Then install and test xboxdrv

    sudo pacman -S xboxdrv
    sudo xboxdrv --detach-kernel-driver --dpad-as-button

You can test with `evtest`. Pick the XBox controller. If it shows up and shows events when you press buttons, that's good. Especially test holding left and right at the same time -- you should see two "1" events. There's a bug in most USB adapters, because most controllers don't let you hold dpad left and dpad right at the same time. You want to make sure both work at the same time for DDR.

Assuming that works fine, you can play now! Let's add it to systemd. Make these two files as root in any text editor.

    # /etc/udev/rules.d/99-dancepad.rules                                                                  15s  130 :(
    ACTION=="add", ATTRS{idVendor}=="054c", ATTRS{idProduct}=="0268", ATTRS{product}=="PLAYSTATION(R)3 Controller", TAG+="systemd", ENV{SYSTEMD_WANTS}="xboxdrv-dancepad.service"

&nbsp;

    # /etc/systemd/system/xboxdrv-dancepad.service                                                            15ms  :)
    [Unit]
    Description=Xbox controller driver for dance pad

    [Service]
    Type=simple
    ExecStart=/usr/bin/xboxdrv --detach-kernel-driver --dpad-as-button
    Restart=on-failure

    [Install]
    WantedBy=multi-user.target

And then you need to restart or run:

    sudo systemctl daemon-reload
    sudo udevadm control --reload-rules

It should work now. If you have the EXACT same pad and it doesn't, drop me a comment/email and I'll try to help.

Some failed attempts:

- The raphnet controller sold on DDRPad.com doesn't *add* anything -- it shows up as XBox. I didn't actually re-check after the above, but you shouldn't need to order it.
- The Wingman FGC retro (ZPP006M) didn't work. Nothing showed up.
- The very cheap Amazon controllers (mine was sold as "[Xahpower](https://www.amazon.com/dp/B097MXJ1BW)" but the hardware presents as SHANWAN). They work, but they can't do left+right together.
- I even tried a [kernel patch](https://github.com/adiel-mittmann/dancepad/), which does seem like it works, but not on this pad (not that it's needed).

Debugged with help from Claude.
