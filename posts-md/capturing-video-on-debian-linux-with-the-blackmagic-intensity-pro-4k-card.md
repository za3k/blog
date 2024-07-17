---
author: admin
categories:
- Technical
date: 2019-08-09 00:49:39-07:00
markup: html
source: wordpress
tags:
- blackmagic
- linux
- streaming
title: Capturing video on Debian Linux with the Blackmagic Intensity Pro 4K card
updated: 2020-05-17 12:55:33-07:00
wordpress_id: 462
wordpress_slug: capturing-video-on-debian-linux-with-the-blackmagic-intensity-pro-4k-card
---
Most of this should apply for any linux system, other than the driver install step. Also, I believe most of it applies to DeckLink and Intensity cards as well.

My main source is [https://gist.github.com/afriza/879fed4ede539a5a6501e0f046f71463](https://gist.github.com/afriza/879fed4ede539a5a6501e0f046f71463). I’ve re-written for clarity and Debian.

1.  Set up hardware. On the Intensity Pro 4K, I see a black screen on my TV when things are set up correctly (a clear rectangle, not just nothing).
2.  From the Blackmagic site, download “Desktop Video SDK” version 10.11.4 (not the latest). Get the matching “Desktop Video” software for Linux.
3.  Install the drivers. In my case, these were in `desktopvideo_11.3a7_amd64.deb`.  
    After driver install, `lsmod | grep blackmagic` should show a driver loaded on debian.  
    You can check that the PCI card is recognized with `lspci | grep Blackmagic` (I think this requires the driver but didn’t check)
4.  Update the firmware (optional). `sudo BlackmagicFirmwareUpdater status` will check for updates available. There were none for me.
5.  Extract the SDK. Move it somewhere easier to type. The relevant folder is `Blackmagic DeckLink SDK 10.11.4/Linux/includes`. Let’s assume you move that to `~/BM_SDK`
6.  Build ffmpeg from source. I’m here copying from my source heavily.
    1.  Get the latest ffmpeg source and extract it. Don’t match the debian version–it’s too old to work.  
        `wget https://ffmpeg.org/releases/ffmpeg-4.2.tar.bz2 && tar xf ffmpeg-*.tar.bz2 && cd ffmpeg-*`
    2.  Install build deps.  
        `sudo apt-get install nasm yasm libx264-dev libx265-dev libnuma-dev libvpx-dev libfdk-aac-dev libmp3lame-dev libopus-dev libvorbis-dev libass-dev`
    3.  Build.  
        `PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure --prefix="$HOME/ffmpeg_build" --pkg-config-flags="--static" --extra-cflags="-I$HOME/ffmpeg_build/include -I$HOME/ffmpeg_sources/BMD_SDK/include" --extra-ldflags="-L$HOME/ffmpeg_build/lib" --extra-libs="-lpthread -lm" --enable-gpl --enable-libass --enable-libfdk-aac --enable-libfreetype --enable-libmp3lame --enable-libopus --enable-libvorbis --enable-libvpx --enable-libx264 --enable-libx265 --enable-nonfree --enable-decklink`  
          
        `` make -j $(`nproc)` ``  
          
        `sudo cp ffmpeg ffprobe /usr/local/bin/`
7.  Use ffmpeg.  
    `ffmpeg -f decklink -list_devices 1 -i dummy` should show your device now. Note the name for below.  
      
    `ffmpeg -f decklink -list_formats 1 -i 'Intensity Pro 4K'` shows supported formats. Here’s what I see for the Intensity Pro 4K:

```
[decklink @ 0x561bd9881800] Supported formats for 'Intensity Pro 4K':
        format_code     description
        ntsc            720x486 at 30000/1001 fps (interlaced, lower field first)
        pal             720x576 at 25000/1000 fps (interlaced, upper field first)
        23ps            1920x1080 at 24000/1001 fps
        24ps            1920x1080 at 24000/1000 fps
        Hp25            1920x1080 at 25000/1000 fps
        Hp29            1920x1080 at 30000/1001 fps
        Hp30            1920x1080 at 30000/1000 fps
        Hp50            1920x1080 at 50000/1000 fps
        Hp59            1920x1080 at 60000/1001 fps
        Hp60            1920x1080 at 60000/1000 fps
        Hi50            1920x1080 at 25000/1000 fps (interlaced, upper field first)
        Hi59            1920x1080 at 30000/1001 fps (interlaced, upper field first)
        Hi60            1920x1080 at 30000/1000 fps (interlaced, upper field first)
        hp50            1280x720 at 50000/1000 fps
        hp59            1280x720 at 60000/1001 fps
        hp60            1280x720 at 60000/1000 fps
        4k23            3840x2160 at 24000/1001 fps
        4k24            3840x2160 at 24000/1000 fps
        4k25            3840x2160 at 25000/1000 fps
        4k29            3840x2160 at 30000/1001 fps
        4k30            3840x2160 at 30000/1000 fps
```

Capture some video: `ffmpeg -raw_format argb -format_code Hp60 -f decklink -i 'Intensity Pro 4K' test.avi`

The format (`raw_format` and `format_code`) will vary based on your input settings. In particular, note that`-raw_format uyvy422` is the default, which I found did not match my computer output. I was able to switch either the command line or the computer output settings to fix it.

Troubleshooting

-   **I’m not running any capture, but passthrough isn’t working.** That’s how the Intensity Pro 4K works. Passthrough is not always-on. I’d recommend a splitter if you want this for streaming.
-   **ffmpeg won’t compile.** Your DeckLink SDK may be too new. Get 10.11.4 instead.
-   **I can see a list of formats, but I can’t select one using -format\_code. ffmpeg doesn’t recognize the option.** Your ffmpeg is too old. Download a newer source.
-   **When I look at the video, I see colored bars. The HDMI output turns on during recording.** The Intensity Pro 4K outputs this when the resolution, hertz, or color format does not match the input. This also happens if your SDK and driver versions are mismatched.

Sources:

-   [https://gist.github.com/afriza/879fed4ede539a5a6501e0f046f71463](https://gist.github.com/afriza/879fed4ede539a5a6501e0f046f71463)
-   [https://ffmpeg.org/ffmpeg-devices.html#decklink](https://ffmpeg.org/ffmpeg-devices.html#decklink)
