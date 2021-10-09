from kalyna import Kalyna, KALYNA_TYPE
import time
import numpy as np


def string2bytes(string, dtype=np.uint64):
    return np.frombuffer(bytearray.fromhex(string), dtype=dtype)


def bytes2string(bytes_array):
    return "".join(["{0:0{1}x}".format(num, 2) for num in bytearray(bytes_array)])


def main():
    print('main')
    key = string2bytes("000102030405060708090A0B0C0D0E0F")
    time_start = time.time()
    t_history = []
    with open('input.txt', 'rb') as inp, open('output.txt', 'wb') as out:
        data = inp.read()
        data = data.replace(b'\r', b'')
        print(len(data))
        count = 0
        temp = []
        ciphertext = []
        print('start')
        time_before = time.time()
        for el in data:
            temp.append(el)
            if len(temp) == 16:
                input_data = string2bytes("".join(["{0:0{1}x}".format(num, 2) for num in temp]))
                encrypted_input = Kalyna(key, KALYNA_TYPE.KALYNA_128_128).encrypt(input_data)
                ciphertext.extend(list(bytearray(encrypted_input)))
                temp = []
                count += 1
                if not count % 10:
                    delta_t = time.time()-time_before
                    t_history.append(delta_t)
                    print(count//10, delta_t, (time.time()-time_start)/(count//10), sep='\t')
                    time_before = time.time()
        #  len(temp) < 16
        if len(temp) > 0:
            temp += [0x00 for _ in range(16)]
            input_data = string2bytes("".join(["{0:0{1}x}".format(num, 2) for num in temp[:16]]))
            encrypted_input = Kalyna(key, KALYNA_TYPE.KALYNA_128_128).encrypt(input_data)
            ciphertext.extend(list(bytearray(encrypted_input)))
        text = bytes(ciphertext)
        out.write(text)

    print(time.time() - time_start)
    print('###################################################')

    with open('output.txt', 'rb') as inp, open('decrypted.txt', 'w') as out:
        data = inp.read()
        temp = []
        plaintext = []
        for el in data:
            temp.append(el)
            if len(temp) == 16:
                input_data = string2bytes("".join(["{0:0{1}x}".format(num, 2) for num in temp]))
                decrypted_input = Kalyna(key, KALYNA_TYPE.KALYNA_128_128).decrypt(input_data)
                plaintext.extend(list(bytearray(decrypted_input)))
                temp = []
        #  len(temp) < 16
        if len(temp) > 0:
            print('ERRRRRRRRROOOOOOOOR: len(input) % 16 != 0')
        text = bytes(plaintext).decode("utf-8").replace('\x00', '')
        out.write(text)

    print(time.time() - time_start)


def test(rounds=10):
    print('test')
    time_before = time.time()

    for _ in range(rounds):
        input_data = string2bytes("101112131415161718191A1B1C1D1E1F")
        key = string2bytes("000102030405060708090A0B0C0D0E0F")

        encrypted_input = Kalyna(key, KALYNA_TYPE.KALYNA_128_128).encrypt(input_data)
        decrypted_input = Kalyna(key, KALYNA_TYPE.KALYNA_128_128).decrypt(encrypted_input)

        #print(f'input_data: {bytes2string(input_data)}')
        #print(f'encrypted_input: {bytes2string(encrypted_input)}')
        #print(f'decrypted_input: {bytes2string(decrypted_input)}')

        time_after = time.time()
    print('***********************************************\n'
            'test duration:', time_after - time_before, 'seconds')


if __name__ == '__main__':
    main()
    test()
