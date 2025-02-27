---
author: admin
categories:
- Technical
date: 2025-02-27
tags:
- programming
- golang
title: 'The Go Programming Language'
---
I recently read "The Go Programming Language" by Alan A. A. Donovan and Brian W. Kernighan. (I like to imagine Mr. Donovan's full name is Alan Alan Alan Donovan--please don't correct me.) So far I have read the book cover to cover, but not programmed any significant Go.

While reading, I wrote myself a list of questions to look up after I finished. Here are the questions (together with answers).

**Q20**: Go came out in 2012 with version 1.0. The book was published in 2016 and uses Go 1.5. As of writing it is 2025, and the latest version is 1.24. What has changed in Go since the book came out and now? (Note: Language changes only, no library or tooling changes mentioned)

- 1.6 (2016) - No changes
- 1.7 - No changes*
- 1.8 (2017) - No changes*
- 1.9
    - Introduced type aliases
- 1.10 (2018) - No changes*
- 1.11 - No changes
- 1.12 (2019) - No changes
- 1.13
    - New number literal syntax.
    - Shift count can be signed now.
- 1.14 (2020)
    - Allow overlapping methods for embedded interfaces (solves the diamond problem for interfaces)
- 1.15 - None
- 1.16 (2021) - No changes
- 1.17
    - Allows conversion from slice to fixed-size array pointer (can panic)
- 1.18 (2022)
    - Generics--type parameters can be used in type definitions as well as function definitions.
    - Added type `any` as a shorter name for `interface{}`
    - Added type `comparable`: == works
    - Added union types: A or B or C
    - Added type ~T : `~int` is any type whose underlying type is int
- 1.19 - None*
- 1.20 (2023)
    - Allow conversion from slice to fixed-size array.
    - Broading of 'comparable' to include interfaces that might panic at runtime.
- 1.21
    - New built-ins (min, max)
    - New built-in (clear) -- applies or slice or map
    - Type inference improvements which went a bit over my head.
    - Fixed an edge case around `panic(nil)`.
- 1.22 (2024) 
    - Fixes the loop iteration gotcha caused by lexical scoping inside loops. (Previously, there was one loop index which was updated -- now a new variable is created and assigned each loop).
    - For loops can range over integers.
- 1.23
    - Added iterator ranges (iterations are functions).
- 1.24 (2025)
    - Type aliases can be parameterized.


**Q1**: *If you try to take the address `&map`, the compiler prevents you, because the address of a map is its backing store, which can silently change. How is this done? Can I do it for my own types?*

Note: You can take the address of `&map`, just not `&map[2]`.

"It just does that". Map is a built-in type, not an implementation, so it just does stuff you can't. No you can't do it for your own types. There are garbage collection reasons they made it work this way but they're not interesting.

**Q2**: *Can you take the address of a slice? Can the same problem happen?*

You can take the address of both `&slice` and `&slice[2]`.

If `append(slice, 599)` re-allocates the backing store, the second points to the original backing store, and prevents it from being garbage collected. Also, any changes to it are not affected in the slice returned by `append`, so you probably shouldn't.

**Q3**: *What are all the forms of `for` loops?*

- `for INITIALIZER; CONDITION; POST {}` - C for loop
- `for {}` - Loop forever
- `for CONDITION` - C while loop
- `for index, value := range THING {}` or `for index := range THING {}` or `for range THING {}`. Range can iterate over:
    - array/slice (index, value)
    - string (index, value) - this is unicode code points ("runes") and not bytes 
    - map (key, value) - this is in random order
    - channel (e, N/A) - received elements of a channel
    - Since 1.22: int (index, N/A) - from 0 to N-1
    - Since 1.23: function (T1, T2) - function is called with a "loop body" function, which can be called once with each value, and returns whether to keep iterating
- Note that `break` and `continue` affect loops

**Q4**: *What are the signatures of `range`, if it's a function?*

No, it's a keyword (p27, for Go 1.4 see also p141 gotchas). See Q3 for all the range variants, and Q18 for general function overloading.

**Q5**: *Why does Go say -0 is not equal to 0 in the following code?*

```
var z float64
fmt.Println(-z) // Prints -0
```

IEEE 754 defines a negative zero. Positive and negative compare equal, so code will generally work as you expect. Go chooses to print "-0" rather than "0" for this value in format strings, while other languages print "0" for both.

Additional discoveries:

- `int(-z)` is 0
- the constant `-0.0` is positive zero (!)

**Q6**: *(p98) Why does ReadRune() in invalid unicode return a replacement char with* length 1 *? The replacement char has byte length 2. Is this a deliberate signal value?*

