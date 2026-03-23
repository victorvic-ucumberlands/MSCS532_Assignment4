#Implementation of a priority queue using a binary heap.
#this is based on the max heap implementation of heapsort.py
#The heap is implemented as an list with each element being the pair of (priority_value, PID), and the hash table maps PID to other information such as arrival time and deadline
import random
#Note: install sympy through pip 
from sympy import primerange


#Node for the linked list in chaining
class Node:
    def __init__(self, key, value,  arrival_time, deadline):
        self.key = key
        self.value = value
        self.arrival_time = arrival_time
        self.deadline = deadline
        self.next = None


class HashTable:
    #For init, we can take a set of key:value pairs and insert them into the hash table
    def __init__(self, initial_data=None):
        #default size of the hash table
        self.size = 10000
        #Allocate memory for the hash table
        self.table = [None] * self.size
        #Generate a prime number larger than the table size for the universal hashing function
        self.p = list(primerange(self.size, self.size*100))[0] 
        #Generate constants a and b for the universal hashing function
        self.a = random.randint(1, self.p - 1)
        self.b = random.randint(0, self.p - 1)

        #If initial data is provided, insert it into the hash table
        if initial_data is not None:
            for key, value, arrival_time, deadline in initial_data.items():
                self.insert(key, value, arrival_time, deadline)

    #Universal hashing function: h(k) = ((a * k + b) mod p) mod m
    def hash_function(self, key):
        return ((self.a * key + self.b) % self.p) % self.size

    def insert(self, key, value, arrival_time, deadline):
        arr_idx = self.hash_function(key)
        new_node = Node(key, value, arrival_time, deadline)

        #If this slice is empty, insert the new  node
        if self.table[arr_idx] is None:
            self.table[arr_idx] = new_node
        #If not empty, add it at the end of the linked list 
        else:
            current = self.table[arr_idx]
            #Keep traversing the linked list until we find the end or a node with the same key
            while current is not None:
                if current.key == key:
                    current.value = value
                    current.arrival_time = arrival_time
                    current.deadline = deadline
                    return
                if current.next is None:
                    break
                current = current.next
            current.next = new_node

    def search(self, key):
        #index from hash function
        index = self.hash_function(key)
        current = self.table[index]

        while current is not None:
            #key found, return the value
            if current.key == key:
                return (current.value, current.arrival_time, current.deadline)
            current = current.next
        #Return False if key not found
        return False

    def delete(self, key):
        #index from hash function
        index = self.hash_function(key)
        #Start on first element
        current = self.table[index]
        prev = None

        while current is not None:
            if current.key == key:
                if prev is None:
                    #First element matched, update the head of the linked list
                    self.table[index] = current.next 
                else:
                    #Delete current by updating the pointer of the previous node to skip current
                    prev.next = current.next
                return True #Key found and deleted
            prev = current
            current = current.next

        return False #Key not found, nothing deleted

