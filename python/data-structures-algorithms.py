#! /usr/bin/env python

#! WARNING: Note that this is old code, written in Python 2!

''' This is a module containing all the data structures and algorithms that I consider important and/or useful, along with relevant information regarding their asymptotic complexity.

NOTE: 
a) Although I wrote all the implementations in this module, all of them were inspired by pseudocode / source code from various other sources.
b) Instead of worrying about 'theta' vs 'big-oh', I will always use 'big-oh', designated by 'O'.
c) 'lg n' = 'log of n, to the base 2'
d) Any item below, whose name starts with only 1 underscore, should be treated as private.
e) Whenever I say 'array', I am actually referring to a Python list.
f) All the sorting algorithms only take an unordered input array.
g) All the sorting algorithms sort in ascending order. '''

__author__ = 'Pranav Marla'

# INFINITY is guaranteed to be bigger than any other number.
# Note that it CANNOT be converted to an integer.
INFINITY = float('inf')

from random import randint

# Data Structures

# Miscellaneous

# Creates a 2D array. Initial array element value defaults to the value None.
def two_d_array(num_rows, num_cols, initial_value = None):
    
    arr = []
    
    for i in range(num_rows):
        
        # For each row, append an array containing num_cols elements, where each element is set to initial_value.
        arr.append(num_cols * [initial_value])

    # NOTE: Do NOT simply do: arr = num_rows * [num_cols * [initial_value]], since that will simply give you a list containing num_rows REFERENCES to the SAME ONE LIST (ROW) containing num_cols elements, such that modifying any of the referenced lists (rows) will modify ALL the referenced lists (rows)!
    # Source (as well as alternate implementation): https://docs.python.org/2/faq/programming.html#faq-multidimensional-list
        
    return arr

def max_subarray(array):
    '''
    Finds the contiguous subarray with the largest sum. This is known as Kadane's algorithm.
    
    Note that this works even when all the numbers in the array are negative.
        Eg. For arr = [-2, -3, -1, -5], max sum = -1 and max subarray = [-1].
    
    Time Complexity: O(n)
    
    Space Complexity: O(1)
    
    '''
    
    # This is the max sum of the subarray ending here (i.e. now that we have considered the current element).
    # Note that the subarray that gave rise to this sum can never be empty -- at a minimum, it consists of ONLY the current element.
    current_max = array[0]
    
    # Indices of the first and last element in the max subarray ending here, at the current element.
    current_start = 0
    # current_end = 0 --> unnecessary since, by definition, current_end will always equal the index of the current element.
    
    # Every element in the array can have a different current_max -- the largest of all of them is stored in overall_max.
    overall_max = array[0]
    
    # Indices of the first and last element in the overall max subarray.
    overall_start = 0
    overall_end = 0
    
    # Note that current_index should start at 1, NOT 0!
    for current_index, current_num in enumerate(array[1:], start = 1):
        
        # NOTE: By definition, current_end will always equal current_index (the index of the current element).
        
        potential_current_max = current_max + current_num
        
        # To get the max subarray ending here, we're better off dumping the previous elements in the subarray (to the left of the current element).
        # NOTE: If we strictly stuck to 'current_num > potential_current_max', then the only difference would be that the max subarray might be longer (but with the same sum), since it now keeps previous elements that cancel out and are thus meaningless.
        #   Eg. For array [-4, 5, -5, 15, -6, 18, 2, -20]:
        #
        #   If 'current_num >= potential_current_max': max_subarray = [15, -6, 18, 2]
        #   If 'current_num > potential_current_max': max_subarray = [5, -5, 15, -6, 18, 2]
        if current_num >= potential_current_max:
            current_max = current_num
            current_start = current_index
            
        # To get the max subarray ending here, we're better off keeping the previous elements in the subarray (to the left of the current element).
        else:
            current_max = potential_current_max
        
        # Max subarray ending here is better than previous potential overall max subarray
        if current_max > overall_max:
            overall_max = current_max
            overall_start = current_start
            overall_end = current_index # By definition, current_end will always equal current_index.
            
    # Return max sum, as well as the subarray that gave rise to that max sum.
    return (overall_max, array[overall_start : overall_end + 1])

