import break_single_character_xor as SingleCharacterDecrypt
import character_frequency_analysis as CharacterFrequencyAnalysis
import itertools
from tqdm import tqdm



#https://cryptopals.com/sets/1/challenges/6

### AI GENERATED CODE
# Model (Gemini 2.5 Flash)
def hamming_distance_bits(s1: bytes, s2: bytes) -> int: #step 2
    """
    Calculates the bit-wise Hamming distance between two byte arrays of equal length.

    Args:
        s1: The first byte array.
        s2: The second byte array.

    Returns:
        The bit-wise Hamming distance between the two byte arrays.

    Raises:
        ValueError: If the two byte arrays have different lengths.
    """
    if len(s1) != len(s2):
        raise ValueError("Byte arrays must be of the same length for bit-wise Hamming distance.")
    
    distance = 0
    for byte1, byte2 in zip(s1, s2):
        # XOR the bytes and count the set bits (1s) in the result
        xor_result = byte1 ^ byte2
        distance += bin(xor_result).count('1')
    return distance

# Model (Polaris Alpha)
def transpose_blocks(blocks: list[bytes], KEYSIZE: int) -> list[bytes]:
    if not blocks:
        return []

    transposed = []

    for i in range(KEYSIZE):
        column_bytes = []
        for block in blocks:
            if i < len(block):  # handle last short block
                column_bytes.append(block[i])
        transposed.append(bytes(column_bytes))

    return transposed


# Model (Kimi K2 Turbo)
def generate_letter_combinations(probability_data):
    """
    Generate all possible combinations of letters from the probability data structure.
    
    Args:
        probability_data: A list of lists, where each inner list contains tuples of (letter, probability)
        
    Yields:
        str: Each possible combination of letters (generator function)
    """
    # Extract just the letters from each position, ignoring probabilities
    letter_options = []
    for position_data in probability_data:
        # Each position_data looks like: [('W', 0.022), ('I', 0.028), ('F', 0.032)]
        letters = [letter for letter, prob in position_data]
        letter_options.append(letters)
    
    # Generate the Cartesian product of all letter options
    # This creates every possible combination by picking one letter from each position
    for combination in tqdm(itertools.product(*letter_options), unit=" combos"):
        yield combination

    

# Model (Kimi K2 Turbo)
def generate_letter_combinations_list(probability_data) -> list:
    """
    Generate all possible combinations as a list (use with caution - may be huge!)
    
    Args:
        probability_data: A list of lists with (letter, probability) tuples
        
    Returns:
        list: All possible letter combinations
    """

    LETTER_COMBINATIONS = list(generate_letter_combinations(probability_data))
    
    return list(set(LETTER_COMBINATIONS))
### END OF AI GENERATED CODE

def break_into_keysize_blocks(ciphertext: bytes, keysize: int) -> list[bytes]:
    blocks = []
    for i in range(0, len(ciphertext), keysize):
        block = ciphertext[i : i + keysize]
        blocks.append(block)
    return blocks

def find_smallest_keysize(ciphertext: bytes, return_size=1) -> list | int:

    SMALLEST_NORMALIZED_EDIT_DISTANCE: float = 10
    TOP_KEYSIZE_CHOICES: list = []

    for KEYSIZE in range(2, 41):
        

        block1 = ciphertext[0:KEYSIZE]
        block2 = ciphertext[KEYSIZE:KEYSIZE*2]

        try:
            edit_distance = hamming_distance_bits(block1, block2)
        except:
            continue
        normalized_edit_distance = edit_distance / KEYSIZE

        if normalized_edit_distance < SMALLEST_NORMALIZED_EDIT_DISTANCE:


            # print(f"Found new smalled Normalized Edit Distance: {normalized_edit_distance} at KEYSIZE {KEYSIZE}")
            SMALLEST_NORMALIZED_EDIT_DISTANCE = normalized_edit_distance

            TOP_KEYSIZE_CHOICES.insert(0, KEYSIZE)
            if len(TOP_KEYSIZE_CHOICES) > return_size:
                TOP_KEYSIZE_CHOICES.pop(return_size)
    if return_size == 1:
        return TOP_KEYSIZE_CHOICES[0]
    
    return TOP_KEYSIZE_CHOICES

def repeating_key_xor(ciphertext: bytes, key: str | bytes | list[int]) -> bytes:

    KEY_ADJUSTED_SIZE = key * int(len(ciphertext) / len(key))
    DIFFERENCE_IN_CIPHERTEXT_AND_KEY_SIZE = len(ciphertext) - len(KEY_ADJUSTED_SIZE)
    if not DIFFERENCE_IN_CIPHERTEXT_AND_KEY_SIZE == 0:
        KEY_ADJUSTED_SIZE += key[:-DIFFERENCE_IN_CIPHERTEXT_AND_KEY_SIZE]
    
    
    if type(key) == str or type(key) == bytes:
        return bytes([c ^ ord(p) for c, p in zip(ciphertext, KEY_ADJUSTED_SIZE)])


    return bytes([c ^ ord(p) for c, p in zip(ciphertext, KEY_ADJUSTED_SIZE)])

