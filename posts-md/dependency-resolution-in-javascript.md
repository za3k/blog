---
author: admin
categories:
- Technical
date: 2015-11-02 18:36:11-07:00
markup: html
source: wordpress
tags:
- control flow
- javascript
- node
- npm
title: Dependency Resolution in Javascript
updated: 2015-11-02 18:36:57-07:00
wordpress_id: 353
wordpress_slug: dependency-resolution-in-javascript
---
Sometimes I have a bunch of dependencies. Say, UI components that need other UI components to be loaded. I’d really just like to have everything declare dependencies and magically everything is loaded in the right order. It turns out that if use “require” type files this isn’t bad (google “dependency injection”), but for anything other than code loading you’re a bit lost. I did find [dependency-graph][1], but this requires the full list of components to run. I wanted a version would you could add components whenever you wanted–an [online][2] framework.

My take is here: [https://github.com/vanceza/dependencies-online][3]

It has no requirements, and is available on npm as **dependencies-online**.

[1]: https://github.com/jriecken/dependency-graph
[2]: https://en.wikipedia.org/wiki/Online_algorithm
[3]: https://github.com/vanceza/dependencies-online
