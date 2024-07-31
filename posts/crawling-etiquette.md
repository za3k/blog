---
author: admin
categories:
- Technical
date: 2021-06-05 15:29:36-07:00
has-comments: false
markup: markdown
source: wordpress
tags:
- programming
- technical advice
- web crawling
title: Crawling Etiquette
updated: 2021-06-05 15:40:05-07:00
wordpress_id: 594
wordpress_slug: crawling-etiquette
---
I participate in a mentoring program, and recently one of the people I mentor asked me about whether it was okay to crawl something. I thought I would share my response, which is posted below nearly verbatim.

For this article, I’m skipping the subject of how to scrape websites (as off-topic), or how to avoid bans.

> People keep telling me that if I scrape pages like Amazon that I’ll get banned. I definitely don’t want this to happen! So, what is your opinion on this?

Generally bans are temporary (a day to two weeks). I’d advise getting used to it, if you want to do serious scraping! If it would be really inconvenient, either don’t scrape the site or learn to use a secondary IP, so when your scraper gets banned, you can still use the site as a user.

More importantly than getting banned, you should learn about **why** things like bans are in place, because they’re not easy to set up–someone decided it was a good idea. Try to be a good person. As a programmer, you can cause a computer to blindly access a website millions of times–you get a big multiplier on anything a normal person can do. As such, you can cause the owners and users of a site problems, even by accident. Learn scraping etiquette, and always remember there’s an actual computer sitting somewhere, and actual people running the site.

That said, there’s a big difference between sending a lot of traffic to a site that hosts local chili cookoff results, and amazon.com. You could cause make the chili cookoff site hard to access or run up a small bill for the owners if you screw up enough, while realistically there’s nothing you can do to slow down Amazon.com even if you tried.

Here are a couple reasons people want to ban automated scraping:

1.  It costs them money (*bandwidth*). Or, it makes the site unusable because too many “people” (all you) are trying to access it at once (*congestion*). Usually, it costs them money because the scaper is *stupid*–it’s something like a badly written search engine, which opens up every comment in a blog as a separate page, or opens up an infinite series of pages. For example, I host a bunch of large binaries (linux installers–big!), and I’ve had a search engine try to download every single one, once an hour. As a scraper, you can can avoid causing these problems by
    -   rate-limiting your bot (ex. only scraping one page every 5-10 seconds, so you don’t overload their server). This is a good safety net–no matter what you do, you can’t break things too badly. If you’re downloading big files, you can also rate-limit your bandwidth or limit your total bandwidth quota.
    -   examining what your scraper is doing as it runs (so you don’t download a bunch of unncessessary garbage, like computer-generated pages or a nearly-identical page for every blog comment)
    -   obeying [robots.txt](https://www.cloudflare.com/learning/bots/what-is-robots.txt/), which you can probably get a scraping framework to do for you. you can choose to ignore robots.txt if you think you have a good reason to, but make sure you understand why robots.txt exists before you decide.
    -   testing the site while you’re scraping by hand or with a computerized timer. If you see the site do something like load slower (even a little) because of what you’re doing, stop your scraper, and adjust your rate limit to be 10X smaller.
    -   make your scraper smart. download only the pages you need. if you frequently stop and restart the scraper, have it remember the pages you downloaded–use some form of local cache to avoid re-downloading things. if you need to re-crawl (for example to maintain a mirror) pass if-modified-since HTTP headers.
    -   declare an HTTP user-agent, which explains what you’re doing and how to contact you (email or phone) in case there is a problem. i’ve never had anyone actually contact me but as a site admin I have looked at user agents.
    -   probably some more stuff i can’t think of off the top of my head
2.  They want to keep their information secret and proprietary, because having their information publicly available would lose them money. This is the main reason Amazon will ban you–they don’t want their product databases published. My personal ethics says I generally ignore this consideration, but you may decide differently
3.  They have a problem with automated bots posting spam or making accounts. Since you’re not doing either, this doesn’t really apply to you, but your program may be caught by the same filters trying to keep non-humans out.

For now I would advise not yet doing any of the above, because you’re basically not doing serious scraping yet. Grabbing all the pages on xkcd.com is fine, and won’t hurt anyone. If you’re going to download more than (say) 10,000 URLs per run, start looking at the list above. One exception–DO look at what your bot does by hand (the list of URLs, and maybe the HTML results), because it will be educational.

> Also, in my web crawler project I eventually want to grab the text on each page crawled and analysis it using the requests library. Is something like this prohibited?

Prohibited by whom? Is it against an agreement you signed without reading with Amazon? Is it against US law? Would Amazon rather you didn’t, while having no actual means to stop you? These are questions you’ll have to figure out for yourself, and how much you care about each answer. You’ll also find the more you look into it that *none* of the three have very satisfactory answers.

The answer of “what bad thing might happen if I do this” is perhaps less satisfying if you’re trying to uphold what you perceive as your responsibilities, but easier to answer.

These are the things that may happen if you annoy a person or company on the internet by scraping their site. What happens will depend both on what you do, and what entity you are annoying (more on the second). *Editor’s note: Some of the below is USA-specific, especially the presence/absence of legal or government action.*

-   You may be shown CAPTCHAs to see if you are a human
-   Your scaper’s IP or IP block may be banned
-   You or your scraper may be blocked in some what you don’t understand
-   Your account may be deleted or banned (if your scraper uses an account, and rarely even if not)
-   They may yell at you, send you an angry email, or send you a polite email asking you to stop and/or informing you that you’re banned and who to contact if you’d like to change that
-   You may be sent a letter telling you to stop by a lawyer (a cease-and-desist letter), often with a threat of legal action if you do not
-   You may be sued. This could be either a legitimate attempt to sue you, or a sort of extra-intimidating cease-and-desist letter. The attempt could be successful, unsuccessful but need you to show up in court, or could be something you can ignore althogether.
-   You may be charged with some criminal charge such as computer, wire, or mail fraud. The only case I’m aware of offhand is [Aaron Swartz](https://en.wikipedia.org/wiki/Aaron_Swartz)
-   You may be brought up on some charge by the FBI, which will result in your computers being taken away and not returned, and possibly jailtime. This one will only happen if you are crawling a government site (and is not supposed to happen ever, but that’s the world we live in).

For what it’s worth, so far I have gotten up to the “polite email” section in my personal life. I do a reasonable amount of scraping, mostly of smaller sites.

\[… section specific to Amazon cut …\]

Craigslist, government sites, and traditional publishers (print, audio, and academic databases) are the only companies I know of that aggressively goes after scrapers through legal means, instead of technical means. Craigslist will send you a letter telling you to stop first.

What a company will do once you publicly post all the information on their site is another matter, and I have less advice there. There are several sites that offer information about historical Amazon prices, for what that’s worth.

You may find [this article](https://privacy-pc.com/articles/that-awesome-time-i-was-sued-for-two-billion-dollars-jason-scotts-extraordinary-experience.html) interesting (but unhelpful) if you are concerned about being sued. Jason Scott is one of the main technical people at the Internet Archive, and people sometimes object to things he posts online.

In my personal opinion, suing people or bringing criminal charges does not work in general, because most people scraping do not live in the USA, and may use technical means to disguise who they are. Scrapers may be impossible to sue or charge with anything. In short, a policy of trying to sue people who scape your site, will result in your site still being scraped. Also, most people running a site don’t have the resources to sue anyone in any case. So you shouldn’t expect this to be a common outcome, but basically a small percentage of people (mostly crackpots) and companies (RIAA and publishers) may.
