import numpy as np
import time


def diophantine_nd_nonnegative(a, b):
  n = len ( a )
  x = np.empty ( [ 0, n ] )
  j = 0
  k = 0
  r = b
  y = np.zeros ( [ 1, n ] )
  while ( True ):
    r = b - sum ( a[0:j] * y[0,0:j] )
    if ( j < n ):
      y[0,j] = np.floor ( r / a[j] )
      j = j + 1
    else:
      if ( r == 0 ):
        x = np.append ( x, y, axis = 0 )
      while ( 0 < j ):
        if ( 0 < y[0,j-1] ):
          y[0,j-1] = y[0,j-1] - 1
          break
        j = j - 1
      if ( j == 0 ):
        break
  return x


n = 10
a = list(range(1, n + 1))
b = n
start = time.time()
result = diophantine_nd_nonnegative(a, b)
end = time.time()
Num = len(result)
for l in result:
  lnew = [int(i) for i in l]
  print(lnew)
print("Number =", Num)