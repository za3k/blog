---
author: admin
categories:
- Technical
date: 2025-02-23
tags:
- ocaml
- software
title: 'Multi-user Text Editor'
---

I finished the text editor I was working on to learn OCaml.

![caption: three people editing one document](text-editor2.png)

It's (tentatively) called textmu. The selling point is that it's designed for multiple users, all SSH-ed into the same machine, to edit a document collaboratively. Otherwise, I basically made it a simplified knockoff of `nano`.

Source code is [on github](https://github.com/za3k/text-multiedit).

If you'd like to try it out (and don't want to compile it locally), feel free to get an account on my public server, [tilde](https://tilde.za3k.com).

Also, an update. The OCaml folks said it's fine to publish their book, so you can now [get your own copy](https://blog.za3k.com/ocaml-manual/) if you want one (link goes to updated blog post with photos).
