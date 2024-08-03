---
author: admin
categories:
- Technical
date: 2017-10-05 23:57:50-07:00
has-comments: false
source: wordpress
tags:
- archiving
- backup
- compression
- data science
- deduplication
- exploratory
- git
- github
- linux
title: "github.com archive \u2013 Background Research"
updated: 2017-11-05 16:49:34-07:00
wordpress_id: 443
wordpress_slug: github-com-archive-background-research
---
My current project is to archive git repos, starting with all of github.com. As you might imagine, size is an issue, so in this post I do some investigation on how to better compress things. It’s currently Oct, 2017, for when you read this years later and your eyes bug out at how tiny the numbers are.

Let’s look at the list of repositories and see what we can figure out.

-   Github has a very limited naming scheme. These are the valid characters for usernames and repositories: \[-.\_0-9a-zA-Z\].
-   Github has 68.8 million repositories
-   Their built-in fork detection is not very aggressive–they say they have 50% forks, and I’m guessing that’s too low. I’m unsure what github considers a fork (whether you have to click the “fork” button, or whether they look at git history). To be a little more aggressive, I’m looking at collections of repos with the same name instead.There are 21.3 million different respository names. 16.7 million repositories do not share a name with any other repository. Subtracting, that means there 4.6million repository names representing the other 52.1 million possibly-duplicated repositories.
-   Here are the most common repository names. It turns out Github is case-insensitive but I didn’t figure this out until later.
    -   hello-world (548039)
    -   test (421772)
    -   datasciencecoursera (191498)
    -   datasharing (185779)
    -   dotfiles (120020)
    -   ProgrammingAssignment2 (112149)
    -   Test (110278)
    -   Spoon-Knife (107525)
    -   blog (80794)
    -   bootstrap (74383)
    -   Hello-World (68179)
    -   learngit (59247)
    -   – (59136)
-   Here’s the breakdown of how many copies of things there are, assuming things named the same are copies:
    -   1 copy (16663356, 24%)
    -   2 copies (4506958, 6.5%)
    -   3 copies (2351856, 3.4%)
    -   4-9 copies (5794539, 8.4%)
    -   10-99 copies (13389713, 19%)
    -   100-999 copies (13342937, 19%)
    -   1000-9999 copies (7922014, 12%)
    -   10000-99999 copies (3084797, 4.5%)
    -   1000000+ copies (1797060, 2.6%)

That’s about everything I can get from the repo names. Next, I downloaded all repos named **dotfiles**. My goal is to pick a compression strategy for when I store repos. My strategy will include putting repos with the name name on the same disk, to improve deduplication. I figured ‘dotfiles’ was a usefully large dataset, and it would include interesting overlap–some combination of forks, duplicated files, similar, and dissimilar files. It’s not perfect–for example, it probably has a lot of small files and fewer authors than usual. So I may not get good estimates, but hopefully I’ll get decent compression approaches.

Here’s some information about dotfiles:

-   102217 repos. The reason this doesn’t match my repo list number is that some repos have been deleted or made private.
-   243G disk size after cloning (233G apparent). That’s an average of 2.3M per repo–pretty small.
-   Of these, 1873 are empty repos taking up 60K each (110M total). That’s only 16K apparent size–lots of small or empty files. An empty repo is a good estimate for per-repo overhead. 60K overhead for every repo would be 6GB total.
-   There are 161870 ‘refs’ objects, or about 1.6 per repo. A ‘ref’ is a branch, basically. Unless a repo is empty, it must have at least one ref (I don’t know if github enforces that you must have a ref called ‘master’).
-   Git objects are how git stores everything.
    -   ‘Blob’ objects represent file content (just content). Rarely, blobs can store content other than files, like GPG signatures.
    -   ‘Tree’ objects represent directory listings. These are where filenames and permissions are stored.
    -   ‘Commit’ and ‘Tag’ objects are for git commits and tags. Makes sense. I think only annotated tags get stored in the object database.
