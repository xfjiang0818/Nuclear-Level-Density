import math


def read_levels():
    f = open("levels.txt", "r")
    linein = f.readlines()
    f.close()
    level_list = []
    for line in linein:
        l = str(line)
        id = int(l[1:4])
        E = float(l[27:35])
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

levels = read_levels()
for i in levels:
    print(i)


fermi = -9.3874







def dizcretization(unit, Elist, Gaplist):
    pass


unit = 0.01