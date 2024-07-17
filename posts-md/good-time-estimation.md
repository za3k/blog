---
author: admin
categories:
- Non-Technical
date: 2023-05-08 17:41:01-07:00
markup: html
source: wordpress
tags: []
title: Good Time Estimation
updated: 2023-05-08 17:45:58-07:00
wordpress_id: 1024
wordpress_slug: good-time-estimation
---
As a programmer, one task I have to do often is estimate how a long a task will take. But as a programmer, most tasks I do have never been done before, and will never be done again, so estimating how long they will take is a little tricky. Here are some tips I’ve learned over the years.

## Always use clock time.

Yes, there are interruptions. You need your coffee. You didn’t get around to it that day. You want to know those things in your estimate, too. Just use the time on the clock for when a task starts and ends.

This is especially important if you’re self-employed.

## Write down how long you think a task will take. Afterwords, write down how long it took.

This simple step is the most important one. This gives you a clear idea of exactly what a task is and when it’s done. It also starts automatically training your brain.

You’ll start seeing patterns. You consistently underestimate how long everything will take. Conversations take longer than they feel. Exercise takes less time than it feels like. Fixing problems is highly variable. Doing something from scratch is easier to predict.

## Play a game. Predict things as well as possible.

Don’t change how you do them. You win if you guess accurately.

## Use as few units as possible.

Don’t use minutes, hours, days, weeks, and months. Personally, I try to use minutes and hours for everything. Of course, when I report to my boss, I convert to days, but in my own notes I estimate things in *one unit*.

## Learn your multiplication factor.

How long will it take you to do a project? Well, last time you had a similarly-sized project, you thought it would take 2 hours, and it actually took 14 hours. Your multiplication factor is about 7x. So this time if it feels like a 3 hour task, plan for 21 hours.

Assume there’s only one multiplication factor for one kind of work (one kind of work like your entire job, not one type of task). You can have different ones for different time scales, though (minutes vs hours vs days vs weeks).

You can measure other peoples’ multiplication factor to figure out when they’ll actually be done with tasks, but I suggest doing it quietly and not mentioning it.

Credit: Folk, but credit to [Joel on Software](https://www.joelonsoftware.com/2007/10/26/evidence-based-scheduling/) for the idea of estimating it for each team member

## To estimate a long task, break it up into pieces, and add up the pieces.

Do this if your task takes 2 days or more. Because of the multiplication factor, carefully budget time for added tasks, things you forgot, problems, etc. Or you can skip it. Just consistently pick one.

Credit: [Joel on Software](https://www.joelonsoftware.com/2007/10/26/evidence-based-scheduling/), including FogBugz which did this as a statistical method displayed with [Gantt Charts](https://en.wikipedia.org/wiki/Gantt_chart).

## Train your credible intervals.

Some tasks are more variable. Saying “something will take 1 hour” is vague. Saying “something will almost certainly take between 30 minutes and 4 hours” is more precise. How big should that range be? That’s called a credible interval.  
  
Train your credible intervals. I trained mine using bug fixing, something which happens several times a day, is hard to predict, and you have little control over (you can’t “call it done” early). Customer calls could be another great candidate.

I trained on bugfixes using 50%, 90%, and 99% intervals. There are specific mathematical scoring rules, but basically if something is in your 50% interval more than half the time, narrow it; if your interval is correct less than half the time, widen it.

Credit: Eliezer Yudkowsky (personal website, no longer up)
