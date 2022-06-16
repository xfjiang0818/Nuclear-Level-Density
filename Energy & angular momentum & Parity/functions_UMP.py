import numpy as np
import sympy
import time


def generate_matrix_without_sympy(N_max, I, M, Elist, Mlist, Plist):
    # for convinence I use 0 and 1 to represent parity +1 and -1, respectively
    Plist_0_and_1 = [0 if i == 1 else 1 for i in Plist]

    # create a matrix V to store parameters of items as elements
    # it should be noted I and M are the maxium values of E and M in matrix V, respectively
    # here we use +1 because we want index begin from 0 and it represent E or M = 0
    V = np.zeros((N_max + 1, I + 1, M + 1, 2))

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

            # (x, y, t, p) -> (x1, y1, t1, p1), I add the old C(in ith matrix) to the new one(in i+1th matrix)
            # it should be noted that I all elements are positive
            matrix_dict[str(i+1)][x1, y1, t1, p1] += matrix_dict[str(i)][x, y, t, p]

            # renew the dict of no-zero index
            if [x1, y1, t1, p1] not in non_zero_dict[str(i+1)]:
                non_zero_dict[str(i+1)].append([x1, y1, t1, p1])
    
    return matrix_dict[str(length)]


def generating_function(Elist, Mlist, Plist):
    expression = "1"
    for i in range(len(Elist)):
        E = str(Elist[i])
        M = str(Mlist[i])
        P = str(Plist[i])
        if P == "1":
            expression += "*(1+x*y**" + E + "*t**" + M + ")"
        elif P == "-1":
            expression += "*(1+x*y**" + E + "*t**" + M + "* neg)"
        else:
            print("P should be 1 or -1")
    return sympy.sympify(expression)


def get_index(line):
    indexlist = ["x", "y", "t", "neg"]
    if line == ["1"]:
        C = 1
        N = 0
        U = 0
        M = 0
        P = 0
    else:
        # calculate parameter C
        if line[0] in indexlist:
            C = 1
        else:
            C = int(line[0])
            line = line[1:]
        # calculate number index N
        if "x" not in line:
            N = 0
        elif "x" == line[-1]:
            N = 1
        else:
            x_index = line.index("x")
            if line[x_index + 1] in indexlist:
                N = 1
            else:
                N = int(line[x_index + 1])
        # calculate energy index U
        if "y" not in line:
            U = 0
        elif "y" == line[-1]:
            U = 1
        else:
            y_index = line.index("y")
            if line[y_index + 1] in indexlist:
                U = 1
            else:
                U = int(line[y_index + 1])
        # calculate angular momentum projection index M
        if "t" not in line:
            M = 0
        elif "t" == line[-1]:
            M = 1
        else:
            t_index = line.index("t")
            if line[t_index + 1] in indexlist:
                M = 1
            else:
                M = int(line[t_index + 1])
        # calculate parity index P
        if "neg" not in line:
            P = 0
        elif "neg" == line[-1]:
            P = 1
        else:
            neg_index = line.index("neg")
            if line[neg_index + 1] in indexlist:
                P = 1
            elif int(line[neg_index + 1]) % 2 == 0:
                P = 0
            else:
                P = 1

    return [N, U, M, P, C]


def generate_matrix_from_sympy(N_max, I, M, generating_function):
    # expression is calculated by sympy.expand
    expanded_expression = str(sympy.expand(generating_function)).split(" + ")
    
    # creat a matrix to store every items of the expression
    V = np.zeros((N_max + 1, I + 1, M + 1, 2))
    
    for l in expanded_expression:
        # change every items in the expession string into a convenient form
        # slice operation will be performed on the l_item
        l = l.split("*")
        l_item = []
        for i in l:
            if i != "":
                l_item.append(i)
        #print(l_item)
        N = get_index(l_item)[0]
        U = get_index(l_item)[1]
        M = get_index(l_item)[2]
        P = get_index(l_item)[3]
        C = get_index(l_item)[4]

        #print(C, N, U, M, P)
        # for every item in the expression, I add it to the matrix
        V[N][U][M][P] = C
    return V


#------------------------------------------------------------------------------------------------------------------------
# Input
#------------------------------------------------------------------------------------------------------------------------
Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Mlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Plist = [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, 1]
#Elist = [1, 2, 3, 4, 5]
#Mlist = [1, 2, 3, 4, 5]
#Plist = [1, 1, 1, -1, -1]

N_max = len(Elist)
I = sum(Elist)
M = sum(Mlist)
#N_max = 5
#I = 15
#M = 15

#------------------------------------------------------------------------------------------------------------------------
# Run
#------------------------------------------------------------------------------------------------------------------------
a = time.time()
V1 = generate_matrix_without_sympy(N_max, I, M, Elist, Mlist, Plist)
b = time.time()
x, y, t, neg = sympy.symbols("x y t neg")
gf = generating_function(Elist, Mlist, Plist)
V2 = generate_matrix_from_sympy(N_max, I, M, gf)
c = time.time()

print("V1 shape =", V1.shape, "V1 size =", V1.size, "V1 bytes =", V1.nbytes, "t1 =", b-a)
print("V2 shape =", V2.shape, "V2 size =", V2.size, "V2 bytes =", V2.nbytes, "t2 =", c-b)

#------------------------------------------------------------------------------------------------------------------------
# Test
#------------------------------------------------------------------------------------------------------------------------
# Now I check whether these two methods get the same expression or not
# It should be noticed that there is a big difference between V1 and V2
# In V1, two elements with different parity P could have same (N, U, M), because they are calculated during expansion process
# I can calculate (N, U, M, 0) - (N, U, M, 1) and get the right items of expanded expression
# In V2, only one element in (N, U, M, 0) & (N, U, M, 1) can be non-zero, because it is determined after expansion process
# I choose the non-zero element (if possible) and attach corresponding sgin to it to get the right item of expanded expression

# V1
# I get the index matrix with P = +1 by type V1[:, :, :, 0]
#print(V1[:, :, :, 0].shape)
# I get the index matrix with P = -1 by type V1[:, :, :, 1]
#print(V1[:, :, :, 1].shape)
# The elements are non-negative integer in both partial matrix and I can get the right parameter by subtraction
V1_final = V1[:, :, :, 0] - V1[:, :, :, 1]

# V2
# I get the index matrix with P = +1 by type V2[:, :, :, 0]. I note it contains all the items with positive parameters
#print(V2[:, :, :, 0].shape)
# I get the index matrix with P = -1 by type V2[:, :, :, 1]. I note it contains all the items with negetive parameters
#print(V2[:, :, :, 1].shape)
# The elements are non-negative integer in both partial matrix and I can get the right parameter by subtraction
V2_final = V2[:, :, :, 0] - V2[:, :, :, 1]

print(V1[5, 24, 24, :])
print(V2[5, 24, 24, :])
print((V1_final == V2_final).all())