def calculate_amount_possible_combinations(key_list: list) -> int:
    TOTAL_POSSIBLE = 1
    for key in key_list:
        TOTAL_POSSIBLE *= len(key)

    return TOTAL_POSSIBLE

def test_all_combinations(ciphertext: bytes, all_possible_combinations: list, return_size=3) -> list:
    LOWEST_CONFIDENCE = 1
    NUMBER_OF_POSSIBLE_COMBINATIONS_OF_KEYS = len(all_possible_combinations)
    COMBINATIONS_TRIED_SO_FAR = 0

    TOP_CANDIDATES = []

    # file = open("test", "w")

    for combination in tqdm(all_possible_combinations, unit=" combos"):
        COMBINATIONS_TRIED_SO_FAR += 1

        DECRYPTED_CIPHERTEXT = repeating_key_xor(ciphertext, combination)
        CONFIDENCE = CharacterFrequencyAnalysis.distance_from_english_text(DECRYPTED_CIPHERTEXT.decode("utf-8"))
        
        # file.write(DECRYPTED_CIPHERTEXT.decode("utf-8") + "\n--------------------------------------------------------------------\n")

        if CONFIDENCE < LOWEST_CONFIDENCE:
            LOWEST_CONFIDENCE = CONFIDENCE
            TOP_CANDIDATES.insert(0, (combination, CONFIDENCE))
            if len(TOP_CANDIDATES) > return_size:
                TOP_CANDIDATES.pop(return_size)
    # file.close()
    return TOP_CANDIDATES

def brute_force_if_reasonable(ciphertext: bytes, POSSIBLE_KEYS_FOR_EACH_POSITION: list) -> list:
    def logic(USER_YN):
        if USER_YN:
            print("Generating all possible key combinations... (this could take a while)")
        else:
            print("Generating all possible key combinations...")

        ALL_POSSIBLE_KEYS = generate_letter_combinations_list(POSSIBLE_KEYS_FOR_EACH_POSITION)

        if USER_YN:
            print("Testing all combinations... (this could take even longer)")

        TOP_COMBINATIONS = test_all_combinations(ciphertext, ALL_POSSIBLE_KEYS)

        if USER_YN:
            print("Done!")
            
        for combination in TOP_COMBINATIONS:
            DECRYPTED_COMBINATION = repeating_key_xor(ciphertext, combination[0])
            print(f"\"{combination[0]}\": {DECRYPTED_COMBINATION.decode(errors="ignore")}\n")

        return TOP_COMBINATIONS

    NUMBER_OF_POSSIBLE_COMBINATIONS_OF_KEYS = calculate_amount_possible_combinations(POSSIBLE_KEYS_FOR_EACH_POSITION)
    if NUMBER_OF_POSSIBLE_COMBINATIONS_OF_KEYS > 10000:
        
        USER_YN = input(f"Are you sure you want to try every key possibility against the ciphertext? There are {NUMBER_OF_POSSIBLE_COMBINATIONS_OF_KEYS} combinations (y/n) ").strip().lower()

        if USER_YN == "n":
            return
        elif USER_YN == "y":
            return logic(True)
        else:
            print("Not a valid input")
            OUT = brute_force_if_reasonable(ciphertext, POSSIBLE_KEYS_FOR_EACH_POSITION)
            return OUT
    else:
        return logic(False)


def break_repeating_key_xor(ciphertext: bytes, type_decode="s", brute_force=False) -> list:
    KEYSIZE = find_smallest_keysize(ciphertext) #steps 1, 3, and 4
    #for KEYSIZE in KEYSIZES:

    # print(f"Using KEYSIZE {KEYSIZE}")

    CIPHERTEXT_BROKEN_INTO_KEYSIZE_BYTES = break_into_keysize_blocks(ciphertext, KEYSIZE) #step 5

    TRANSPOSED_BLOCKS = transpose_blocks(CIPHERTEXT_BROKEN_INTO_KEYSIZE_BYTES, KEYSIZE)

    POSSIBLE_KEYS_FOR_EACH_POSITION = []
    MOST_LIKELY_KEY: list[int] = []
    for block in TRANSPOSED_BLOCKS:
        TOP_KEY_CHOICES_FOR_BLOCK: list[tuple] = SingleCharacterDecrypt.get_most_likely_keys(block, type_decode=type_decode)
        POSSIBLE_KEYS_FOR_EACH_POSITION.append(TOP_KEY_CHOICES_FOR_BLOCK)
        MOST_LIKELY_KEY.append(TOP_KEY_CHOICES_FOR_BLOCK[0][0])
    
    # print(f"The most likely key is \"{MOST_LIKELY_KEY}\"\n")
    # print(f"Decrypted ciphertext is: \n{repeating_key_xor(ciphertext, MOST_LIKELY_KEY)}")

    if brute_force:
        return brute_force_if_reasonable(ciphertext, POSSIBLE_KEYS_FOR_EACH_POSITION)

    return MOST_LIKELY_KEY


def main():
    
    CHALLENGE_BYTES: bytes = open('data/blob', 'rb').read() # "Wildats everywhere" is the key

    print(break_repeating_key_xor(CHALLENGE_BYTES, brute_force=False))

    
if __name__ == "__main__":
    main()

