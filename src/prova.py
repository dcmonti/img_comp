import time
import multiprocessing as mp
import numpy as np
from scipy.fft import dctn, idctn, fft2, ifft2
import cv2

mat = np.random.randint(255, size=(1000000)).reshape((1000,1000))

sci_start = time.time()

fft_sci = fft2(mat, norm='ortho', workers=-1)
sci_mat = ifft2(fft_sci, norm='ortho', workers=-1)
sci_end = time.time()-sci_start

cv_start = time.time()

fft_num = np.fft.fft2(mat, norm='ortho')
mat = np.fft.ifft2(fft_num, norm='ortho')
cv_end = time.time() - cv_start
print(sci_end)
print(cv_end)


print("Number of processors: ", mp.cpu_count())


