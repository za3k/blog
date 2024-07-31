---
author: admin
categories:
- Technical
date: 2014-07-26 23:29:47-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- AWS
- cloud
title: Amazon AWS
updated: 2014-10-18 03:28:55-07:00
wordpress_id: 7
wordpress_slug: amazon-aws
---
I was originally planning to write a rosetta-stone style guide for similar commands between digital ocean, google compute, and AWS. Instead, I spent all day writing this [CLI tool for EC2](https://github.com/vanceza/ec2-cli) which wraps the enormous and unintuitive AWS command-line tool. It’s not totally polished, namely you’ll have to hand-substitute some stuff at the top of the script that should properly go in a config file, but hopefully someone will find it useful.

As a warning it terminates, not just stops, all amazon instances when asked.
