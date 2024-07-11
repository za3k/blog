---
author: admin
categories:
- Technical
date: 2021-07-10 21:36:51-07:00
markup: html
source: wordpress
tags:
- compression
- formats
- gzip
- informative
title: Understanding gzip
updated: 2021-07-11 18:25:09-07:00
wordpress_id: 668
wordpress_slug: understanding-gzip-2
---
Let’s take a look at the gzip format. Why might you want to do this?

1.  Maybe you’re curious how gzip works
2.  Maybe you’re curious how DEFLATE works. DEFLATE is the “actual” compression method inside of gzip. It’s also used in zip, png, git, http, pdf… the list is pretty long.
3.  Maybe you would like to write a gzip/DEFLATE decompressor. (A compressor is more complicated–understanding the format alone isn’t enough)

Let’s work a few examples and look at the format in close detail. For all these examples, I’m using GNU gzip 1.10-3 on an x86\_64 machine.

I recommend checking out the linked resources below for a deeper conceptual overview if you want to learn more. That said, these are the only worked examples of gzip and/or DEFLATE of which I’m aware, so they’re a great companion to one another. In particular, you may want to learn what a prefix code is ahead of time.

References:  
\[1\] [RFC 1951][1], DEFLATE standard, by Peter Deutsch  
\[2\] [RFC 1952][2], gzip standard, by Peter Deutsch  
\[3\] [infgen][3], by Mark Adler (one of the zlib/gzip/DEFLATE authors), a tool for dis-assembling and printing a gzip or DEFLATE stream. I found this useful in figuring out the endian-ness of bitfields, and somewhat in understanding the dynamic huffman decoding process. Documentation is [here][4].  
\[4\] [An explanation of the ‘deflate’ algorithm][5] by Antaeus Feldspar. A great conceptual overview of LZ77 and Huffman coding. **I recommend reading this *before* reading my DEFLATE explanation.**  
\[5\] [LZ77][6] compression, Wikipedia.  
\[6\] [Prefix-free codes][7] generally and [Huffman][8]‘s algorithm specifically  
\[7\] After writing this, I learned about [puff.c][9], a reference (simple) implementation of a DEFLATE decompressor by Mark Adler.

## Gzip format: Basics and compressing a stream

Let’s take a look at our first example. If you’re on Linux, feel free to run the examples I use as we go.

    echo "hello hello hello hello" | gzip

The bytes gzip outputs are below. You can use *xxd* or any other hex dump tool to view binary files. Notice that the original is 24 bytes, while the compressed version is 29 bytes–gzip is not really intended for data this short, so all of the examples in this article actually get bigger.

Byte

**0**

**1**

**2**

**3**

**4**

**5**

**6**

**7**

**8**

**9**

10

11

12

13

14

15

16

17

18

19

20

**21**

**22**

**23**

**24**

**25**

**26**

**27**

**28**

Hex

**1f**

**8b**

**08**

**00**

**00**

**00**

**00**

**00**

**00**

**03**

cb

48

cd

c9

c9

57

c8

40

27

b9

00

**00**

**88**

**59**

**0b**

**18**

**00**

**00**

**00**

hello (1) – gzip contents

The beginning and end in bold are the gzip header and footer. I learned the details of the format by reading [RFC 1952: gzip][10]

-   Byte 0+1 (1f8b): Two fixed bytes that indicate “this is a gzip file”. These file-type indicators are also called “magic bytes”.
-   Byte 2 (08): Indicates “the compression format is DEFLATE”. DEFLATE is the only format supported by gzip.
-   Byte 3 (00): Flags. 8 single-bit flags.
    -   Not set: TEXT (indicates this is ASCII text. hint to the decompressor only. i think gzip never sets this flag)
    -   Not set: HCRC (adds a 16-bit CRC to the header)
    -   Not set: EXTRA (adds an “extras” field to the header)
    -   Not set: NAME (adds a filename to the header–if you compress a file instead of stdin this will be set)
    -   Not set: COMMENT (adds a comment to the header)
    -   There are also three reserved bits which are not used.
-   Byte 4-7 (00000000): Mtime. These indicate when the compressed file was last modified, as a unix timestamp. gzip doesn’t set an associated time when compressing stdin. Technically the standard says it should use the current time, but this makes the output the same every time you run gzip, so it’s better than the original standard.
-   Byte 8 (00): Extra flags. 8 more single-bit flags, this time specific to the DEFLATE format. None are set so let’s skip it. All they can indicate is “minimum compression level” and “max compression level”.
-   Byte 9 (03): OS. OS “03” is Unix.
-   Byte 10-20: Compressed (DEFLATE) contents. We’ll take a detailed look at DEFLATE below.
-   Byte 21-24 (0088590b): CRC32 of the uncompressed data, “hello hello hello hello\\n”. I assume this is correct. It’s worth noting, there are multiple things called “CRC32”.
-   Byte 25-28 (18000000): Size of the uncompressed data. This is little-endian byte order, 0x00000018 = 16\*1+1\*8 = 24. The uncompressed text is 24 bytes, so this is correct.

Byte

10

11

12

13

14

15

16

17

18

19

20

Hex

cb

48

cd

c9

c9

57

c8

40

27

b9

00

Binary

11001011

01001000

11001101

11001001

11001001

01010111

11001000

01000000

00100111

10111001

00000000

R. Bin.

11010011

00010010

10110011

10010011

10010011

11101010

00010011

00000010

11100100

10011101

00000000

hello (1) – DEFLATE contents

## DEFLATE format: Basics and fixed huffman coding

DEFLATE is the actual compression format used inside gzip. The format is detailed in [RFC 1951: DEFLATE][11]. DEFLATE is a dense format which uses bits instead of bytes, so we need to take a look at the binary, not the hex, and things will not be byte-aligned. The endian-ness is a little confusing in gzip, so we’ll usually be looking at the “reversed binary” row.

-   As a hint, whenever we read bits, we use the “reverse” binary order. For Huffman codes, we keep the bit order in reverse. For fixed-length fields like integers, we reverse again into “normal” binary order. I’ll call out the order for each field.
-   Byte 10: **1** 1010011. Is it the last block? Yes.
    -   1: Last block. The last block flag here means that after this block ends, the DEFLATE stream is over
-   Byte 10: 1 **10** 10011\. Fixed huffman coding. We reverse the bits (because it’s always 2 bits, and we reverse any fixed number of bits) to get 01.
    
    -   00: Not compressed
    
    -   **01: Fixed huffman coding.**
    -   10: Dynamic huffman coding.
    -   11: Not allowed (error)
