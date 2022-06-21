import numpy as np
from decimal import Decimal


f = open("Ne20singleparticle.txt", "r")
linein = f.readlines()
f.close()

# delta E = 10 keV

E_list = []
M_list = []

for line in linein:
    l = line.split()
    i = int(l[0])
    E = int(Decimal(float(l[1])).quantize(Decimal("1"), rounding = "ROUND_HALF_UP"))
    M = int(2 * float(l[2]))
    E_list.append(E)
    E_list.append(E)
    M_list.append(M)
    M_list.append(-M)

#print(E_list)
#print(M_list)

# for particle, E(i) = E(Z+i) - E(Z), where the E(Z) is fermi energy
fermi = -12

E_list_new = [i - fermi for i in E_list]

E_particle = E_list_new[10:]
E_hole = [-i for i in E_list_new[:10][::-1]]

#print(E_particle)
#print(E_hole)

M_particle = M_list[10:]
M_hole = [-i for i in M_list[:10][::-1]]
#print(M_particle)
#print(M_hole)


import numpy as np
import time


def generate_matrix_without_sympy(N_max, E_max, M_max, Elist, Mlist, Plist):
    # for convinence I use 0 and 1 to represent parity +1 and -1, respectively
    Plist_0_and_1 = [0 if i == 1 else 1 for i in Plist]

    # create a matrix V to store parameters of items as elements
    # it should be noted E_max and M_max are the maximum values of E and M in matrix V, respectively
    # here we use +1 because we want index begin from 0 and it represent E or M = 0
    V = np.zeros((N_max + 1, E_max + 1, M_max + 1, 2))

    # before open any braket, the expression is 1 and the only elements in the matrix is [0, 0, 0, 0]
    # it should be noted the 4th index (0 or 1) represents parity (+1 or -1) 
    V[0, 0, 0, 0] = 1

    # create a dict to store index[N, U, M, P] of non-zero elements after open nth braket
    # the list of indexes have the key string "n"
    # the list after open 0st braket has the key "0" 
    non_zero_dict = {}
    non_zero_dict["0"] = [[0, 0, 0, 0]]

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

        # creat a copy of the dicts of last i, with them I will calculate the dicts of i+1
        non_zero_dict[str(i+1)] = non_zero_dict[str(i)].copy()
        matrix_dict[str(i+1)] = matrix_dict[str(i)].copy()

        for [x, y, t, p] in non_zero_dict[str(i)]:
            # the actual operations of opening a braket be like:
            # the first item 1 does not matter
            # the second item x * y**E * t**M * P would multiply every non-zero elements in ith matrix
            x1 = x + 1
            y1 = y + E
            t1 = t + M

            # if (P, p) is (0, 0) or (1, 1), I add C to the p = 0 half
            # if (P, p) is (1, 0) or (0, 1), I add C to the p = 1 half
            p1 = abs(P - p)

            # the index (x, y, z) have their minimum (0, 0, 0) and maximum (N_max, E_max, M_max)
            # if an element's (x, y, z) exceed this range, I would not record it
            # it should be noted (N, E, M)'s values are all positive, so they are always growing bigger when opening brakets
            if x1 <= N_max and y1 <= E_max and t1 <= M_max:

                # (x, y, t, p) -> (x1, y1, t1, p1), I add the old C(in ith matrix) to the new one(in i+1th matrix)
                # it should be noted that I all elements are positive
                matrix_dict[str(i+1)][x1, y1, t1, p1] += matrix_dict[str(i)][x, y, t, p]

                # renew the dict of no-zero index
                if [x1, y1, t1, p1] not in non_zero_dict[str(i+1)]:
                    non_zero_dict[str(i+1)].append([x1, y1, t1, p1])
        
        t_1 = time.time()
        
        # there are two methods to check how many non-zero items are stored in matrix
        # I can print the length of non_zero_dict or just use np.nonzero method of numpy  
        # print(len(non_zero_dict[str(i+1)]))
        # print(len(np.nonzero(matrix_dict[str(i+1)])[0]))
        print(i, "\t", len(non_zero_dict[str(i+1)]), "\t", t_1 - t_0)

    return matrix_dict[str(length)]


Elist = E_particle
Mlist = M_particle
Plist = np.random.choice([-1, 1], size = len(Elist))
N_max = 10
E_max = 200
M_max = 50

print(Elist)
print(Mlist)
print(Plist)

a = time.time()
V1 = generate_matrix_without_sympy(N_max, E_max, M_max, Elist, Mlist, Plist)
b = time.time()




print("V1 shape =", V1.shape, "V1 size =", V1.size, "V1 bytes =", V1.nbytes, "t1 =", b-a)
