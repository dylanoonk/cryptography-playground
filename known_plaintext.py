# known_plaintext.py
KNOWN_PLAINTEXT = b'csg{'

# Read the first 5 bytes of the encrypted file
with open('blob', 'rb') as f:
    ciphertext_header = f.read()

# Calculate the key by XORing the two
key = bytes([c ^ p for c, p in zip(ciphertext_header, KNOWN_PLAINTEXT)])

print(f"The calculated key is: {key.decode()}")