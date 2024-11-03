---
author: admin
categories:
- Technical
date: 2024-11-02
tags:
- hack-a-day
title: 'Hack-a-Day, Day 02: Acrylic Soma Cube (FAILED)'
---

![caption: The Soma Cube is a 3D, tetris-like puzzle -- picture credit 2ndlook.nl](soma-cube.gif)

Today I tried to design a laser-cut set of Soma cube pieces. The pieces (shown above) are (conceptually, and sometimes actually) made of 3D blocks glued together.

I've seen a particular style of joinery for acryllic, called finger joints. Those looked easy to cut and easy to put together (if hard to design).

![caption: Acrylic box made with finger joints -- photo credit txoof](acrylic-joints.png)

I wrote a python script that takes a description of a piece, like this:

    Piece E
    xx x-
    x- --
    -- --

And draws all the flat faces I need to cut.

![caption: Flat faces for the soma cube](soma-pieces-flat.png)

I was already running far behind, time-wise. I ran out of time before I could get the joinery working. Honestly, I don't think I'm very close, either.

![caption: Finger joins drawn incorrectly with turtle graphics](finger-joint-attempt.png)

How to do a three-piece corner join was especially confusing me.
