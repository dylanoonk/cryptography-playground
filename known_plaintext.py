def get_key_by_known_plaintext(ciphertext: bytes, known_plaintext: bytes) -> bytes:
    return bytes([c ^ p for c, p in zip(ciphertext, known_plaintext)])


def main():
    KNOWN_PLAINTEXT = b'csg{'

    CIPHERTEXT = open('data/blob', 'rb').read()

    KEY = get_key_by_known_plaintext(CIPHERTEXT, KNOWN_PLAINTEXT)

    print(f"The calculated key is: {KEY.decode()}")

if __name__ == "__main__":
    main()