-   So we’re using “fixed” huffman coding. That means there’s a static, fixed encoding scheme being used, defined by the DEFLATE standard. The scheme is given by the tables below. Note that Length/Distance codes are special–after you read one, you may read some extra bits according to the length/distance lookup tables.

Binary

Bits

Extra bits

Type

Code

00110000-10111111

8

0

Literal byte

0-143

110010000-111111111

9

0

Literal byte

144-255

0000000

7

0

End of block

256

0000001-0010111

7

varies

Length

257-279

11000000-11000111

8

varies

Length

280-285

Literal/End of Block/Length Huffman codes

Binary Code

Bits

Extra bits

Type

Value

00000-111111

5

varies

Distance

0-31

Distance Huffman codes

Code

Binary

Meaning

Extra bits

267

0001011

Length 15-16

1

Length lookup (abridged)

Code

Binary

Meaning

Extra bits

4

00100

Distance 5-6

1

Distance lookup (abridged)

-   Now we read a series of codes. Each code might be
    -   a literal (one binary byte), which is directly copied to the output
    -   “end of block”. either another block is read, or if this was the last block, DEFLATE stops.
    -   a length-distance pair. first code is a length, then a distance is read. then some of the output is copied–this reduces the size of repetitive content. the compressor/decompressor can look up to 32KB backwards for duplicate content. This copying scheme is called [LZ77][12].
-   Huffman codes are a “prefix-free code” (confusingly also called a “prefix code”). What that means is that, even though the code words are different lengths from one another, you can always unambigously tell which binary *codeword* is next. For example, suppose the bits you’re reading starts with: 0101. Is the next binary codeword 0, 01, 010, or 0101? In a prefix-free code, only one of those is a valid codeword, so it’s easy to tell. You don’t need any special separator to tell you the codeword is over. The space savings from not having a separator is really important for good compression. The “huffman” codes used by DEFLATE are prefix-free codes, but they’re not really optimal Huffman codes–it’s a common misnomer.
-   Byte 10-11: 110 **10011000** 10010: A literal. 10011000 (152) minus 00110000 (48) is 104. 104 in ASCII is ‘h’.
-   Byte 11-12: 000 **10010101** 10011: A literal. 10010101 (149) minus 00110000 (48) is 101. 101 in ASCII is ‘e’.
-   Byte 12-13: 101 **10011100** 10011: A literal. 10011100 (156) minus 00110000 (48) is 108. 108 in ASCII is ‘l’.
-   Byte 13-14: 100 **10011100** 10011: Another literal ‘l’
-   Byte 14-15: 100 **10011111** 01010: A literal. 10011111 (159) minus 00110000 (48) is 111. 111 in ASCII is ‘o’.
-   Byte 15-16: 111 **01010000** 10011: A literal. 01010000 (80) minus 00110000 (48) is 32. 32 in ASCII is ‘ ‘ (space).
-   Byte 16-17: 000 **10011000** 00010: Another literal ‘h’.
-   Byte 17: 000 **0001011**: A length. 0001011 (11) minus 0000001 (1) is 10, plus 257 is 267. We look up distance 256 in the “length lookup” table. The length is 15-16, a range.
-   Byte 18: **1** 00100: Because the length is a range, we read extra bits. The “length lookup” table says to read 1 extra bit: 1. The extra bits need to be re-flipped back to normal binary order to decode them, but 0b1 flipped is still 0b1. 15 (bottom of range) plus 0b1 = 1 (extra bits) is 16, so the final length is 16.
-   Byte 18-19: 111 **00100** 10011101: After a length, we always read a distance next. Distances are encoded using a second huffman table. 00100 is code 4, which using the “distance lookup” table is distance 5-6.
-   Byte 18-19: 11100100 **1** 0011101. Using the “distance lookup” table, we need to read 1 extra bit: 0b1. Again, we reverse it, and add 5 (bottom end of range) to 0b1 (extra bits read), to get a distance of 6.
-   We copy from 6 characters ago in the output stream. The stream so far is “hello h”, so 6 characters back is starting at “e”. We copy 16 characters, resulting in “hello h**ello hello hello**“. Why this copy didn’t start with the second “h” instead of the second “e”, I’m not sure.
-   Byte 19-20: 1 **00111010** 0000000: A literal. 00111010 (58) minus 00110000 (48) is 10. 10 in ASCII is “\\n” (new line)
-   Byte 20: 0 **0000000**: End of block. In this case we ended nicely on the block boundry, too. This is the final block, so we’re done decoding entirely.
-   At this point we’d check the CRC32 and length match what’s in the gzip footer right after the block.

Our final output is “hello hello hello hello\\n”, which is exactly what we expected.

## Gzip format: Compressing a file

Let’s generate a second example using a file.

    echo -en "\xff\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6\xf5\xf4\xf3\xf2\xf1" >test.bin
    gzip test.bin

This input file is pretty weird. In fact, it’s so weird that gzip compression will fail to reduce its size at all. We’ll take a look at what happens when compression fails in the next DEFLATE section below. But first, let’s see how gzip changes with a file instead of a stdin stream.

Byte

0

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19-38

39

40

41

42

43

44

45

46

Hex

1f

8b

08

08

9f

08

ea

60

00

03

74

65

73

74

2e

62

69

6e

00

see below

c6

d3

15

7e

0f

00

00

00

binary garbage (2) – abridged gzip contents

Okay, let’s take a look at how the header and footer changed.

-   Byte 0+1 (1f8b): Two fixed bytes that indicate “this is a gzip file”. These file-type indicators are also called “magic bytes”.
-   Byte 2 (08): Indicates “the compression format is DEFLATE”. DEFLATE is the only format supported by gzip.
-   Byte 3 (08): Flags. 8 single-bit flags.
    -   Not set: TEXT (indicates this is ASCII text. hint to the decompressor only. i think gzip never sets this flag)
    -   Not set: HCRC (adds a 16-bit CRC to the header)
    -   Not set: EXTRA (adds an “extras” field to the header)
    -   **Set: NAME** (adds a filename to the header)
    -   Not set: COMMENT (adds a comment to the header)
    -   There are also three reserved bits which are not used.
