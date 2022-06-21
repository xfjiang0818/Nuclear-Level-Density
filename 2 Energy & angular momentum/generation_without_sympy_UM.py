import numpy as np


N_max = 10
I = 55
M = 55

Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
Mlist = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]


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
len = len(Elist)
# for Elist = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], i = 0, 1, 2, ..., 9
for i in range(len):
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

#print(matrix_dict[str(len)])
print(matrix_dict[str(len)][5][24])
