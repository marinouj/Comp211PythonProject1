#for k in range(bufferSize):
                #buffer[k] = int(page[k], 2)
            #buffer.append(int.from_bytes(page, byteorder='big', signed=True))


#page = bytearray(buffer)
#buffer = [x for x in page]


# for k in range(bufferSize):
# page.append(f'{buffer[k]:012b}')

#page.append(f'{buffer[j]:012b}')

# page = convertToBytes(buffer)
import array
import random
import struct


def test():
    list = [10, 11, 12, 13]
    b = bytearray(list)

    print("list: ", list)
    print("b", b)

    file = open("test.txt", "wb")
    file.write(b)
    file.close()
    file = open("test.txt", "rb")
    b = file.read()
    print(b)
    a = [x for x in b]
    print("a", a)


def convertToBytes(b):
    byte_buffer = []
    for k in range(buffer_size):
        byte_buffer[k] = int(b[k], 2)
    return byte_buffer


def test2():

    list = []
    number_of_integers = 1000
    for_wirte = "wb"
    for_read = "rb"
    max_value = 500
    list = [random.randint(0, 2**32-1) for i in range(number_of_integers)]
    bytes = array.array("L", list).tobytes()
    listB = array.array("L", bytes).tolist()
    #listB = [x(0) for x in struct.iter_unpack("L",bytes)]
    print(list == listB)
    #print(bytes)
    #print(listB)
    #chunkList = [x for x in chunks(bytes, 4)]
    #listB = [struct.unpack("L", x)[0] for x in chunkList]
    #print(chunkList)
    print(listB)


def chunks(i, n):
    for i in range(0, len(i), n):
        yield 1[i:i + n]


exit(test2())