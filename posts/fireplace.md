---
author: admin
categories:
- Technical
- Non-technical
date: 2024-11-30
tags:
- electronics
- hardware
- decoration
- hack-a-day
title: 'Hack-a-Day, Day 30: LED Fireplace'
---

Having prepped my ESP-32, I decided to make an LED fireplace today.

The plan was to put an LED strip on a piece of cardboard, and have slowly shifting red, orange, and yellow lights going up and down, somewhat like a music visualizer. I knew the bare LEDs wouldn't look good, so the plan was to put the cardboard somewhat deep into the fireplace, and add some translucent tissue paper layers in front to diffuse the lights.

![caption: vertical 'strips' of lights](fireplace-cardboard.jpg)

Sadly, of my three ESP-32s, two were broken. I ended up instead using an ESP-8266, since I had several laying around. Annoyingly, the boards I have are so wide it's impossible to breadboard the, so I used [perfboard](https://en.wikipedia.org/wiki/Perfboard) instead.

![](fireplace-circuitback.jpg)
![](fireplace-circuitfront.jpg)

Having carefully set up the circuit, I flipped the on switch and... nothing happened. It was about 10pm at this point, and I was starting to run out of energy, so I gave up.

Very late that night, I found the problem was the resistor I added--the LED strip has a built-in resistor as well, and apparently the two together were too much. I eventually got the lights to turn on, but too late to finish the project for the day.

![caption: my test pattern looks a little christmas-y](fireplace-animated.gif)
