---
author: admin
categories:
- Technical
date: 2015-12-05 19:18:13-07:00
has-comments: false
source: wordpress
tags:
- backup
- http
- https
- mitm
- proxy
title: Archiving all web traffic
updated: 2015-12-06 01:06:20-07:00
wordpress_id: 388
wordpress_slug: archiving-all-web-traffic
---
Today I’m going to walk through a setup on how to archive all web (HTTP/S) traffic passing over your Linux desktop. The basic approach is going to be to install a proxy which records traffic. It will record the traffic to WARC files. You can’t proxy non-HTTP traffic (for example, chat or email) because we’re using an HTTP proxy approach.

The end result is pretty slow for reasons I’m not totally sure of yet. It’s possible warcproxy isn’t streaming results.

1.  Install the server
    
    ```
    # pip install warcproxy
    ```
    
2.  Make a warcprox user to run the proxy as.
    
    ```
    # useradd -M --shell=/bin/false warcprox
    ```
    
3.  Make a root certificate. You’re going to intercept HTTPS traffic by pretending to be the website, so if anyone gets ahold of this, they can fake being every website to you. Don’t give it out.
    
    ```
    # mkdir /etc/warcprox
    # cd /etc/warcprox
    # sudo openssl genrsa -out ca.key 409
    # sudo openssl req -new -x509 -key ca.key -out ca.crt
    # cat ca.crt ca.key >ca.pem
    # chown root:warcprox ca.pem ca.key
    # chmod 640 ca.pem ca.key
    ```
    
4.  Set up a directory where you’re going to store the WARC files. You’re saving all web traffic, so this will get pretty big.
    
    ```
    # mkdir /var/warcprox
    # chown -R warcprox:warcprox /var/warcprox
    ```
    
5.  Set up a boot script for warcproxy. Here’s mine. I’m using supervisorctl rather than systemd.
    
    ```
    #/etc/supervisor.d/warcprox.ini
    [program:warcprox]
    command=/usr/bin/warcprox -p 18000 -c /etc/warcprox/ca.pem --certs-dir ./generated-certs -g sha1
    directory=/var/warcprox
    user=warcprox
    autostart=true
    autorestart=unexpected
    ```
    
6.  Set up any browers, etc to use localhost:18000 as your proxy. You could also do some kind of global firewall config. Chromium in particular was pretty irritating on Arch Linux. It doesn’t respect $http\_proxy, so you have to pass it separate options. This is also a good point to make sure anything you don’t want recorded BYPASSES the proxy (for example, maybe large things like youtube, etc).
