"""pure Python implementation of image filters"""

import numpy as np
from instapy.io import read_image, write_image
def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    colour_weights = [0.07, 0.72, 0.21]

    # iterate through the pixels, and apply the grayscale transform
    shape =  np.asarray((np.shape(image)))
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            weight = image[i][j][0] * colour_weights[2] + image[i][j][1] * colour_weights[1] + image[i][j][2] * colour_weights[0]
            gray_image[i][j] = (weight, weight, weight)

    #write_image(gray_image, "test/rain_grayscalePy.jpg")
    gray_image = gray_image.astype("uint8")
    #gray_image.save("rain_grayscalePy.jpg")


    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    shape =  np.asarray((np.shape(image)))
    # Iterate through the pixels
    # applying the sepia matrix

    sepia_matrix = [
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ]
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            pixel_red = image[i][j][0] * sepia_matrix[0][0] + image[i][j][1] * sepia_matrix[0][1] + image[i][j][2] * sepia_matrix[0][2]
            if(pixel_red > 255):
                pixel_red = 255

            pixel_green = image[i][j][0] * sepia_matrix[1][0] + image[i][j][1] * sepia_matrix[1][1] + image[i][j][2] * sepia_matrix[1][2]
            if(pixel_green > 255):
                pixel_green = 255


            pixel_blue = image[i][j][0] * sepia_matrix[2][0] + image[i][j][1] * sepia_matrix[2][1] + image[i][j][2] * sepia_matrix[2][2]
            if(pixel_blue > 255):
                pixel_blue = 255


            sepia_image[i][j] = (pixel_red, pixel_green, pixel_blue)

    #write_image(sepia_image, "test/rain_sepiaPy.jpg")
    sepia_image = sepia_image.astype("uint8")

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image