Yes (no citation)

**Q7**: *What happens if you convert `Inf`, `-Inf`, `NaN`, or a float too large to fit into an int, to an int? Book claims conversions don't panic.*

All of them are converted to

- uint/uint64: 2^63 = 9223372036854775808
- int/int64: -2^63 = -9223372036854775808 (even +Inf and 1e200)

I don't know why these particular values. I have [asked on Stack Overflow](https://stackoverflow.com/questions/79473743/why-does-converting-a-float64-to-a-uint64-give-me-this-particular-sentinel-value)

**Q8**: *In Go, can you marshal functions or closures?*

No.

Reflect does not support it (and so neither does json.Marshal, etc). I couldn't immediately come up with a way even to distinguish closures and non-closures, or get the name of a function. You can get a function pointer and then do some heuristics to get the name, maybe.

**Q9.1**: *How do map literals work for non-strings?*

```
map[Point]string{Point{0, 0}: "orig"}
    or
map[Point]string{{0, 0}: "orig"} // Names can be left out of keys or values in map literals
```

**Q9.2**: *Can I make user types with this mechanism? (ex. my own literal initialization)*

No. Literals are only for built-in types, and the mechanism is not extensible. (But you can have the underlying type be a map an initialize your type with one.)

**Q10**: *Struct fields can have metadata ("struct tags"). Can whole types?*

No.

**Q11**: *How does `...` variadic notation fail if the slice can be too short to fill all arguments? Is it only allowed for the variadic argument or can it span multiple?*

Yeah, you have to match it with the variadic argument.

**Q12**: *Thomson, Pike, Kernighan, Richie -- fill in a Venn Diagram of what they made/wrote.*

- Ken Thompson: B, Unix, Plan 9, Go, regexes, UTF8, QED, ed, chess endgames, Inferno, "Reflections on Trusting Trust"
- Dennis Richie: B, C, Unix (inc. man pages?), Plan 9, Inferno, Limbo, "The C Programming Language"
- Brian Kernighan: awk, "The C Programming Language" (including "Hello, world!"), "The Go Programming Language", "The Elements of Programming Style", "The Practice of Programming", "The Unix Programming Environment"
- Rob Pike: Plan 9, Go , Inferno, Limbo, Newsqueak, sam, acme, Sawsall, "The Unix Programming Environment", "The Practice of Programming"

**Q13**: *What order are `deferreds` called in?*

Last in, first out. Then exit the function, and so on up the stack.

**Q14**: *What happens if a `panic` happens, a `deferred` is called, and the `deferred` `panic`s?*

It prints nested panics informationally, but continues to pop the deferreds

**Q15**: *`map[x] = y` panics if `map` is a nil map, but `slice = append(slice, 1)` works fine if `slice` is a nil slice. Why? I feel like I'm being nickle-and-dimed by Go that the zero value panics.*

Both slice and map suck if they're nil. It's just that slice is so bad (normal use case of append panics even for non-nil values) that they added a library `append` function, which happened to deal with the nil case too. 

You can write a `map_set` which returns a new map much like `append`. You can't write a better map, because there's no operator overloading (see also Q17)

**Q16**: *Why is the `*p` vs `p` method consistency principle a thing?*

Because `a.Method()` notation sugars between the two, but interfaces don't. You want at least one of `*p` and `p` to support an interface.

**Q17**: *Is there operator overloading?*

No.

And Go has a broader principle that none of the core language calls any specific method name (`String()`, `Error()`, etc), which came up in the 1.23 iterator design.

**Q18**: *Is there function overloading? (range, map.get, json.Marshal, type assertion)*

Map lookup, type assertion, and channel receive are keyword-level overloading, not functions. They are special cases.

In general, a function has to take the same number of inputs and return the same number of outputs, of the same types. There is one exception, which is that one of the inputs can be variadic--for example, the built-in function `make`.

*1.6 (2016) answer:* BUT, you can "return" a generic type like `interface{}` (which the user has to cast unsafely to the right type) or modify one of the inputs (which can be something like `interface{}`). The latter is how `json.Marshal` works and knows what type to deserialize. To compliment this, you can do runtime inspect of types through a `select` statement or the `reflect` module.

*1.18 (2022) answer*: Same for number of arguments, but also functions can now be generic (ex. type A -> A). If only the return type varies, you can use named returns to do stuff with the return type. See Q24 also.

**Q19**: *Does Go have parametric polymorphism?*

*1.6 (2016)*: No.

