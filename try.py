import os
import random
import array
buffer_size = 1000
file_size = 100000
sorted_file_size = 10000
page_size = buffer_size*4
maximum_random_number = 100000
sorted_file_number = int(file_size/sorted_file_size)
final_sorted_name = "finalSortedFile.txt"

def main():
    create_file()
    sort()
    final_sort()
    #print_file(final_sorted_name)
    serial_search()
    binary_search()


def create_file():
    disk_access = 0
    buffer = []
    file = open("filename.txt", "wb")
    for i in range(int(file_size / buffer_size)):
        buffer.clear()
        # buffer = deb[buffer_size * i: (buffer_size * i) + buffer_size]
        for j in range(buffer_size):  # filling buffer with random integers
            buffer.append(random.randint(0, maximum_random_number))  # generating a random int grater than zero
        page_of_file = array.array("L", buffer).tobytes()  # converting buffer to bytes
        # print(buffer)
        file.write(page_of_file)
        disk_access = disk_access + 1
    file.close()
    print("Disk accesses required to create file: ", disk_access)


"""The sort algorithm is used in order to sort the random generated file into many seperate once.
    We read using the buffer array enough elements from the random file to fill one of the sorted files.
    We sort that array using the quick sort algorithm amd thn we write it in one of the empty sorted files"""
def sort():
    sorting_disk_access_counter = 0                                     #how many disk accesses we needed while executing the algorithm
    file_pointer = 0
    #file = open("filename.txt", "rb")
    for i in range(int(file_size / sorted_file_size)):                  #For loop that repeats the proccess for as many sorted files as we need
        sorted_array, file_pointer, da = read_from_file(file_pointer, "filename.txt", sorted_file_size)            #Loading enough pages to fill the sorted array
        quick_sort(sorted_array, 0, sorted_file_size - 1)               #Sorting the array using quicksort algorithm
        disk_access = write_in_file(0, sorted_array, generate_file_name(i))[1]
        sorting_disk_access_counter = sorting_disk_access_counter + da + disk_access#Converting the sorted array to bytes and saving it in a new file
    #file.close()
    print("Disk accesses required to sort the file into many separate once: ", sorting_disk_access_counter)


"""This function merges the individual sorted files to one final sorted file. It loads a page from every 
    single one of the sorted files. It reads the buffer numbers serially it finds the smaller it saves it
    to an other buffer and it moves the buffer pointer to the next number. When a buffer is empty it gets
    the next page from the corresponding file. If the buffer where we are saving numbers is full we write
    the to the final file and empty the buffer."""
def final_sort():
    file_pointer = [0 for i in range(sorted_file_number+1)]
    file_ended = [False for i in range(sorted_file_number)]
    empty_buffer = [False for i in range(sorted_file_number)]
    buffer_pointer = [0 for i in range(sorted_file_number + 1)]
    sorted_buffer = [[0 for y in range(buffer_size)]for x in range(sorted_file_number + 1)]
    column = [0 for x in range(sorted_file_number)]
    open(final_sorted_name, 'w').close()
    for i in range(sorted_file_number):
        sorted_buffer[i], file_pointer[i] = read_from_file(file_pointer[i], generate_file_name(i), buffer_size)[0:2]
    while file_pointer[sorted_file_number] != file_size*4:
        for i in range(sorted_file_number):
            column[i] = sorted_buffer[i][buffer_pointer[i]]
        position = minimum(column, empty_buffer)
        sorted_buffer[sorted_file_number][buffer_pointer[sorted_file_number]] = \
            sorted_buffer[position][buffer_pointer[position]]
        buffer_pointer[position] += 1
        buffer_pointer[sorted_file_number] += 1

        if file_ended[position] and (buffer_pointer[position] == buffer_size):
            empty_buffer[position] = True
            buffer_pointer[position] = buffer_size - 1
            delete_file(position)

        if buffer_pointer[sorted_file_number] == buffer_size:
            file_pointer[sorted_file_number] = write_in_file(file_pointer[sorted_file_number], sorted_buffer[sorted_file_number], final_sorted_name)[0]
            buffer_pointer[sorted_file_number] = 0

        if buffer_pointer[position] == buffer_size:
            sorted_buffer[position], file_pointer[position] = \
                read_from_file(file_pointer[position], generate_file_name(position), buffer_size)[0:2]
            buffer_pointer[position] = 0
            file_ended[position] = (file_pointer[position] == sorted_file_size*4)


def print_file(filename):
    fp = 0
    while fp < file_size*4:
        buffer, fp = read_from_file(fp, filename, buffer_size)[0:2]
        print(buffer)


"""Algorithm used to search serially 40 random numbers in the sorted file"""
def serial_search():
    disk_access = [0 for i in range(40)]
    for k in range(40):
        key = random.randint(0, maximum_random_number)
        disk_access[k] = search_in_file_serial(key)
    print("Average disk accesses required for the serial search", average(disk_access))


