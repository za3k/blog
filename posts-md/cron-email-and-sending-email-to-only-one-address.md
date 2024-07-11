---
author: admin
categories:
- Technical
date: 2020-05-18 22:13:02-07:00
markup: html
source: wordpress
tags:
- cron
- email
- linux
- system administration
title: Cron email, and sending email to only one address
updated: 2020-05-18 22:16:46-07:00
wordpress_id: 535
wordpress_slug: cron-email-and-sending-email-to-only-one-address
---
So you want to know when your monitoring system fails, or your cron jobs don’t run? Add this to your crontab:

    MAILTO=me@me.com

Now install a mail-sending agent. I like ‘[nullmailer][1]‘, which is much smaller than most mail-sending agents. It can’t receive or forward mail, only send it, which is what I like about it. No chance of a spammer using my server for something nasty.

The way I have it set up, I’ll have a server (avalanche) sending all email from one address (nullmailer@avalanche.za3k.com) to one email (admin@za3k.com), and that’s it. Here’s my setup on debian:

    sudo apt-get install nullmailer
    echo "admin@za3k.com" | sudo tee /etc/nullmailer/adminaddr # all mail is sent to here, except for certain patterns
    echo "nullmailer@`hostname`.za3k.com" | sudo tee /etc/nullmailer/allmailfrom # all mail is sent from here
    echo "`hostname`.za3k.com" | sudo tee /etc/nullmailer/defaultdomain # superceded by 'allmailfrom' and not used
    echo "`hostname`.za3k.com" | sudo tee /etc/nullmailer/helohost # required to connect to my server. otherwise default to 'me'
    echo "smtp.za3k.com smtp --port=587 --starttls" | sudo tee /etc/nullmailer/remotes && sudo chmod 600 /etc/nullmailer/remotes

Now just run `echo "Subject: sendmail test" | /usr/lib/sendmail -v admin@za3k.com` to test and you’re done!

[1]: http://untroubled.org/nullmailer/
