"""numba-optimized filters"""
from numba import jit
import numpy as np
from instapy.io import read_image, write_image

def numba_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = calculateGray(image).astype("uint8")

    #write_image(gray_image, "test/rain_grayscaleNb.jpg")

    return gray_image

@jit(nopython = True)
def calculateGray(image: np.array) -> np.array:
    out_image = np.empty_like(image)
    colour_weights = [0.07, 0.72, 0.21]
    shape =  np.asarray((np.shape(image)))

    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            weight = image[i][j][0] * colour_weights[2] + image[i][j][1] * colour_weights[1] + image[i][j][2] * colour_weights[0]
            out_image[i][j] = (weight, weight, weight)

    return out_image

def numba_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = calculateSepia(image).astype("uint8")

    #write_image(sepia_image, "test/rain_sepiaNb.jpg")

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image

@jit(nopython = True)
def calculateSepia(image: np.array) -> np.array:
    out_image = np.empty_like(image)

    # define sepia matrix (optional: with `k` tuning parameter for bonus task 13)
    sepia_matrix = [
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ]

    # HINT: For version without adaptive sepia filter, use the same matrix as in the pure python implementation
    # use Einstein sum to apply pixel transform matrix
    # Apply the matrix filter
    # Check which entries have a value greater than 255 and set it to 255 since we can not display values bigger than 255
    pixel_red = image[:, :, 0] * sepia_matrix[0][0] + image[:, :, 1] * sepia_matrix[0][1] + image[:, :, 2] * sepia_matrix[0][2]
    red = np.minimum(255, pixel_red)

    pixel_green = image[:, :, 0] * sepia_matrix[1][0] + image[:, :, 1] * sepia_matrix[1][1] + image[:, :, 2] * sepia_matrix[1][2]
    green = np.minimum(255, pixel_green)

    pixel_blue = image[:, :, 0] * sepia_matrix[2][0] + image[:, :, 1] * sepia_matrix[2][1] + image[:, :, 2] * sepia_matrix[2][2]
    blue = np.minimum(255, pixel_blue)

    out_image[:, :, 0] = red
    out_image[:, :, 1] = green
    out_image[:, :, 2] = blue

    return out_image
