import random
import array
buffer_size = 2
file_size = 8
sorted_file_size = 4
page_size = buffer_size*4
maximum_random_number = 10
sorted_file_number = int(file_size/sorted_file_size)

def main():
    disk_access = 0
    buffer = []
    file = open("filename.txt", "wb")
    for i in range(int(file_size / buffer_size)):
        buffer.clear()
        #buffer = deb[buffer_size * i: (buffer_size * i) + buffer_size]

        for j in range(buffer_size):                                        #filling buffer with random integers
            buffer.append(random.randint(0, maximum_random_number))                           #generating a random int grater than zero
        page_of_file = array.array("L", buffer).tobytes()                   #converting buffer to bytes
        print(buffer)
        file.write(page_of_file)
        disk_access = disk_access + 1
    file.close()
    print("Disk accesses required to create file: ", disk_access)
    sort()
    final_sort()
    serial_search()



"""The sort algorithm is used in order to sort the random generated file into many seperate once.
    We read using the buffer array enough elements from the random file to fill one of the sorted files.
    We sort that array using the quick sort algorithm amd thn we write it in one of the empty sorted files"""
def sort():
    sorting_disk_access_counter = 0                                     #Variable used to keep track of how many disk accesses we needed while executing the algorithm
    file = open("filename.txt", "rb")
    for i in range(int(file_size / sorted_file_size)):                  #For loop that repeats the proccess for as many sorted files as we need
        sorted_array, da = read_sorted_array_from_file(file)            #Loading enough pages to fill the sorted array
        quick_sort(sorted_array, 0, sorted_file_size - 1)               #sorting the array using quicksort algorithm
        sorting_disk_access_counter = sorting_disk_access_counter + da + write_sorted_array_in_file(sorted_array, i)  #Converting the sorted array to bytes and saving it in a new file    file.close()
    print("Disk accesses required to sort the file into many separate once: ", sorting_disk_access_counter)


"""Converting the sorted array to bytes and saving it in a new file"""
def write_sorted_array_in_file(sorted_array, i):
    disk_access = 0
    sorted_file = open("filename" + str(i) + ".txt", "wb")              #Creating new file to save each sorted array
    for j in range(int(sorted_file_size / buffer_size)):
        buffer = sorted_array[(buffer_size * j): ((buffer_size * j) + buffer_size)] #Getting a buffer size chunk off of the sorted array
        page = array.array("L", buffer).tobytes()                       #Converting buffer to byte sized page
        sorted_file.write(page)                                         #Writing page in current sorted file
        #print(buffer)
        disk_access = disk_access + 1                                   #Increasing the disk accesses
    sorted_file.close()                                                 #Closing current sorted file after we filled it
    return disk_access


"""Reading an array that has the length of a sorted file from the random file. To achieve this we read repetitively
    a page from the file, convert it to buffer (int[]) and add it to the sorted array."""
def read_sorted_array_from_file(file):
    disk_access = 0
    sorted_array = []
    for j in range(int(sorted_file_size / buffer_size)):
        page = file.read(page_size)                                     #Reading a page of bytes from the random file
        buffer = array.array("L", page).tolist()                        #Converting the page to int buffer array
        sorted_array.extend(buffer)                                     #Adding buffer to sorted array
        disk_access = disk_access +1                                    #Increasing the disk accesses
    return sorted_array, disk_access


def final_sort():
    file_pointer = [0 for i in range(sorted_file_number+1)]
    file_ended = [False for i in range(sorted_file_number)]
    empty_buffer = [False for i in range(sorted_file_number)]
    buffer_pointer = [0 for i in range(sorted_file_number + 1)]
    sorted_buffer = [[0 for y in range(buffer_size)]for x in range(sorted_file_number + 1)]
    column = [0 for x in range(sorted_file_number)]

    for i in range(sorted_file_number):
        sorted_buffer[i], file_pointer[i] = get_next_page(file_pointer[i], generate_file_name(i))
    while file_pointer[sorted_file_number] != file_size*4:
        for i in range(sorted_file_number):
            column[i] = sorted_buffer[i][buffer_pointer[i]]
        position = minimum(column, empty_buffer)
        sorted_buffer[sorted_file_number][buffer_pointer[sorted_file_number]] = sorted_buffer[position][buffer_pointer[position]]
        buffer_pointer[position] = buffer_pointer[position] + 1
        buffer_pointer[sorted_file_number] = buffer_pointer[sorted_file_number] + 1

        if file_ended[position] and (buffer_pointer[position] == buffer_size):
            empty_buffer[position] = True
            buffer_pointer[position] = buffer_size - 1

        if buffer_pointer[sorted_file_number] == buffer_size:
            #print(sorted_buffer[sorted_file_number])
            file_pointer[sorted_file_number] = write_next_page(file_pointer[sorted_file_number], sorted_buffer[sorted_file_number], "finalSortedFile.txt")
            buffer_pointer[sorted_file_number] = 0

        if buffer_pointer[position] == buffer_size:
            sorted_buffer[position], file_pointer[position] = get_next_page(file_pointer[position], generate_file_name(position))
            buffer_pointer[position] = 0
            file_ended[position] = (file_pointer[position] == sorted_file_size*4)


def serial_search():
    disk_access = [0 for i in range(40)]
    for k in range(40):
        key = random.randint(0, maximum_random_number)
        disk_access[k] = search_in_file_serial("finalSortedFile.txt", key)
    print(average(disk_access))


def search_in_file_serial(final_file, key):
    disk_access = 0
    successful_search = False
    file_pointer = 0
    while file_pointer != file_size * 4 and not successful_search:
        disk_access = disk_access + 1
        buffer, file_pointer = get_next_page(file_pointer, final_file)
        successful_search = search_number(buffer, key)
    return disk_access


def search_number(buffer, key):
    for i in range(buffer_size):
        if buffer[i] == key:
            return True
    return False


def average(arr):
    s = 0
    for i in range(len(arr)):
        s = s + arr[i]
    return s/len(arr)


def minimum(column, has_finished):
    x = 0
    while x in range(sorted_file_number) and has_finished[x]:
        x = x + 1
    min = column[x]
    pos = x
    for k in range(sorted_file_number):
        if column[k] < min and has_finished[k] is False:
            min = column[k]
            pos = k
    return pos


def generate_file_name(i):
    return "filename" + str(i) + ".txt"


def write_next_page(fp, buffer, filename):
    file = open(filename, "wb")
    page = array.array("L", buffer).tobytes()
    file.seek(fp)
    file.write(page)
    file_pointer = file.tell()
    file.close()
    return file_pointer


def get_next_page(fp, filename):     #loading new page from sorted files when needed and turning it into int
    sorted_file = open(filename, "rb")
    sorted_file.seek(fp)
    page = sorted_file.read(page_size)
    fp = sorted_file.tell()
    buffer = array.array("L", page).tolist()
    sorted_file.close()
    return buffer, fp


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
