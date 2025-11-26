---
author: admin
categories:
- Technical
date: 2024-11-07 18:00:00
tags:
- data logging
- home automation
title: 'Home automation'
---

I added some temperature sensors around my house.

![caption: Temperature sensor, $4/ea on aliexpress](temperature-sensor.jpg)

The sensors run on AAA battery, and periodically transmit the temperature on [zigbee](https://en.wikipedia.org/wiki/Zigbee), a radio protocol in similar frequencies as Wifi. The signals get received by a USB dongle designed to receive and transmit zigbee. 

![caption: A raspberry pi listens to zigbee using a USB dongle](zigbee-pi.jpg)

This is connected to a raspberry pi running [zigbee2mqtt](https://www.zigbee2mqtt.io/). The messages get sent to an [mqtt](https://man.archlinux.org/man/mqtt.7.en) broker via wifi. mqtt is a pub/sub protocol that runs over the internet. Any computer on my LAN can then be notified of temperature updates, by asking the mqtt broker to send them updates.

I wrote a small server which stays on all the time, listening to updates and recording changes to a database. It also generates reports periodically.

I think my database format is mildly interesting, in that it's designed to use a fixed amount of space. Anyone who wants to see the technical details, can check [the github repo](https://github.com/za3k/temp-monitor), specifically [this file](https://raw.githubusercontent.com/za3k/temp-monitor/refs/heads/master/database.py).

Temperatures can be seen in [celsius](https://status.za3k.com/house-temp.c.txt) or [fahrenheit](https://status.za3k.com/house-temp.f.txt) online. An example in Fahrenheit is below.

        Current Temperature
        last updated: 2024-11-07 8:34pm

        Sensor                        Temperature  Humidity    Last update
        Outside - Front                51.51°F      69.86%     1 minutes ago
        Outside - Back                 64.26°F      99.99%     22 hours, 49 min ago
        Upstairs - Dining Room         69.67°F      53.24%     0 minutes ago
        Upstairs - Bedroom - Za3k      71.35°F      60.15%     21 minutes ago
        Upstairs - Bedroom - Master    68.90°F      58.11%     4 minutes ago
        Upstairs - Kitchen             71.20°F      50.50%     6 minutes ago
        Upstairs - Garage              65.55°F      60.65%     2 minutes ago
        Basement - HVAC/Server         68.02°F      51.27%     3 minutes ago
        Basement - Workshop            67.10°F      52.91%     14 minutes ago

        -------------

        Hourly Temperature
        last updated: 2024-11-07 8:34pm

                        outside    inside     
        2024-11-07  8am    54.49°F    69.44°F   
        2024-11-07  9am    53.81°F    69.04°F   
        [...]
        2024-11-07  6pm    56.11°F    69.86°F   
        2024-11-07  7pm    53.53°F    69.65°F   

        -------------

        Historical highs and lows
        last updated: 2024-11-07 8:34pm

                    outside             inside              
        2024-11-07    51.51 -  64.15°F    67.06 -  81.54°F   
        2024-11-06    61.21 -  71.24°F    68.36 -  81.18°F   
        [...]
        2024-10-10    49.39 -  60.89°F    67.59 -  77.49°F   

        -------------

        Code: https://github.com/za3k/temp-monitor

---

Having tested out zigbee and mqtt, I felt ready for my actual use case -- curtains. I live across the street from a major parking lot, and they have floodlights on all night. To sleep, I need blackout curtains. The problem is, it's pretty hard to wake up with blackout curtains drawn.

My solution was to get some smart curtains, and have them automatically go down at the end of the day, and go up in the morning.

![caption: Smart curtains from IKEA](smart-curtains.jpg)

This worked fine, after I got the curtains set up. I've completely forgotten about them, which is exactly how I like my home automation--I want to never think about it. For more about how to set up IKEA smart curtains, see [my notes](https://za3k.com/archive/smart-curtains). It comes with 6 manuals.

[blinds](https://github.com/za3k/short-programs#blinds-mqtt2mqtt) controls my blinds via the computer, and [mqtt2mqtt](https://github.com/za3k/short-programs#blinds-mqtt2mqtt) allows my IKEA remote to control them too. cron and [heliocron](https://github.com/mfreeborn/heliocron) automatically open and close the curtains on a timer.

---

I worked on monitoring power usage via my circuit breaker with current transformers and the [circuitsetup ESP32 energy meter](https://circuitsetup.us/) but it's currently stalled. The main problem is that I can't fit the CTs into my circuit breaker. If I get it working, I'll post an update.
