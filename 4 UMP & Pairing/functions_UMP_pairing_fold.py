import numpy as np
import time


def V_hole(N_max, E_max, M_max, Elist, Mlist, Plist, Gaplist):
    '''
    Expand generating function and get V matrix for CN parameters

    N_max, E_max, M_max: maximum of particle number, excitation energy, projection of angular momentum
    Elist, Mlist, Plist, Gaplist: list of single particle energy, projection of angular momentum, parity, energy gap
    '''
    # for convinence I use 0 and 1 to represent parity +1 and -1, respectively
    Plist_0_and_1 = [0 if i == 1 else 1 for i in Plist]

    # create a matrix V to store parameters of items as elements
    # note M could be negative so I use M_max * 2 + 1, and it means: value + M_max = index
    V = np.zeros((N_max + 1, E_max + 1, M_max * 2 + 1, 2))

    # before open any braket, the expression is 1 and the only elements in the matrix is [0, 0, M_max, 0]
    # the 4th index (0 or 1) represents parity (+1 or -1)
    V[0, 0, int(M_max), 0] = 1

    # create a dict to store index[N, U, M, P] of non-zero elements after open nth braket
    # the list of indexes have the key string "n"
    # the list after open 0st braket has the key "0" 
    non_zero_dict = {}
    non_zero_dict["0"] = [[0, 0, int(M_max), 0]]
    
    # create a dict to track matrix
    matrix_dict = {}
    matrix_dict["0"] = V.copy()

    # for each excited state (each E), I have a braket with the form (1 + x * y**E * t**M * P), I will open them one by one
    # there might be an E showing up several times, so I use index of Elist
    length = len(Elist)

    # for i = 0, 1, 2, ..., 9
    # Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
    for i in range(length):
        t_0 = time.time()

        E = Elist[i]
        M = Mlist[i]
        P = Plist_0_and_1[i]
        Gap = Gaplist[i]

        # creat a copy of the dicts of last i, with them I will calculate the dicts of i+1
        non_zero_dict[str(i+1)] = non_zero_dict[str(i)].copy()
        matrix_dict[str(i+1)] = matrix_dict[str(i)].copy()

        for [x, y, t, p] in non_zero_dict[str(i)]:
            # the actual operations of opening a braket be like:
            # the first item 1 does not matter
            # the second item x * y**E * t**M * P would multiply every non-zero elements in ith matrix
            
            # particle number
            x1 = x + 1

            # energy
            if x == 0:
                y1 = int(0.5 + y + (E ** 2 + Gap ** 2) ** 0.5)
            else:
                y1 = y + E
            
            # projection of angular momentum       
            t1 = t + M

            # if (P, p) is (0, 0) or (1, 1), I add C to the p = 0 half
            # if (P, p) is (1, 0) or (0, 1), I add C to the p = 1 half
            p1 = abs(P - p)

            # the index (x, y, z) have their minimum (0, 0, 0) and maximum (N_max, E_max, M_max)
            # if an element's (x, y, z) exceed this range, I would ignore it
            # it should be noted (N, E, M)'s values are all positive, so they are always growing bigger when opening brakets
            if x1 <= N_max and y1 <= E_max and t1 <= M_max * 2 and t1 >= 0:

                # (x, y, t, p) -> (x1, y1, t1, p1), I add the old C(in ith matrix) to the new one(in i+1th matrix)
                # it should be noted that I all elements are positive
                matrix_dict[str(i+1)][x1, y1, t1, p1] += matrix_dict[str(i)][x, y, t, p]

                # renew the dict of no-zero index
                if [x1, y1, t1, p1] not in non_zero_dict[str(i+1)]:
                    non_zero_dict[str(i+1)].append([x1, y1, t1, p1])

        # release memory
        non_zero_dict[str(i)] = 0
        matrix_dict[str(i)] = 0
        
        t_1 = time.time()
        
        # there are two methods to check how many non-zero items are stored in matrix
        # I can print the length of non_zero_dict or just use np.nonzero method of numpy
        a = len(non_zero_dict[str(i+1)])
        print(i, "\t", a, "\t", t_1 - t_0)

    return matrix_dict[str(length)]


