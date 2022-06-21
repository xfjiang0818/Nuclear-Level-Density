import numpy as np
import sympy


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


def generate_matrix_from_sympy(generating_function):
    # expression is calculated by sympy.expand
    expanded_expression = str(sympy.expand(generating_function)).split(" + ")
    
    # creat a matrix to store every items of the expression
    V = np.zeros((13, 79, 79, 2))
    
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

        if N == 5 and U == 24 and M == 24:
            print(l)
            print("C =", C, "P =", P, "M =", M, "N =", N, "U =", U)

        
        # for every item in the expression, I add it to the matrix
        V[N][U][M][P] += C
    return V


#------------------------------------------------------------------------
Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Mlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
Plist = [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1, 1]

#------------------------------------------------------------------------
x, y, t, neg = sympy.symbols("x y t neg")
gf = generating_function(Elist, Mlist, Plist)
#print(sympy.expand(gf))

#------------------------------------------------------------------------
V = generate_matrix_from_sympy(gf)
#print(V[5][24])
print(V.shape)
