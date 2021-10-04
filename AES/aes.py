from consts import s, s_inv, Nb, Nr, key
from key_expansion import KeyExpansion
#from test import print_matrix

import copy

round_keys_list = KeyExpansion(key)


def encrypt(input):
    state = copy.deepcopy(input)
    AddRoundKey(state, 0)
    for round in range(1,Nr):
        SubBytes(state)
        ShiftRows(state)
        MixColumns(state)
        AddRoundKey(state, (round)*Nb)
        #  debuging
        #print_matrix(state, title=f'round {round}')
    SubBytes(state)
    ShiftRows(state)
    AddRoundKey(state, (round+1)*Nb)
    return state

def AddRoundKey(state, r):
    buf = copy.deepcopy(state)
    for i in range(4):
        for j in range(4):
            idx = (i*4)+j
            state[idx] = buf[idx] ^ round_keys_list[r][j]
        r += 1

def SubBytes(state):
    row = len(state)//4
    for i in range(row):
        for j in range(4):
            idx = (i*4)+j
            state[idx] = s[state[idx]]
    return state


def ShiftRows(state):
    buf = copy.deepcopy(state)
    row = len(state)//4
    for i in range(row):
        output = ''
        for j in range(4):
            idx = (j*4)+i
            b_idx = idx - i*4
            row_min_idx = i

            if b_idx < row_min_idx:
                b_idx = idx + (4-i)*4
            
            state[b_idx] = buf[idx]
        
def MixColumns(state):
    buf = copy.deepcopy(state)
    for i in range(4):
        n = i*4
        state[n] = mult(2, buf[n]) ^ mult(3, buf[n+1]) ^ mult(1, buf[n+2]) ^ mult(1, buf[n+3])
        state[n+1] = mult(1, buf[n]) ^ mult(2, buf[n+1]) ^ mult(3, buf[n+2]) ^ mult(1, buf[n+3])
        state[n+2] = mult(1, buf[n]) ^ mult(1, buf[n+1]) ^ mult(2, buf[n+2]) ^ mult(3, buf[n+3])
        state[n+3] = mult(3, buf[n]) ^ mult(1, buf[n+1]) ^ mult(1, buf[n+2]) ^ mult(2, buf[n+3])

#########################################################

def decrypt(state):
    buf = copy.deepcopy(state)
    AddRoundKey(buf, Nr*Nb)

    for round in reversed(range(1, Nr)):
        InvShiftRows(buf)
        InvSubBytes(buf)
        AddRoundKey(buf, (round)*Nb)
        InvMixColumns(buf)

    InvShiftRows(buf)
    InvSubBytes(buf)
    AddRoundKey(buf, 0)

    return buf

def InvSubBytes(state):
    row = len(state)//4
    for i in range(row):
        for j in range(4):
            idx = (i*4)+j
            state[idx] = s_inv[state[idx]]

def InvShiftRows(state):
    buf = copy.deepcopy(state)
    row = len(state)//4
    for i in range(row):
        for j in range(4):
            idx = (j*4)+i
            b_idx = idx + i*4
            row_max_idx = 4*(row-1)+i
            if b_idx > row_max_idx:
                b_idx = idx - (4-i)*4
            state[b_idx] = buf[idx]

def InvMixColumns(state):
    buf = copy.deepcopy(state)
    for i in range(4):
        n = i*4
        state[n] = mult(0x0e, buf[n]) ^ mult(0x0b, buf[n+1]) ^ mult(0x0d, buf[n+2]) ^ mult(0x09, buf[n+3])
        state[n+1] = mult(0x09, buf[n]) ^ mult(0x0e, buf[n+1]) ^ mult(0x0b, buf[n+2]) ^ mult(0x0d, buf[n+3])
        state[n+2] = mult(0x0d, buf[n]) ^ mult(0x09, buf[n+1]) ^ mult(0x0e, buf[n+2]) ^ mult(0x0b, buf[n+3])
        state[n+3] = mult(0x0b, buf[n]) ^ mult(0x0d, buf[n+1]) ^ mult(0x09, buf[n+2]) ^ mult(0x0e, buf[n+3])


def mult(a, b, fast=True):
    if a == 1:
        return b
    if fast:
        mult_dict = {
            0x02: mul_by_02,
            0x03: mul_by_03,
            0x09: mul_by_09,
            0x0b: mul_by_0b,
            0x0d: mul_by_0d,
            0x0e: mul_by_0e,
        }
        if a in mult_dict:
            result = mult_dict[a](b)
        else:
            print(f'long multiplication for a={a} b={b}')
            return mult(a, b, fast=False)
    else:
        result = 0
        a_bit = 1
        for i in range(4):
            if a_bit&a:
                temp = b
                for _ in range(i):
                    temp_r = 0
                    for k in range(8):
                        b_bit = temp>>k&1
                        if b_bit:
                            temp_r ^= (b_bit << k) * 0x02
                    h = temp_r>>8
                    if h:
                        temp_r &= 0xFF
                        temp_r ^= 0x1b
                    temp = temp_r
                result ^= temp
            a_bit<<=1
    return result

def mul_by_02(num):
    if num < 0x80:
        res = (num << 1)
    else:
        res = (num << 1) ^ 0x1b

    return res % 0x100


def mul_by_03(num): return mul_by_02(num) ^ num
def mul_by_09(num): return mul_by_02(mul_by_02(mul_by_02(num))) ^ num
def mul_by_0b(num): return mul_by_02(mul_by_02(mul_by_02(num))) ^ mul_by_02(num) ^ num
def mul_by_0d(num): return mul_by_02(mul_by_02(mul_by_02(num))) ^ mul_by_02(mul_by_02(num)) ^ num
def mul_by_0e(num): return mul_by_02(mul_by_02(mul_by_02(num))) ^ mul_by_02(mul_by_02(num)) ^ mul_by_02(num)
