import math
import time

import numpy as np
from scipy.fft import dctn
from timeit import default_timer as timer

def my_dct_1d(arr):
	vec_size = arr.shape[0]

	dct = np.empty(shape=vec_size)

	cj = math.sqrt(2.0) / math.sqrt(vec_size)
	for idx in range(0, vec_size):
		sum = 0

		for pos in range(0, vec_size):
			sum += arr[pos] * math.cos((2.0 * pos + 1.0) * idx * np.pi / (2.0 * vec_size))

		# normalize
		if idx == 0:
			dct[idx] = (1.0 / math.sqrt(vec_size)) * sum

		else:
			dct[idx] = cj * sum
	return dct


def my_dct2_2d(matrix):
	matrix_size = matrix.shape[0]
	# init result matrix
	dct = np.empty(shape=matrix.shape)

    # dct + normalization
	tmp_dct = np.empty(shape=matrix.shape)
	for i in range(0, matrix_size):
		tmp_dct[i, :] = my_dct_1d(matrix[i, :])

	for j in range(0, matrix_size):
		dct[:, j] = my_dct_1d(tmp_dct[:, j])
	return dct

def bench(size):
	matrix = np.random.randint(255, size=(size, size))
	start = timer()
	for _ in range(0, 100):
		dctn(matrix, type=2, norm='ortho', workers=-1)
	end = timer() - start
	return end / 100


if __name__ == "__main__":
	sizes = [i for i in range(5, 100, 5)]
	new_sizes = [i for i in range(100, 1001, 100)]
	sizes.extend(new_sizes)
	scipy_times = [bench(size) for size in sizes]
	out = f"{sizes[0]} {scipy_times[0]}"
	for i in range(1, len(sizes)):
		out = f'{out}\n{sizes[i]} {scipy_times[i]}'
	f = open('scipy.txt', 'w')
	f.write(out)