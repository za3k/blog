---
author: admin
categories:
- Technical
date: 2025-03-12
tags:
- zorchpad
title: 'Zorchpad Prototype Roadmap'
---

It's me, and I'm back working on the [Zorchpad](/tag/zorchpad/). This is the brainchild of one [Kragen](http://canonical.org/~kragen/). We have somewhat different, but related ideas for where to take the project. The idea is to make a computer that will continue to work as long as the human using it. 

It's been a while (9 months) since I've posted about the Zorchpad. Basically, I developed an [ugh field](https://medium.com/@robertwiblin/ugh-fields-or-why-you-can-t-even-bear-to-think-about-that-task-5941837dac62)[\*](https://www.lesswrong.com/posts/EFQ3F6kmt4WHXRqik/ugh-fields) around the case. I had been designing it in CAD and trying to print 3D versions of it, for approaching 2 or 3 months, and I just got sick of it. I kept getting stuck, and delayed, and etc. The problem was that I was just emotionally burnt out on the whole subject, and unwilling to look at the case, let alone try to make it yet again. (Even though there are probably some pretty easy ways to do it, like cardboard or clay.)

[Adam Simonyi](https://github.com/Odwalla-J) to the rescue! I sat down with Adam and woefully begged him to take care of the case for me. And he did! 

![caption: this case took me 2 months](/wp-content/uploads/2024/06/printed_assembly.jpg)
![caption: this case took him 2 days. top half designed but not printed](zorchpad-case-adam.jpg)

Blame any aesthetic shortcomings on me -- I pushed him pretty hard on "we're just testing electronics! It should look like shit!

Now I am feeling much better and mostly unstuck. I'm ready to start work on the pad again. Even though no big milestones have been accomplished recently, this seems like a good time to summarize the state of the project. 

tl;dr: **The power budget is 1 milli-watt.** As a bit of context, Kragen's approach to making a computer that lasts a long time is to avoid parts that fail. In his experience (he walks around with pocket computers a lot), this seems to include dead batteries. They're out of charge, or need replaced, or there's no power outlet, or he forgot his charger. So his design does not include a battery. Instead, the whole thing is designed to run on solar cells indoors, and hide any power failures from the user. Think an old-school pocket calculator. So, because we want to run on indoor solar, we have a REALLY small power budget (1 milli-watt). Personally, I think even if you have to run on battery, low power use will still be cool.

This heavily influences our hardware choices. We're experimenting and seeing how it works in practice!

Okay, on to the prototype. Where is it at? Get ready for a dump of how my brain works.

### v0.1 Roadmap

- **CPU**:
  - Priority: (Done)
  - Design notes: Apollo3 system-on-a-chip (on an Adafruit breakout board)
  - Hardware State: Working.
  - Software State: Working.
  - Power: Not tested.
- **Keyboard**: 
  - Priority: Blocking
  - Design notes: We need a low-power keyboard. I'm making a "matrix" keyboard (zero power usage, needs outside electronics). You can buy these premade up to numpad size.
  - Hardware State: Not working. I have a 12x5 plate to put keyswitches into, I have switches, and I have keycaps. I should be able to assemble the hardware. Then I will [hand-solder them](https://golem.hu/guide/first-macropad/), following instructions from the custom mechanical keyboard community.
  - Software State: Partially working. Tested with 4x4 keyboard.
  - Power: Not tested.
  - Next step: 3D Print
- **Video (Screen)**:
  - Priority: (Done)
  - Design notes: We need a low-power screen. We selected the SHARP memory-in-pixel display.
  - Hardware State: Working.
  - Software State: Working.
  - Power: Not tested.
  - Next step blocker: Power measurement
- **Audio Out**:
  - Priority: (Done for v0.1)
  - Design notes: Audio is low-power enough that we can do it for headphones. We are adding an audio jack. This also has the advantage that earbuds are easier to replace than speakers.
  - Hardware State: Working.
  - Software State: Beeps only (with PWM)
  - Power: Not tested.
  - Next step blocker: Power measurement
- **Persistent Storage**:
  - Priority: High
  - Hardware State: Working (built-in to apollo3)
  - Software State: Working.
  - Power: Not tested.
  - Next step blocker: Power measurement
- **Power Switch**:
  - Priority: Blocking
  - Hardware State: Trivial
  - Next step: Do it
- **Wire reduction**:
  - Priority: Blocking
  - Design notes: A 12x5 matrix keyboard needs not (12+5) wires, but 9 wires. Combined with all the other peripherals, that's too many, so we need something like a shift register to reduce the wire count.
  - Hardware State: Not working. Have not found a low-power shift register or alternative.
  - Software State: (Blocked on hardware)
  - Next step: Order parts *OR* Do it with high-power shifter for v0.1
- **Wiring, General**:
  - Priority: Blocking
  - Hardware State: Not working. (Plan is jumpers or connectors, with wire ends soldered to boards)
  - Next step: Draw wiring diagram, Order parts
- **Power Supply**:
  - Priority: Blocking
  - Design notes: The first version will probably just be a AA battery (not solar)
  - Hardware State: Not working
  - Next step: Order parts (AA holder), Check required voltages for all parts, Design schematic

---

### v0.2 Roadmap

- **E-ink Screen**:
  - Priority: Mid 
  - Design notes: I'm testing adding an e-ink display as well, because the memory-in-pixel display goes up to around 3-4 inches diagonal only.
  - Hardware State: Not spec'ed. I have two around the house.
  - Software State: Large screen working on RPi but not apollo3, small screen not working.
  - Power: Probably uses too much power. Looking around for different screens that use less.
  - Next step: Research
- **PC Communicator**:
  - Priority: High. 
  - Design notes: How do we talk to the apollo3 from a normal computer? With the larger apollo3 breakout board, we get a UBS programmer, which solves this for early versions. But we can't measure power usage with USB plugged in, it uses some GPIO pins, and it won't work for the final prototypes with the small breakout board. The main goal is to reprogram the software, not to "talk" and send internet traffic.
  - Power: Not tested (could be net power gain!)
  - Next step blocker: GPIO pins
- **Audio In**:
  - Priority: Very Low
  - Design notes: (none)
  - Hardware State: The apollo3 may have an integrated microphone, I wasn't clear.
  - Software State: Not working.
  - Power: Not tested.
  - Next step: Research
- **Hard Disk**:
  - Priority: Low
  - Design notes: First version will use a microsd.
  - Hardware: Not working. If we want a slot (as opposed to soldering to the pads), also not ordered.
  - Software: Not working.
  - Power: Not tested.
  - Next step: Buy parts
- **Audio Out**:
  - Priority: Mid
  - Design notes: Improve to support voices
  - Hardware State: ?
  - Software State: No voice/music yet. Unclear whether that will need a hardware upgrade.
  - Power: Not tested.
  - Next step: Programming, Testing
- **GPIO**:
  - Priority: Mid
  - Design notes: To let us hook up new peripherals and/or talk to a computer
  - Hardware State: Not working
  - Software State: Not working
  - Next step blocker: Wire reduction
- **Power supply v2: Capacitor buffer**:
  - Priority: Low
  - Design notes: The actual power source is solar power or a battery. We want a buffer so that when the power dies, we have enough time to hibernate.
  - Next step: Ask for help
- **Power supply v3: Solar power**:
  - Priority: Low
  - Design notes: *Testing* solar panels is high priority to make sure they can supply the right amounts of power, but not actually using them.
  - Next step: Buy panels, Test panels
- **Power Use Measurement**:
  - Priority: Mid
  - Next step: Ask for help (in progress)
- **Battery Level Measurement**:
  - Priority: Mid
  - Design notes: Monitor the current battery %/runtime, capacitor %/runtime. Optional: trigger an alert when the battery/solar panel is removed, so we can know to hibernate.
  - Next step: Ask for help
- **Clock**:
  - Priority: Very Low
  - Design notes: Is this needed for power monitors? If so becomes a high priority.
  - Next step: Research
- **Connectors + Sockets**:
  - Priority: Low
  - Design notes: I'd like to learn how to make sockets. This enables to use better connectors than jumper wires, slot in more expensive chips like the apollo3 to re-use them across builds, and use displays with flex ribbon cables. It also allows end-user servicability.
  - Next step: Requirements, Research, Order parts
- **Circuitboarding**:
  - Priority: Low
  - Design notes: We're wiring together a bunch of floating parts with hot glue and jumper wires. Switch to having circuitboards instead at some point. Could be perfboard or traditional printed circuits. Printed circuits could be done with a service or at home.
  - Next step: Design in KiCAD, Print
  - Next step blocker: Connectors + Sockets
- **Persistence on Power Loss**:
  - Design notes: We're planning to run on solar (maybe also battery). If it's dark, you shouldn't lose state. We should just "pause" until the light comes back.
  - Hardware notes: Blocked
  - Software notes: Difficult. This is an OS-level software problem.
  - Next step blockers: Capacitor buffer, Battery level measurement
- **OS / VM**:
  - Design notes: We want an OS that stops badly-written software from locking up your machine in unfixable ways.
  - Software notes: Not designed
  - Next step: Write software
- **Software**:
  - Design notes: We need some test software! Text editor, text reader, software editor/compiler.
  - Software notes: Not written
  - Next step: Write software
