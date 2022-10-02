"""numpy implementation of image filters"""

from typing import Optional
import numpy as np
from instapy.io import read_image, write_image
from PIL import Image

def numpy_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    colour_weights = [0.07, 0.72, 0.21]
    #Makes numpy arrays for each colour channel and adds them to to make the out-array
    gray_image = np.empty_like(image)
    weight = (image[:, :, 0]) * colour_weights[2] + (image[:, :, 1]) *colour_weights[1]+ (image[:, :, 2]) * colour_weights[0]

    gray_image[:, :, 0] = weight
    gray_image[:, :, 1] = weight
    gray_image[:, :, 2] = weight


    gray_image = gray_image.astype("uint8")
    #write_image(gray_image, "test/rain_grayscaleNp.jpg")

    return gray_image


def numpy_color2sepia(image: np.array, k: Optional[float] = 1) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
        k (float): amount of sepia filter to apply (optional)

    The amount of sepia is given as a fraction, k=0 yields no sepia while
    k=1 yields full sepia.

    (note: implementing 'k' is a bonus task,
    you may ignore it for Task 9)

    Returns:
        np.array: sepia_image
    """

    #if not 0 <= k <= 1:
        # validate k (optional)
        #raise ValueError(f"k must be between [0-1], got {k=}")

    sepia_image = np.empty_like(image)

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

    sepia_image[:, :, 0] = red
    sepia_image[:, :, 1] = green
    sepia_image[:, :, 2] = blue

    sepia_image = sepia_image.astype("uint8")
    #write_image(sepia_image, "test/rain_sepiaNp.jpg")

    # Return image (make sure it's the right type!)
    return sepia_image
