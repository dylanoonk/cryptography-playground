# Cryptography Playground

Okay i'm making my way through the cryptopals challenges and I want some place to throw all my files in just in case I need to reference this later.

I also tried to break a challenge from UTD CSG so there's some stuff here about that too.

## Files

### character_frequency_analysis.py

This is for analyzing the frequency of characters in any given text. It comes with a handy `distance_from_english_text()` function which will analyze the frequency of characters and compare it to the frequency of characters in Pride and Prejudice (thank you Project Gutenberg). It returns a float and the closer to zero it is, the more likely it is that the string given is English text.

```python3
import character_frequency_analysis

EXAMPLE_STRING: str = "This is an example sentence. The quick brown fox jumps over the lazy dog! What the heck is even going on?"
DISTANCE_FROM_ENGLISH_TEXT: float = character_frequency_analysis.distance_from_english_text(EXAMPLE_STRING)

print(f"DISTANCE_FROM_ENGLISH_TEXT: {DISTANCE_FROM_ENGLISH_TEXT}")
```

```text
DISTANCE_FROM_ENGLISH_TEXT: 0.011079250374797388
```

### known_plaintext.py

This was one of my attempts at breaking a UTD CSG challenge with a known plaintext attack. It sorta worked but I didn't know enough of the plaintext to get any success with it.

```python3
import known_plaintext

KNOWN_PLAINTEXT = b'csg{'

CIPHERTEXT = open('data/blob', 'rb').read()

KEY = known_plaintext.get_key_by_known_plaintext(CIPHERTEXT, KNOWN_PLAINTEXT)

print(f"The calculated key is: {KEY.decode()}")
```

```text
The calculated key is: Wild
```


### break_single_character_xor.py

This uses character frequency analysis to attempt to break a given ciphertext assuming that its key is only a single byte or character.

```python3
import break_single_character_xor

CIPHERTEXT: str = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
MOST_LIKELY_KEYS: list[tuple] = break_single_character_xor.get_most_likely_keys(CIPHERTEXT, type_decode="b")
DECODED_TEXT_FROM_KEY: str = break_single_character_xor.decode_from_single_byte(bytearray.fromhex(CIPHERTEXT), MOST_LIKELY_KEYS[0][0]).decode("utf-8")

print(f"The most likely key is {MOST_LIKELY_KEYS[0][0]} with text \"{DECODED_TEXT_FROM_KEY}\"")
```

```text
The most likely key is 88 with text "Cooking MC's like a pound of bacon"
```

### break_repeating_key_xor.py

Breaks ciphertext into keysize blocks, transposes those blocks into a new array that's made of all the characters of the first character of the key, then the second, etc.

Then it attempts to break each character.

```python3
import break_repeating_key_xor

CHALLENGE_BYTES: bytes = open('data/blob', 'rb').read()
MOST_LIKELY_KEY = break_repeating_key_xor.break_repeating_key_xor(CHALLENGE_BYTES)

print(f"The most likely key is \"{''.join(MOST_LIKELY_KEY)}\")
```

```text
The most likely key is "Wirzats nverywhehd"
```

(This is wrong but it's very close)

### detect_single_character_xor.py

There's no function here that you can use. It was a one off file to solve https://cryptopals.com/sets/1/challenges/4

### challenge_6.py

There's no function here that you can use. It was a one off file to solve
https://cryptopals.com/sets/1/challenges/6