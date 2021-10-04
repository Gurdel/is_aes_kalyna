from consts import Nk, Nb, Nr, Rcon, s

import copy

def KeyExpansion(key):
    word = {}
    for i in range(Nk):
        word[i] = [key[4*i], key[4*i+1], key[4*i+2], key[4*i+3]]

    for i in range(Nk, Nb*(Nr+1)):
        temp = copy.deepcopy(word[i-1])
        if i % Nk == 0:
            temp = SubWord(RotWord(temp))
            temp[0] ^= Rcon[i//Nk]
        elif Nk > 6 and i % Nk == 4:
            SubWord(temp)

        word[i] = {}
        for j in range(len(word[i-Nk])):
            word[i][j] = word[i-Nk][j] ^ temp[j]
    return word

def RotWord(temp):
    buf = copy.deepcopy(temp)
    for i in range(4):
        idx = i
        b_idx = idx - 1
        row_min_idx = 0
        if b_idx < row_min_idx:
            b_idx += 4
        
        temp[b_idx] = buf[idx]
    return temp

def SubWord(temp):
    row = len(temp) // 4
    for i in range(row):
        for j in range(4):
            idx = (i*4)+j
            temp[idx] = s[temp[idx]]
    return temp