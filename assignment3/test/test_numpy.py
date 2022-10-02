from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
from instapy.io import read_image, write_image, random_image
import numpy as np

def test_color2gray():
    # Generate random image to use for tests
    in_image = random_image(320, 180).astype("uint8")

    # run color2gray
    out_image = numpy_color2gray(in_image)

    # Get the shapes to use for tests
    in_shape = np.asarray(np.shape(in_image))
    out_shape = np.asarray(np.shape(out_image))
    write_image(out_image, "test/test_color2gray")
    # check that the result has the right shape, type
    assert in_shape[0] == out_shape[0] and in_shape[1] == out_shape[1]

    # random choice of 2 pixels in the random Image to use for tests
    randX1 = np.random.randint(in_shape[0])
    randY1 = np.random.randint(in_shape[1])

    randX2 = np.random.randint(in_shape[0])
    randY2 = np.random.randint(in_shape[1])

    # check types
    assert type(in_image[randX1][randY1]) == type(out_image[randX1][randY1])

    # assert uniform r,g,b values
    expectedVal1 = in_image[randX1][randY1][0] * 0.21 + in_image[randX1][randY1][1] * 0.72 + in_image[randX1][randY1][2] * 0.07
    expectedVal2 = in_image[randX2][randY2][0] * 0.21 + in_image[randX2][randY2][1] * 0.72 + in_image[randX2][randY2][2] * 0.07

    assert int(expectedVal1) == int(out_image[randX1][randY1][0])
    assert int(expectedVal1) == int(out_image[randX1][randY1][1])
    assert int(expectedVal1) == int(out_image[randX1][randY1][2])

    assert int(expectedVal2) == int(out_image[randX2][randY2][0])
    assert int(expectedVal2) == int(out_image[randX2][randY2][1])
    assert int(expectedVal2) == int(out_image[randX2][randY2][2])


def test_color2sepia(image):
    # Generate random image to use for tests
    in_image = random_image(320, 180)

    # run color2sepia
    out_image = numpy_color2sepia(in_image)

    # Get the shapes to use for tests
    in_shape = np.asarray(np.shape(in_image))
    out_shape = np.asarray(np.shape(out_image))
    write_image(out_image, "test/test_color2sepia")
    # check that the result has the right shape, type
    assert in_shape[0] == out_shape[0] and in_shape[1] == out_shape[1]

    # random choice of 2 pixels in the random Image to use for tests
    randX1 = np.random.randint(in_shape[0])
    randY1 = np.random.randint(in_shape[1])

    randX2 = np.random.randint(in_shape[0])
    randY2 = np.random.randint(in_shape[1])

    # check types
    assert type(in_image[randX1][randY1]) == type(out_image[randX1][randY1])
    assert type(in_image[randX2][randY2]) == type(out_image[randX2][randY2])
    # verify some individual pixel samples
    # according to the sepia matrix
    sepia_matrix = [
        [ 0.393, 0.769, 0.189],
        [ 0.349, 0.686, 0.168],
        [ 0.272, 0.534, 0.131],
    ]

    expectedRed1 = in_image[randX1][randY1][0] * sepia_matrix[0][0] + in_image[randX1][randY1][1] * sepia_matrix[0][1] + in_image[randX1][randY1][2] * sepia_matrix[0][2]
    if(expectedRed1 > 255):
        expectedRed1 = 255

    expectedGreen1 = in_image[randX1][randY1][0] * sepia_matrix[1][0] + in_image[randX1][randY1][1] * sepia_matrix[1][1] + in_image[randX1][randY1][2] * sepia_matrix[1][2]
    if(expectedGreen1 > 255):
        expectedGreen1 = 255

    expectedBlue1 = in_image[randX1][randY1][0] * sepia_matrix[2][0] + in_image[randX1][randY1][1] * sepia_matrix[2][1] + in_image[randX1][randY1][2] * sepia_matrix[2][2]
    if(expectedBlue1 > 255):
        expectedBlue1 = 255

    assert int(expectedRed1) == out_image[randX1][randY1][0]
    assert int(expectedGreen1) == out_image[randX1][randY1][1]
    assert int(expectedBlue1) == out_image[randX1][randY1][2]

    expectedRed2 = in_image[randX2][randY2][0] * sepia_matrix[0][0] + in_image[randX2][randY2][1] * sepia_matrix[0][1] + in_image[randX2][randY2][2] * sepia_matrix[0][2]
    if(expectedRed2 > 255):
        expectedRed2 = 255

    expectedGreen2 = in_image[randX2][randY2][0] * sepia_matrix[1][0] + in_image[randX2][randY2][1] * sepia_matrix[1][1] + in_image[randX2][randY2][2] * sepia_matrix[1][2]
    if(expectedGreen2 > 255):
        expectedGreen2 = 255

    expectedBlue2 = in_image[randX2][randY2][0] * sepia_matrix[2][0] + in_image[randX2][randY2][1] * sepia_matrix[2][1] + in_image[randX2][randY2][2] * sepia_matrix[2][2]
    if(expectedBlue2 > 255):
        expectedBlue2 = 255

    assert int(expectedRed2) == out_image[randX2][randY2][0]
    assert int(expectedGreen2) == out_image[randX2][randY2][1]
    assert int(expectedBlue2) == out_image[randX2][randY2][2]
