import numpy as np
import sympy
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
        print("i =", i, "\t\tnumber =", len(non_zero_dict[str(i+1)]), "\t\tDelta t =", t_1 - t_0)

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
        N, U, M, P, C = 0, 0, 0, 0, 1
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


def generate_matrix_from_sympy(N_max, E_max, M_max, generating_function):
    # expression is calculated by sympy.expand
    expanded_expression = str(sympy.expand(generating_function)).split(" + ")
    
    # creat a matrix to store every items of the expression
    V = np.zeros((N_max + 1, E_max + 1, M_max + 1, 2))
    
    for l in expanded_expression:
        # change every items in the expession string into a convenient form
        # slice operation will be performed on the l_item
        l = l.split("*")
        l_item = []
        for i in l:
            if i != "":
                l_item.append(i)
        #print(l_item)
        indexlist = get_index(l_item).copy()
        N, U, M, P, C = indexlist[0], indexlist[1], indexlist[2], indexlist[3], indexlist[4]

        # I add items in the expression to the matrix
        if N <= N_max and U <= E_max and M <= M_max:
            V[N][U][M][P] += C
    return V


#------------------------------------------------------------------------------------------------------------------------
# Input
#------------------------------------------------------------------------------------------------------------------------
Elist = np.random.randint(1, 11, size = 20)
Mlist = np.random.randint(0, 6, size = 20)
Plist = np.random.choice([-1, 1], size = 20)
print(Elist)
print(Mlist)
print(Plist)

#------------------------------------------------------------------------------------------------------------------------
# I limit the number of excited particles
N_max = 50

# I limit the size of matrix
E_max = 100
M_max = 50

#------------------------------------------------------------------------------------------------------------------------
# Run
#------------------------------------------------------------------------------------------------------------------------
a = time.time()
V1 = generate_matrix_without_sympy(N_max, E_max, M_max, Elist, Mlist, Plist)
b = time.time()

x, y, t, neg = sympy.symbols("x y t neg")
gf = generating_function(Elist, Mlist, Plist)
V2 = generate_matrix_from_sympy(N_max, E_max, M_max, gf)
c = time.time()

print("V1 shape =", V1.shape, "V1 size =", V1.size, "V1 bytes =", V1.nbytes, "t1 =", b-a)
print("V2 shape =", V2.shape, "V2 size =", V2.size, "V2 bytes =", V2.nbytes, "t2 =", c-b)

#------------------------------------------------------------------------------------------------------------------------
# Test
#------------------------------------------------------------------------------------------------------------------------
# Now I check whether these two methods get the same expression or not
# It should be noticed that two elements with different parity P could have same (N, U, M)
# The elements are non-negative integer in both partial matrix and I can get the right parameter by subtractions
# I can calculate (N, U, M, 0) - (N, U, M, 1) and get the right items of expanded expression

# V1
V1_final = V1[:, :, :, 0] - V1[:, :, :, 1]

# V2
V2_final = V2[:, :, :, 0] - V2[:, :, :, 1]

print((V1_final == V2_final).all())