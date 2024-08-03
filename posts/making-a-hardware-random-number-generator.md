---
author: admin
categories:
- Technical
date: 2021-06-06 17:23:06-07:00
has-comments: true
source: wordpress
tags:
- hardware
- linux
- randomness
title: Making a hardware random number generator
updated: 2021-06-06 17:28:29-07:00
wordpress_id: 598
wordpress_slug: making-a-hardware-random-number-generator
---
If you want a really good source of random numbers, you should get a hardware generator. But there’s not a lot of great options out there, and most people looking into this get (understandably) paranoid about backdoors. But, there’s a nice trick: if you combine multiple random sources together with [xor](https://github.com/za3k/short-programs#xor), it doesn’t matter if one is backdoored, as long as they aren’t all backdoored. There are some exceptions–if the backdoor is actively looking at the output, it can still break your system. But as long as you’re just generating some random pads, instead of making a kernel entropy pool, you’re fine with this trick.

So! We just need a bunch of sources of randomness. Here’s the options I’ve tried:

-   /dev/urandom (40,000KB/s) – this is nearly a pseudo-random number generator, so it’s not that good. But it’s good to throw in just in case. \[[Learn](https://stackoverflow.com/questions/23712581/differences-between-random-and-urandom) about /dev/random vs /dev/urandom if you haven’t. Then [unlearn](https://www.2uo.de/myths-about-urandom/) it again.\]
-   [random-stream](https://github.com/za3k/short-programs#prng) (1,000 KB/s), an implementation of the merenne twister pseudo-random-number generator. A worse version of /dev/urandom, use that unless you don’t trust the Linux kernel for some reason.
-   [infnoise](https://github.com/waywardgeek/infnoise) (20-23 KB/s), a USB hardware random number generator. Optionally whitens using [keccak](https://en.wikipedia.org/wiki/SHA-3). Mine is unfortunately broken (probably?) and outputs “USB read error” after a while
-   [OneRNG](https://onerng.info/) (55 KiB/s), a USB hardware random number generator. I use a [custom script](https://gist.github.com/za3k/64faa4aa0a9ecb338a8af8b0569fccb6) which outputs raw data instead of the provided scripts (although they look totally innocuous, do recommend
-   /dev/hwrng (123 KB/s), which accesses the hardware random number generator built into the raspberry pi. this device is provided by the [raspbian](https://packages.debian.org/buster/rng-tools-debian) package [rng-tools](https://github.com/nhorman/rng-tools). I learned about this option [here](https://scruss.com/blog/2013/06/07/well-that-was-unexpected-the-raspberry-pis-hardware-random-number-generator/)
-   [rdrand-gen](https://github.com/jtulak/RdRand) (5,800 KB/s), a command-line tool to output random numbers from the Intel hardware generator instruction, [RDRAND](https://en.wikipedia.org/wiki/RDRAND).

At the end, you can use my [xor](https://github.com/za3k/short-programs#xor) program to combine the streams/files. Make sure to use limit the output size if using files–by default it does not stop outputting data until EVERY file ends. The speed of the combined stream is at most going to be the slowest component (plus a little slowdown to xor everything). Here’s my final command line:

```
#!/bin/bash
# Fill up the folder with 1 GB one-time pads. Requires 'rng-tools' and a raspberry pi. Run as sudo to access /dev/hwrng.
while true; do
  sh onerng.sh | dd bs=1K count=1000000 of=tmp-onerng.pad 2>/dev/null
  infnoise --raw | dd bs=1K count=1000000 of=tmp-infnoise.pad 2>/dev/null
  xor tmp-onerng.pad tmp-infnoise.pad /dev/urandom /dev/hwrng | dd bs=1K count=1000000 of=/home/pi/pads/1GB-`\date +%Y-%m-%d-%H%M%S`.pad 2>/dev/null;
done
```

Great, now you have a good one-time-pad and can join [ok-mixnet](https://za3k.com/ok-mixnet.md) 🙂

P.S. If you *really* know what you’re doing and like shooting yourself in the foot, you could try combining and whitening entropy sources with a randomness sponge like keccak instead.
