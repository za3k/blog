---
author: admin
categories:
- Non-Technical
date: 2024-12-16
tags:
- questions
title: 'Question #2: Verifiably Random Numbers'
---

We want to generate some random numbers. For simplicity, we'll assume we want a random number between 1 and 100. We want our random-number generator to be:

- Public (everyone knows the same random numbers, at roughly the same time)
- Fair (every number has the same odds of coming up)
- Trustable (everyone **knows** it's fair--it should be above doubt)
- Fast (we want to generate as many numbers as possible, as often as possible)
- Unpredictable (you shouldn't be able to guess the result before it's revealed)

Some security experts suggest that a trustable system should also be:

- Decentralized (no single person, organization, or computer picking the numbers). This is because a central trusted group requires faith in that group and its security.

One for this in the real world was the "Numbers Game", a popular illegal lottery in the 1800s, in the USA. The winning numbers were selected at random each day, like most lotteries--by the mob. After complaints about rigged lotteries, the winning numbers started to be picked more transparently. For example, it might be the closing price of the New York Stock Exchange--just the cents value. For a hundred dollar lottery, you would be crazy to worry about someone messing with the New York Stock Exchange. (But if it became a billion- or trillion-dollar lottery, you should worry again.)

The biggest problem with using a stock exchange that it's slow. You only get one set of numbers a day.

**Can you come up with a better random-number generator?**

