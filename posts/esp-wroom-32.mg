---
author: admin
categories:
- Technical
date: 2024-11-29
tags:
- microcontroller
- electronics
- hack-a-day
title: 'Hack-a-Day, Day 29: ESP32 Microcontroller Documentation'
---

A while back, I was trying to set up a power monitoring system, and I mistakenly bought the wrong ESP dev board. The ones I ended up are sold by some fake-named Chinese manufacturer. They seem pretty fine, much like any other ESP32 dev board, but they have an unusual 30-pin layout.

![](esp32-photo.jpg)

I tried to add some electronics to my [whiteboard hack](https://blog.za3k.com/hack-a-day-day-12-whiteboard-to-do-list/) earlier this month, but got frustrated pretty quickly, failing to program the microcontroller, and with no idea what the pinout was.

Today I decided to take it slower. I'd figure out how to program it, and understand the pins. If I had any time left over, I'd do a project.

First, I got flashing the chip to work. It turns out my main problem from the first time was a bad upload serial rate. I debugged the problem with the help of friendly folks on IRC. Espressif (the ESP32 manufacturer) has helpful troubleshooting instructions, which suggest using the python serial terminal, **miniterm**. By taking a step at a time, I got the microcontroller working.

Next, I installed and set up platformio, which I had never used before. My experience was that it was pretty good once set up, but a little hard to get started on the command line. Still, I'm happy, and will probably use it again. Platformio has two options--the popular **Arduino** framework libraries, or the Espressif-provided **esp-idf** libraries. Based on the small code samples I found, I'll most likely use the Arduino libraries, but some specialty features are just not available on Arduino.

Finally, I set up platformio one last time, with the VS-Code based PlatformIO IDE. Again my experience was pretty good. Sadly, the open-source VS-Code does not show the same set of extensions, and I had to use the binary version. (*Aside: Come on, vs-code. Don't call your package and program **code**. That's a dick move.*)

The writeup of how to get your dev environment set up is [on github](https://github.com/za3k/esp-wroom-32).

Finally, I made the below pinout diagram with the rest of my night.

[![caption: the colors looked better when it was bigger, I swear](esp32-pinout.png)](/images/esp32-pinout.png)

Happy hacking!
