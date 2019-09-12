import threading
import time


def show_test(arr_job):
    for indx in arr_job:
        print(indx)
        time.sleep(3)

list_a = [1, 2, 3, 4]
list_b = [5, 6, 7, 8]

x = threading.Thread(target=show_test, args=(list_a, ), daemon=False)
y = threading.Thread(target=show_test, args=(list_b, ), daemon=False)
x.start()
y.start()