def V_particle(N_max, E_max, M_max, Elist, Mlist, Plist, Gaplist):
    '''
    Expand generating function and get V matrix for CN parameters

    N_max, E_max, M_max: maximum of particle number, excitation energy, projection of angular momentum
    Elist, Mlist, Plist, Gaplist: list of single particle energy, projection of angular momentum, parity, energy gap
    '''
    # for convinence I use 0 and 1 to represent parity +1 and -1, respectively
    Plist_0_and_1 = [0 if i == 1 else 1 for i in Plist]

    # create a matrix V to store parameters of items as elements
    # note M could be negative so I use M_max * 2 + 1, and it means: value + M_max = index
    V = np.zeros((N_max + 1, E_max + 1, M_max * 2 + 1, 2))

    # before open any braket, the expression is 1 and the only elements in the matrix is [0, 0, M_max, 0]
    # the 4th index (0 or 1) represents parity (+1 or -1)
    V[0, 0, int(M_max), 0] = 1

    # create a dict to store index[N, U, M, P] of non-zero elements after open nth braket
    # the list of indexes have the key string "n"
    # the list after open 0st braket has the key "0" 
    non_zero_dict = {}
    non_zero_dict["0"] = [[0, 0, int(M_max), 0]]
    
    # create a dict to track matrix
    matrix_dict = {}
    matrix_dict["0"] = V.copy()

    # for each excited state (each E), I have a braket with the form (1 + x * y**E * t**M * P), I will open them one by one
    # there might be an E showing up several times, so I use index of Elist
    length = len(Elist)

    # for i = 0, 1, 2, ..., 9
    # Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
    for i in range(length):
        t_0 = time.time()

        E = Elist[i]
        M = Mlist[i]
        P = Plist_0_and_1[i]
        Gap = Gaplist[i]

        # creat a copy of the dicts of last i, with them I will calculate the dicts of i+1
        non_zero_dict[str(i+1)] = non_zero_dict[str(i)].copy()
        matrix_dict[str(i+1)] = matrix_dict[str(i)].copy()

        for [x, y, t, p] in non_zero_dict[str(i)]:
            # the actual operations of opening a braket be like:
            # the first item 1 does not matter
            # the second item x * y**E * t**M * P would multiply every non-zero elements in ith matrix
            
            # particle number
            x1 = x + 1

            # energy
            y1 = y + E
            
            # projection of angular momentum       
            t1 = t + M

            # if (P, p) is (0, 0) or (1, 1), I add C to the p = 0 half
            # if (P, p) is (1, 0) or (0, 1), I add C to the p = 1 half
            p1 = abs(P - p)

            # the index (x, y, z) have their minimum (0, 0, 0) and maximum (N_max, E_max, M_max)
            # if an element's (x, y, z) exceed this range, I would ignore it
            # it should be noted (N, E, M)'s values are all positive, so they are always growing bigger when opening brakets
            if x1 <= N_max and y1 <= E_max and t1 <= M_max * 2 and t1 >= 0:

                # (x, y, t, p) -> (x1, y1, t1, p1), I add the old C(in ith matrix) to the new one(in i+1th matrix)
                # it should be noted that I all elements are positive
                matrix_dict[str(i+1)][x1, y1, t1, p1] += matrix_dict[str(i)][x, y, t, p]

                # renew the dict of no-zero index
                if [x1, y1, t1, p1] not in non_zero_dict[str(i+1)]:
                    non_zero_dict[str(i+1)].append([x1, y1, t1, p1])

        # release memory
        non_zero_dict[str(i)] = 0
        matrix_dict[str(i)] = 0
        
        t_1 = time.time()
        
        # there are two methods to check how many non-zero items are stored in matrix
        # I can print the length of non_zero_dict or just use np.nonzero method of numpy
        a = len(non_zero_dict[str(i+1)])
        print(i, "\t", a, "\t", t_1 - t_0)

    return matrix_dict[str(length)]


def fold_ph(N_max, E_max, M_max, V1, V2):
    '''
    fold V1 and V2 to get V12
    '''
    # V12 has the same shape as V1 and V2
    # I set all elements to 0
    V12 = np.zeros_like(V1)

    for n in range(N_max + 1):
        ta = time.time()

        V1n = V1[n, :, :, :]
        V2n = V2[n, :, :, :]
        
        # count number
        i = 0

        # I use zip to get index of nonzero elements from V1 and V2
        for (e1, m1, p1) in zip(np.nonzero(V1n)[0], np.nonzero(V1n)[1], np.nonzero(V1n)[2]):
            for (e2, m2, p2) in zip(np.nonzero(V2n)[0], np.nonzero(V2n)[1], np.nonzero(V2n)[2]):
                e = e1 + e2
                m = m1 + m2
                p = abs(p1 - p2)
                i += 1
                if e <= E_max and m <= M_max * 2 and m >= 0:
                    V12[n, e, m, p] += V1n[e1, m1, p1] * V2n[e2, m2, p2]

        tb = time.time()
        print("n =", n, "\t", i,  "\t", tb - ta)
    
    return V12


#------------------------------------------------------------------------------------------------------------------------
# Input
#------------------------------------------------------------------------------------------------------------------------
size = 5
Elist = np.random.randint(1, 11, size)
Mlist = np.random.randint(0, 6, size)
Plist = np.random.choice([-1, 1], size)
Gaplist = np.array([1] * size)


#------------------------------------------------------------------------------------------------------------------------
# I limit the number of excited particles
N_max = size

# I limit the size of matrix
E_max = 20000
M_max = 50

#------------------------------------------------------------------------------------------------------------------------
# Run
#------------------------------------------------------------------------------------------------------------------------
print("\n---------------- input ----------------\n")
print("Elist =", Elist)
print("Mlist =", Mlist)
print("Plist =", Plist)
print("Gaplist =", Gaplist)

a = time.time()
print("\n---------------- V1 ----------------\n")
V_1 = V_particle(N_max, E_max, M_max, Elist, Mlist, Plist, Gaplist)

b = time.time()
print("\n---------------- V2 ----------------\n")
V_2 = V_hole(N_max, E_max, M_max, Elist, Mlist, Plist, Gaplist)

c = time.time()
print("\n---------------- fold ----------------\n")
V12 = fold_ph(N_max, E_max, M_max, V_1, V_2)
d = time.time()

print("shape =", V_1.shape, "size =", V_1.size, "bytes =", V_1.nbytes, "t =", b-a)
print("shape =", V_2.shape, "size =", V_2.size, "bytes =", V_2.nbytes, "t =", c-b)
print("shape =", V12.shape, "size =", V12.size, "bytes =", V12.nbytes, "t =", d-c)

lineout = []
lineout.append("shape ="+str(V_1.shape)+"\tsize ="+str(V_1.size)+"\tbytes ="+str(V_1.nbytes)+"\tt ="+str(b-a)+"\n")
lineout.append("shape ="+str(V_2.shape)+"\tsize ="+str(V_2.size)+"\tbytes ="+str(V_2.nbytes)+"\tt ="+str(c-b)+"\n")
lineout.append("shape ="+str(V12.shape)+"\tsize ="+str(V12.size)+"\tbytes ="+str(V12.nbytes)+"\tt ="+str(d-c)+"\n")

f = open("fold.text", "w")
f.writelines(lineout)
f.close()
