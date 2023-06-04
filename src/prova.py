from dct import my_dct2_2d
import math
import time

import numpy as np
from scipy.fft import dctn


matrix =np.array(
    [
             [231, 32, 233, 161, 24, 71, 140, 245],
             [247, 40, 248, 245, 124, 204, 36, 107],
             [234, 202, 245, 167, 9, 217, 239, 173],
             [193, 190, 100, 167, 43, 180, 8, 70],
             [11, 24, 210, 177, 81, 243, 8, 112],
             [97, 195, 203, 47, 125, 114, 165, 181],
             [193, 70, 174, 167, 41, 30, 127, 245],
             [87, 149, 57, 192, 65, 129, 178, 228],
        ]
)
matrix = np.random.randint(255, size=(300, 300))

start = time.time()
my_dct = my_dct2_2d(matrix)
end = time.time() -start
print(end)
start = time.time_ns()
lib_dct = dctn(matrix, type=2, norm='ortho', workers=-1)
end = time.time_ns() -start
print(end)
for i in range(0,matrix.shape[0]):
    for j in range(0, matrix.shape[0]):
        delta = abs(my_dct[i][j] - lib_dct[i][j] < 0.00001)
        if not delta:
            print(i, j)