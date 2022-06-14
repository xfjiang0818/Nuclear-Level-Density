import numpy as np

# One Dimension Array
my_array_0 = np.array([1, 2, 3, 4, 5])
print(my_array_0)
print(my_array_0[0])
print(my_array_0[-1])

my_array_0[0] = 10
print(my_array_0)

my_array_1 = np.zeros((5)) 
print(my_array_1)

my_array_2 = np.ones((5)) 
print(my_array_2)

my_array_random = np.random.random((5))
print(my_array_random)


# Two Dimension Array
my_2d_array_0 = np.zeros((2, 3)) 
print(my_2d_array_0)

my_2d_array_1 = np.ones((2, 4))
print(my_2d_array_1)

my_2d_array_2 = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(my_2d_array_2)
print(my_2d_array_2.shape)
# print(2,1)
print(my_2d_array_2[1][0])
print(my_2d_array_2[1, 0])
# print row(2)
print(my_2d_array_2[1, :])
# print column(1)
print(my_2d_array_2[:, 0])


# Operations
a = np.array([[1.0, 2.0], [3.0, 4.0]]) 
b = np.array([[5.0, 6.0], [7.0, 8.0]])
# Check what they are
print(a)
print(b)
# Do something now
sum = a + b 
difference = a - b 
product = a * b 
quotient = a / b 
print("Sum = \n", sum) 
print("Difference = \n", difference)
print("Product = \n", product)
print("Quotient = \n", quotient)
matrix_product = a.dot(b)
print("matrix_product = \n", matrix_product)