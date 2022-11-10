from typing import List

def rotate(A: List[int], k: int) -> List[int]:
    # Calculate index for slicing array
    # This considers full rotation by modulo
    index = len(A) % k
    return A[index:] + A[:index]

def missing_int(A: List[int]) -> int:
    # Remove and sort positive numbers from A
    positives_sorted_arr = sorted([num for num in A if num > 0])
    # Get first positive element from positives_sorted_arr
    # positives_sorted_arr can be empty, defaults to 0
    first_positive = next(iter(positives_sorted_arr), 0)
    diff_from_zero = abs(0 - first_positive)

    # check for 0 and first element from positives_sorted_arr
    if diff_from_zero != 1:
        return 1

    for index in range(0, len(positives_sorted_arr) - 1):
        a = positives_sorted_arr[index]
        b = positives_sorted_arr[index+1]
        if a == b:
            continue

        diff = abs(a - b)
        if diff != 1:
            return a + 1
    
    # Return the last element of the sorted positive array + 1
    return positives_sorted_arr[-1] + 1

if __name__ == '__main__':
    print(
        """
Given an array A of N integers, write a function missing_int(A) that returns the smallest
positive integer (greater than 0) that does not occur in A.
    ○ Case 1: A = [1, 3, 6, 4, 1, 2] should return 5
    ○ Case 2: A = [1, 2, 3] should return 4
    ○ Case 3: A = [-1, -1, -1, -5] should return 1
    ○ Case 4: A = [1, 3, 6, 4, 1, 7, 8, 10] should return 2
    """)
    print(f'Case 1: {missing_int([1, 3, 6, 4, 1, 2])}')
    print(f'Case 2: {missing_int([1, 2, 3])}')
    print(f'Case 3: {missing_int([-1, -1, -1, -5])}')
    print(f'Case 4: {missing_int([1, 3, 6, 4, 1, 7, 8, 10])}')
    print()
    print(
        """
Write a rotate(A, k) function which returns a rotated array A, k times; that is, each
element of A will be shifted to the right k times
    ○ Case 1: rotate([3, 8, 9, 7, 6], 3) returns [9, 7, 6, 3, 8]
    ○ Case 2: rotate([0, 0, 0], 1) returns [0, 0, 0]
    ○ Case 3: rotate([1, 2, 3, 4], 4) returns [1, 2, 3, 4]
        """)
    print(f'Case 1: {rotate([3, 8, 9, 7, 6], 3)}')
    print(f'Case 2: {rotate([0, 0, 0], 1)}')
    print(f'Case 3: {rotate([1, 2, 3, 4], 4)}')

    