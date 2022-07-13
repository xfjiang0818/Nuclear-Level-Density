import numpy as np
import time
import multiprocessing as mp


def sp_levels(name):
    '''
    get single particle levels from RHB-Triaxial-v1 output
    the output is a list of sets: energy(float), gap(float), mz(float), P(int, 1 or -1)
    '''
    f = open(name, "r")
    linein = f.readlines()
    f.close()
    level_list = []
    for line in linein:
        l = str(line)
        id = int(l[1:4])
        # get single particle energy
        E = float(l[27:35])
        # get gap energy
        D = abs(float(l[37:44]))
        # get angular momentum projection
        if id % 2 == 1:
            mz = +float(l[89:91])/2
        else:
            mz = -float(l[89:91])/2
        # get parity
        if l[82] in ["s", "d", "g", "i", "l", "n"]:
            P = int(1)
        elif l[82] in ["p", "f", "h", "k", "m"]:
            P = -int(1)
        level_list.append((E, D, mz, P))
        #print("id =", id, "\tE =", E, "\tD =", D, "\tmz =", mz, "\tp =", P)
    levels = sorted(level_list)
    return levels


def ph_levels(levels, fermi_energy, unit):
    '''
    1. get particle levels and hole levels with single particle levels and fermi energy
    2. get quasi-particle energy
    3. energy discretization with unit
    '''
    p_list = []
    h_list = []
    for level in levels:
        # read levels information
        E = level[0]
        D = level[1]
        mz = level[2]
        P = level[3]
        # excitation energy
        epsilon = E - fermi_energy
        # quasi-particle energy
        quasi_epsilon = (epsilon ** 2 + D ** 2) ** 0.5
        # if above fermi level, add it to particle levels
        # if below or equal to fermi level, add it to hole levels
        if epsilon > 0:
            # energy discretization
            nu = int(0.5 + epsilon / unit)
            mu = int(0.5 + quasi_epsilon / unit)
            # single particle energy, gap energy, mz, parity, quasi-particle energy
            p_list.append((nu, mu, mz, P))
        else:
            epsilon = abs(epsilon)
            nu = int(0.5 + epsilon / unit)
            mu = int(0.5 + quasi_epsilon / unit)
            h_list.append((nu, mu, mz, P))
    p_levels = sorted(p_list)
    h_levels = sorted(h_list)
    return p_levels, h_levels


def V_hole(N_max, E_max, M_max, h_levels):
    '''
    Expand generating function and get V matrix for CN parameters

    N_max, E_max, M_max: maximum of particle number, excitation energy, projection of angular momentum
    h_levels: list of nu, mu, mz, P 
    '''
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
    length = len(h_levels)

    # for i = 0, 1, 2, ..., 9
    # Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
    for i in range(length):
        t_0 = time.time()

        # element in h_levels is a set (nu, mu, mz, P)
        nu = h_levels[i][0]
        mu = h_levels[i][1]
        mz = int(h_levels[i][2] * 2)

        # for convinence I use 0 and 1 to represent parity +1 and -1, respectively
        if h_levels[i][3] == 1:
            P = 0
        else:
            P = 1

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
                y1 = mu
            else:
                y1 = y + nu
            
            # projection of angular momentum       
            t1 = t + mz

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
        print("i = ", i, "\t\tLen = ", a, "\t\tT = ", round(t_1 - t_0, 2))

    return matrix_dict[str(length)]


#------------------------------------------------------------------------------------------------------------------------
# Input
#------------------------------------------------------------------------------------------------------------------------
unit = 0.1
fermi_energy = -9.3928

N_max = 30
E_max = 2000
M_max = 50


#------------------------------------------------------------------------------------------------------------------------
# Run
#------------------------------------------------------------------------------------------------------------------------
spl = sp_levels("Fe56n.txt")
p_levels, h_levels = ph_levels(spl, fermi_energy, unit)[0], ph_levels(spl, fermi_energy, unit)[1]

print("\n----------------------- single particle levels -----------------------")
for i in spl: print(i)
print("\n--------------------------- particle levels ---------------------------")
for i in p_levels: print(i)
print("\np levels number = ", len(p_levels))
print("\n----------------------------- hole levels -----------------------------")
for i in h_levels: print(i)
print("\nh levels number = ", len(h_levels))


print("\n---------------- V1 ----------------\n")
a = time.time()
V_1 = V_hole(N_max, E_max, M_max, h_levels[:21])
b = time.time()
print("shape =", V_1.shape, "size =", V_1.size, "bytes =", V_1.nbytes, "t =", b-a)


#------------------------------------------------------------------------------------------------------------------------
# Output
#------------------------------------------------------------------------------------------------------------------------

