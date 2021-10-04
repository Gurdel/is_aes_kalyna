from aes import encrypt, decrypt

import time

def main():
    time_start = time.time()
    t_history = []
    with open('input.txt', 'rb') as inp, open('output.txt', 'wb') as out:
        data = inp.read()
        print(len(data))
        data = data.replace(b'\r', b'')
        count = 0
        temp = []
        ciphertext = []
        print('start')
        time_before = time.time()
        for el in data:
            temp.append(el)
            if len(temp) == 16:
                #print(temp)
                ciphertext.extend(encrypt(temp))
                temp = []
                count += 1
                if not count % 1000:
                    delta_t = time.time()-time_before
                    t_history.append(delta_t)
                    print(count//1000, delta_t, (time.time()-time_start)/(count//1000), sep='\t')
                    time_before = time.time()
        #  len(temp) < 16
        if len(temp) > 0:
            temp += [0x00 for _ in range(16)]
            ciphertext.extend(encrypt(temp[:16]))
        #print(cryptotext)
        text = bytes(ciphertext)
        out.write(text)

        #  debugging
        while len(ciphertext) and False:
            decr = decrypt(ciphertext[:16])
            ciphertext = ciphertext[16:]
            print(decr)

    print(time.time() - time_start)
    print('###################################################')

    with open('output.txt', 'rb') as inp, open('decrypted.txt', 'w') as out:
        data = inp.read()
        temp = []
        plaintext = []
        for el in data:
            temp.append(el)
            if len(temp) == 16:
                #print(temp)
                plaintext.extend(decrypt(temp))
                temp = []
        #  len(temp) < 16
        if len(temp) > 0:
            print('ERRRRRRRRROOOOOOOOR: len(input) % 16 != 0')
        text = bytes(plaintext).decode("utf-8").replace('\x00', '')
        #print(text)
        out.write(text)

    print(time.time() - time_start)

if __name__ == '__main__':
    main()
