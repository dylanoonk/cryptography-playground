from base64 import b64decode
import break_repeating_key_xor as BreakRepeatingKeyXor
import character_frequency_analysis as CharacterFrequencyAnalysis


def main():
    CHALLENGE_BYTES = open("data/6.txt", "r").readlines()

    xor_keys_and_line = []
    for CHALLENGE in CHALLENGE_BYTES:
        
        ciphertext = b64decode(CHALLENGE)
        xor_keys_and_line.append((BreakRepeatingKeyXor.break_repeating_key_xor(ciphertext), ciphertext))

    for line in xor_keys_and_line:
        result = BreakRepeatingKeyXor.repeating_key_xor(line[1], line[0])
        try:
            confidence = round((1 - CharacterFrequencyAnalysis.distance_from_english_text(result.decode())) * 100, 2)
        except:
            pass

        print(f"{result}: {confidence}% and KEY: '{''.join(line[0])}'")


if __name__ == "__main__":
    main()