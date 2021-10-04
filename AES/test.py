from aes import key, encrypt, decrypt

def print_matrix(m, title=''):
    output = ''
    if title != '':
        print(' -',title)

    row = len(m)//4
    for i in range(row):
        for j in range(4):
            idx = (j*4)+i
            output += "%02x " % (m[idx])
        
        output += '\r\n'

    print(output)

input = [0x32,0x43,0xf6,0xa8,0x88,0x5a,0x30,0x8d,0x31,0x31,0x98,0xa2,0xe0,0x37,0x07,0x34]


print_matrix(input, 'Input')
print_matrix(key, 'Cipher Key')

print('------- Encrypt')
encrypt_data = encrypt(input)
print_matrix(encrypt_data, '')

print('-------- Decrypt')
decrypt_data = decrypt(encrypt_data)
print_matrix(decrypt_data, '')
