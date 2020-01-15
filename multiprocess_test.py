import time
import multiprocessing


def is_prime(n):
    if (n <= 1):
        return 'not a prime number'
    if (n <= 3):
        return 'prime number'

    if (n % 2 == 0 or n % 3 == 0):
        return 'not a prime number'

    i = 5
    while (i * i <= n):
        if (n % i == 0 or n % (i + 2) == 0):
            return 'not a prime number'
        i = i + 6

    return 'prime number'


def multiprocessing_func(x):
    time.sleep(2)
    print('{} is {} number'.format(x, is_prime(x)))


if __name__ == '__main__':
    starttime = time.time()
    pool = multiprocessing.Pool()
    pool.map(multiprocessing_func, range(1, 10))
    pool.close()
    print()
    print('Time taken = {} seconds'.format(time.time() - starttime))