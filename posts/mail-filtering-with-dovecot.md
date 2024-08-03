---
author: admin
categories:
- Technical
date: 2015-11-10 04:21:16-07:00
has-comments: false
source: wordpress
tags:
- debian
- dovecot
- linux
- sieve
- spamassassin
- system administration
title: Mail filtering with Dovecot
updated: 2015-11-29 22:33:56-07:00
wordpress_id: 370
wordpress_slug: mail-filtering-with-dovecot
---
This expands on my previous post about [how to set up an email server](https://blog.za3k.com/installing-email-with-postfix-and-dovecot/ "Installing email with Postfix and Dovecot (with Postgres)").

We’re going to set up a few spam filters in Dovecot under Debian. We’re going to use Sieve, which lets the user set up whichever filters they want. However, we’re going to run a couple pre-baked spam filters regardless of what the user sets up.

1.  Install Sieve.
    
    ```
    sudo apt-get install dovecot-sieve dovecot-managesieved
    ```
    
2.  Add Sieve to Dovecot
    
    ```
    # /etc/dovecot/dovecot.conf
    # Sieve and ManageSieve
    protocols = $protocols sieve
    protocol lmtp {
     mail_plugins = $mail_plugins sieve
    }
    service managesieve-login {
     inet_listener sieve {
     port = 4190
     }
    }
    protocol sieve {
     managesieve_logout_format = bytes ( in=%i : out=%o )
    }
    plugin {
     # Settings for the Sieve and ManageSieve plugin
     sieve = file:~/sieve;active=~/.dovecot.sieve
     sieve_before = /etc/dovecot/sieve.d/
     sieve_dir = ~/sieve # For old version of ManageSieve
     #sieve_extensions = +vnd.dovecot.filter
     #sieve_plugins = sieve_extprograms
    }
    ```
    
3.  Install and update SpamAssassin, a heuristic perl script for spam filtering.
    
    ```
    sudo apt-get install spamasssassin
    sudo sa-update
    ```
    
    ```
    # /etc/default/spamassassin
    ENABLED=1
    #CRON=1 # Update automatically
    ```
    
    ```
    # /etc/spamassassin/local.cf
    report_safe 0 # Don't modify headers
    ```
    
    ```
    sudo service spamassassin start
    ```
    
4.  There’s a lot of custom configuration and training you should do to get SpamAssassin to accurately categorize what you consider spam. I’m including a minimal amount here. The following will train SpamAssassin system-wide based on what users sort into spam folders.
    
    ```
    #!/bin/sh
    # /etc/cron.daily/spamassassin-train
    all_folders() {
            find /var/mail/vmail -type d -regextype posix-extended -regex '.*/cur|new$'
    }
    
    all_folders | grep "Spam" | sa-learn --spam -f - >/dev/null 2>/dev/null
    all_folders | grep -v "Spam" | sa-learn --ham -f - >/dev/null 2>/dev/null
    ```
    
5.  Make Postfix run SpamAssassin as a filter, so that it can add headers as mail comes in.
    
    ```
    # /etc/postfix/master.cf
    smtp inet n - - - - smtpd
     -o content_filter=spamassassin
    # ...
    spamassassin unix - n n - - pipe user=debian-spamd argv=/usr/bin/spamc -f -e /usr/sbin/sendmail -oi -f ${sender} ${recipient}
    ```
    
    ```
    sudo service postfix restart
    ```
    
6.  Add SpamAssassin to Sieve. Dovecot (via Sieve) will now move messages with spam headers from SpamAssassin to your spam folder. Make sure you have a “Spam” folder and that it’s set to autosubscribe.
    
    ```
    # /etc/dovecot/sieve.d/spam-assassin.sieve
    require ["fileinto"];
    # Move spam to spam folder
    if header :contains "X-Spam-Flag" "YES" {
     fileinto "Spam";
     # Stop here - if there are other rules, ignore them for spam messages
     stop;
    }
    ```
    
    ```
    cd /etc/dovecot/sieve.d
    sudo sievec spam-assassin.sieve
    ```
    
7.  Restart Dovecot
    
    ```
    sudo service dovecot restart
    ```
    
8.  Test spam. The [GTUBE](https://spamassassin.apache.org/gtube/) is designed to definitely get rejected. Set the content of your email to this:
    
    ```
    XJS*C4JDBQADN1.NSBN3*2IDNEN*GTUBE-STANDARD-ANTI-UBE-TEST-EMAIL*C.34X
    ```
    
9.  You should also be able to create user-defined filters in Sieve, via the ManageSieve protocol. I tested this using a Sieve thunderbird extension. You’re on your own here.