#Heap class
class MaxHeap:
    def __init__(self, initial_data=None):
        #Each element is a pair of (priority_value, PID)
        self.heap = []        
        self.size = 0
        #Hash table to map PID to index in the heap array
        self.hash_table = HashTable()
        #If initial data is provided, insert it into the heap
        #initial_data is a dictionary of PID:priority_value,arrival_time,deadline
        if initial_data is not None:
            for list_element in initial_data:
                self.insert(list_element[0], list_element[1], list_element[2], list_element[3])

        print ("Initial heap:", self.heap)

    #Increase key function: Update the priority of an element in the heap and maintain the heap priority
    def increase_key(self, index, new_priority):
        #Update the priority in the heap array
        pid = self.heap[index][1]
        self.heap[index] = (new_priority, pid)
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index][0] > self.heap[parent_index][0]:
                #Swap the current element with its parent
                #Update the hash table with the new index for the PID
                self.hash_table.insert(pid, parent_index, self.hash_table.search(pid)[1], self.hash_table.search(pid)[2])
                parent_pid = self.heap[parent_index][1]
                #Update the hash table with the new index for the parent PID
                self.hash_table.insert(parent_pid, index, self.hash_table.search(parent_pid)[1], self.hash_table.search(parent_pid)[2])
                tmp_val = self.heap[index]
                self.heap[index] = self.heap[parent_index]
                self.heap[parent_index] = tmp_val
                #Update the index to the parent's index for the next iteration
                index = parent_index
            else:
                break

    
    #Insert function: First insert it in the heap array and return the index, then insert the PID and index into the hash table, then maintain the heap property by bubbling up the new element
    def insert(self, pid, priority, arrival_time, deadline):
        #Insert the PID,priority pair into the heap array
        self.heap.append((priority, pid))
        self.size += 1
        #Insert the PID and index into the hash table
        self.hash_table.insert(pid, self.size - 1, arrival_time, deadline)
        #Bubble up the new element to maintain the heap property
        self.increase_key(self.size - 1, priority)
    
    def extract_max(self):
        if self.size == 0:
            return None #Heap is empty
        max_element = self.heap[0]
        priority, pid, arrival_time, deadline = max_element[0], max_element[1], self.hash_table.search(max_element[1])[1], self.hash_table.search(max_element[1])[2]
        #Delete the PID from the hash table since it's extracted from the heap
        self.hash_table.delete(max_element[1])
        #Make the priorty of the root element negative infinity and swap it with the last element in the heap array, then heapify the root to maintain the heap property
        self.heap[0] = (float('-inf'), max_element[1])
        #Swap the root with the last element in the heap array
        tmp_val = self.heap[0]
        self.heap[0] = self.heap[self.size - 1]
        self.heap[self.size - 1] = tmp_val
        #Heapify the root to maintain the heap property
        self.size -= 1

        self.heapify(self.heap, self.size, 0)

        return pid, priority,arrival_time, deadline #Return the priority, PID, and hash table
    
    def extract_min(self):
        if self.size == 0:
            return None #Heap is empty        
        #To extract the min, we need to traverse the heap array to find the element with the smallest priority value
        min_index = 0
        for i in range(1, self.size):
            if (self.heap[i][0] < self.heap[min_index][0]) and (self.heap[i][0] != float('-inf')):
                min_index = i
        min_element = self.heap[min_index]
        priority, pid, arrival_time, deadline = min_element[0], min_element[1], self.hash_table.search(min_element[1])[1], self.hash_table.search(min_element[1])[2]
        #Delete the PID from the hash table since it's extracted from the heap
        self.hash_table.delete(min_element[1])
        #Make the priority of the min element negative infinity and swap it with the last element in the heap array, then heapify to maintain the heap property
        self.heap[min_index] = (float('-inf'), min_element[1])
        #Swap the min element with the last element in the heap array
        tmp_val = self.heap[min_index]
        self.heap[min_index] = self.heap[self.size - 1]
        self.heap[self.size - 1] = tmp_val
        #Heapify the element at min_index to maintain the heap property
        self.size -= 1
        self.heapify(self.heap, self.size, min_index)
        return pid, priority, arrival_time, deadline #Return the PID, priority, arrival_time, and deadline
   

    def increase_key_element(self, pid, new_priority):
        #Search for the index of the element with the given PID in the hash table
        search_result = self.hash_table.search(pid)
        if search_result is False:
            return False #PID not found in the hash table
        index = search_result[0]
        #Increase the key of the element at the found index
        self.increase_key(index, new_priority)
        return True

    def decrease_key_element(self, pid, new_priority):
        #Search for the index of the element with the given PID in the hash table
        search_result = self.hash_table.search(pid)
        if search_result is False:
            return False #PID not found in the hash table
        index = search_result[0]
        #Update the priority in the heap array
        self.heap[index] = (new_priority, pid)
        #Heapify the element at the found index to maintain the heap property
        self.heapify(self.heap, self.size, index)
        return True
    
    def is_empty(self):
        return self.size == 0

    def heapify(self, arr, n, i):
        #Start with i as the largest element (the element to be heapified)
        largest = i 
        l = 2 * i + 1 # left = 2*i + 1
        r = 2 * i + 2 # right = 2*i + 2

        
        # If left child is larger than root
        if l < n and arr[l][0] > arr[largest][0]:
            largest = l

        # If right child is larger than largest so far
        if r < n and arr[r][0] > arr[largest][0]:
            largest = r

        # If largest is not root
        if largest != i:
            # Update hash table with new indices before swapping
            pid_i = arr[i][1]
            pid_largest = arr[largest][1]
            self.hash_table.insert(pid_i, largest, self.hash_table.search(pid_i)[1], self.hash_table.search(pid_i)[2])
            self.hash_table.insert(pid_largest, i, self.hash_table.search(pid_largest)[1], self.hash_table.search(pid_largest)[2])
            
            # Swap elements in heap
            tmp_val = arr[i]
            arr[i] = arr[largest]
            arr[largest] = tmp_val
            
            #largest keeps the swapped element's index, so we need to heapify the affected sub-tree
            self.heapify(arr, n, largest)  
    
#Entry point of the program, it takes as an input a csv file containing the initial data for the heap, and then performs the allowed operations based on the command line arguments
if __name__ == "__main__":
    import csv
    import argparse
    parser = argparse.ArgumentParser(description='Priority Queue using Binary Heap')
    parser.add_argument('--input_file', type=str, help='CSV file containing initial data for the heap. Each row should contain PID, priority, arrival_time, deadline')
    parser.add_argument('--operation', type=str, help='Operation to perform: insert, extract_max, extract_min, increase_key, decrease_key')
    parser.add_argument('--pid', type=int, help='PID for insert, increase_key, or decrease_key operation')
    parser.add_argument('--priority', type=int, help='Priority for insert, increase_key, or decrease_key operation')
    parser.add_argument('--arrival_time', type=int, help='Arrival time for insert operation')
    parser.add_argument('--deadline', type=int, help='Deadline for insert operation')
    parser.add_argument('--output_file', type=str, help='CSV file to output the results of the scheduling algorithm ')
    args = parser.parse_args()

    #Read initial data from the input csv file and create the heap
    initial_data = []
    with open(args.input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            pid = int(row[0])
            priority = int(row[1])
            arrival_time = int(row[2])
            deadline = int(row[3])
            initial_data.append((pid, priority, arrival_time, deadline))

    heap = MaxHeap(initial_data)

    #Perform the specified operation
    if args.operation == 'insert':
        heap.insert(args.pid, args.priority, args.arrival_time, args.deadline)
    elif args.operation == 'extract_max':
        print(heap.extract_max())
    elif args.operation == 'extract_min':
        print(heap.extract_min())
    elif args.operation == 'increase_key':
        heap.increase_key_element(args.pid, args.priority)
    elif args.operation == 'decrease_key':
        heap.decrease_key_element(args.pid, args.priority)

    #Complete the scheduling algorithm and output the results to the output csv file
    #In a max priority scheduling algorithm, we repeatedly extract the max until the heap is empty, and write the PID, priority, arrival time, and deadline of the extracted element to the output csv file
    with open(args.output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['PID', 'Priority', 'Arrival Time', 'Deadline'])
        while not heap.is_empty():
            max_element = heap.extract_max()
            writer.writerow([max_element[0], max_element[1], max_element[2], max_element[3]])

    print(heap.heap)