-   **Byte 4-7 (9f08ea60) . Mtime.** This is in little-endian order: 0x60ea089f is 1625950367. This is a unix timestamp — 1625950367 seconds after midnight, Jan 1, 1970 is 2021-07-10 20:52:47 UTC, which is indeed earlier today. This is the time the original file was last changed, not when compression happened. This is here so we can restore the original modification time if we want.
-   Byte 8 (00): Extra flags. None are set.
-   Byte 9 (03): OS. OS “03” is Unix.
-   **Byte 10-18 (74 65 73 74 2e 62 69 6e 00): Zero-terminated string.** The string is “test.bin”, the name of the file to decompress. We know this field is present because of the flag set.
-   Byte 19-38: The compressed DEFLATE stream.
-   **Byte 39-42 (c6d3157e): CRC32 of the uncompressed data.** Again, I’ll just assume this is correct.
-   **Byte 25-28 (0f000000): Size of the uncompressed data.** 0x0000000f = 15 bytes, which is correct.

## DEFLATE format: Uncompressed data

Uncompressed data is fairly rare in the wild from what I’ve seen, but for the sake of completeness we’ll cover it.

Byte

19

20

21

22

23

24-38

Hex

01

0f

00

f0

ff

ff fe fd fc fa f9 f8 f7 f6 f5 f4 f3 f2 f1

Binary

00000001

00001111

00000000

11110000

11111111

omitted

R. Binary

10000000

11110000

00000000

00001111

11111111

omitted

binary garbage (2) – DEFLATE contents

-   Again, we start reading “r. binary” — the binary bits in reversed order.
-   Byte 19: **1**0000000\. The first three bits are the most important bits in the stream:
    -   1: Last block. The last block flag here means that after this block ends, the DEFLATE stream is over
-   Byte 19: 1**00** **00000**. Not compressed. For a non-compressed block only, we also skip until the end of the byte.
    
    -   **00: Not compressed**
    
    -   01: Fixed huffman coding.
    -   10: Dynamic huffman coding.
-   Byte 20-21: **11110000 00000000**. Copy 15 uncompressed bytes. We reverse the binary bits as usual for fixed fields. 0b0000000000001111 = 0x000f = 15.
-   Byte 22-23: **00001111 11111111.** This is just the NOT (compliment) of byte 20-21 as a check. It can be ignored.
-   Byte 24-38: **ff fe fd fc fb fa f9 f8 f7 f6 f5 f4 f3 f2 f1**: 15 literal bytes of data, which are directly copied to the decompressed output with no processing. Since we only have one block, this is the whole of the decompressed data.

## DEFLATE format: Dynamic huffman coding

Dynamic huffman coding is by far the most complicated part of the DEFLATE and gzip specs. It also shows up a lot in practice, so we need to learn this too. Let’s take a look with a third and final example.

    echo -n "abaabbbabaababbaababaaaabaaabbbbbaa" | gzip

The bytes we get are:

-   Byte 0-9 (**1f 8b 08 00 00 00 00 00 00 03**): Header
-   Byte 10-32 (1d c6 49 01 00 00 10 40 c0 ac a3 7f 88 3d 3c 20 2a 97 9d 37 5e 1d 0c): DEFLATE contents
-   Byte 33-40 (**6e 29 34 94 23 00 00 00**): Footer. The uncompressed data is 35 bytes.

We’ve already seen everything interesting in the gzip format, so we’ll skip the header and footer, and move straight to looking at DEFLATE this time.

Byte

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

Hex

1d

c6

49

01

00

00

10

40

c0

ac

a3

7f

88

3d

3c

20

2a

97

9d

37

5e

1d

0c

Binary

00011101

11000110

01001001

00000001

00000000

00000000

00010000

01000000

11000000

10101100

10100011

01111111

10001000

00111101

00111100

00100000

00101010

10010111

10011101

00110111

01011110

00011101

00001100

R. Binary

10111000

01100011

10010010

10000000

00000000

00000000

10000000

00000010

00000011

00110101

11000101

11111110

00010001

10111100

00111100

00000100

01010100

11101001

10111001

11101100

01111010

10111000

00110000

abaa stream – DEFLATE contents

-   As usual, we read “r. binary” — the binary bits in reversed order.
-   Byte 10: **1**0111000\. Last (only) block. The DEFLATE stream is over after this block.
-   Byte 10: 1**01**11000\. 10=Dynamic huffman coding
    
    -   00: Not compressed
    
    -   01: Fixed huffman coding.
    -   **10: Dynamic huffman coding.**

## Which parts are dynamic?

Okay, so what does “dynamic” huffman coding mean? A fixed huffman code had several hardcoded values defined by the spec. Some are still hardcoded, but some will now be defined by the gzip file.

1.  The available literals are all single-byte literals. **The literals remain fixed by the spec.**
2.  There is a “special” literal indicating the end of the block in both.
3.  The lengths (how far to look backwards when copying) were given as ranges whose size was a power of two. For example, there would be one binary code (0001011) for the length range 15-16. Then, we would read one extra bit (because the range is 2^1 elements long) to find the specific length within that range. **In a dynamic coding, the length ranges remain fixed by the spec.** (“length lookup” table)
4.  Again, the actual ranges and literals are fixed by the spec. **The binary codewords to represent (lengths/literals/end-of-block) are defined in the gzip stream instead of hardcoded.** (“literal/end-of-block/length huffman codes” table)
5.  Like the literal ranges, **the distance ranges remain fixed by the spec.** (“distance lookup” table)
6.  Although the distance ranges themselves are fixed, **the binary codewords to represent distance ranges are defined in the gzip stream instead of hardcoded.** (“distance huffman codes” table)

So basically, the possible lengths and distances are still the same (fixed) ranges, and the literals are still the same fixed literals. But where we had two hardcoded tables before, now we will load these two tables from the file. Since storing a table is bulky, the DEFLATE authors heavily compressed the representation of the tables, which is why dynamic huffman coding is so complicated.

## Aside: Storing Prefix-Free Codewords as a List of Lengths

Suppose we have a set of prefix-free codewords: 0, 10, 1100, 1101, 1110, 1111. Forget about what each codeword means for a second, we’re just going to look at the codewords themselves.

We can store the lengths as a list: 1, 2, 4, 4, 4, 4.

-   You could make another set of codewords with the same list of lengths. But for our purposes, as long as each value gets the same length of codeword, we don’t really care which of those codes we pick–the compressed content will be the same length.
-   Since we don’t really care how if the bits change, any code is fine. For simplicity, we pick a unique “standard” code. When we list the codewords, the standard one can be listed BOTH in order of length, AND in normal sorted order. That is, the those two orders are the same. The example code above is a standard code. Here’s one that isn’t: 1, 01, 00.
-   It turns out that if we have the lengths, we can generate a set of prefix-free codewords with those lengths. There’s an easy algorithm to generate the “standard” code from the list of lengths (see RFC 1951, it’s not very interesting)
-   Since we picked the standard codewords, we can switch back and forth between codewords and codeword lengths without losing any information.
-   It’s more compact to store the codeword lengths than the actual codewords. DEFLATE just stores codeword lengths everywhere (and uses the corresponding generated code).

