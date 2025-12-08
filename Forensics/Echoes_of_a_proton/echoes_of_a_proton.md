# Echoes of a Proton

**Event:** EY-DSCI CTF 2025 (Pullman Aerocity, Delhi)  
**Category:** Forensics  
**Points:** 200  
**Date:** Dec 3, 2025  

# 1. Initial Analysis and Scenario Setup 🕵️‍♀️

The challenge presented an image (challenge.jpg) with a quote about the dissolution of a proton, hinting at multiple layers, hidden files, and useful metadata.

You're given a single, innocent-looking image... Somewhere inside this file, there's a flag hidden across multiple layers. The clues are scattered... The metadata may be whispering something useful...

Figure 01_challenge.png : The initial challenge prompt.

# 2. Metadata Whispers: The Cipher Key

My first step was to examine the metadata of challenge.jpg using exiftool, as hinted by the prompt.

exiftool challenge.jpg
This revealed two crucial hints:

Subject: secret_key=#E6E6FA

User Comment: not ROT, not ATBASH... keyword rules

Figure 02_exiftool.png : Exiftool reveals the hex code and cipher type hint.

The hex code #E6E6FA is the color code for Lavender. The comment "keyword rules" strongly indicated a Vigenère Cipher using the key lavender.

# 3. Extraction: Files Within Files

The mention of "files hiding inside other files" pointed towards steganography or data appending. I used binwalk to analyze the file structure and extract any embedded archives.

binwalk -e challenge.jpg

binwalk successfully extracted a compressed archive containing three files:

note.txt
banner.png
core.bin

Figure 03_binwalk.jpg : Failed steghide attempts followed by the successful binwalk extraction.

# 4. Deep Forensics: Locating the Ciphertext
Inside the extracted directory, I first read note.txt:

cat note.txt
# Output: Three layers deep. The picture is just a picture. Look where strings ring true.

Following the hint to look where "strings ring true," I ran strings on the binary file, core.bin. This revealed a long Base64-encoded string:

strings core.bin
# ... (lots of garbage) ...
# bnRhaWxnd3R0e3Btc2dycl9nbHJ2aGjhfQ==
# ... (lots of garbage) ...

I immediately decoded the Base64 string:

echo "bnRhaWxnd3R0e3Btc2dycl9nbHJ2aGjhfQ==" | base64 -d
# Output: ntailgwtt{pmsgrr_glrvhba}

This was our ciphertext.

Figure 04_strings.jpg : Reading note.txt and locating the Base64 string inside core.bin.

# 5. Decryption: The Custom Python Solver

We now had all the components for decryption:

Ciphertext: ntailgwtt{pmsgrr_glrvhba}

Key: lavender

Algorithm: Vigenère Cipher (Decryption)

To ensure correct handling of the non-alphabetic characters ({, }, _), I used a local Python script named solve.py to implement the Vigenère decryption logic.

import string
c = 'ntailgwtt{pmsgrr_glrvhba}'
k = 'lavender'
res = []
ki = 0
for char in c:
    if char.lower() in string.ascii_lowercase:
        # Calculate shift based on key character
        shift = ord(k[ki % len(k)].lower()) - 97
        # Vigenere Decryption formula: (c - k) mod 26
        p = (ord(char.lower()) - 97 - shift) % 26
        # Append as Uppercase for clear reading (A=65)
        res.append(chr(p + 65)) 
        ki += 1
    else:
        # Preserve non-alphabetic characters
        res.append(char)
        
print(''.join(res))

Executing the script gave the decoded text:

python3 solve.py
# Output: CTFEYDSCI{PROTON_PARADOX}

Figure 05_solver.png : The execution of the Python script to decrypt the ciphertext.

# 6. Case-Sensitivity Insight ⚠️
The script successfully decrypted the ciphertext to CTFEYDSCI{PROTON_PARADOX}. However, upon submission, the flag was rejected.

Result: ❌ Incorrect.

I quickly realized that while the original Base64-decoded ciphertext was entirely lowercase (excluding format characters), my Python script was forcing the output to be uppercase (chr(p + 65)). In CTF challenges, flags are often case-sensitive and may require matching the case of the original ciphertext.

By converting the result to entirely lowercase, the correct flag was revealed:

ctfeydsci{proton_paradox}
Result: ✅ Correct.

# The Flag 🚩
ctfeydsci{proton_paradox}
