---
author: admin
categories:
- Technical
date: 2020-05-20 15:56:18-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- linux
- mon
- status.za3k.com
- system administration
title: mon(8)
updated: 2020-05-20 15:56:19-07:00
wordpress_id: 539
wordpress_slug: mon8
---
I had previously hand-rolled a status monitor, [status.za3k.com](http://status.za3k.com/), which I am in the process of replacing ([new version](https://germinate.za3k.com/pub/status/mon.txt)). I am replacing it with a linux monitoring daemon, [mon](https://mirrors.edge.kernel.org/pub/software/admin/mon/html/man/mon.html), which I recommend. It is targeted at working system administrators. ‘mon’ adds many features over my own system, but still has a very bare-bones feeling.

The old service, ‘[simple-status](https://github.com/za3k/za3k.com/blob/master/cgi-bin/status-simple)‘ worked as follows:

-   You visited the URL. Then, the status page would (live) kick of about 30 parallel jobs, to check the status of 30 services
-   The list of services is one-per-file in a the services.d directory.
-   For each service, it ran a short script, with no command line arguments.
-   All output is displayed in a simple html table, with the name of the service, the status (with color coding), and a short output line.
-   The script could return with a success (0) or non-success status code. If it returned success, that status line would display in green for success. If it failed, the line would be highlighted red for failure.
-   Scripts can be anything, but I wrote several utility functions to be called from scripts. For example, “[ping?](https://github.com/za3k/za3k.com/blob/master/cgi-bin/ping%3F)” checks whether a host is pingable.
-   Each script was wrapped in [timeout](https://www.gnu.org/software/coreutils/manual/html_node/timeout-invocation.html#timeout-invocation). If the script took too long to run, it would be highlighted yellow.
-   The reason all scripts ran every time, is to prevent a failure mode where the information could ever be stale without me noticing.

Mon works as follows

-   The list of 30 services is defined in /etc/mon/con.cf.
-   For each service, it runs a single-line command (monitor) with arguments. The hostname(s) are added to the command line automatically.
-   All output can be displayed in a simple html table, with the name of the service, the status (with color coding), the time of last and next run, and a short output line. Or, I use ‘[monshow](https://mirrors.edge.kernel.org/pub/software/admin/mon/html/man/monshow.html)‘, which is similar but in a text format.
-   Monitors can be anything, but several useful ones are provided in /usr/lib/mon/mon.d (on debian). For example the monitor “ping” checks whether a host is pingable.
-   The script could return with a success (0) or non-success status code. If it returned success, the status line would display in green for success (on the web interface), or red for failure.
-   All scripts run periodically. A script have many states, not just “success” or “failure”. For example “untested” (not yet run) or “dependency failing” (I assume, not yet seen).

As you can see, the two have a very similar approach to the component scripts, which is natural in the Linux world. Here is a comparison.

-   ‘simple-status’ does exactly one thing. ‘mon’ has many features, but does the minimum possible to provide each.
-   ‘simple-status’ is stateless. ‘mon’ has state.
-   ‘simple-status’ runs on demand. ‘mon’ is a daemon which runs monitors periodically.
-   Input is different. ‘simple-status’ is one script which takes a timeout. ‘mon’ listens for trap signals and talks to clients who want to know its state.
-   both can show an HTML status page that looks about the same, with some CGI parameters accepted.
-   ‘mon’ can also show a text status page.
-   both run monitors which return success based on status code, and provide extra information as standard output. ‘mon’ scripts are expected to be able to run on a list of hosts, rather than just one.
-   ‘mon’ has a config file. ‘simple-status’ has no options.
-   ‘simple-status’ is simple (27 lines). ‘mon’ has longer code (4922 lines)
-   ‘simple-status’ is written in bash, and does not expose this. ‘mon’ is written in perl, all the monitors are written in perl, and it allows inline perl in the config file
-   ‘simple-status’ limits the execution time of monitors. ‘mon’ does not.
-   ‘mon’ allows alerting, which call an arbitrary program to deliver the alert (email is common)
-   ‘mon’ supports traps, which are active alerts
-   ‘mon’ supports watchdog/heartbeat style alerts, where if a trap is not regularly received, it marks a service as failed.
-   ‘mon’ supports dependencies
-   ‘mon’ allows defining a service for several hosts at once

Overall I think that ‘mon’ is much more complex, but only to add features, and it doesn’t have a lot of features I wouldn’t use. It still is pretty simple with a simple interface. I recommend it as both good, and overall better than my system.

My only complaint is that it’s basically impossible to Google, which is why I’m writing a recommendation for it here.