-   Internally, git both stores diffs (for example, a 1 line file change is represented as close to 1 line of actual disk storage), and compresses the files and diffs. Below, I list a “virtual” size, representing the size of the uncompressed object, and a “disk” size representing the actual size as used by git.For more information on git internals, I recommend the excellent “[Pro Git](https://git-scm.com/book/en/v2/)” (available for free online and as a book), and then if you want compression and bit-packing details the [fine internals documentation](https://github.com/git/git/tree/master/Documentation/technical) has some information about objects, deltas, and packfile formats.
-   Git object counts and sizes:
    -   Blob
        -   41031250 blobs (401 per repo)
        -   taking up 721202919141 virtual bytes = 721GB
        -   239285368549 bytes on disk = 239GB (3.0:1 compression)
        -   Average size per object: 17576 bytes virtual, 5831 bytes on disk
        -   Average size per repo: 7056KB virtual, 2341KB on disk
    -   Tree
        -   28467378 trees (278 per repo)
        -   taking up 16837190691 virtual bytes = 17GB
        -   3335346365 bytes on disk = 3GB (5.0:1 compression)
        -   Average size per object: 591 bytes virtual, 117 bytes on disk
        -   Average size per repo: 160KB virtual, 33KB on disk
    -   Commit
        -   14035853 commits (137 per repo)
        -   taking up 4135686748 virtual bytes = 4GB
        -   2846759517 bytes on disk = 3GB (1.5:1 compression)
        -   Average size per object: 295 bytes virtual, 203 bytes on disk
        -   Average size per repo: 40KB virtual, 28KB on disk
    -   Tag
        -   5428 tags (0.05 per repo)
        -   taking up 1232092 virtual bytes = ~0GB
        -   1004941 bytes on disk = ~0GB (1.2:1 compression)
        -   Average size: 227 bytes virtual, 185 bytes on disk
        -   Average size per repo: 12 bytes virtual, 10 bytes on disk
    -   Ref: ~2 refs, above
    -   Combined
        -   83539909 objects (817 per repo)
        -   taking up 742177028672 virtual bytes = 742GB
        -   245468479372 bytes on disk = 245GB
        -   Average size: 8884 bytes virtual, 2938 bytes on disk
    -   Usage
        -   Blob, 49% of objects, 97% of virtual space, 97% of disk space
        -   Tree, 34% of objects, 2.2% of virtual space, 1.3% of disk space
        -   Commit, 17% of objects, 0.5% of virtual space, 1.2% of disk space
        -   Tags: 0% ish

Even though these numbers may not be representative, let’s use them to get some ballpark figures. If each repo had 600 objects, and there are 68.6 million repos on github, we would expect there to be 56 billion objects on github. At an average of 8,884 bytes per object, that’s 498TB of git objects (164TB on disk). At 40 bytes per hash, it would also also 2.2TB of hashes alone. Also interesting is that files represent 97% of storage–git is doing a good job of being low-overhead. If we pushed things, we could probably fit non-files on a single disk.

Dotfiles are small, so this might be a small estimate. For better data, we’d want to randomly sample repos. Unfortunately, to figure out how deduplication works, we’d want to pull in some more repos. It turns out picking 1000 random repo names gets you 5% of github–so not really feasible.

164TB, huh? Let’s see if there’s some object duplication. Just the unique objects now:

-   Blob
    -   10930075 blobs (106 per repo, 3.8:1 deduplication)
    -   taking up 359101708549 virtual bytes = 359GB (2.0:1 dedup)
    -   121217926520 bytes on disk = 121GB (3.0:1 compression, 2.0:1 dedup)
    -   Average size per object: 32854 bytes virtual, 11090 bytes on disk
    -   Average size per repo: 3513KB virtual, 1186KB on disk
-   Tree
    -   10286833 trees (101 per repo, 2.8:1 deduplication)
    -   taking up 6888606565 virtual bytes = 7GB (2.4:1 dedup)
    -   1147147637 bytes on disk = 1GB (6.0:1 compression, 2.9:1 dedup)
    -   Average size per object: 670 bytes virtual, 112 bytes on disk
    -   Average size per repo: 67KB virtual, 11KB on disk
-   Commit
    -   4605485 commits (45 per repo, 3.0:1 deduplication)
    -   taking up 1298375305 virtual bytes = 1.3GB (3.2:1 dedup)
    -   875615668 bytes on disk = 0.9GB (3.3:1 dedup)
    -   Average size per object: 282 bytes virtual, 190 bytes on disk
    -   Average size per repo: 13KB virtual, 9KB on disk
-   Tag
    -   2296 tags (0.02 per repo, 2.7:1 dedup)
    -   taking up 582993 virtual bytes = ~0GB (2.1:1 dedup)
    -   482201 bytes on disk = ~0GB (1.2:1 compression, 2.1:1 dedup)
    -   Average size per object: 254 virtual, 210 bytes on disk
    -   Average size per repo: 6 bytes virtual, 5 bytes on disk
-   Combined
    -   25824689 objects (252 per repo, 3.2:1 dedup)
    -   taking up 367289273412 virtual bytes = 367GB (2.0:1 dedup)
    -   123241172026 bytes of disk = 123GB (3.0:1 compression, 2.0:1 dedup)
    -   Average size per object: 14222 bytes virtual, 4772 bytes on disk
    -   Average size per repo: 3593KB, 1206KB on disk
-   Usage
    -   Blob, 42% of objects, 97.8% virtual space, 98.4% disk space
    -   Tree, 40% of objects, 1.9% virtual space, 1.0% disk space
    -   Commit, 18% of objects, 0.4% virtual space, 0.3% disk space
    -   Tags: 0% ish

All right, that’s 2:1 disk savings over the existing compression from git. Not bad. In our imaginary world where dotfiles are representative, that’s 82TB of data on github (1.2TB non-file objects and 0.7TB hashes)

Let’s try a few compression strategies and see how they fare:

-   243GB (233GB apparent). Native git compression only
-   243GB. Same, with ‘git repack -adk’
-   237GB. As a ‘.tar’
-   230GB. As a ‘.tar.gz’
-   219GB. As a’.tar.xz’ We’re only going to do one round with ‘xz -9’ compression, because it took 3 days to compress on my machine.
-   124GB. Using shallow checkouts. A shallow checkout is when you only grab the current revision, not the entire git history. This is the only compression we try that loses data.
-   125GB. Same, with ‘git repack -adk’)

Throwing out everything but the objects allows other fun options, but there aren’t any standard tools and I’m out of time. Maybe next time. Ta for now.
