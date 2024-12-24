---
author: admin
categories:
- Technical
- Non-Technical
date: 2024-11-27
tags:
- hack-a-day
- minecraft
title: 'Hack-a-Day, Day 27: Minecraft Mod'
---

Today I made a minecraft mod, using Fabric. Modding sure has changed a lot since I last tried it in Forge, maybe ten years ago! Java's changed a little too, even.

![](dirt-slab.png)
![](dirt-slab-recipe.png)

My mod adds a dirt slab, that's it. I didn't really have time to get past the basics, but I think the occasional hack that's just a learning experience is okay.

[Code](https://github.com/za3k/dirt-slab-fabric-mod) and [mod download](https://github.com/za3k/dirt-slab-fabric-mod/releases/tag/v1.0.0) are both on github this time.

Fabric is well-documented and friendly. The main downside is that there's no "abstraction later" between Minecraft and the mod. This means your mod will work with exactly one minecraft version on release. Additionally, when a new version of minecraft is released, you need to update and re-release your mod (and there are usually actual changes to be made).

Tutorials used:

- [Fabric wiki](https://wiki.fabricmc.net/tutorial:start)
- [Fabric documentation](https://docs.fabricmc.net/develop/getting-started/introduction-to-fabric-and-modding)
- [Changelog](https://fabricmc.net/blog/)
- [Fabric Discord Server](https://discord.gg/v6v4pMv)
