import math
import hashlib
import sys


def int2bin(integer, length):  # integer to binary conversion | binary with length
    return bin(integer)[2:].zfill(length)


def bin2int(binary):  # binary to integer conversion
    return int(binary, 2)


def str2byte(string):  # string to bytes conversion
    return int(string, 2).to_bytes(len(string) // 8, byteorder='big')


fname = sys.argv[-1]
with open(fname, 'r') as f:
    nums = f.readlines()  # list nums = file lines
    nums = [int(i) for i in nums]  # list nums = ints
    nums.sort()  # sort in ascending order
    n = len(nums)  # total number of set elements
    m = nums[n-1]  # largest number of set
    bit_len = nums[n-1].bit_length()  # the bit length of the numbers to encode == the bit length of the largest number
    nums = [int2bin(i, bit_len) for i in nums]  # integers to binary format

    # calculating l ----------------------------------------------------------------------------------------------------
    l = round(math.log2(m/n))  # length of lower part == log2(m/n) "rounded"
    print("l", l)

    # calculating array L ----------------------------------------------------------------------------------------------
    L = [i[-l:] for i in nums]  # lower part list (left to -l position == last l bits)
    L = ''.join(L)  # concatenate the lower part numbers
    if len(L) % 8 != 0:  # if not multiple of 8
        L = L.ljust(len(L) + 8 - (len(L) % 8), "0")  # make it reach a multiple of 8 by 0s left filling
    print("L")
    for i in range(0, len(L), 8):  # print 8 bits per line
        print(L[i:i+8])  # slicing: print chars with index from i to i+7

    # calculating array U ----------------------------------------------------------------------------------------------
    oldU = [i[:-l] for i in nums]  # upper part list (right to -l-1 position == first n-l bits)
    oldU = [bin2int(i) for i in oldU]  # upper part numbers are converted back to integers
    U = [oldU[0]]  # keep the 1st element
    for i in range(1, len(oldU)):  # going through elements to perform the subtraction: (present - previous)
        U.append(oldU[i]-oldU[i-1])
    oldU = U  # to update U with the unary representation of numbers
    U = [int2bin(1, i+1) for i in oldU]  # right zero filling before the 1 stop bit | number of zeros == number in oldU
    U = ''.join(U)  # concatenate the upper part encoded numbers
    if len(U) % 8 != 0:  # if not multiple of 8
        U = U.ljust(len(U) + 8 - (len(U) % 8), "0")  # make it reach a multiple of 8 by 0s left filling
    print("U")
    for i in range(0, len(U), 8):  # print 8 bits per line
        print(U[i:i+8])  # slicing: print chars with index from i to i+7

    # SHA-256 hash code ------------------------------------------------------------------------------------------------
    m = hashlib.sha256()   # m instantiation
    m.update(str2byte(L))  # L & U converted to byte | the update method is fed only bytes-like objects
    m.update(str2byte(U))
    digest = m.hexdigest()  # returns the encoded data in hexadecimal format of the concatenation of the data fed
    print(digest)
