---
author: admin
categories:
- Technical
date: 2025-11-15
tags:
- llm
- vibe coding
- hack-a-day
- throwaway
- ai coding
title: "Hack-a-Day, Day 15: Vibe Chat"
---

Today's project was a vibe-coded chat program. For those unfamiliar, "vibe coding" is programming where an AI does the majority of the coding, and in fact is often undertaken by non-programmers. In my case I took an approach a bit closer to "architect" than entirely hands-off, but an LLM did all the heavy lifting.

[![](vibechat.png)](https://github.com/za3k/vibechat)

The code is [here](https://github.com/za3k/vibechat) -- roughly one commit per interaction, with a few combined. The prompts are not included.

I've mostly been using AI very little during hack-a-day... sometimes to help debug, and in one case to write another "boring bit" (convert Minecraft world to JSON, for the voxel engine). It might get stuff done, but it's not going to improve the same set of skills to do stuff with an AI. And I'm generally a bit wary of using AI, because it can really just spew some absolute bullshit, which is in my head afterwards.

I've had a relatively better experience using Anthropic's Claude than most other products (for which I have a paid plan). Unfortunately they have very opaque usage caps, and I'd hit limits repeatedly during this project. Then it would say "please try again at 4pm" (in 3 hours). So I pretty much ran out of LLM usage on this one.

Overall I'd say I got to do some coding I usually wouldn't. The project was a curses frontend for a chat (and backend, but that didn't really get done yet). Something like making a curses interface would usually be a bit too boring for me--being able to collaborate with an LLM, who doesn't find such things boring, is great. Other than tooling issues, the main problem is that Claude doesn't write the best code. It generally has a very "junior programmer" vibe, with no use of abstraction, and tends toward the verbose.

My general take on AI though is that someone showed me a horse than can write an essay, and I'm complaining its penmanship is atrocious. It's pretty amazing stuff, and we're probably all going to be dead soon.

In the meantime it's pretty fun to mess about with.

PS: I do plan to update this one further, it just will require a bit of work each day given the rate limits. I had really grand plans, but we only got the bare minimum done.

Peace out!
