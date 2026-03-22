#This script implements the heapsort algorithm in Python.

#Heapify function to maintain the heap property

#array, size of the heap, index of the element to be heapified
def heapify(arr, n, i):
    #Start with i as the largest element (the element to be heapified)
    largest = i 
    l = 2 * i + 1 # left = 2*i + 1
    r = 2 * i + 2 # right = 2*i + 2

    
    # If left child is larger than root
    if l < n and arr[l] > arr[largest]:
        largest = l

    # If right child is larger than largest so far
    if r < n and arr[r] > arr[largest]:
        largest = r

    # If largest is not root
    if largest != i:
        tmp_val = arr[i]
        arr[i] = arr[largest]
        arr[largest] = tmp_val
        #largest keeps the swapped element's index, so we need to heapify the affected sub-tree
        heapify(arr, n, largest)

#Build max heap function
def build_max_heap(arr):
    n = len(arr)
    # Call heapify for all non-end nodes (n//2 - 1 down to 0)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

#Main function to perform heapsort
def heap_sort(arr, l, r):
    n = len(arr)
    #Initial heap construction
    build_max_heap(arr)
    # One by one extract elements from heap
    # Stop at 1 because the last element will be in place after the second to last swap
    for i in range(n - 1, 0, -1):
        tmp_val = arr[i]
        arr[i] = arr[0]
        arr[0] = tmp_val
        heapify(arr, i, 0)
    




#Entry point of the program: accept a csv file containing an array, and output the sorted array to a new csv file
if __name__ == "__main__":
    import csv
    import random
    #Memory profiler
    import tracemalloc
    #Time profiler
    import time

    #Parse arguments from the command line
    import argparse
    parser = argparse.ArgumentParser(description='Sort an array using quick sort with random pivot selection.')
    parser.add_argument('--input_file', type=str, help='The input csv file containing the array to be sorted.')
    parser.add_argument('--output_file', type=str, help='The output csv file to write the sorted array to.')
    args = parser.parse_args()
    #Read the array from the input csv file
    with open(args.input_file, 'r') as f:
        reader = csv.reader(f)
        arr = list(reader)[0]
        arr = [int(x) for x in arr]
    #Sort the array using quick sort with random pivot selection
    start_time = time.time()
    tracemalloc.start()
    heap_sort(arr, 0, len(arr) - 1)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    
    tracemalloc.stop()
    #Write the sorted array to the output csv file
    with open(args.output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(arr)

    #Write the stats to a text file 
    #seconds, peak memory usage in KB
    peak_kb = peak / 1024

    with open('stats.txt', 'w') as f:
        f.write(f"{end_time - start_time},{peak_kb}")  



