---
author: admin
categories:
- Technical
date: 2014-11-23 14:35:14-07:00
markup: html
source: wordpress
tags:
- apis
- backup
- jq
- system administration
- twitter
title: Archiving twitter
updated: 2014-11-24 13:12:44-07:00
wordpress_id: 61
wordpress_slug: archiving-twitter
---
([Output][1])

I wanted to archive twitter so that I could

1.  Make sure old content was easily available
2.  Read twitter in a one-per-line format without ever logging into the site

[twitter\_ebooks][2] is a framework to make twitter bots, but it includes an ‘archive’ component to fetch historical account content which is apparently unique in that it 1) works with current TLS and 2) works the current twitter API. It stores the tweets in a JSON format which presumably matches the API return values. Usage is simple:

while read account
do
    [ebooks][3] archive "${account}" "archive/${account}.json"
    [jq][4] -r 'reverse | .\[\] | "\\(.created\_at|@sh)\\t \\(.text|@sh)"' "archive/${account}.json" >"archive/${account}.txt"
done <accounts.txt

I ran into a bug with [upstream incompatibilities][5] which is easily fixed. Another caveat is that the twitter API only allows access 3200 tweets back in time for an account–all the more reason to set up archiving ASAP. Twitter’s rate-limiting is also extreme ([15-180 req/15 min][6]), and I’m [worried about][7] a problem where my naive script can’t make it through a list of more than 15 accounts even with no updates.

[1]: https://za3k.com/~twitter_archive/
[2]: https://github.com/mispy/twitter_ebooks
[3]: https://github.com/mispy/twitter_ebooks
[4]: http://stedolan.github.io/jq/
[5]: https://github.com/mispy/twitter_ebooks/issues/34
[6]: https://dev.twitter.com/rest/public/rate-limiting
[7]: https://github.com/mispy/twitter_ebooks/issues/37