def linear_selection(array, order):
    '''
    Randomised algorithm to get the ith order statistic (input variable 'order') of an unsorted array.
    
    This is merely a client-side wrapper for _linear_selection().
    
    Time Complexity:
        Average/Expected:       O(n)
        Worst (RARE):           O(n^2)
        
    Space Complexity: O(1)
    
    '''
    
    # Eg. If we want the 3rd order statistic ('order' = 3), it means we want the 3rd smallest element (the element which is only bigger than 2 other elements in the array).
    
    # Note that, at this point, 'order' is NOT an array index! 
    # Thus, if we want the minimum element (the element which would be at index 0 if the array was sorted), 'order' = 1. If we want the maximum element (the element which would be at index len(array)-1 if the array was sorted), order = len(array).
    # Thus, for simplicity, decrement 'order' so that it does match the corresponding sorted array index.
    
    return _linear_selection(array, 0, len(array) - 1, order - 1)

def _linear_selection(subarray, first_index, last_index, order_index):
    
    # Base Cases: 
    
    # If want min / max element, probably faster (not asymptotically, but smaller constant factors) to use the built-in functions.
    
    if order_index == first_index:
        return min(subarray[first_index : last_index + 1])
    
    if order_index == last_index:
        return max(subarray[first_index : last_index + 1])
    
    # If we have the min and max base cases, then the subarray will never get smaller than 2 elements -- thus, only need the below base case if do not have the min and max base cases.
    # If only 1 element in the subarray, that must be the element we want.
    # Will never recurse on an empty subarray, so no need to check for it.
    # if first_index == last_index:
       # return subarray[first_index]
        
    # Partition input subarray around a randomly chosen pivot element such that, in the resulting subarray, elements to the left of the pivot are <= pivot and elements to the right of the pivot are > pivot.    
    # Obtain the end index of (index of last element in) the first partition (containing all elements <= pivot, apart from the pivot itself) and the beginning index of (index of first element in) the second partition (containing all elements > pivot)
    end_first_part, start_second_part = _partition_around_pivot(subarray, first_index, last_index)
    
    # By definition, pivot is in its rightful place.
    # Eg. If pivot is the 3rd smallest element in the subarray, it will be located in the subarray at the 3rd position (subarray index = pivot_index = 2).
    
    # pivot_index = end_first_part + 1 = start_second_part - 1
    pivot_index = end_first_part + 1
    
    # Order statistic element is smaller than the pivot -- located in the first / left partition.
    if order_index < pivot_index:
        return _linear_selection(subarray, first_index, end_first_part, order_index)
    
    # Order statistic element is greater than the pivot -- located in the second / right partition.
    # Conceptually, since the smaller elements (left partition + pivot) will be effectively removed from the subarray in the following recursive call, it would seem as if the desired order statistic would need to be correspondingly reduced to still refer to the same position in the reduced subarray.
    # However, in practice, since all the indices (pivot_index, start_second_part, first_index, last_index, etc.) are always relative to the full original array, it is simpler to keep order untouched, such that it too is always relative to the full original array, thus enabling easy comparison / interaction with the indices.
    elif pivot_index < order_index:
        return _linear_selection(subarray, start_second_part, last_index, order_index)
    
    # Pivot happens to be the exact order statistic element that we want (order_index = pivot_index)
    else:
        return subarray[pivot_index]
        
# Sorting Algorithms

def quick_sort(array):
    '''
    Randomised algorithm to sort the input array in ascending order.
    This is merely a client-side wrapper for _quick_sort().
    
    Time Complexity:
        Average/Expected:       O(n log(n))
        Worst (RARE):           O(n^2)
        
    Space Complexity: O(1)
    
    '''
    _quick_sort(array, 0,  len(array) - 1)
    
