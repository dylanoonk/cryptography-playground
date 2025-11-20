import break_single_character_xor as SingleCharacterDecrypt
import character_frequency_analysis as CharacterFrequencyAnalysis

def main():
    CHALLENGE_LINES = open("data/4.txt", "r").readlines()
    POTENTIAL_ENGLISH = []

    for line in CHALLENGE_LINES:
        key = SingleCharacterDecrypt.get_most_likely_keys(line, type_decode="b")[0][0]

        try:
            DECODE_FROM_SINGLE_CHARACTER = SingleCharacterDecrypt.decode_from_single_byte(bytearray.fromhex(line), key).decode(errors="strict")
            POTENTIAL_ENGLISH.append(DECODE_FROM_SINGLE_CHARACTER)
            print(f"{DECODE_FROM_SINGLE_CHARACTER} | {key}")
        except:
            pass

    HIGHEST_CONFIDENCE = 0
    BEST_CHOICES = []
    count = 0

    
    for choice in POTENTIAL_ENGLISH:
        count += 1
        CONFIDENCE = int(1 / CharacterFrequencyAnalysis.distance_from_english_text(choice))

        if CONFIDENCE >= HIGHEST_CONFIDENCE:
            HIGHEST_CONFIDENCE = CONFIDENCE

            BEST_CHOICES.insert(0, (choice, CONFIDENCE))
            if len(BEST_CHOICES) > 3:
                BEST_CHOICES.pop(3)

    for choice in BEST_CHOICES:
        print(f"\"{choice[0].replace("\n", "")}\" has confidence {choice[1]}")

if __name__ == "__main__":
    main()