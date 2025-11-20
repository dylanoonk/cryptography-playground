import string
import character_frequency_analysis as CharacterFrequencyAnalysis

#https://cryptopals.com/sets/1/challenges/3

def remove_new_lines(input_string: str) -> str:
    OUTPUT = ""

    for char in input_string:
        if not char == "\n":
            OUTPUT += char

    return OUTPUT


def decode_from_single_character(ciphertext: bytearray, char: str) -> bytearray:

    OUTPUT: bytearray = bytearray()

    for byte in ciphertext:
        OUTPUT.append(int(byte) ^ ord(char))

    return OUTPUT


def decode_from_single_byte(ciphertext: bytearray, char: int) -> bytearray:

    OUTPUT: bytearray = bytearray()

    for byte in ciphertext:
        OUTPUT.append(int(byte) ^ int(char))

    return OUTPUT


def try_decode_from_all_characters(ciphertext: bytearray, return_top_choices_size: int = 3) -> list[tuple]:

    ALL_CHARACTERS: str = string.ascii_lowercase + string.ascii_uppercase + string.digits + " "
    LOWEST_CONFIDENCE: float = 1
    
    TOP_KEY_CHOICES: list = []

    for character in ALL_CHARACTERS:
        DECODED_TEXT: str = decode_from_single_character(ciphertext, character).decode("utf-8", errors="ignore")
        CONFIDENCE: float = CharacterFrequencyAnalysis.distance_from_english_text(DECODED_TEXT)
        
        if CONFIDENCE <= LOWEST_CONFIDENCE:
            LOWEST_CONFIDENCE = CONFIDENCE

            TOP_KEY_CHOICES.insert(0, (character, CONFIDENCE))
            if len(TOP_KEY_CHOICES) > return_top_choices_size:
                TOP_KEY_CHOICES.pop(return_top_choices_size)


    return TOP_KEY_CHOICES

def try_decode_from_all_bytes(ciphertext: bytearray, return_top_choices_size: int = 3) -> list[tuple]:

    ALL_CHARACTERS = range(0, 256)
    LOWEST_CONFIDENCE: float = 1
    
    TOP_KEY_CHOICES: list = []

    for character in range(256):
        try:
            DECODED_TEXT: str = decode_from_single_byte(ciphertext, character).decode("utf-8")
            CONFIDENCE: float = CharacterFrequencyAnalysis.distance_from_english_text(DECODED_TEXT)
        except:
            CONFIDENCE = 1
        
        if CONFIDENCE <= LOWEST_CONFIDENCE:
            LOWEST_CONFIDENCE = CONFIDENCE

            TOP_KEY_CHOICES.insert(0, (character, CONFIDENCE))
            if len(TOP_KEY_CHOICES) > return_top_choices_size:
                TOP_KEY_CHOICES.pop(return_top_choices_size)


    return TOP_KEY_CHOICES

def get_most_likely_keys(line: str | bytes, type_decode:str="s") -> list[tuple]:
    if type(line) == str:
        LINE_BYTES = bytearray.fromhex(line)
    
    if type(line) == bytes:
        LINE_BYTES = bytearray(line)

    if type_decode == "s":
        TOP_KEY_CHOICES = try_decode_from_all_characters(LINE_BYTES)
    elif type_decode == "b":
        TOP_KEY_CHOICES = try_decode_from_all_bytes(LINE_BYTES)

    return TOP_KEY_CHOICES

def main():
    CIPHERTEXT: str = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
    MOST_LIKELY_KEYS: list[tuple] = get_most_likely_keys(CIPHERTEXT, type_decode="b")
    DECODED_TEXT_FROM_KEY: str = decode_from_single_byte(bytearray.fromhex(CIPHERTEXT), MOST_LIKELY_KEYS[0][0]).decode("utf-8")


    
    print(f"The most likely key is {MOST_LIKELY_KEYS[0][0]} with text \"{DECODED_TEXT_FROM_KEY}\"")

if __name__ == "__main__":
    main()