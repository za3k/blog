---
author: admin
categories:
- Technical
date: 2014-10-04 02:10:39-07:00
has-comments: true
markup: markdown
source: wordpress
tags:
- minecraft
title: Running a forge server on headless linux
updated: 2014-10-18 03:29:32-07:00
wordpress_id: 13
wordpress_slug: running-a-forge-server-on-headless-linux
---
I’ve had a lot of trouble getting Minecraft Forge to run headless. They have a friendly installer option that I just can’t use in my situation, but one of the devs seems actively hostile around providing help to headless servers, so I didn’t bother asking forge for help. I thought I’d write up what I had to do to get things working. As a warning, it requires some local work; you can’t do everything headless with these directions.

I’m running Minecraft 1.6.4, with the latest version of forge for that, 9.11.1.965.

1.  Locally, download and start the minecraft client for the correct version at least once. Not sure if you’ll need to ‘play online’ or not. If you have the current installer, you need to make a new profile with the correct minecraft version and play that.
2.  Copy ~/.minecraft/libraries to the headless machine.
3.  Download forge (the installer version, not the universal) from [http://files.minecraftforge.net/](http://files.minecraftforge.net/). The non-adly version is the little star for non-interactive use.
4.  Run
    
    ```
    java -jar forge-1.6.4-9.11.1.965-installer.jar --installServer
    ```
    
5.  Delete the installer, you don’t need it any more.
6.  Install any mods you want to the ‘mods’ directory, edit server.properties, etc. Normal server setup.
7.  To execute the server, run the file indicated in the installer. In my case, I run
    
    ```
    java -jar minecraftforge-universal-1.6.4-9.11.1.965-v164-pregradle.jar nogui
    ```
    

Alternatively, you can install the entire server locally and copy it over.