def _quick_sort(subarray, first_index, last_index):

    # Base Case: 0/1 elements -- already sorted.
    if first_index >= last_index:
        return

    # Partition input subarray around a randomly chosen pivot element such that, in the resulting subarray, elements to the left of the pivot are <= pivot and elements to the right of the pivot are > pivot.
    # Obtain the end index of (index of last element in) the first partition (containing all elements <= pivot, apart from the pivot itself) and the beginning index of (index of first element in) the second partition (containing all elements > pivot)
    end_first_part, start_second_part = _partition_around_pivot(subarray, first_index, last_index)
    
    # Recursively sort the 2 partitions
    _quick_sort(subarray, first_index, end_first_part)
    _quick_sort(subarray, start_second_part, last_index)

def _partition_around_pivot(subarray, first_index, last_index):
    '''
    Partition input subarray (from first_index to last_index) around a randomly chosen pivot element such that, in the resulting subarray, elements to the left of the pivot are <= pivot and elements to the right of the pivot are > pivot.
    
    Time Complexity:
        O(n)    where n = last_index - first_index + 1
        
    Space Complexity:
        O(1)    [i.e. in place]
    
    '''
    
    # Randomly choose index of pivot element
    pivot_index = _choose_pivot(subarray, first_index, last_index)
    
    # Get actual pivot element
    pivot = subarray[pivot_index]
    
    # Ensure that pivot element is in the beginning of the subarray
    # Note that first_index is NOT necessarily 0!
    if first_index < pivot_index:
        
        # Swap with first element in the subarray
        subarray[pivot_index] = subarray[first_index]
        subarray[first_index] = pivot
        
    # Pointer to (index of) the first element greater than the pivot (always to the right of the partition of the subarray containing all the elements <= pivot).
    first_greater_index = first_index + 1
    
    # first_unpartitioned_index: Pointer to (index of) the first element that has not yet been partitioned (i.e. moved depending on whether or not it is <= pivot).
    
    
    # For the bulk of this algorithm, this is the partition structure we will be building / maintaining in the subarray:
    #    ______________________________________________________________________________
    #   | pivot | elements <= pivot | elements > pivot | new / unpartitioned elements |
    #                                ^                  ^
    #                               |                   |
    #                              |                    |
    #                             |                     |
    #                first_greater_index         first_unpartitioned_index
    #
    
    
    # Keeps track of whether or not we found at least one element that was greater than the pivot.
    found_greater_element = False
    
    # first_unpartitioned_index goes from first_index+1 to last_index.
    for first_unpartitioned_index in range(first_index + 1, last_index + 1):
        
        # Get next new / unpartitioned element
        first_unpartitioned_element = subarray[first_unpartitioned_index]
        
        # To ensure that the below 'elif' is only accessible when first_unpartitioned_element > pivot, do NOT put the found_greater_element check in (on the same line as) this same 'if' statement!
        if (first_unpartitioned_element <= pivot):
            
            # If we haven't found at least one element > pivot, then there would actually be no need to swap first_unpartitioned_element that is <= pivot since the entire 'seen so far' / partitioned part of the subarray would consist of elements <= pivot!
            if found_greater_element:
            
                # Swap first_unpartitioned_element with first element greater than the pivot, to preserve the invariant that (in the partitioned part of the subarray) all the elements <= pivot are always to the left of the elements > pivot.
                subarray[first_unpartitioned_index] = subarray[first_greater_index]
                subarray[first_greater_index] = first_unpartitioned_element
            
            # Partition containing elements <= pivot has now grown by 1 -- need to increment first_greater_index to once again point to the right of this partition.
            first_greater_index += 1
                
        # Else, if first_unpartitioned_element > pivot, it's already in the correct position (i.e. it's already to the right of all the elements <= pivot) -- thus, no need to do any swaps.
        # However, need to remember that we found at least one element > pivot.
        elif not found_greater_element:
            found_greater_element = True
    
    # At this point, there are no more new / unpartitioned elements. All the elements <= pivot are to the left of all the elements > pivot. Note that, within each of the 2 partitions (<= pivot  and  > pivot), the elements are NOT necessarily sorted.
    #
    # This is how the subarray currently looks:
    #    _______________________________________________
    #   | pivot | elements <= pivot | elements > pivot |
    #                                ^                  ^
    #                               |                   |
    #                              |                    |
    #                             |                     |
    #                first_greater_index         first_unpartitioned_index
    #
    #
    # This is the final structure we want in the subarray:
    #    _______________________________________________
    #   | elements <= pivot | pivot | elements > pivot |
    #
    
    # However, pivot is still in the beginning of the subarray (at first_index).
    # To achieve this structure (i.e. to move the pivot into its rightful place -- the place it would be in if this entire array was actually sorted as opposed to just partitioned), we swap the pivot (currently at first_index) with the last element <= pivot.
    subarray[first_index] = subarray[first_greater_index - 1]
    subarray[first_greater_index - 1] = pivot
    
    # Return end index of (index of last element in) the first partition (containing all elements <= pivot, apart from the pivot itself) and the beginning index of (index of first element in) the second partition (containing all elements > pivot).
    return (first_greater_index - 2, first_greater_index)