Finally, we need to make them correspond to symbols, so we actually store

-   We store lengths for each symbol: A=4, B=1, C=4, D=4, E=2, F=4
-   We can get the correct codewords by going through the symbols in order, and grabbing the first available standard codeword: A=1100, B=0, C=1101, D=1110, E=10, F=1111.

## Dynamic Huffman: Code Lengths

What’s a “code length”? It’s yet another hardcoded lookup table, which explains how to compress the dynamic huffman code tree itself. We’ll get to it in a second–the important thing about it for now is that there are 19 rows in the table. The binary column (not yet filled in) is what we’re about to decode.

Binary

Code

What it means

Extra bits

?

0-15

Code length 0-15

0

?

16

Copy the previous code length 3-6 times

2

?

17

Copy “0” code length 3-10 times

3

?

18

Copy “0” code length 11-138 times

7

Code Lengths (static)

-   Byte 10: 101 **11000**. Number of literal/end-of-block/length codes (257-286). Read bits in forward order, 0b00011=3, plus 257 is 260 length/end-of-block/literal codes.
-   Byte 11: **01100** 011. Number of distance codes (1-32). Read bits in forward order, 0b00110=6, plus 1 is 7 distance codes.
-   Byte 11-12: 01100 **0111** 0010010\. Number of *code length codes* used (4-19). Read bits in forward order, 0b1110=14, plus 4 is 18.
-   Byte 12-18 1 **001 001 010 000 000 000 000 000 000 000 000 001 000 000 000 100 000 001** 1: There are 18 codes used (out of 19 available). For each code length code, we read a 3-bit number (in big-endian order) called the “code length code length”, and fill the end with 0s: 4, 4, 2, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0, 4\[, 0\]
-   Next, we re-order the codes in the order 16, 17, 18, 0, 8, 7, 9, 6, 10, 5, 11, 4, 12, 3, 13, 2, 14, 1, 15. This re-order is just part of the spec, don’t ask why–it’s to save a small amount of space.  
    The old order is: 16: 4, 17: 4, 18: 2, 0:0, 8:0, 7:0, 9:0, 6:0, 10:0, 5:0, 11:0, 4:4, 12:0, 3:0, 13:0, 2:1, 14:0, 1:4, 15:0  
    The new order is: 0:0, 1:4, 2:1, 3:0, 4:4, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16: 4, 17: 4, 18: 2
-   0s indicate the row is not used (no codeword needed). Let’s re-write it without those.  
    1:4, 2:1, 4:4, 16: 4, 17: 4, 18: 2
-   Now we assign a binary codewords of length N, to each length N in the list.  
    1:1100,2:0,4:1101,16:1110,17:1111,18:10
-   Finally, let’s take a look at the whole table again.

Binary

Code

What it means

Extra bits

1100

1

Code length 1

0

0

2

Code length 2

0

1101

4

Code length 4

0

1110

16

Copy the previous code length 3-6 times

2

1111

17

Copy “0” code length 3-10 times

3

10

18

Copy “0” code length 11-138 times

7

Code Lengths

-   Great, we’ve parsed the code lengths table.

## Dynamic Huffman: Parsing the Huffman tree

-   As a reminder, in bytes 10-12 we found there was a 260-row literal/end-of-block/length table and a 7-row distance table. Let’s read 267 numbers: the lengths of the codeword for each row.
-   Byte 18-19: 0000001 **10 0110101**. Copy “0” code length 11-138 times  
    0b1010110=86, plus 11 is 97. Literals 0-96 are not present.
-   Byte 20: **1100** 0101: Literal 1. Literal 97 (‘a’) has a codeword of length 1.
-   Byte 20: 1100 **0** 101: Literal 2. Number 98 (‘b’) has a codeword of length 2.
-   Byte 20-21: 11000 **10 1111111** 10. Copy “0” code length 11-138 times. 0b1111111=127, plus 11 is 138. Literals 99-236 are not present.
-   Byte 21-22: 111111 **10** **0001000** 1. Copy “0” code length 11-138 times. 0b0001000=8, plus 11 is 19. Literals 237-255 are not present.
-   Bytes 22-23: 0001000 **1101** 11100\. Literal 256 (end-of-block) has a codeword of length 4.
-   Byte 23-24: 101 **1110** **00** 0111100. Copy previous code 3-6 times. 0b00=0, plus 3 is 3. “Literals” 257-259 (all lengths) have codewords of length 4.
-   We read 260 numbers, that’s the whole literal/end-of-block/length table. Assign the “standard” binary codewords based on the lengths to generate the following table:

Literal Code

Code Length

Binary

Meaning

Extra bits

97

1

0

Literal ‘a’

0

98

2

10

Literal ‘b’

0

256

4

1100

End-of-block

0

257

4

1101

Length 3

0

258

4

1110

Length 4

0

259

4

1111

Length 5

0

abaa dynamic literal/end-of-block/length Huffman codes

-   Now we read 7 more numbers in the same format: the 7-row distances table.
-   Byte 24: 0 **0** 111100\. Distance 0 has a codeword of length 2.
-   Byte 24-25: 00 **1111** **000** 0000100. Copy “0” code length 3-10 times. 0b000=0, plus 3 is 3. Distances 1-3 are not present.
-   Byte 25: 0 **0 0 0** 0100: Distances 4-6 have length 2.
-   We read 7 numbers, that’s the whole distances table. Assign the “standard” binary codewords to generate the following table:

Code

Bits

Binary

Meaning

Extra Bits

0

2

00

Distance 1

0

4

2

01

Distance 5-6

1

5

2

10

Distance 7-8

1

6

2

11

Distance 9-12

2

abaa dynamic literal/end-of-block/length Huffman codes

## Dynamic Huffman: Data stream decoding

