---
author: admin
categories:
- Technical
date: 2014-10-30 08:56:07-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- configuration
- linux
- mailx
title: "Configuring mailx\u2019s .mailrc with Gmail"
updated: 2014-10-30 08:57:14-07:00
wordpress_id: 33
wordpress_slug: configuring-mailxs-mailrc-with-gmail
---
Here’s how I added gmail to .mailrc for the BSD program mailx, provided by the *s-nail* package in arch.

```
account gmail {
  set folder=imaps://example@gmail.com@imap.gmail.com
  set password-example@gmail.com@imap.gmail.com="PASS"
  set smtp-use-starttls
  set smtp=smtp://smtp.gmail.com:587
  set smtp-auth=login
  set smtp-auth-user=example@gmail.com
  set smtp-auth-password="PASS"
  set from="John Smith <example@gmail.com>"
}
```

Replace **PASS** with your actual password, and **example@gmail.com** with your actual email. Read the documentation if you want to avoid plaintext passwords.

You can send mail with ‘mail -A gmail <params>’. If you have only one account, remove the first and last line and use ‘mail <params>’
