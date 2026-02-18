---
author: admin
categories:
- Non-Technical
- Technical
date: 2025-12-20 18:00:01
tags:
- minecraft
- math
title: "Minecraft Villager Trading Halls: Probability Math"
---
Recently I was making a villager trading hall in minecraft.

![](villager-gui.png)

One of the main goals of a trading hall is to collect all villager trades. One of the trickiest is books, provided by a librarian. I got to wondering -- how long is this going to take?

Well, we can do some math to find out.

There are currently (as of Minecraft Java Edition 1.21.11) 40 trade-able books. 36 of them are available from the enchanting table, treasure chests\[1\], or trading.

4 are available only from treasure chests and trading. These are called *Treasure* enchantments.

- Curse of Binding
- Curse of Vanishing
- Frost Walker I and II
- Mending

There's also three books, which can be found only from treasure chests. We don't care about them for trading halls:

- Soul Speed
- Swift Sneak
- Wind Burst

There are no books available only from enchanting and not trading.

---

The core mechanic of searching for book trades is *resetting*. If we look at a librarian and find it has a trade we don't want, we reset it. 

Villagers remember their profession and trades forever after trading. But if we haven't traded with a villager, we simply remove its profession, and then give it a profession again. Then we can see if we like the new starting trades better.

This is very useful for librarians, because they have every book available as a starting trade, so there's no need to investigate later trades for books.

These are the options to make the villager forget their profession I'm aware of:

- Ignore the villager and get a new one (for example with a breeder), moving or killing the old one. This isn't a "reset" per se, but it acts similarly.
- Break the profession block manually. In the case of a librarian, the lectern. When breaking the block, the villager loses their profession instantly.
- Block the path between the villager and their profession block. I haven't seen this documented, but they reset at the same time as trades reset (twice per minecraft day). I did this by dropping the villager 1 block using a piston.
- Move the villager at least 48 taxicab blocks from their profession block. (Not tested)
- Move the profession block with a piston. This is an instant reset, but you can't do it for a lectern in Java edition. (Not tested)

Some of these are instant, some take longer. Once villagers are shown a profession block, it only takes them a couple seconds to get their new profession, so that part is easy.

I found breaking and re-placing blocks to be annoying, so I settled on moving librarians up and down with pistons. It takes about 5 real-time minutes for them to reset, so I used about 50 librarians to counteract that. By the time I finished checking all 50 librarians, they were ready to reset again because 5 minutes had passed.

Then the question is: How many librarians do we need to look at, to get every book?

---

Well, the first question is: what are we interested in? Let's say we're interested in getting each of the 40 enchantments.

Well, it turns out each enchantment is equally likely: there's a 1/40 chance of getting it. Well actually, 1/60 -- there's a chance that no book trade is offered at all.

