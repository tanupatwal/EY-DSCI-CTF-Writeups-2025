# -----------------------------------------------------------------------------
# Challenge: Echoes of a Proton
# Event:     EY-DSCI CTF 2025 (Pullman Aerocity, Delhi)
# Note:      This is the exact script executed in the terminal.
#            (See evidence/05_solver.png)
# -----------------------------------------------------------------------------

import string

c = 'ntailgwtt{pmsgrr_glrvhba}'
k = 'lavender'
res = []
ki = 0

for char in c:
    if char.lower() in string.ascii_lowercase:
        shift = ord(k[ki % len(k)].lower()) - 97
        p = (ord(char.lower()) - 97 - shift) % 26
        res.append(chr(p + 65))
        ki += 1
    else:
        res.append(char)

print(''.join(res))