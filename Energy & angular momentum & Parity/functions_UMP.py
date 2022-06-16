import numpy as np
import sympy
import time


#------------------------------------------------------------------------
N_max = 10
I = 55
M = 55

Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Mlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#------------------------------------------------------------------------


def generate_matrix_without_sympy(N_max, I, M, Elist, Mlist):
    # create a matrix to store parameters of items as elements
    V = np.zeros((N_max + 1, I + 1, M + 1))
    # before open any braket, the expression is 1 and the only elements in the matrix is [0, 0]
    V[0, 0, 0] = 1

    # create a dict to store index[N,U] of no-zero elements after open nth braket
    # the list of indexes have the key string "n"
    no_zero_dict = {}
    # the list after open 0st braket has the key "0" 
    no_zero_dict["0"] = [[0, 0, 0]]

    # create a dict to track matrix
    matrix_dict = {}
    matrix_dict["0"] = V.copy()

    # for every E, I have a braket with form (1 + x * y**E), I will open them one by one
    # there might be an E showing up several times, so I use index of Elist
    length = len(Elist)
    # for Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], i = 0, 1, 2, ..., 9
    for i in range(length):
        E = Elist[i]
        M = Mlist[i]

        # creat a copy of the dicts of last i, with them I will calculate the dicts of i+1
        no_zero_dict[str(i+1)] = no_zero_dict[str(i)].copy()
        matrix_dict[str(i+1)] = matrix_dict[str(i)].copy()

        for [x, y, t] in no_zero_dict[str(i)]:
            # the actual operations of opening a braket be like:
            # the first item 1 do not matter
            # the second item x * y**E would multiply every no-zero elements in ith matrix
            x1 = x + 1
            y1 = y + E
            t1 = t + M
            # (x, y, t) -> (x + 1, y + E, t + M), I add the old C(in ith matrix) to the new one(in i+1th matrix)
            matrix_dict[str(i+1)][x1, y1, t1] += matrix_dict[str(i)][x, y, t]
            # renew the dict of no-zero index
            if [x1, y1, t1] not in no_zero_dict[str(i+1)]:
                no_zero_dict[str(i+1)].append([x1, y1, t1])

    return matrix_dict[str(length)]


#------------------------------------------------------------------------
x, y, t = sympy.symbols("x y t")
generation_function = \
(1 + x * y * t) * (1 + x * y**2 * t**2) * (1 + x * y**3 * t **3) * (1 + x * y**4 * t**4) * (1 + x * y**5 * t**5) * \
(1 + x * y**6 * t**6) * (1 + x * y**7 * t**7) * (1 + x * y**8 * t**8) * (1 + x * y**9 * t**9) * (1 + x * y**10 * t**10)
print(sympy.expand(generation_function))
#------------------------------------------------------------------------


def generate_matrix_from_sympy(generation_function):
    # expression is calculated by sympy.expand
    expanded_expression = str(sympy.expand(generation_function)).split(" + ")
    
    # creat a matrix to store every items of the expression
    V = np.zeros((11, 56, 56))
    
    for l in expanded_expression:
        # change every items in the expession string into a convenient form
        # slice operation will be performed on the l_item
        l = l.split("*")
        l_item = []
        for i in l:
            if i != "":
                l_item.append(i)
        # item 1
        if l_item == ["1"]:
            C = 1
            N = 0
            U = 0
            M = 0
        else:
            # calculate parameter C
            if l_item[0] == "t":
                C = 1
            else:
                C = int(l_item[0])
                l_item = l_item[1:]

            # calculate angular momentum index M
            l_item = l_item[1:]
            if l_item[0] == "x":
                M = 1
            else:
                M = int(l_item[0])
                l_item = l_item[1:]

            # calculate number index N
            l_item = l_item[1:]
            if l_item[0] == "y":
                N = 1
            else:
                N = int(l_item[0])
                l_item = l_item[1:]

            # calculate energy index U
            if l_item[-1] == "y":
                U = 1
            else:
                U = int(l_item[-1])

        # print(C, N, U, M)
        # for every item in the expression, I add it to the matrix
        V[N][U][M] = C
    return V


a = time.time()
V1 = generate_matrix_without_sympy(N_max, I, M, Elist, Mlist)
b = time.time()
V2 = generate_matrix_from_sympy(generation_function)
c = time.time()

print(V1 == V2)
print("t1 =", b-a)
print("t2 =", c-b)