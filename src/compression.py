from scipy.fft import dctn, idctn, fft2, ifft2
import numpy as np
from PIL import Image

def reshape_matrix(matrix, tile_size):
    height, width = matrix.shape
    reshaped_matrix = matrix.reshape(
        height // tile_size,
        tile_size,
        width // tile_size,
        tile_size
    )
    reshaped_matrix = reshaped_matrix.swapaxes(1,2)
    return reshaped_matrix


def reverse_reshape_matrix(matrix, tile_size):
    height_tile, width_tile, _, _ = matrix.shape
    reshaped_matrix = matrix.swapaxes(1,2)

    reshaped_matrix = reshaped_matrix.reshape(
        height_tile * tile_size,
        width_tile * tile_size
    )
    return reshaped_matrix


def freq_cut_mask(f, d):
    # create matrix with 0 after d antidiagonal
    mask = np.ones((f,f))
    for row in range(0, f):
        for col in range(f - 1, d - 1 - row, -1):
            mask[row, col] = 0
    return mask


def compress(matrix, f, d, alg):
    # remove pixel if not f multiple
    x_limit = matrix.shape[0] - (matrix.shape[0] % f)
    y_limit = matrix.shape[1] - (matrix.shape[1] % f)
    matrix = matrix[0:x_limit, 0:y_limit]

    #compression and decompression
    comp_matrix = jpeg_compression(matrix, f, d) if alg == 'dct' else fft_compression(matrix, f, d)
    #save image
    return comp_matrix


def jpeg_compression(matrix, f, d):
    # reshape matrix in f*f tiles (4 dims: height/f, width/f, f, f)
    matrix = reshape_matrix(matrix, f)

    # apply dct on each f*f tile
    matrix = dctn(matrix, type=2, norm='ortho', axes=(2,3), workers=-1)

    # create mask for setting lower tile value to 0
    mask = freq_cut_mask(f, d)

    # multiply each tile for mask in order to cut lower frequencies
    matrix = np.einsum('ijkz,kz->ijkz',matrix,mask)

    # inverse dct
    matrix = idctn(matrix, type=2, norm='ortho', axes=(2,3), workers=-1)

    #return to normal shape
    matrix = reverse_reshape_matrix(matrix, f)

    # round value to int
    matrix = np.rint(matrix)
    return matrix


def fft_compression(matrix, f, d):
    # reshape matrix in f*f tiles (4 dims: height/f, width/f, f, f)
    matrix = reshape_matrix(matrix, f)

    # apply dct on each f*f tile
    matrix = fft2(matrix, norm='ortho', axes=(2,3), workers=-1)

    # create mask for setting lower tile value to 0
    mask = freq_cut_mask(f, d)

    # multiply each tile for mask in order to cut lower frequencies
    matrix = np.einsum('ijkz,kz->ijkz',matrix,mask)

    # inverse dct and reshape to original shape
    matrix = ifft2(matrix, norm='ortho', axes=(2,3), workers=-1).real
    matrix = reverse_reshape_matrix(matrix, f)

    # round value to int
    matrix = np.rint(matrix)

    return matrix