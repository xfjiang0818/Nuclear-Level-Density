import sympy


Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Mlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Plist = [1, 1, 1, 1, 1, -1, -1, -1, -1, -1]


def generating_function(Elist, Mlist, Plist):
    expression = "1"
    for i in range(len(Elist)):
        E = str(Elist[i])
        M = str(Mlist[i])
        P = str(Plist[i])
        if P == "1":
            expression += "*(1+x*y**" + E + "*t**" + M + ")"
        elif P == "-1":
            expression += "*(1-x*y**" + E + "*t**" + M + ")"
        else:
            print("P should be 1 or -1")
    return sympy.sympify(expression)


print(generating_function(Elist, Mlist, Plist))