def _choose_pivot(subarray, first_index, last_index):
    '''
    Given an unsorted subarray, return a random pivot index (i.e. the index of the pivot element, rather than the actual pivot element itself).
    
    '''
    return randint(first_index, last_index)
    
    
def insertion_sort(input):
    '''
    Due to its tight inner loops, this is a fast, in-place sorting algorithm for small input sizes.
    Input:
        Unordered input array.
        
    Output:
        The unordered input array is sorted in place (i.e. only a constant number of elements of input are ever stored outside input).
        
    Return Value:
        N/A
        
    Time Complexity:
        Worst:      O(n^2)
        Average:    O(n^2)
    
    Space Complexity: O(1)
        
    '''
    
    # array indices
    i = None
    j = None
    
    # Number of input elements
    input_size = len(input)
    
    # Current, unsorted input element -- this is the element currently being sorted.
    current_unsorted = None
    
    # Current, sorted input element (located in the sorted subarray to the left of current_unsorted)
    current_sorted = None
    
    # Iterate from the 2nd element (index 1) up to the last element
    for j in range(1, input_size):
        current_unsorted = input[j]
        
        # All the elements in input prior to (to the left of) index j are sorted (form a sorted "subarray").
        # Insert current_unsorted into this sorted subarray by comparing current_unsorted against each of the elements in the sorted subarray (i.e. current_sorted), from right to left.
        
        # Note: Although the below code may look inefficient, it actually avoids many edge cases that would trip up a seemingly more efficient Python 'for' loop.
        
        # Start from the end of the sorted subarray, which is right before current_unsorted.
        i = j - 1
        current_sorted = input[i]
        
        while (i >= 0) and (current_sorted > current_unsorted):
            
            # Since current_sorted > current_unsorted, current_unsorted should definitely be placed somewhere before current_sorted -- move current_sorted 1 place to the right.
            input[i + 1] = current_sorted
            
            # Move on to the next element in the sorted subarray
            i -= 1
            current_sorted = input[i]
        
        # At this point, either:
        # a) current_sorted <= current_unsorted
        # Since all the elements to the left of current_sorted are guaranteed to be <= current_sorted, they are also guaranteed to be <= current_unsorted -- thus, no need to keep iterating through the sorted subarray.
        #   or
        # b) We've reached the beginning of the sorted subarray (current_unsorted is smaller than all the elements in the sorted subarray, i.e. every current_sorted is > current_unsorted)
        # Either way, thanks to the design of the above 'while' loop, 'i + 1' is the correct index where current_unsorted should be placed. 
        input[i + 1] = current_unsorted
       
       
def merge_sort(input):
    '''
    This is merely a nice, client-side wrapper. The real work is done by _merge_sort()
    
    Input:
        Unordered input array.
        
    Output:
        The unordered input array is replaced by a sorted array.
        
    Return Value:
        N/A
        
    Time Complexity:
        Worst:      O(n log n)
        Average:    O(n log n)
    
    Space Complexity: O(n)
        
    '''
    
    _merge_sort(input, 0, len(input) - 1)