*1.18 (2022)*: Yes.

**Q21**: *Can I extend someone else's package after the fact? (ex. add new methods to json, perhaps to make it support some interface)*

No. (But you can do type and interface embedding.)

**Q22**: *What happens if I call `defer` inside a defer function or during a panic?*

It works normally, either way.

If you create an infinite loop of deferred functions (with or without infinite panics) it does a stack overflow, and it's not obvious it was mid-panic immediately.

**Q23**: *(p208) Why does `.(` type assertion return one OR two things depending? Did not seem to cover in multiple return assignments.*

See Q18.

**Q24**: *Can type switching do slices, maps, arrays, etc? (p212)*

*1.6 (2016)*: No. You need to use reflection.

*1.18 (2022)*: Unsure. Generics were introduced, and I don't know how they interface with type switching. I *think* type switches only take (fully-specified) concrete types in the case statements?

**Q25**: Does Go have a preprocessor or macros?

No to both.

**Q26**: *TODO: Read proposal that caused unix pipes*

There wasn't a written one, I was misremembering [Douglas McIlroy's](https://en.wikipedia.org/wiki/Douglas_McIlroy) suggestions as being a formal memo. The v3 vs v4 pipeline description seems interesting to compare, however. See [v3, 1973](https://dspinellis.github.io/unix-v3man/v3man.pdf#page=121) notation (p121-123, 3 pages) vs [v4, 1973](https://dspinellis.github.io/unix-v4man/v4man.pdf#page=98) (p98, one paragraph).

**Q27**: *Is 'make' a keyword? What args does it take for each type? (Can I change what it takes for my types)*

Both `make` and `new` are built-in functions, not keywords. `make` takes a type, and optionally size parameters, and returns that type. `new` takes a type and returns a pointer to a new variable of that type.

- `make(CHANNEL\_TYPE, size)` - size defaults to 0
- `make(SLICE\_TYPE, size, capacity)` - capacity defaults to size. (no default for size?)
- `make(MAP, starting size)` - starting size defaults to something reasonable
- `new(TYPE)` - only one form

**Q28**: *Can you write 'map' in Go? (or something to join two channels)*

*1.6 (2016)*: Only awkwardly, using reflection (see Q19). Map could have the signature: `map(in_list interface{}, f interface{}, out_list interface{})`

*1.18 (2022)*: Yes, both. Generics got added.

**Q29**: *Are CSP in Go + Erlang basically the same model?*

Not sure, didn't look this one up. But basically no, even if the deeper model is the same.

- Erlang has out-of-order reading, indefinitely growing channel size, one unidirection 'channel' per process, and the notion of 'links' between processes to cause cascading failure.
- Go has channel closing, and the notion of a specific channel size (which defaults to 0), so it's more synchronous by default.

**Q30**: *Why is there a `&` in `memo := &Memo{request: make(chan request)}` on p278, when I thought you couldn't address constants (p159)?*

It's a special case for `&` and `new` only. From [Stack Overflow](https://stackoverflow.com/questions/40793289/go-struct-literals-why-is-this-one-addressable):

> Calling the built-in function new or taking the address of a composite literal allocates storage for a variable at run time. Such an anonymous variable is referred to via a (possibly implicit) pointer indirection.

**Suggested exerciae 31**: *(p280) Test # of goroutines and stack sizes before crash*

Knock yourself out.

**Suggested exercise 32**: *Test # of bits in an int/uint*

```^uint(0) >> 63 == 1```

**Q33**: *How do you detect int overlow (signed or unsigned) in Go?*

You can't. There is a [library for it](https://github.com/JohnCGriffin/overflow)

---

While reading the book, I noticed three big problems in Go that popped out to me.

- The gotchas around for-loop scoping (fixed in 2024)
- The lack of generics looked really painful (fixed in 2022). Functional programming looked pretty impossible (annoying, since Go lets you pass around functions and even closures), and it looked hard to glue together channels at a high level. The book's example of memoization code was pretty bad. This mostly seems all fixed (although I'm not sure how to test "A is a B" for non-concrete B at runtime).
- The number of built-in panics looked bad. In particular, I though the default value for `map` being `nil`, which panics when you try to insert something, was a dumb default. Now that I learned more, I think it's a dumb default and the default slice is dumb too.

Adding generics to the language made me much more likely to give it a whirl.

References:

\[1]: <https://go.dev/play/> "The Go Playground"

\[2]: <https://go.dev/doc/#references> "The Go Documentation"

\[3]: The Go Programming Language, by Alan A. A. Donovan and Brian W. Kernighan