"""Algorithm used to search serially each random number in the sorted file"""
def search_in_file_serial(key):
    disk_access = 0
    successful_search = False
    file_pointer = 0
    while file_pointer != file_size * 4 and not successful_search:
        disk_access += 1
        buffer, file_pointer = read_from_file(file_pointer, final_sorted_name, buffer_size)[0:2]
        successful_search = search_number(buffer, key)
    return disk_access


"""Algorithm used to search each random numbers in the buffer"""
def search_number(buffer, key):
    for i in range(buffer_size):
        if buffer[i] == key:
            return True
    return False


"""Algorithm used to search binary 40 random numbers in the sorted file"""
def binary_search():
    disk_access = [0 for i in range(10)]
    num_of_pages = file_size/buffer_size
    file_pointer = num_of_pages*buffer_size*4/2
    for k in range(10):
        key = random.randint(0, maximum_random_number)
        disk_access[k] = search_in_file_binary(file_pointer, num_of_pages/2, key)
        #print(disk_access[k])
    print("Average disk accesses needed for the binary search: ", average(disk_access))


"""This recursive function reads the page of the file that corresponds to
    the file pointer, searches for the key in the page."""
def search_in_file_binary(fp, l, key):
    length = l
    file_pointer = int(fp)
    disk_access = 0
    buffer, f_pointer = read_from_file(file_pointer, final_sorted_name, buffer_size)[0:2]
    disk_access += 1
    move = search_in_buffer(buffer, key)
    if move == "Found":
        #print(key, move)
        return disk_access
    elif move == "Not Found":
        #print(key, move)
        return disk_access
    elif move == "Left":
        if file_pointer == buffer_size*4:
            return disk_access + search_in_file_binary(0, length/2, key)
        file_pointer -= length*buffer_size*2
        length = length/2
    else:
        file_pointer += length*buffer_size*2
        length = length / 2
    if 0 <= file_pointer <= file_size*4 - 1 and length >= 1:
        disk_access += search_in_file_binary(file_pointer, length, key)
    return disk_access


"""This function returns found or not found if the key is a number between buffer[0] and
    buffer[buffer_size - 1]. Else it removes whether it is placed in previous or next pages
    of the file"""
def search_in_buffer(buffer, key):
    if buffer[0] <= key <= buffer[buffer_size-1]:
        if search_number(buffer, key):
            return "Found"
        else:
            return "Not found"
    elif buffer[0]>key:
        return "Left"
    else:
        return "Right"


"""Finds and returns the average of an array"""
def average(arr):
    s = 0
    for i in range(len(arr)):
        s = s + arr[i]
    return s/len(arr)


"""This function finds the position of minimum value of an array.
    It also excludes from the column array the nodes whose corresponding has finished node is true"""
def minimum(column, has_finished):
    x = 0
    while x in range(sorted_file_number) and has_finished[x]: #choosing the starting point of our search for the min skipping the has finished nodes
        x = x + 1
    min = column[x]
    pos = x
    for k in range(sorted_file_number):
        if column[k] < min and has_finished[k] is False:
            min = column[k]
            pos = k
    return pos


"""This function is generating names for the sorted files"""
def generate_file_name(i):
    return "filename" + str(i) + ".txt"


def delete_file(i):
    if os.path.exists(generate_file_name(i)):
        os.remove(generate_file_name(i))
    else:
        print("The file does not exist")


"""Converting the sorted array to bytes and saving it in a new file"""
def write_in_file(fp, input_array, filename):
    disk_access = 0
    file_pointer = fp
    file = open(filename, "ab")                              #Creating new file to save each sorted array
    for j in range(int(len(input_array) / buffer_size)):
        buffer = input_array[(buffer_size * j): ((buffer_size * j) + buffer_size)] #Getting a buffer size chunk off of the sorted array
        page = array.array("L", buffer).tobytes()                #Converting buffer to byte sized page
        file.seek(file_pointer)
        file.write(page)                                         #Writing page in current sorted file
        file_pointer = file.tell()
        disk_access += 1                            #Increasing the disk accesses
    file.close()                                                 #Closing current sorted file after we filled it
    return file_pointer, disk_access


"""We use this function to read a page of a file
    Reading an array that has the length of a sorted file from the random file. To achieve this we read 
    repetitively a page from the file, convert it to buffer (int[]) and add it to the sorted array."""
def read_from_file(fp, filename, array_size):
    file = open(filename, "rb")
    disk_access = 0
    file_pointer = fp
    output_array = []
    for j in range(int(array_size / buffer_size)):
        file.seek(file_pointer)
        page = file.read(page_size)                                     #Reading a page of bytes from the random file
        file_pointer = file.tell()
        buffer = array.array("L", page).tolist()  # Converting the page to int buffer array
        output_array.extend(buffer)  # Adding buffer to sorted array
        disk_access += 1                                                #Increasing the disk accesses
    file.close()
    return output_array, file_pointer, disk_access


def partition(arr, low, high):
    i = (low - 1)  # index of smaller element
    pivot = arr[high]  # pivot
    for j in range(low, high):
        # If current element is smaller than or
        # equal to pivot
        if arr[j] <= pivot:
            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return (i + 1)


# Function to do Quick sort
def quick_sort(arr, low, high):
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, low, high)

        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)


exit(main())
