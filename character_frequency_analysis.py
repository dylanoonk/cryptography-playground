# This was a helper file I wrote because I didn't want to clutter up challenge_3.py

from collections import Counter
import json

CACHED_KNOWN_CHARACTER_FREQUENCY: dict = None


def get_normalized_character_count(raw_string: str) -> dict:
    CHARACTER_FREQUENCY: Counter = Counter(raw_string)
    STRING_LENGTH: int = len(raw_string)

    CHARACTER_FREQUENCY_DICT: dict = CHARACTER_FREQUENCY.items()
    for character in CHARACTER_FREQUENCY_DICT:
        CHARACTER_FREQUENCY[character[0]] = character[1] / STRING_LENGTH

    return dict(CHARACTER_FREQUENCY.copy().items())
        
def get_average_distance_of_input_text_frequency_and_known_frequency(normalized_input_character_count: dict, KNOWN_CHARACTER_FREQUENCY: dict) -> float:
    AVERAGE_DISTANCE: float = 0.0
    TOTAL_CHARACTERS: int = 0

    for characters in normalized_input_character_count.items():
        KNOWN_CHARACTER_FREQUENCY_LOOKUP: float | None = KNOWN_CHARACTER_FREQUENCY.get(characters[0])

        if KNOWN_CHARACTER_FREQUENCY_LOOKUP is None:
            continue
        
        DISTANCE_FROM_KNOWN_CHARACTER_FREQUENCY: float = abs(KNOWN_CHARACTER_FREQUENCY_LOOKUP -  characters[1])
        AVERAGE_DISTANCE += DISTANCE_FROM_KNOWN_CHARACTER_FREQUENCY
        TOTAL_CHARACTERS += 1
        
    if TOTAL_CHARACTERS == 0 or AVERAGE_DISTANCE == 0:
        return 1
    AVERAGE_DISTANCE = AVERAGE_DISTANCE / TOTAL_CHARACTERS
    return AVERAGE_DISTANCE


def distance_from_english_text(input_string: str) -> float:
    if CACHED_KNOWN_CHARACTER_FREQUENCY == None:
        KNOWN_CHARACTER_FREQUENCY: dict = json.loads(open("data/KNOWN_CHARACTER_FREQUENCY_PAP.json", "r").read()) #pride and prejudice
    else:
        KNOWN_CHARACTER_FREQUENCY: dict = CACHED_KNOWN_CHARACTER_FREQUENCY
    NORMALIZED_CHARACTER_COUNT: dict = get_normalized_character_count(input_string)
    AVERAGE_DISTANCE_FROM_KNOWN_FREQUENCY: float = get_average_distance_of_input_text_frequency_and_known_frequency(NORMALIZED_CHARACTER_COUNT, KNOWN_CHARACTER_FREQUENCY)

    return AVERAGE_DISTANCE_FROM_KNOWN_FREQUENCY


def main():
    EXAMPLE_STRING: str = "This is an example sentence. The quick brown fox jumps over the lazy dog! What the heck is even going on?"
    DISTANCE_FROM_ENGLISH_TEXT: float = distance_from_english_text(EXAMPLE_STRING)
    
    print(f"The distance of the normalized character count of example string: \n\"{EXAMPLE_STRING}\"\nfrom Pride and Prejudice is {DISTANCE_FROM_ENGLISH_TEXT}")
    
    

if __name__ == "__main__":
    main()