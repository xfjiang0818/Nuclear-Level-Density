Plist = [1, 1, 1, 1, 1, -1, -1, -1, -1, -1]
#------------------------------------------------------------------------

# for convinence I use 0 and 1 to represent parity 1 and -1, respectively
Plist_0_and_1 = [0 if i == 1 else 1 for i in Plist]

print(Plist_0_and_1)