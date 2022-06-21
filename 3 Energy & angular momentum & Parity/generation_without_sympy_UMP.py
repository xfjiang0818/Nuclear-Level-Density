import numpy as np


#------------------------------------------------------------------------
N_max = 10
I = 55
M = 55

Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Mlist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Plist = [1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
#------------------------------------------------------------------------

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


V1 = matrix_dict[str(length)]
print(V1)
print(V1.shape)