-   Now we’re ready to actually decode the data. Again, we’re reading a series of codes from the literal/end-of-block/length Huffman code table.
-   Byte 25: 0000**0 10 0**: Literal ‘a’, ‘b’, ‘a’
-   Byte 26: **0** **10** **10** **10** **0**: Literal ‘a’, ‘b’, ‘b’, ‘b’, ‘a’.
-   Byte 27: **1110 10** **0** 1. Length 4. Whenever we read a length, we read a distance. The distance is a range, 7-8. The extra bit we read is 0b0=0, plus 7 is Distance 7. So we look back 7 bytes and copy 4. The new output is: baabbba**baab**
-   Byte 27-28: 1110100 **1101** **11** **00** 1: Length 3, Distance 9. We look back 9 bytes and copy 3. The new output is: abbabaab**abb**
-   Byte 28-29: 1011100 **1111** **01** **1** 00. Length 5, Distance 6. We look back 6 bytes and copy 5. The new output is: aababb**aabab**
-   Byte 29: 111011 **0 0**. Literal ‘a’, ‘a’.
-   Byte 30: **0** 1111010. Literal ‘a’.
-   Byte 30: 0 **1111 01** **0**. Length 5, Distance 5. We look back 5 bytes and copy 5. The new output is: abaaa**abaaa**
-   Byte 31: **10** 111000: Literal ‘b’
-   Byte 31: 10 **1110** **00**: Length 4, Distance 1. We look back 1 byte and copy 4. The new output is: b**bbbb**
-   Byte 32: **0 0** 110000: Literal ‘a’, ‘a’.
-   Byte 32: 00 **1100** **00**: End-of block. Since this is the final block it’s also the end of the stream. This didn’t come up in the first example, but we zero-pad until the end of the byte when the block ends.
-   The final output is a b a a b b b a baab abb aabab a a a abaaa b bbbb a a (spaces added for clarity), which is exactly what we expected.

