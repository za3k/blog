---
author: admin
categories:
- Technical
date: 2021-07-10 21:36:51-07:00
has-comments: true
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
\[1\] [RFC 1951](https://www.rfc-editor.org/rfc/rfc1951.txt), DEFLATE standard, by Peter Deutsch  
\[2\] [RFC 1952](https://www.rfc-editor.org/rfc/rfc1952.txt), gzip standard, by Peter Deutsch  
\[3\] [infgen](https://github.com/madler/infgen), by Mark Adler (one of the zlib/gzip/DEFLATE authors), a tool for dis-assembling and printing a gzip or DEFLATE stream. I found this useful in figuring out the endian-ness of bitfields, and somewhat in understanding the dynamic huffman decoding process. Documentation is [here](https://github.com/madler/infgen/blob/master/infgen.c).  
\[4\] [An explanation of the ‘deflate’ algorithm](https://zlib.net/feldspar.html) by Antaeus Feldspar. A great conceptual overview of LZ77 and Huffman coding. **I recommend reading this *before* reading my DEFLATE explanation.**  
\[5\] [LZ77](https://en.wikipedia.org/wiki/LZ77_and_LZ78) compression, Wikipedia.  
\[6\] [Prefix-free codes](https://en.wikipedia.org/wiki/Prefix_code) generally and [Huffman](https://en.wikipedia.org/wiki/Huffman_coding)‘s algorithm specifically  
\[7\] After writing this, I learned about [puff.c](https://github.com/madler/zlib/blob/master/contrib/puff/puff.c), a reference (simple) implementation of a DEFLATE decompressor by Mark Adler.

## Gzip format: Basics and compressing a stream

Let’s take a look at our first example. If you’re on Linux, feel free to run the examples I use as we go.

```
echo "hello hello hello hello" | gzip
```

The bytes gzip outputs are below. You can use *xxd* or any other hex dump tool to view binary files. Notice that the original is 24 bytes, while the compressed version is 29 bytes–gzip is not really intended for data this short, so all of the examples in this article actually get bigger.

|     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Byte | **0** | **1** | **2** | **3** | **4** | **5** | **6** | **7** | **8** | **9** | 10  | 11  | 12  | 13  | 14  | 15  | 16  | 17  | 18  | 19  | 20  | **21** | **22** | **23** | **24** | **25** | **26** | **27** | **28** |
| Hex | **1f** | **8b** | **08** | **00** | **00** | **00** | **00** | **00** | **00** | **03** | cb  | 48  | cd  | c9  | c9  | 57  | c8  | 40  | 27  | b9  | 00  | **00** | **88** | **59** | **0b** | **18** | **00** | **00** | **00** |

<figcaption>hello (1) – gzip contents</figcaption>

The beginning and end in bold are the gzip header and footer. I learned the details of the format by reading [RFC 1952: gzip](https://www.rfc-editor.org/rfc/rfc1952.txt)

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

<figure class="wp-block-table" markdown="1">

|     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Byte | 10  | 11  | 12  | 13  | 14  | 15  | 16  | 17  | 18  | 19  | 20  |
| Hex | cb  | 48  | cd  | c9  | c9  | 57  | c8  | 40  | 27  | b9  | 00  |
| Binary | 11001011 | 01001000 | 11001101 | 11001001 | 11001001 | 01010111 | 11001000 | 01000000 | 00100111 | 10111001 | 00000000 |
| R. Bin. | 11010011 | 00010010 | 10110011 | 10010011 | 10010011 | 11101010 | 00010011 | 00000010 | 11100100 | 10011101 | 00000000 |

<figcaption>hello (1) – DEFLATE contents</figcaption>

## DEFLATE format: Basics and fixed huffman coding

DEFLATE is the actual compression format used inside gzip. The format is detailed in [RFC 1951: DEFLATE](https://www.rfc-editor.org/rfc/rfc1951.txt). DEFLATE is a dense format which uses bits instead of bytes, so we need to take a look at the binary, not the hex, and things will not be byte-aligned. The endian-ness is a little confusing in gzip, so we’ll usually be looking at the “reversed binary” row.

-   As a hint, whenever we read bits, we use the “reverse” binary order. For Huffman codes, we keep the bit order in reverse. For fixed-length fields like integers, we reverse again into “normal” binary order. I’ll call out the order for each field.
-   Byte 10: **1** 1010011. Is it the last block? Yes.
    -   1: Last block. The last block flag here means that after this block ends, the DEFLATE stream is over
-   Byte 10: 1 **10** 10011\. Fixed huffman coding. We reverse the bits (because it’s always 2 bits, and we reverse any fixed number of bits) to get 01.
    
    -   00: Not compressed
    
    -   **01: Fixed huffman coding.**
    -   10: Dynamic huffman coding.
    -   11: Not allowed (error)
-   So we’re using “fixed” huffman coding. That means there’s a static, fixed encoding scheme being used, defined by the DEFLATE standard. The scheme is given by the tables below. Note that Length/Distance codes are special–after you read one, you may read some extra bits according to the length/distance lookup tables.

| Binary | Bits | Extra bits | Type | Code |
| --- | --- | --- | --- | --- |
| 00110000-10111111 | 8   | 0   | Literal byte | 0-143 |
| 110010000-111111111 | 9   | 0   | Literal byte | 144-255 |
| 0000000 | 7   | 0   | End of block | 256 |
| 0000001-0010111 | 7   | varies | Length | 257-279 |
| 11000000-11000111 | 8   | varies | Length | 280-285 |

<figcaption>Literal/End of Block/Length Huffman codes</figcaption>

| Binary Code | Bits | Extra bits | Type | Value |
| --- | --- | --- | --- | --- |
| 00000-111111 | 5   | varies | Distance | 0-31 |

<figcaption>Distance Huffman codes</figcaption>

| Code | Binary | Meaning | Extra bits |
| --- | --- | --- | --- |
| 267 | 0001011 | Length 15-16 | 1   |

<figcaption>Length lookup (abridged)</figcaption>

| Code | Binary | Meaning | Extra bits |
| --- | --- | --- | --- |
| 4   | 00100 | Distance 5-6 | 1   |

<figcaption>Distance lookup (abridged)</figcaption>

-   Now we read a series of codes. Each code might be
    -   a literal (one binary byte), which is directly copied to the output
    -   “end of block”. either another block is read, or if this was the last block, DEFLATE stops.
    -   a length-distance pair. first code is a length, then a distance is read. then some of the output is copied–this reduces the size of repetitive content. the compressor/decompressor can look up to 32KB backwards for duplicate content. This copying scheme is called [LZ77](https://en.wikipedia.org/wiki/LZ77_and_LZ78).
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

```
echo -en "\xff\xfe\xfd\xfc\xfb\xfa\xf9\xf8\xf7\xf6\xf5\xf4\xf3\xf2\xf1" >test.bin
gzip test.bin
```

This input file is pretty weird. In fact, it’s so weird that gzip compression will fail to reduce its size at all. We’ll take a look at what happens when compression fails in the next DEFLATE section below. But first, let’s see how gzip changes with a file instead of a stdin stream.

|     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Byte | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   | 9   | 10  | 11  | 12  | 13  | 14  | 15  | 16  | 17  | 18  | 19-38 | 39  | 40  | 41  | 42  | 43  | 44  | 45  | 46  |
| Hex | 1f  | 8b  | 08  | 08  | 9f  | 08  | ea  | 60  | 00  | 03  | 74  | 65  | 73  | 74  | 2e  | 62  | 69  | 6e  | 00  | see below | c6  | d3  | 15  | 7e  | 0f  | 00  | 00  | 00  |

<figcaption>binary garbage (2) – abridged gzip contents</figcaption>

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

|     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- |
| Byte | 19  | 20  | 21  | 22  | 23  | 24-38 |
| Hex | 01  | 0f  | 00  | f0  | ff  | ff fe fd fc fa f9 f8 f7 f6 f5 f4 f3 f2 f1 |
| Binary | 00000001 | 00001111 | 00000000 | 11110000 | 11111111 | omitted |
| R. Binary | 10000000 | 11110000 | 00000000 | 00001111 | 11111111 | omitted |

<figcaption>binary garbage (2) – DEFLATE contents</figcaption>

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

```
echo -n "abaabbbabaababbaababaaaabaaabbbbbaa" | gzip
```

The bytes we get are:

-   Byte 0-9 (**1f 8b 08 00 00 00 00 00 00 03**): Header
-   Byte 10-32 (1d c6 49 01 00 00 10 40 c0 ac a3 7f 88 3d 3c 20 2a 97 9d 37 5e 1d 0c): DEFLATE contents
-   Byte 33-40 (**6e 29 34 94 23 00 00 00**): Footer. The uncompressed data is 35 bytes.

We’ve already seen everything interesting in the gzip format, so we’ll skip the header and footer, and move straight to looking at DEFLATE this time.

|     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Byte | 10  | 11  | 12  | 13  | 14  | 15  | 16  | 17  | 18  | 19  | 20  | 21  | 22  | 23  | 24  | 25  | 26  | 27  | 28  | 29  | 30  | 31  | 32  |
| Hex | 1d  | c6  | 49  | 01  | 00  | 00  | 10  | 40  | c0  | ac  | a3  | 7f  | 88  | 3d  | 3c  | 20  | 2a  | 97  | 9d  | 37  | 5e  | 1d  | 0c  |
| Binary | 00011101 | 11000110 | 01001001 | 00000001 | 00000000 | 00000000 | 00010000 | 01000000 | 11000000 | 10101100 | 10100011 | 01111111 | 10001000 | 00111101 | 00111100 | 00100000 | 00101010 | 10010111 | 10011101 | 00110111 | 01011110 | 00011101 | 00001100 |
| R. Binary | 10111000 | 01100011 | 10010010 | 10000000 | 00000000 | 00000000 | 10000000 | 00000010 | 00000011 | 00110101 | 11000101 | 11111110 | 00010001 | 10111100 | 00111100 | 00000100 | 01010100 | 11101001 | 10111001 | 11101100 | 01111010 | 10111000 | 00110000 |

<figcaption>abaa stream – DEFLATE contents</figcaption>

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

|     |     |     |     |
| --- | --- | --- | --- |
| Binary | Code | What it means | Extra bits |
| ?   | 0-15 | Code length 0-15 | 0   |
| ?   | 16  | Copy the previous code length 3-6 times | 2   |
| ?   | 17  | Copy “0” code length 3-10 times | 3   |
| ?   | 18  | Copy “0” code length 11-138 times | 7   |

<figcaption>Code Lengths (static)</figcaption>

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

| Binary | Code | What it means | Extra bits |
| --- | --- | --- | --- |
| 1100 | 1   | Code length 1 | 0   |
| 0   | 2   | Code length 2 | 0   |
| 1101 | 4   | Code length 4 | 0   |
| 1110 | 16  | Copy the previous code length 3-6 times | 2   |
| 1111 | 17  | Copy “0” code length 3-10 times | 3   |
| 10  | 18  | Copy “0” code length 11-138 times | 7   |

<figcaption>Code Lengths</figcaption>

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

| Literal Code | Code Length | Binary | Meaning | Extra bits |
| --- | --- | --- | --- | --- |
| 97  | 1   | 0   | Literal ‘a’ | 0   |
| 98  | 2   | 10  | Literal ‘b’ | 0   |
| 256 | 4   | 1100 | End-of-block | 0   |
| 257 | 4   | 1101 | Length 3 | 0   |
| 258 | 4   | 1110 | Length 4 | 0   |
| 259 | 4   | 1111 | Length 5 | 0   |

<figcaption>abaa dynamic literal/end-of-block/length Huffman codes</figcaption>

-   Now we read 7 more numbers in the same format: the 7-row distances table.
-   Byte 24: 0 **0** 111100\. Distance 0 has a codeword of length 2.
-   Byte 24-25: 00 **1111** **000** 0000100. Copy “0” code length 3-10 times. 0b000=0, plus 3 is 3. Distances 1-3 are not present.
-   Byte 25: 0 **0 0 0** 0100: Distances 4-6 have length 2.
-   We read 7 numbers, that’s the whole distances table. Assign the “standard” binary codewords to generate the following table:

| Code | Bits | Binary | Meaning | Extra Bits |
| --- | --- | --- | --- | --- |
| 0   | 2   | 00  | Distance 1 | 0   |
| 4   | 2   | 01  | Distance 5-6 | 1   |
| 5   | 2   | 10  | Distance 7-8 | 1   |
| 6   | 2   | 11  | Distance 9-12 | 2   |

<figcaption>abaa dynamic literal/end-of-block/length Huffman codes</figcaption>

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
