# Number Systems

## Binary

* 45 in Decimal: `4 * 10^1 + 5 * 10^0`
* 45 in Binary: `101101 = 1*2^5 + 1*2^3 + 1*2^2 + 1*2^0 = 32 + 8 + 4 + 1 = 45`
* 45 in Hex: `2D = 2*16^1 + D*16^0 = 32 + 13 = 45`

## Prefixes/suffixes

* `0x` means hex
* `b` or `B` is binary
* Many others depending on use-case

## Common Data Types:

### Boolean: `true/false`

* Binary numbers w/ all `0` are `false`
* Anything else is `true`
* `AND`: `true && true = true`, `false && true = false`
* `OR`: `true && true = true`, `false && true = true`, `false && false = false`
* `XOR`: `true && true = false`, `false && true = true`, `true && false = true`, `false && false = false`

### Numbers:

* Integers: `{-inf..inf}` only whole numbers (can be negative or positive unless `unsigned`)
  * Signed numbers use the first bit for the sign, where `1` is negative, and `0` is positive.
  * Unsigned numbers have no sign bit, so they are always positive
* Float: `{-inf..inf}` with all decimals in between. Stored like: `.5 -> 1 * 2^(-1)`

### Characters:

* ASCII: 7 bits, letters, digits, punctuation and some control characters
* Unicode: 32 bits, aims to represent every written language, 100k+ characters
