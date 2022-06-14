import numpy as np
import sympy


x, y = sympy.symbols("x y")
generation_function = \
(1 + x * y) * (1 + x * y**2) * (1 + x * y**3) * (1 + x * y**4) * (1 + x * y**5) * \
(1 + x * y**6) * (1 + x * y**7) * (1 + x * y**8) * (1 + x * y**9) * (1 + x * y**10)

def generate_matrix_from_sympy(generation_function):
    # expression is calculated by sympy.expand
    expanded_expression = str(sympy.expand(generation_function)).split(" + ")
    
    # creat a matrix to store every items of the expression
    V = np.zeros((11,56))
    
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
        else:
            # calculate parameter C
            if l_item[0] == "x":
                C = 1
            else:
                C = int(l_item[0])
                l_item = l_item[1:]
            # calculate number index N
            if l_item[1] == "y":
                N = 1
                l_item = l_item[1:]
            else:
                N = int(l_item[1])
                l_item = l_item[2:]
            # calculate energy index U
            if l_item[-1] == "y":
                U = 1
            else:
                U = int(l_item[-1])
        # print(C, N, U)
        # for every item in the expression, I add it to the matrix
        V[N][U] = C
    return V

V = generate_matrix_from_sympy(generation_function)
#print(V[5][24])
print(V)
