import time
import multiprocessing

def my_sleep(length):
    print(f'sleeping for {length}')
    time.sleep(length)

def main():
    times = [1,2,3,2,4,2,3,5,3,2]
    pool = multiprocessing.Pool(4)
    pool.map(my_sleep, times)

if __name__ == '__main__':
    main()