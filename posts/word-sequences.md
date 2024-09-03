---
author: admin
categories:
- Non-technical
date: 2024-09-03
tags:
- words
title: 'Word Sequences'
---

What's the longest sequence of words you can make, beginning with any word and adding one letter at a time, if each step must also be a word?

If you can add them only at the end, a computer search outputs the dubious:

    co
    com
    comp
    compo
    compos
    compose
    composer
    composers

Adding letters only at the beginning I get the equally doubtful:

    es
    hes
    shes
    ashes
    lashes
    plashes
    splashes


If you add can add letters on either end, I found this valid 10-letter sequence:

    I
    in
    tin
    ting
    sting
    siting
    sitting
    slitting
    splitting
    splittings

My personal favorite, allowing rearranging letters, yields this whopping 15-letter series:

    I
    it
    tie
    rite
    irate
    attire
    cattier
    interact
    intricate
    recitation
    ratiocinate
    ratiocinated
    accreditation
    contraindicate
    contraindicated

The above answers found using a python, and the [GNU aspell](https://ftp.gnu.org/gnu/aspell/dict/0index.html) dictionary. Words containing ', -, or capital letters were removed.
