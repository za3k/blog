---
author: admin
categories:
- Technical
date: 2015-03-13 11:15:07-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- git
- markdown
- system administration
- website
title: Roll-your-own git push-to-deploy, and markdown support
updated: 2015-03-13 13:15:05-07:00
wordpress_id: 136
wordpress_slug: markdown-support
---
Today I added support for development of za3k.com using git:

```
# !/bin/sh
# /git/bare-repos/za3k.com/hooks/post-update
cd ~za3k/public_html
env -i git pull
echo "Deployed za3k.com"
```

and markdown support, via a [cgi markdown wrapper](https://github.com/alue/markdown-handler/blob/master/README.md) someone wrote for apache (yes, I’m still using Apache).

Edit: I ended up wanting support for tables in markdown, so I used [Ruby](https://www.ruby-lang.org/)‘s [redcarpet](https://github.com/vmg/redcarpet) markdown gem (the same thing [Github](https://github.com/) uses, supports [this style of tables](http://www.tablesgenerator.com/markdown_tables) as well as code blocks).

CGI support via [http://blog.tonns.org/2013/10/enabling-markdown-on-your-apache.html](http://blog.tonns.org/2013/10/enabling-markdown-on-your-apache.html)
