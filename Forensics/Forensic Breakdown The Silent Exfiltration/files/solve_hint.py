cipher_hex = "032c22e3b5827f3262e276022b2c23330b6531622072e23324b2bd063e612523e2386322e273312b313631e22324632706322e27123736b2d2c7de2137127e24d30272c313b2b6126221302334b2b2c256c260272212d26272632e27622330b2b242321366e"

print("[-] Brute forcing XOR (Looser Filter)...")

for key in range(256):
    try:
        # XOR decryption
        decrypted = bytes([b ^ key for b in bytes.fromhex(cipher_hex)])

        # Count how many characters are readable letters/numbers
        readable_count = sum(1 for b in decrypted if 32 <= b <= 126 or b == 10)

        # If 90% of the characters are readable, print it!
        if readable_count > len(decrypted) * 0.9:
            print(f"[+] Key {hex(key)}: {decrypted.decode('utf-8', errors='ignore')}")
    except:
        pass
