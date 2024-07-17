---
author: admin
categories:
- Non-Technical
- Technical
date: 2022-08-10 09:32:40-07:00
markup: html
source: wordpress
tags:
- linux
- self-improvement
- system administration
title: problem-log.txt
updated: 2022-08-10 09:38:02-07:00
wordpress_id: 767
wordpress_slug: problem-log-txt
---
One of the more useful things I did was to start logging all my technical problems. Whenever I hit a problem, I write an entry in problem-log.txt. Here’s an example

```
2022-08-02
Q: Why isn't the printer working? [ SOLVED ]
A: sudo cupsenable HL-2270DW

// This isn't in the problem log, but the issue is that CUPS will silently disable the printer if it thinks there's an issue. This can happen if you pull a USB cord mid-print.
```

I write the date, the question, and the answer. Later, when I have a tough or annoying problem, I try to grep problem-log.txt. I’ll add a note if I solve a problem using the log, too.

This was an interesting project to look at 5 years later. I didn’t see benefits until 1-2 years later. It does not help me think through a problem. It’s hard to remember to do. But, over time it’s built up and become invaluable to me. I hit a tricky problem, and I can’t immediately find an answer on the web. I find out it’s in problem-log.txt. And, someone’s written it exactly with my hardware (and sometimes even my folder names) correctly in there. Cool!

Here’s another example:

```
2018-10-21
Q: How do I connect to the small yellow router?
```

Not every problem gets solved. Oh well.