1.  ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
    
    [July 23, 2021 at 1:47 pm][13]
    
    “Now we assign a binary codewords of length N, to each length N in the list.  
    1:1100,2:0,4:1101,16:1110,17:1111,18:10”  
    
    There’s no explanation as to where you pulled these bits from, I understand the number of bits comes from the aforementioned 414442 pulled out prior to this but I’ve seen nothing that explains how you pulled out the bit values for each of these code words
    
    [Reply][14]
    
    -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
        
        [July 23, 2021 at 2:04 pm][15]
        
        This is what “Aside: Storing Prefix-Free Codewords as a List of Lengths” is about. The algorithm is given in full in RFC 1952 if you’re interested. Basically, the code words are assigned starting from 0 (or 00, 000, etc) and counting up. As each code is assigned, anything with that code as a prefix becomes unavailable. They are assigned first from shortest to longest, and in the case of ties from leftmost in the list to rightmost in the list.
        
        So first we assign 0 to the length-1 codeword (0 is lower than 1), then we assign the length-2 codeword 10 (the lowest length-2 code that doesn’t have a prefix 0), and finally we assign the length-4 codewords from left to right (1100, 1101, 1110, 1111 don’t have a prefix of 0 or 10 — they are the lowest and only codewords without one of those prefixes).
        
        Thanks for the comment, it makes me happy to know anyone is reading this, and it’s very helpful to know what’s unclear in my writeup. I’d love to make it as good as possible.
        
        [Reply][16]
        
        -   ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
            
            [July 23, 2021 at 3:23 pm][17]
            
            I think I get it now, as soon as I resolve some compile errors I’m gonna try this:
            
            “\`  
            while ( cur\_leng < max\_leng )  
            {  
            for ( uint j = 0; j leng > cur\_leng )  
            continue;  
              
              
              
            
            word->code = code;
            
            code++;  
            }  
            
            while ( !(code >> cur\_leng) )  
            ++code;  
            
            ++cur\_leng;  
            }  
            “\`  
              
            
            [Reply][18]
            
2.  ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
    
    [July 25, 2021 at 12:06 pm][19]
    
    Took me a while to understand that I was supposed to be building the tree at this point (although this method compared to what I though of and implemented prior to this is inefficient both in space and speed, also terribly um-intuitive). I’m having trouble understanding exactly how to extract some literals you’ve mentioned:
    
    “Byte 18-19: 0000001 10 0110101. Copy “0” code length 11-138 times  
    0b1010110=86, plus 11 is 97. Literals 0-96 are not present.  
    Byte 20: 1100 0101: Literal 1. Literal 97 (‘a’) has a codeword of length 1.  
    Byte 20: 1100 0 101: Literal 2. Number 98 (‘b’) has a codeword of length 2.”  
      
      
    
    At first I though to get the literals I was supposed to add the code list position to the copy count but then I saw this after:
    
    “Byte 20-21: 11000 10 1111111 10. Copy “0” code length 11-138 times. 0b1111111=127, plus 11 is 138. Literals 99-236 are not present.  
    Byte 21-22: 111111 10 0001000 1. Copy “0” code length 11-138 times. 0b0001000=8, plus 11 is 19. Literals 237-255 are not present”
    
    Which doesn’t follow that pattern, how do you determine the literals range?
    
    [Reply][20]
    
    -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
        
        [July 25, 2021 at 12:27 pm][21]
        
        I’m glad this was helpful, but you should really go read RFC 1951 if you’re going to build a decoder. This isn’t meant to be a stand-alone guide.
        
        I’m pretty lost trying to follow this comment, sorry. To clarify, for the “dynamic” compression, you first extract the CODING TABLE for the literals (the step you’re talking about). Then, you use the coding table to decompress the actual stream of content. It’s a two-step process, which is why it’s so complex.
        
        The key point I suspect you’re missed was: “Let’s read 267 numbers: the lengths of the codeword for each row.” These numbers are the length of the code for each literal in order (all of them, not just some of them). A length of 0 means “not present”.
        
        [Reply][22]
        
        -   ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
            
            [July 25, 2021 at 1:41 pm][23]
            
            Was gonna say I already had the code table but when it printed it seems the codes got corrupted, I’ll have to get back to you after fixing it. Anyways I find “guides” that don’t use real examples as this one does to be confusing sometimes, usually where it matters, that’s why I was consulting you who provided those key examples, I got a heck of a lot further with your guide than any other I’ve tried following which didn’t give the byte by byte, bit by bit example.
            
            [Reply][24]
            
            -   ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
                
                [July 25, 2021 at 1:50 pm][25]
                
                Turned out I was just printing the wrong value, here’s my current output:
                
                \`  
                ./a.out aba.gz  
                path = ‘aba.gz’  
                PrintStreamDetails( 0x7ffd2cf70d80 ): ptr = 0x556653fbc480, pos = 0, num = 0, max = 328, fed = 0  
                PrintBytes( 0x556653fbc480, 41, 16 )  
                1F 8B 0 0 0 0 0 0 0 3 1D C6 49 1 0 0  
                40 C0 AC A3 7F 88 3D 3C 20 2A 97 9D 37 5E 1D C  
                29 34 94 23 0 0 0  
                PrintStreamDetails( 0x7ffd2cf70d80 ): ptr = 0x556653fbc480, pos = 136, num = 80, max = 328, fed = 56  
                gzip.magic = 1F8B, gzip.format = 0, gzip.flags = 0, gzip.mtime = 0, zlib.xflags = 0, zlib.system = 3  
                gzip.flag\_TEXT = false, gzip.flag\_HCRC = false, gzip.flag\_MORE = false, gzip.flag\_NAME = false, gzip.flag\_NOTE = false, gzip.flag\_RESERVED = 0  
                PrintStreamDetails( 0x7ffd2cf70d80 ): ptr = 0x556653fbc480, pos = 136, num = 80, max = 328, fed = 56  
                last = true, type = 2  
                lengc = 260, distc = 7, codec = 18, left = 60  
                pos = 212, max = 328, count = 267  
                left = 61, byte = 18, bit = 7  
                Code Table:  
                \_list\[ 0\]: from = 1, more = 0, leng = 4, copy = 0, code = 1100  
                \_list\[ 1\]: from = 2, more = 0, leng = 1, copy = 0, code = 0  
                \_list\[ 2\]: from = 4, more = 0, leng = 4, copy = 0, code = 1101  
                \_list\[ 3\]: from = 16, more = 2, leng = 4, copy = 3, code = 1110  
                \_list\[ 4\]: from = 17, more = 3, leng = 4, copy = 3, code = 1111  
                \_list\[ 5\]: from = 18, more = 7, leng = 2, copy = 11, code = 10  
                i = 0010 j = 5, from = 18, copy = 97  
                Expecting character ‘a’  
                Expecting character ‘b’  
                i = 0010 j = 5, from = 18, copy = 138  
                i = 0010 j = 5, from = 18, copy = 19  
                Expecting character ”  
                i = 1110 j = 3, from = 16, copy = 3  
                Expecting character ”  
                i = 1111 j = 4, from = 17, copy = 3  
                Expecting character ”  
                Expecting character ”  
                Expecting character ”  
                PrintBytes( 0x556653fbf4a0, 0, 16 )  
                \`
                
                And here’s the currently unfixed loop producing the bottom part of the output (also where the interpretation ends atm)
                
                \`  
                /\* Should be building a tree here. \*/  
                while ( num < count && stream.num < stream.max )  
                {  
                CODEWORD \*word = NULL;  
                uint j = 0;
                
                for ( cur\_leng = 1; cur\_leng <= max\_leng; ++cur\_leng )  
                {  
                i = RevBits( CopyStreamBits( &stream, cur\_leng, false ), cur\_leng );
                
                for ( j = 0; j leng == cur\_leng && word->code == i )  
                {  
                IncStreamCount( &stream, cur\_leng );  
                break;  
                }  
                }
                
                if ( j max\_leng )  
                {  
                printf  
                (  
                “i = %u, j = %u, list.used = %u, cur\_leng = %u\\n”,  
                i, j, list.used, cur\_leng  
                );  
                return Return( ret, EINVAL );  
                }
                
                size = CopyStreamBits( &stream, word->more, true );
                
                if ( word->from >= 16 )  
                {  
                printf( “i = ” );  
                SeeBits( &i, max\_leng );  
                printf  
                (  
                ” j = %u, from = %2u, copy = %u\\n”,  
                j, word->from, (uint)(size + word->copy)  
                );  
                num += min\_literal\_code = size + word->copy;  
                }  
                else  
                {  
                int c = (int)(min\_literal\_code + j);  
                printf( “Expecting character ‘%c’\\n”, c );  
                symbol = symbols + num;  
                symbol->sym = (char)c;  
                symbol->len = j;  
                ++num;  
                }  
                }  
                \`
                
                [Reply][26]
                
                -   ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
                    
                    [July 25, 2021 at 3:32 pm][27]
                    
                    Never min, I think I know where the literals are coming from now, I did this:
                    
                    `    printf( "Expecting character '%c', ", c );   printf( "num as a character = '%c'\n", num );    `
                    
                    To see if num lined up, since it did I’m guessing those ranges where all the wasted leaves/branches of the huffman tree.
                    
3.  ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
    
    [July 26, 2021 at 7:46 am][28]
    
    I think I still misunderstood something somewhere, I’ve done a detailed post on the section I think I’ve mis-interpreted here:
    
    [https://cboard.cprogramming.com/c-programming/180462-increment-gone-wrong.html#post1302477][29]
    
    The forum there is better able to handle pre-formatted code than this comment system so please take a look and tell me if you think I’ve mis-interpreted something also, and if so what you think is being mis-interpreted, in mean time I’m going to try and clean up my code so I can upload to gitlab so that you can a clearer idea of where I’m at and perhaps help me get to the last part, converting huffman codes to original values
    
    [Reply][30]
    
    -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
        
        [July 26, 2021 at 8:54 am][31]
        
        Sorry, I don’t really want to help someone else debug code or output. I’d suggest following the links at the start of the blog article. Check out ‘infgen’ in particular.
        
        [Reply][32]
        
        -   ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
            
            [July 26, 2021 at 9:34 am][33]
            
            I originally gave up on infgen due to an access rights error when I tried installing via the package manager, the server refused to let me download it, then after your last comment I though to look for it’s github page, that one worked out fine, judging by it’s output the only thing I’ve got wrong are the length values for the distance symbols/codes/whatever you want to call them, where do you get that 2 from? same applies to the bit code along side them, where does that come from, is it just an iterated number for each valid symbol?
            
            [Reply][34]
            
            -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
                
                [July 26, 2021 at 10:56 am][35]
                
                You read 267=260+7 codeword-lengths (the numbers 260 and 7 are given by bytes 10-12 in this example).
                
                The first 260 codeword-lengths are used for one huffman table: 256 literals (always 256), then 1 “end of block” (always 2), then the remaining 3 are lengths.
                
                The next 7 codeword-lengths are used to generate a second huffman table, for distances. The code generation works exactly the same as for the first table.
                
                [Reply][36]
                
                -   ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
                    
                    [July 26, 2021 at 11:50 am][37]
                    
                    Even if I use the same method of code generation as before I stiil would need to know where you got those “2”s from in the table immediately following this:
                    
                    “We read 7 numbers, that’s the whole distances table. Assign the “standard” binary codewords to generate the following table:”
                    
                    Because the previous method used that to determine what symbols to ignore until the code length increases, more specifically I had a “while ( cur\_leng < max\_leng )" loop and a sub loop that went looking for symbols expecting cur\_leng codes and assigning them that way before using those same codes in another sub loop to decide if the next code should be increased further. Without knowing where those code lengths for the distance came from I can't progress.
                    
                    Thinking about it now I don't even have the codes for the length symbols, I just have the symbols. If it was supposed to be auto generated then I could understand the codes for the length symbols but I then don't understand the codes for the distance codes as they don't follow the huffman principle of no codes that can be misinterpreted.
                    
                -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
                    
                    [July 26, 2021 at 12:23 pm][38]
                    
                    Re-read above the table. The “bits” column is from bytes 24-25.
                    
4.  ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
    
    [July 26, 2021 at 12:43 pm][39]
    
    No option to reply so I’ll do it here instead, I still don’t see where the 2 came from, is that a minimum length or from another hard code table? So far I can only see the bits given as a set/unset symbol & code flag, there’s no clear source for the length & extra bits values
    
    [Reply][40]
    
    -   ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
        
        [July 26, 2021 at 5:54 pm][41]
        
        Finally found where you got the 2 from:
        
        [https://www.w3.org/Graphics/PNG/RFC-1951][42]
        
        ” HDIST + 1 code lengths for the distance alphabet,
        
        encoded using the code length Huffman code  
        ”
        
        That was far too easily over looked, now I at least can generate the codes, though I think I will add a specialised handler and object to minimize code now that it’s getting more complicated than need be.
        
        [Reply][43]
        
5.  ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
    
    [July 31, 2021 at 11:29 am][44]
    
    I’ve clearly misunderstood something somewhere, could you take a look at the code I outlined in the below post please and see if you can spot what I’m misunderstanding, up until the point I have to lookup previously deflated values I’ve read the bits correctly but I’ve obviously not understood all the implied information correctly, I would post the code here but as you’ve seen these comments don’t support maintaining the code formatting resulting in a more confusing than necessary code.
    
    [https://cboard.cprogramming.com/c-programming/180462-increment-gone-wrong-post1302541.html#post1302541][45]
    
    [Reply][46]
    
    -   ![](https://secure.gravatar.com/avatar/a82f569a804e9883d4fc220ed42386f9?s=40&d=mm&r=g)Lee says:
        
        [August 2, 2021 at 5:36 pm][47]
        
        You’ll be glad to know I finally got the algorithm right, have not looked at any source code from zlib or other projects so I’m free to slap MIT License on it the whole way through once I convert it to a cleaner version of itself. The unclean version is here for anyone’s reference.
        
        [https://gitlab.com/awsdert/uc-evidence/-/tree/9441a73e59834456c41c1049036fc60925b705a0][48]
        
        [Reply][49]
        
6.  ![](https://secure.gravatar.com/avatar/7872694d27b3b6fd8d71297a4799a82b?s=40&d=mm&r=g)neubert says:
    
    [December 21, 2021 at 1:00 am][50]
    
    From the Fixed huffman coding section:
    
    “Byte 10-11: 110 10011000 10010: A literal. 10011000 (152) minus 00110000 (48) is 104. 104 in ASCII is ‘h’.”
    
    Why are you subtracting 48?
    
    [Reply][51]
    
    -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
        
        [December 21, 2021 at 1:11 am][52]
        
        The binary range (given above) is 00110000-10111111. Rather than decoding the binary value, we decode the offset within that range.
        
        [Reply][53]
        
7.  ![](https://secure.gravatar.com/avatar/7872694d27b3b6fd8d71297a4799a82b?s=40&d=mm&r=g)neubert says:
    
    [December 22, 2021 at 7:27 am][54]
    
    “Now we assign a binary codewords of length N, to each length N in the list.  
    1:1100,2:0,4:1101,16:1110,17:1111,18:10”
    
    Could you elaborate on this? I thought I could get the same thing by using huffman encoding, using the code length as the frequency, but when I do that I get this:
    
    1:111,2:1100,4:00,16:10,17:01,18:1101
    
    Thanks!
    
    [Reply][55]
    
    -   ![](https://secure.gravatar.com/avatar/7872694d27b3b6fd8d71297a4799a82b?s=40&d=mm&r=g)neubert says:
        
        [December 22, 2021 at 10:49 pm][56]
        
        I figured it out. It’s this bit from RFC1951:
        
        `   1) Count the number of codes for each code length. Let   bl_count[N] be the number of codes of length N, N >= 1.`
        
        2) Find the numerical value of the smallest code for each  
        code length:
        
        code = 0;  
        bl\_count\[0\] = 0;  
        for (bits = 1; bits <= MAX\_BITS; bits++) {  
        code = (code + bl\_count\[bits-1\]) << 1;  
        next\_code\[bits\] = code;  
        }
        
        3) Assign numerical values to all codes, using consecutive  
        values for all codes of the same length with the base  
        values determined at step 2. Codes that are never used  
        (which have a bit length of zero) must not be assigned a  
        value.
        
        for (n = 0; n <= max\_code; n++) {  
        len = tree\[n\].Len;  
        if (len != 0) {  
        tree\[n\].Code = next\_code\[len\];  
        next\_code\[len\]++;  
        }  
        
        [Reply][57]
        
8.  ![](https://secure.gravatar.com/avatar/7872694d27b3b6fd8d71297a4799a82b?s=40&d=mm&r=g)neubert says:
    
    [December 24, 2021 at 10:38 pm][58]
    
    ““Literals” 257-259 (all lengths) have codewords of length 4” Is this a hard and fast rule that’s always true regardless of the data or is this true \_just\_ for the compressed string in this example?
    
    [Reply][59]
    
    -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
        
        [December 25, 2021 at 2:25 pm][60]
        
        Just for the example. If it was always true, we wouldn’t have to encode it.
        
        [Reply][61]
        
9.  ![](https://secure.gravatar.com/avatar/7872694d27b3b6fd8d71297a4799a82b?s=40&d=mm&r=g)neubert says:
    
    [December 27, 2021 at 12:54 am][62]
    
    “Byte 27: 1110 10 0 1. Length 4. Whenever we read a length, we read a distance. The distance is a range, 7-8. The extra bit we read is 0b0=0, plus 7 is Distance 7. So we look back 7 bytes and copy 4. The new output is: baabbbabaab”
    
    I think there should be an extra a before the baabbbabaab
    
    [Reply][63]
    
10.  ![](https://secure.gravatar.com/avatar/83113fa84f7bb884648d75b769d23a6c?s=40&d=mm&r=g)inco says:
    
    [June 22, 2022 at 1:56 pm][64]
    
    I’ve been reading quite a bit on DEFLATE in png files and I think this is the exact level of depth i needed to crack this whole mess. Thanks so much for writing this, sources like RFC1951 talk more about abstraction and general rules but to have a few examples lined out here its EXTREMELY useful. Thanks again
    
    [Reply][65]
    
    -   ![](https://secure.gravatar.com/avatar/83113fa84f7bb884648d75b769d23a6c?s=40&d=mm&r=g)inco says:
        
        [June 22, 2022 at 3:38 pm][66]
        
        Small question about reading bits: for Huffman codes of the code itself defines a length range and then the extra bits are reversed so that they can be interpreted. But should I reverse the distance or the distance extra bits as well?
        
        [Reply][67]
        
11.  ![](https://secure.gravatar.com/avatar/7b25d5e576e752e12d04d663247f0989?s=40&d=mm&r=g)Ricardo says:
    
    [May 31, 2024 at 4:32 am][68]
    
    Byte 31: 10 111000: Literal ‘b’  
    Byte 31: 10 1110 00: Length 4, Distance 1. We look back 1 byte and copy 4. The new output is: bbbbb
    
    How can I understand the distance 1 and copy 4 symbols?  
    Should I repeat the ‘b’ four times?
    
    What if the distance was 2 and copying 4 symbols?
    
    [Reply][69]
    
    -   ![](https://secure.gravatar.com/avatar/09485be3ee1e86da6e39412f5c1b2a48?s=40&d=mm&r=g)admin says:
        
        [May 31, 2024 at 5:23 pm][70]
        
        Distance is how far back you start. Copy is how many symbols you copy.  
        You just blindly copy characters starting DISTANCE back, but since you’re appending to the string, you never run out of symbols to copy.
        
        If your string so far was “Wow, copying is really neat”, with distance 3 and copy 10 you would add: eateateate
        
        [Reply][71]
        

[1]: https://www.rfc-editor.org/rfc/rfc1951.txt
[2]: https://www.rfc-editor.org/rfc/rfc1952.txt
[3]: https://github.com/madler/infgen
[4]: https://github.com/madler/infgen/blob/master/infgen.c
[5]: https://zlib.net/feldspar.html
[6]: https://en.wikipedia.org/wiki/LZ77_and_LZ78
[7]: https://en.wikipedia.org/wiki/Prefix_code
[8]: https://en.wikipedia.org/wiki/Huffman_coding
[9]: https://github.com/madler/zlib/blob/master/contrib/puff/puff.c
[10]: https://www.rfc-editor.org/rfc/rfc1952.txt
[11]: https://www.rfc-editor.org/rfc/rfc1951.txt
[12]: https://en.wikipedia.org/wiki/LZ77_and_LZ78
[13]: https://blog.za3k.com/understanding-gzip-2/#comment-4739
[14]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4739#respond
[15]: https://blog.za3k.com/understanding-gzip-2/#comment-4740
[16]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4740#respond
[17]: https://blog.za3k.com/understanding-gzip-2/#comment-4741
[18]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4741#respond
[19]: https://blog.za3k.com/understanding-gzip-2/#comment-4742
[20]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4742#respond
[21]: https://blog.za3k.com/understanding-gzip-2/#comment-4743
[22]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4743#respond
[23]: https://blog.za3k.com/understanding-gzip-2/#comment-4744
[24]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4744#respond
[25]: https://blog.za3k.com/understanding-gzip-2/#comment-4745
[26]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4745#respond
[27]: https://blog.za3k.com/understanding-gzip-2/#comment-4747
[28]: https://blog.za3k.com/understanding-gzip-2/#comment-4756
[29]: https://cboard.cprogramming.com/c-programming/180462-increment-gone-wrong.html#post1302477
[30]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4756#respond
[31]: https://blog.za3k.com/understanding-gzip-2/#comment-4757
[32]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4757#respond
[33]: https://blog.za3k.com/understanding-gzip-2/#comment-4758
[34]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4758#respond
[35]: https://blog.za3k.com/understanding-gzip-2/#comment-4759
[36]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4759#respond
[37]: https://blog.za3k.com/understanding-gzip-2/#comment-4760
[38]: https://blog.za3k.com/understanding-gzip-2/#comment-4762
[39]: https://blog.za3k.com/understanding-gzip-2/#comment-4763
[40]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4763#respond
[41]: https://blog.za3k.com/understanding-gzip-2/#comment-4764
[42]: https://www.w3.org/Graphics/PNG/RFC-1951
[43]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4764#respond
[44]: https://blog.za3k.com/understanding-gzip-2/#comment-4773
[45]: https://cboard.cprogramming.com/c-programming/180462-increment-gone-wrong-post1302541.html#post1302541
[46]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4773#respond
[47]: https://blog.za3k.com/understanding-gzip-2/#comment-4786
[48]: https://gitlab.com/awsdert/uc-evidence/-/tree/9441a73e59834456c41c1049036fc60925b705a0
[49]: https://blog.za3k.com/understanding-gzip-2/?replytocom=4786#respond
[50]: https://blog.za3k.com/understanding-gzip-2/#comment-5413
[51]: https://blog.za3k.com/understanding-gzip-2/?replytocom=5413#respond
[52]: https://blog.za3k.com/understanding-gzip-2/#comment-5414
[53]: https://blog.za3k.com/understanding-gzip-2/?replytocom=5414#respond
[54]: https://blog.za3k.com/understanding-gzip-2/#comment-5432
[55]: https://blog.za3k.com/understanding-gzip-2/?replytocom=5432#respond
[56]: https://blog.za3k.com/understanding-gzip-2/#comment-5435
[57]: https://blog.za3k.com/understanding-gzip-2/?replytocom=5435#respond
[58]: https://blog.za3k.com/understanding-gzip-2/#comment-5441
[59]: https://blog.za3k.com/understanding-gzip-2/?replytocom=5441#respond
[60]: https://blog.za3k.com/understanding-gzip-2/#comment-5444
[61]: https://blog.za3k.com/understanding-gzip-2/?replytocom=5444#respond
[62]: https://blog.za3k.com/understanding-gzip-2/#comment-5449
[63]: https://blog.za3k.com/understanding-gzip-2/?replytocom=5449#respond
[64]: https://blog.za3k.com/understanding-gzip-2/#comment-8298
[65]: https://blog.za3k.com/understanding-gzip-2/?replytocom=8298#respond
[66]: https://blog.za3k.com/understanding-gzip-2/#comment-8300
[67]: https://blog.za3k.com/understanding-gzip-2/?replytocom=8300#respond
[68]: https://blog.za3k.com/understanding-gzip-2/#comment-11528
[69]: https://blog.za3k.com/understanding-gzip-2/?replytocom=11528#respond
[70]: https://blog.za3k.com/understanding-gzip-2/#comment-11531
[71]: https://blog.za3k.com/understanding-gzip-2/?replytocom=11531#respond