def _merge_sort(input, start_index, end_index):
    '''
    Helper function for merge_sort(). 
    Sorts the subarray input[start_index ... end_index].
    '''
    # If start_index = end_index, subarray has only 1 element and, thus, is sorted.
    # If start_index > end_index, input is not a valid subarray.
    # In both cases, no further processing (recursion) is necessary.
    if start_index >= end_index:
        return
    
    # Do not use the more intuitive formula of middle_index = (start_index + end_index) / 2 since that could lead to an integer overflow!
    # Note that the integer division already performs integer truncation.
    middle_index = start_index + ((end_index - start_index) / 2)
    
    # Sort the left subarray
    _merge_sort(input, start_index, middle_index)
    
    # Sort the right subarray
    _merge_sort(input, middle_index + 1, end_index)
    
    # Merge the two sorted subarrays into 1 sorted subarray that replaces input[start_index ... end_index]
    _merge(input, start_index, middle_index, end_index)
    
def _merge(input, start_index, middle_index, end_index):
    '''
    Helper function for _merge_sort(). 
    Merges the 2 sorted subarrays (input[start_index ... middle_index] and input[middle_index + 1 ... end_index]) into a single sorted array that replaces input[start_index ... end_index].
    This does NOT operate in place.
    
    Time complexity: O(n) 
    [n = end_index - start_index + 1 = total number of elements being merged]
    '''
    
    # A pair of elements are compared at a time, 1 from the left subarray and 1 from the right subarray. The smaller of the two is placed into input. When one of the subarrays is exhausted, the remaining subarray is placed into input as is.
    # To avoid having to check if any of the subarrays are exhausted every time, we add an extra element to the end of both subarrays to serve as a sentinel: INFINITY.
    
    # Copy the left and right sorted subarrays of 'input', from 'input' into new arrays 'left' and 'right'.
    
    # Left sorted subarray is input[start_index ... middle_index]
    # Note that start_index is NOT always 0!!
    left = input[start_index:(middle_index + 1)]
    
    # Right sorted subarray is input[middle_index + 1 ... end_index]
    # Note that end_index is NOT always (len(input) - 1)!!
    right = input[(middle_index + 1):(end_index + 1)]
    
    # Add the sentinel element INFINITY to the end of both subarrays
    left.append(INFINITY)
    right.append(INFINITY)
    
    # Left and right indices, initialised to the beginning of the two subarrays.
    i = 0
    j = 0
    
    # Iterate over input from start_index to end_index
    for k in range(start_index, end_index + 1):
        
        # Compare the smallest element from the left sorted subarray (left[i]) with the smallest from the right sorted subarray (right[j]) and place the smaller of the two in input[k]
        
        # Left is smaller/equal
        if left[i] <= right[j]:
            input[k] = left[i]
            # Update index of left subarray
            i += 1
            
        # Right is smaller
        else:
            input[k] = right[j]
            # Update index of right subarray
            j += 1
        
        
        
        
        
# Searching Algorithms

def binary_search(array, desired_num):
    '''
    Iterative algorithm that searches a SORTED array for desired_num (refers to an element, not an index).
    This is merely a client-side wrapper for _binary_search().
    
    Note that the array has to be already sorted (in ascending order)!
    
    Return Value:
        If desired_num is in the array: Array index of desired_num
        If desired_num is not in the array: None
    
    Time Complexity:
        Worst:      O(log(n))
        Average:    O(log(n))
        
    Space Complexity: O(1)
    
    '''
    return _binary_search(array, 0, len(array) - 1, desired_num)

def _binary_search(array, start_index, end_index, desired_num):
    
    # While the array is not empty
    while (start_index <= end_index):
        
        # Do not use the more intuitive formula of middle_index = (start_index + end_index) / 2 since that could lead to an integer overflow!
        # Note that the integer division already performs integer truncation.
        middle_index = start_index + ((end_index - start_index) / 2)
        
        middle_num = array[middle_index]
        
        # Focus on left subarray by reducing end_index
        if desired_num < middle_num:
            end_index = middle_index - 1
            
        # Focus on right subarray by increasing start_index
        elif middle_num < desired_num:
            start_index = middle_index + 1
            
        # middle_num = desired_num -- return middle_index (= index of desired_num)
        else:
            return middle_index
            
    # Array is now empty (either because it was empty to start with or because we exhaustively searched through the array as far as possible -- i.e., not that we looked at every element, but that we went as far as we could in the direction where desired_num should have been)
    # desired_num is not in the array
    return None


