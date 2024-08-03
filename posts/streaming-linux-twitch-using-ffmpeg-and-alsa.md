---
author: admin
categories:
- Technical
date: 2020-03-21 21:26:52-07:00
has-comments: true
source: wordpress
tags:
- alsa
- ffmpeg
- linux
- streaming
- twitch
title: Streaming Linux->Twitch using ffmpeg and ALSA
updated: 2020-05-17 12:53:43-07:00
wordpress_id: 509
wordpress_slug: streaming-linux-twitch-using-ffmpeg-and-alsa
---
I stopped using OBS a while ago for a couple reasons–the main one was that it didn’t support my video capture card, but I also had issues with it crashing or lagging behind with no clear indication of what it was doing. I ended up switching to `ffmpeg` for live streaming, because it’s very easy to tell when ffmpeg is lagging behind. OBS uses ffmpeg internally for video. I don’t especially recommend this setup, but I thought I’d document it in case someone can’t use a nice GUI setup like OBS or similar.

I’m prefer less layers, so I’m still on ALSA. My setup is:

-   I have one computer, running linux. It runs what I’m streaming (typically minecraft), and captures everything, encodes everything, and sends it to twitch
-   Video is captured using [libxcb](https://xcb.freedesktop.org/) (captures X11 desktop)
-   Audio is captured using [ALSA](https://en.wikipedia.org/wiki/Advanced_Linux_Sound_Architecture). My mic is captured directly, while the rest of my desktop audio is sent to a loopback device which acts as a second mic.
-   Everything is encoded together into one video stream. The video is a [Flash video](https://en.wikipedia.org/wiki/Flash_Video) container with [x264](https://en.wikipedia.org/wiki/X264) video and [AAC](https://en.wikipedia.org/wiki/Advanced_Audio_Coding) audio, because that’s what twitch wants. Hopefully we’ll all switch to [AV1](https://en.wikipedia.org/wiki/AV1) soon.
-   That stream is sent to [twitch](https://www.twitch.tv/) by ffmpeg
-   There is no way to pause the stream, do scenes, adjust audio, see audio levels, etc while the stream is going. I just have to adjust program volumes independently.

Here’s my .asoundrc:

```
# sudo modprobe snd-aloop is required to set up hw:Loopback
pcm.!default {
  type plug
  slave.pcm {
    type dmix
    ipc_key 99
    slave {
      pcm "hw:Loopback,0"
      rate 48000
      channels 2
      period_size 1024
    }
  }
}
```

My ffmpeg build line:

```
./configure --enable-libfdk-aac --enable-nonfree --enable-libxcb --enable-indev=alsa --enable-outdev=alsa --prefix=/usr/local --extra-version='za3k' --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --arch=amd64 --enable-gpl --disable-stripping --enable-avresample --disable-filter=resample --enable-avisynth --enable-libaom --enable-libass --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libmp3lame --enable-libopus --enable-libpulse --enable-libvorbis --enable-libvpx --enable-libx265 --enable-opengl --enable-libdrm --enable-libx264 --enable-shared --enable-librtmp && make -j 4 && sudo make install
```

And most imporantly, my ffmpeg command:

```
ffmpeg 
  -video_size 1280x720 -framerate 30 -f x11grab -s 1280x720 -r 30 -i :0.0 
  -f alsa -ac 1 -ar 48000 -i hw:1,0 
  -f alsa -ac 2 -ar 48000 -i hw:Loopback,1
  -filter_complex '[1:a][1:a]amerge=inputs=2[stereo1] ; [2:a][stereo1]amerge=inputs=2[a]' -ac 2 
  -map '[a]' -map 0:v 
  -f flv -ac 2 -ar 48000 
  -vcodec libx264 -g 60 -keyint_min 30 -b:v 3000k -minrate 3000k -maxrate 3000k -pix_fmt yuv420p -s 1280x720 -preset ultrafast -tune film 
  -c:a libfdk_aac -b:a 160k -strict normal -bufsize 3000k 
  rtmp://live-sjc.twitch.tv/app/${TWITCH_KEY}
```

Let’s break that monster down a bit. `ffmpeg` structures its command line into input streams, transformations, and output streams.

**ffmpeg input streams**

`-video_size 1280x720 -framerate 30 -f x11grab -s 1280x720 -r 30 -i :0.0`:  
Grab 720p video (`-video_size 1280x720`) at 30fps (`-framerate 30`) using x11grab/libxcb (`-f x11grab`), and we also want to output that video at the same resolution and framerate (`-s 1280x720 -r 30`). We grab `:0.0` (`-i :0.0`)–that’s X language for first X server (you only have one, probably), first display/monitor. And, since we don’t say otherwise, we grab the whole thing, so the monitor better be 720p.

`-f alsa -ac 1 -ar 48000 -i hw:1,0`:  
Using alsa (`-f alsa`), capture mono (`-ac 1`, 1 audio channel) at the standard PC sample rate (`-ar 48000`, audio rate=48000 Hz). The ALSA device is `hw:1,0` (`-i hw:1,0`), my microphone, which happens to be mono.

`-f alsa -ac 2 -ar 48000 -i hw:Loopback,1`:  
Using alsa (`-f alsa`), capture stereo (`-ac 2`, 2 audio channels) at the standard PC sample rate (`-ar 48000`, audio rate=48000 Hz). The ALSA device is `hw:Loopback,1`. In the ALSA config file `.asoundrc` given above, you can see we send all computer audio to `hw:Loopback,0`. Something sent to play on `hw:Loopback,0` is made available to record as `hw:Loopback,1`, that’s just the convention for how snd-aloop devices work.

**ffmpeg transforms**

`-filter_complex '[1:a][1:a]amerge=inputs=2[stereo1] ; [2:a][stereo1]amerge=inputs=2[a]' -ac 2`:  
All right, this one was a bit of a doozy to figure out. In ffmpeg’s special filter notation, `1:a` means “stream #1, audio” (where stream #0 is the first one).

First we take the mic input `[1:a][1:a]` and convert it from a mono channel to stereo, by just duplicating the sound to both ears (`amerge=inputs=2[stereo1]`). Then, we combine the stereo mic and the stereo computer audio (`[2:a][stereo1]`) into a single stereo stream using the default mixer (`amerge=inputs=2[a]`).

`-map '[a]' -map 0:v` :  
By default, ffmpeg just keeps all the streams around, so we now have one mono, and two stereo streams, and it won’t default to picking the last one. So we manually tell it to keep that last audio stream we made (`-map '[a]'`), and the video stream from the first input (`-map 0:v`, the only video stream).

**ffmpeg output streams**

`-f flv -ac 2 -ar 48000`:  
We want the output format to be Flash video (`-f flv`) with stereo audio (`-ac 2`) at 48000Hz (`-ar 48000`). Why do we want that? Because we’re streaming to Twitch and that’s what Twitch says they want–that’s basically why everything in the output format.

`-vcodec libx264 -g 60 -keyint_min 30 -b:v3000k -minrate 3000k -maxrate 3000k -pix_fmt yuv420p -s 1280x720 -preset ultrafast -tune film`:  
Ah, the magic. Now we do x264 encoding (`-vcodec libx264`), a modern wonder. A lot of the options here are just [what Twitch requests](https://help.twitch.tv/s/article/broadcast-requirements?language=en_US). They want keyframes every 2 seconds (`-g 60 -keyint_min 30`, where 60=30\*2=FPS\*2, 30=FPS). They want a constant bitrate (`-b:v3000k -minrate 3000k -maxrate 3000k`) between 1K-6K/s at the time of writing–I picked 3K because it’s appropriate for 720p video, but you could go with 6K for 1080p. Here are [Twitch’s recommendations](https://stream.twitch.tv/encoding/). The pixel format is standard (`-pix_gmt yub720p`) and we still don’t want to change the resolution (`-s 1280x720`). Finally the options you might want to change. You want to set the preset as high as it will go with your computer keeping up–mine sucks (`-preset ultrafast`, where the options go ultrafast,superfast,veryfast,faster,fast,medium, with a [2-10X jump in CPU power needed](https://trac.ffmpeg.org/wiki/Encode/H.264) for each step). And I’m broadcasting minecraft, which in terms of encoders is close to film (`-tune film`)–lots of panning, relatively complicated stuff on screen. If you want to re-encode cartoons you want something else.

`-c:a libfdk_aac -b:a 160k`:  
We use AAC (`-c:a libfdk_aac`). Note that libfdk is many times faster than the default implementation, but it’s not available by default in debian’s ffmpeg for ([dumb](https://www.gnu.org/licenses/license-list.html#fdk)) license reasons. We use 160k bitrate (`-b:a 160k` ) audio since I’ve found that’s good, and 96K-160K is Twitch’s allowable range. \`-strict normal\`

`-strict normal`: Just an ffmpeg option. Not interesting.  
`-bufsize 3000k`: One second of buffer with CBR video

`rtmp://live-sjc.twitch.tv/app/${TWITCH_KEY}`:  
The twitch streaming URL. Replace ${TWITCH\_KEY} with your actual key, of course.

Sources:

-   jrayhawk on IRC (alsa)
-   ffmpeg wiki and docs (pretty good)
-   ALSA docs (not that good)
-   Twitch documentation, which is pretty good once you can find it
-   [mark hills](http://www.pogo.org.uk/~mark/trx/streaming-desktop-audio.html) on how to set up snd-aloop
