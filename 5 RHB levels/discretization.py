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


#------------------------------------------------------------------------------------------------------------------------
# Input
#------------------------------------------------------------------------------------------------------------------------
unit = 0.01
#fermi_energy = -9.3928
fermi_energy = -7.7457

#------------------------------------------------------------------------------------------------------------------------
# Run
#------------------------------------------------------------------------------------------------------------------------
spl = sp_levels("Fe56p.txt")
p_levels, h_levels = ph_levels(spl, fermi_energy, unit)[0], ph_levels(spl, fermi_energy, unit)[1]


#------------------------------------------------------------------------------------------------------------------------
# Output
#------------------------------------------------------------------------------------------------------------------------
print("\n----------------------- single particle levels -----------------------")
for i in spl: print(i)
print("\n--------------------------- particle levels ---------------------------")
for i in p_levels: print(i)
print("\np levels number = ", len(p_levels))
print("\n----------------------------- hole levels -----------------------------")
for i in h_levels: print(i)
print("\nh levels number = ", len(h_levels))



