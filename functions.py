from functools import lru_cache


def sum_even(list_of_nums):
    """
    Utility function to calculate sum of even numbers in a list.
    :param list_of_nums: list of integers
    :return: integer
    """
    return sum(filter(lambda x: x % 2 == 0, list_of_nums))


@lru_cache()  # caches recently computed results of a function:
def fibonacci(n):
    """
    Calculates the nth fibonacci number.
    :param n: nth fibonacci in the general sequence.
    :return: the nth fib number
    """
    if n < 0:
        return Exception("N must be positive. Got: {}".format(n))
    if n <= 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def test_sum_event():
    list_20 = [8, 8, 4, 1, 3, 3, 1, 7, 9]
    list_8 = [1, 2, 4, 2, 11, 111]
    list_0 = [1, 3, 7, 9, 11, 13]
    list_4 = [-1, -2, 2, 2, 4, -2]
    assert sum_even(list_20) == 20, 'Sum should be 20'
    assert sum_even(list_8) == 8, 'Sum should be 8'
    assert sum_even(list_0) == 0, 'Sum should be 0'
    assert sum_even(list_4) == 4, 'Sum should be 4'
    print("test_sum_event : OK")


def test_fibonacci():
    fib_n1 = 1
    fib_n2 = 2
    fib_n10 = 89
    assert fibonacci(1) == fib_n1, 'First fibonacci number is 1.'
    assert fibonacci(2) == fib_n2, 'Sum of the first two numbers is 2.'
    assert fibonacci(10) == fib_n10, 'Sum of the first two numbers is 89.'
    assert type(fibonacci(-1)) == Exception, 'N must be a positive int.'
    print("test_fibonacci : OK")

test_sum_event()
test_fibonacci()