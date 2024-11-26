---
author: admin
categories:
- Technical
date: 2024-11-25
tags:
- software
title: 'Power Beeps'
---

One feature I really liked about older ThinkPad models was that when you plugged in power, it would give a little chirpy beep. Same when you disconnected it.

The downside to system beeping is that it gets really annoying. I don't want a failed tab completion to go "beep" aloud, especially when I'm in public.

I aggressively turn off all kinds of system bells, etc. Sadly, I get no beeps either.

Today I wrote a little python script to monitor power beep how I want. It plays it through my computer speakers (unmuting them if needed, just long enough to beep). It works for me on both ALSA and pulseaudio with an ALSA bridge (I have a few computers on each).

My default settings are:

- Two falling tones when power is unplugged
- Two rising tones when power is plugged back in
- Two warning beeps when the lowest battery reaches 10% (my laptop has two)
- Three warning beeps when the lowest battery reaches 5%.

Source code is [on github](https://github.com/za3k/short-programs#power-beeps) if you want to use it too. To change the thresholds or beeps, you'd have to change the code. No fancy configs, sorry!
