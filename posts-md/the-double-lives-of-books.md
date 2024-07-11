---
author: admin
categories:
- Non-Technical
- Technical
date: 2014-11-21 19:20:29-07:00
markup: html
source: wordpress
tags: []
title: The Double Lives of Books
updated: 2015-12-24 19:46:17-07:00
wordpress_id: 46
wordpress_slug: the-double-lives-of-books
---
Two forces pull at me: the desire to have few possessions and be able to travel flexibly, and the convenience of reading and referencing physical books. I discovered a third option: I have digital copies of all my books, so I can freely get rid of them at any time, or travel without inconvenience.

So that’s where we start. Here’s where I went.

I thought, if these books are just a local convenience for an online version, it’s more artistically satisfying to have some representation of that. So I printed up a card catalog of all my books, both the ones I have digital copies of and not:

[![An example catalog card](https://blog.za3k.com/wp-content/uploads/2014/11/sample_card-300x186.png)][1]

An example catalog card

That’s what a card looks like. There’s information about the book up top, and a link in the form of a [QR code][2] in the middle. The link downloads a PDF version of that book. Obviously being a programmer, the cards all all automatically generated.

[![Book with a card inside](https://blog.za3k.com/wp-content/uploads/2014/11/book-186x300.jpg)][3]

Book with a card inside

For the books where I have a physical copy, I put the card in the book, and it feels like I’m touching the digital copy. My friends can pirate their own personal version of the book (saving me the sadness of lost lent-out books I’m sure we’ve all felt at times). And I just thing it looks darn neat. Some physical books I don’t have a digital version of, since the world is not yet perfect. But at least I can identify them at a glance (and consider sending them off to a service like [http://1dollarscan.com/][4])

[![Card catalog of digital books](https://blog.za3k.com/wp-content/uploads/2014/11/catalog-225x300.jpg)][5]

Card catalog of digital books

And then, I have a box full of all the books I \*don’t\* have a physical copy of, so I can browse through them, and organize them into reading lists or recommendations. It’s not nearly as cool as the ones in books, but it’s sort of nice to keep around.

And if I ever decide to get rid of a book, I can just check to make sure there’s a card inside, and move the card into the box, reassured nothing is lost, giving away a physical artifact I no longer have the ability to support.

I sadly won’t provide a link to the library since that stuff is mostly pirated.

Interesting technical problems encountered during this project (you can stop reading now if you’re not technically inclined):

-   Making sure each card gets printed exactly once, in the face of printer failures and updating digital collections. This was hard and took up most of my time, but it’s also insanely boring so I’ll say no more.
-   Command-line QR code generation, especially without generating intermediate files. I used rqrcode\_png in ruby. I can now hotlink link qr.png?text=Hello%20World and see any text I want, it’s great.
-   Printing the cards. This is actually really difficult to automate–I generate the cards in HTML and it’s pretty difficult to print HTML, CSS, and included images. I ended up using the ‘[wkhtmltoimage][6]‘ project, which as far as I can tell, renders the image somewhere internally using [webkit][7] and screenshots it. There’s also a wkhtmltopdf available, which worked well but I couldn’t get to cooperate with index-card sized paper. Nothing else really seems to handle CSS, etc properly and as horrifying as the fundamental approach is, it’s both correct and well-executed. (They solved a number of problems with upstream patches to Qt for example, the sort of thing I love to hear)
-   The [zbarcam][8] software (for scanning QR codes among other digital codes) is just absolute quality work and I can’t say enough good things about it. Scanning cards back into the computer was one of the most pleasant parts of this whole project. It has an intuitive command UI using all the format options I want, and camera feedback to show it’s scanned QR codes (which it does very quickly).
-   [Future-proofed][9] links to pirated books–the sort of link that usually goes down. I opted to use a [SHA256 hash][10] (the mysterious numbers at the bottom which form a unique signature generated from the content of the book) and provide a small page on my website which gives you a download based on that. This is what the QR code links to. I was hoping there was some way to provide that without involving me, but I’m unaware of any service available. [Alice Monday][11] suggested just typing the SHA hash into Google, which sounded like the sort of clever idea which might work. It doesn’t.

1.  Pingback: [Paper archival | Optimal Prime][12]
    

[1]: https://blog.za3k.com/wp-content/uploads/2014/11/sample_card.png
[2]: http://en.wikipedia.org/wiki/QR_code "QR code"
[3]: https://blog.za3k.com/wp-content/uploads/2014/11/book.jpg
[4]: http://1dollarscan.com/
[5]: https://blog.za3k.com/wp-content/uploads/2014/11/catalog.jpg
[6]: http://wkhtmltopdf.org/ "wkhtmltoimage"
[7]: http://en.wikipedia.org/wiki/WebKit "webkit"
[8]: http://zbar.sourceforge.net/ "zbarcam"
[9]: http://en.wikipedia.org/wiki/Future_proof "Future-proofed"
[10]: http://en.wikipedia.org/wiki/SHA-2 "SHA256 hash"
[11]: https://twitter.com/ali0mt "Alice Monday"
[12]: https://blog.za3k.com/paper-archival/
