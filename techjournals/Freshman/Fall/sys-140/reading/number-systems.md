# Number Systems

## Number systems: (article #1)

This article provides a rather useful illustration that compares decimal (base 10) to binary (base 2), and shows how the two systems both work in fundamentally the same way, despite having a different number of symbols to use to describe numbers with.

A number in base 10 (decimal), for example, 156, is made up of one hundred, plus fifty, plus 6.\
`(1*10^2) + (5*10^1) + (6*10^0) = 100 + 5 + 6 = 156`

In base 2 (binary), 156 would be 10011100, and is made up of 4 + 8 + 16 +128\
`(0*2^0) + (0*2^1) + (1*2^2) + (1*2^3) + (1*2^4) + (0*2^5) + (0*2^6) + (1*2^7) = 4 + 8 + 16 + 128`

### Key terms:

Base 10 (also called decimal) is the typical number system that humans use. With a combination of 10 characters, \[0-9], we can describe any number.

Base 2 (also known as binary) is the numbering system that computers use internally, as logic gates can only have two states. As such, the binary number system only has two digits \[0-1], but can still express any number.

Base 8 (octal) represents any number using 8 digits \[0-7] (Question: where might I encounter octal?)

Base 16 (Hexadecimal) represents any number using 16 digits (0-9) & (A-F). Hexadecimal is used by humans interfacing with computers at levels close to the hardware, as it can be easily translated back into binary.

### Reaction:

While this text is a useful overview of different number systems that someone in the tech space might encounter, it would be useful if the author went into more depth about where you’re likely to encounter each. The author’s explanation of how both systems fundamentally work the same way finally helped it click for me, though.

## Hexadecimal Notation (article #2)

To convert a number from hexadecimal to binary, you divide the digits, and convert each individually to binary.

For example, with `5abf`,

```
   5         a         b         f
 0101       1010      1011      1111       →   0101101010111111
```

To convert back to hexadecimal from binary, you do basically the same process in reverse, and add 0’s to the front group if necessary.

With `101111001101` (oops came out evenly):

```
1011 1100 1101
  B   C    D
```

I can’t think of any new key terms from this article

### Reaction:

I can’t quite wrap my head around how individually converting hex digits into binary or vice versa can possibly come out in the right order, but I checked the examples in the article against a calculator, and they checked out. Part of me is hyped that it is that straightforward, but also I can’t figure out how it’s not more complicated than that.

## Signed and Unsigned Numbers (article #3)

Computers use words to store data, using a defined bit length. The naive assumption, then, is that a computer with a word length of 32 would be able to store (0-2^32) numbers. This is true if the number is “unsigned”, otherwise known as assumed to be positive. Signed numbers, on the other hand, use the first bit as the sign (“sign bit”) to show if the number is positive or negative. The sign bit is 1 if the number is negative.

### Key terms

In a computer context, a word is a binary number of length n, the word length. Even if the number being represented is less than n in length, it gets padded with 0’s so that the CPU can understand the value.

Unsigned numbers are numbers assumed to be positive.

The sign bit indicates if a number/word is negative or positive.

Signed numbers are negative if their first bit (“sign bit”) is 1.

### Reaction

Fundamentally, I understand the idea that using one bit for the sign is the cheapest approach to storing negative numbers. And, implementing them seems straightforward enough, too. The article talking about converting between formats has me confused, though. There were quite a few terms that the author used without fully explaining.

## Binary Numbers and Base Systems as Fast as Possible (source #4)

Using positional notation, you can describe any number with whatever set of characters you want.

We likely use base 10 as our primary system because we have 10 fingers.

In systems with bases higher than 10, it’s typical to use letters as the additional digits.

### Key Terms

Positional notation is the term to describe the idea of reusing symbols in different positions to represent a multiple of value.

### Reaction

I was interested to find out that there’s a term for any number system working in the way base 10, base 2, and base 16 all do. And, as I figured, I was not so surprised to learn that for whatever reason, humans have decided to use arbitrarily high base numbers to create ridiculously small character, but high value numbers.
