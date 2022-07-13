# importing the multiprocessing module 
import multiprocessing 




def cube(i):
    a = i ** 2
    global num
    num += a

    print(a)

line = [1, 2, 3, 4]

num = 0

cube(2)
print(num)