# Test the above items by running this module as a script.
if __name__ == '__main__':
    
    from sys import argv, exit
    
    # List of valid test subjects
    test_subjects = ['stack', 'queue', 'linked_list', 'heap', 'priority_queue', 'binary_tree', 'binary_search_tree', 'insertion_sort', 'merge_sort', 'heap_sort', 'quick_sort', 'binary_search', 'depth_first_search', 'breadth_first_search']
    
    # When the command-line arguments are incorrect, print an error message and exit.
    def input_error():
        print '''\
Error! Please follow this format: ./my_stuff.py <test_subject>

<test_subject> can be any of the following:\n'''
        for test_subject in test_subjects:
            print test_subject,
            
        print
        exit(1)
    
    # Generic function that tests any sorting algorithm
    # Input is a sorting algorithm (as a function object)
    def test_sort(sorting_algorithm):
        
        # Empty list: Should be unchanged
        print 'Empty list: Should be unchanged'
        
        l = []
        print 'Original:                l = {}'.format(l)
        
        sorting_algorithm(l)
        print 'After attempted sorting: l = {}\n'.format(l)
        
        assert l == []
        
        # List with only 1 element: Should be unchanged
        print 'List with only 1 element: Should be unchanged'
        
        l = [3]
        print 'Original:                l = {}'.format(l)
        
        sorting_algorithm(l)
        print 'After attempted sorting: l = {}\n'.format(l)
        
        assert l == [3]
        
        # List with elements in descending order
        print 'List with elements in descending order'
        
        l = [9, 7, 5, 4, 3, 2, 1]
        print 'Original:                l = {}'.format(l)
        
        ideal = sorted(l)
        print 'Ideally:                 l = {}'.format(ideal)
        
        sorting_algorithm(l)
        print 'After attempted sorting: l = {}\n'.format(l)
        
        
        assert l == ideal
        
        # List with elements in random order
        print 'List with elements in random order'
        
        l = [2, 8, 9, 3, 7, 1, 5, 4, 0, 6]
        print 'Original:                l = {}'.format(l)
        
        ideal = sorted(l)
        print 'Ideally:                 l = {}'.format(ideal)
        
        sorting_algorithm(l)
        print 'After attempted sorting: l = {}\n'.format(l)
        
        assert l == ideal
        
        # List with elements in random order, with duplicates
        print 'List with elements in random order, with duplicates'
        
        l = [2, 8, 9, 3, 7, 2, 1, 5, 8, 4, 0, 5, 6, 1, 7, 2]
        print 'Original:                l = {}'.format(l)
        
        ideal = sorted(l)
        print 'Ideally:                 l = {}'.format(ideal)
        
        sorting_algorithm(l)
        print 'After attempted sorting: l = {}\n'.format(l)
        
        assert l == ideal
        
        # List with odd number of elements in random order
        print 'List with odd number of elements in random order'
        
        l = [2, 8, 9, 3, 7, 1, 5, 4, 0, 6, 11]
        print 'Original:                l = {}'.format(l)
        
        ideal = sorted(l)
        print 'Ideally:                 l = {}'.format(ideal)
        
        sorting_algorithm(l)
        print 'After attempted sorting: l = {}\n'.format(l)
        
        assert l == ideal
    
    # Incorrect number of command-line arguments
    if len(argv) != 2:
        input_error()
        
    test_subject = argv[1]
    
    if test_subject not in test_subjects:
        input_error()
        
    print
        
    if test_subject.endswith('sort'):
        test_sort(eval(test_subject))
        
    elif test_subject.endswith('search'):
        test_search(eval(test_subject))
        
    # test_subject is a data type and has its own specific test function named as per the following format: 'test_<data_type>' -- eg. 'test_stack'
    else:
        # Get the function object name and evaluate it to get the function object
        test_function = eval('_'.join(['test', test_subject]))
        
        # Call the function
        test_function()
        
    print 'All tests passed'
    
    exit()