Then this is the [coupon collector's problem](https://en.wikipedia.org/wiki/Coupon_collector%27s_problem), a classic math problem.

The number of trades to look at turns out to be: `3/2 x n x H(n)` where `H(n)` is the *n*-th harmonic number. For n=40, `H(40) = 1/1 + 1/2 + 1/3 + ... + 1/39 + 1/40 = 4.2785`. So we need to check **257 librarians** on average to get every enchantment.

---

But, are we really okay with that result? Given that Efficiency V is available as a starting trade, I want a librarian with Efficiency V, not Efficiency I!

There are:

| Enchantment           | Level |
|-----------------------|-------|
|Aqua Affinity|I|
|Channeling|I|
|Curse of Binding|I|
|Curse of Vanishing|I|
|Flame|I|
|Infinity|I|
|Mending|I|
|Multishot|I|
|Silk Touch|I|
|Fire Aspect|II|
|Frost Walker|II|
|Knockback|II|
|Punch|II|
|Depth Strider|III|
|Fortune|III|
|Looting|III|
|Loyalty|III|
|Luck of the Sea|III|
|Lunge|III|
|Lure|III|
|Quick Charge|III|
|Respiration|III|
|Riptide|III|
|Sweeping Edge|III|
|Thorns|III|
|Unbreaking|III|
|Blast Protection|IV|
|Breach|IV|
|Feather Falling|IV|
|Fire Protection|IV|
|Piercing|IV|
|Projectile Protection|IV|
|Protection|IV|
|Bane of Arthropods|V|
|Density|V|
|Efficiency|V|
|Impaling|V|
|Power|V|
|Sharpness|V|
|Smite|V|

- 9 tradable enchantments with a max level of I
- 4 with a max level of II
- 13 with a max level of III
- 7 with a max level of IV
- 7 with a max level of V

What's the chance of getting each level of enchantment? It's equal. So for Mending, there's a 1/60 chance to get Mending I, because it's the only choice. For Efficiency, there's a `2/3 * 1/40 x 1/5 = 1/300` chance to get Efficiency I, Efficiency II, or Efficiency V.

How do we calculate the coupon collector's problem for un-equal probabilities? Well... it's really complicated\[2\].

But the answer is that we will have to talk to an average of **933 librarians** to get all enchants at max level.

---

But hey. We can buy Efficiency V for 17 emeralds, if we get the right trade. Are we really okay getting a 64 emerald trade? What if we want only the best trades?

| Enchantment           | Level | Cost |
|-----------------------|-------|------|
|Aqua Affinity|I|5-19|
|Bane of Arthropods|V|17-71|
|Blast Protection|IV|14-58|
|Breach|IV|14-58|
|Channeling|I|5-19|
|**Curse of Binding**|I|10-38|
|**Curse of Vanishing**|I|10-38|
|Depth Strider|III|11-45|
|Density|V|17-71|
|Efficiency|V|17-71|
|Feather Falling|IV|14-58|
|Fire Aspect|II|8-32|
|Fire Protection|IV|14-58|
|Flame|I|5-19|
|Fortune|III|11-45|
|**Frost Walker**|II|16-64|
|Impaling|V|17-71|
|Infinity|I|5-19|
|Knockback|II|8-32|
|Looting|III|11-45|
|Loyalty|III|11-45|
|Luck of the Sea|III|11-45|
|Lunge|III|11-45|
|Lure|III|11-45|
|**Mending**|I|10-38|
|Multishot|I|5-19|
|Piercing|IV|14-58|
|Power|V|17-71|
|Projectile Protection|IV|14-58|
|Protection|IV|14-58|
|Punch|II|8-32|
|Quick Charge|III|11-45|
|Respiration|III|11-45|
|Riptide|III|11-45|
|Sharpness|V|17-71|
|Silk Touch|I|5-19|
|Smite|V|17-71|
|Sweeping Edge|III|11-45|
|Thorns|III|11-45|
|Unbreaking|III|11-45|

Mostly, the price range is based only on the level, but there are a few minor complications:

- Some price ranges go above 64! In the game, these get capped. For this reason, you're 8 times more likely to get Efficiency V for 64 emeralds than any other number.
- Treasure enchantments (in bold above) are double the price of any other enchantment. This is actually a double -- they're never offered for odd numbers of emeralds. Interesting!

The chance of getting an Efficiency V book at the best possible price is: `1/16,500 = 2/3 x 1/40 x 1/5 x 1/55` (because there are 55 possible different prices -- counting ones above 64).

To get every book at the best price, we'd need to talk to **45,594 librarians**\[2\] to get every max-level enchant at the best price.

---

Addendum: As I later noticed, as well as at least one commenter, there's no reason to get Efficient V at 17 emeralds. You can get it at 21 emeralds if you plan to cure the villagers -- because the price will still drop to 1 emerald after the cure.

The current cure mechanic is: book prices drop 20 emeralds, and you can't permanently stack more than 1 cure. So we're happy with any price 21 emeralds or lower, for any book, as the "best possible" price.

The chance of getting an Efficiency V book at the best is now: `1/3300 = 2/3 x 1/40 x 1/5 x 5/55`. The chance of getting of getting an Aqua Affinity book at the best price is `1/60 = 2/3 x 1/40`, because the whole price range of 5-19 is under 21!

Under these assumptions, we'd need to talk to **2,741 librarians**\[2\] to get every max-level enchant at the best discounted price.

\[1\]: I think
\[2\]: Source code [here](https://gist.github.com/za3k/d695594048ab8eb6239cb1dafdb97413). This uses the inclusion-exclusion principle to estimate set sizes, together with optimizations to take care of repeat probabilities.
