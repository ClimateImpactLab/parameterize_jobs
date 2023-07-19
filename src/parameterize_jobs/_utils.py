
import functools


def _product(arr):
    return functools.reduce(lambda x, y: x * y, arr, 1)


def _cumprod(arr):
    return [_product(arr[i:]) for i in range(len(arr))]
