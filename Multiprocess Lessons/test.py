# importing the multiprocessing module 
import multiprocessing 


num = []


def cube(i, line):
    a = line[i] ** 2
    global num
    num.append(a)

    print(a)



if __name__ == "__main__":
    line = [1, 2, 3, 4]
    
    # creating processes 
    p1 = multiprocessing.Process(target=cube, args=(0, line)) 
    p2 = multiprocessing.Process(target=cube, args=(1, line))
    p3 = multiprocessing.Process(target=cube, args=(2, line)) 
    p4 = multiprocessing.Process(target=cube, args=(3, line)) 

    # starting process 1&2
    p1.start() 
    p2.start() 
    p3.start() 
    p4.start() 
    # wait until process 1&2 is finished 
    p1.join() 
    p2.join() 
    p3.join() 
    p4.join() 

    # both processes finished 
    print(num)
    print("Done!")