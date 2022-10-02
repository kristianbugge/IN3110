"""
Timing our filter implementations.

Can be executed as `python3 -m instapy.timing`

For Task 6.
"""
import time
import instapy
import io
from typing import Callable
import numpy as np
from instapy import get_filter
from PIL import Image

from instapy.io import read_image, write_image
from instapy.python_filters import python_color2gray, python_color2sepia
from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
from instapy.numba_filters import numba_color2gray, numba_color2sepia


def time_one(filter_function: Callable, arguments, calls: int = 3) -> float:
    """Return the time for one call

    When measuring, repeat the call `calls` times,
    and return the average.

    Args:
        filter_function (callable):
            The filter function to time
        *arguments:
            Arguments to pass to filter_function
        calls (int):
            The number of times to call the function,
            for measurement
    Returns:
        time (float):
            The average time (in seconds) to run filter_function(*arguments)
    """
    # run the filter function `calls` times
    # return the _average_ time of one call
    totalTime = 0
    for i in range(calls):
        start = time.time()
        filter_function(arguments)
        end = time.time()
        totalTime += (end - start)

    avgTime = totalTime/calls

    return avgTime



def make_reports(filename: str = "test/rain.jpg", calls: int = 3):
    """
    Make timing reports for all implementations and filters,
    run for a given image.

    Args:
        filename (str): the image file to use
    """
    # load the image
    image = read_image(filename)
    # print the image name, width, height
    Image.fromarray(image).show()
    shape = np.asarray(np.shape(image))
    print("Timing performed using", filename, ": ", shape[0],"x",shape[1],"\n")


    #A dictionary so i dont have to call string objects
    filters = {
        "python_color2gray": python_color2gray,
        "numpy_color2gray": numpy_color2gray,
        "numba_color2gray": numba_color2gray,
        "python_color2sepia": python_color2sepia,
        "numpy_color2sepia": numpy_color2sepia,
        "numba_color2sepia": numba_color2sepia
    }
    # iterate through the filters
    filter_names = ["color2gray", "color2sepia"]
    for filter_name in filter_names:
        # get the reference filter function
        if (filter_name == "color2gray"):
            # time the reference implementation
            reference_time = time_one(python_color2gray, image, 3)

        elif (filter_name == "color2sepia"):
            reference_time = time_one(python_color2sepia, image, 3)
        print(
            f"Reference (pure Python) filter time {filter_name}: {reference_time:.3}s ({calls=})"
        )
        # iterate through the implementations
        implementations = ["numpy", "numba"]
        for implementation in implementations:

            filter = str(implementation+"_"+filter_name)
            # time the filter
            filter_time = time_one(filters[filter], image, 3)
            # compare the reference time to the optimized time
            speedup = reference_time/filter_time
            print(
                f"Timing: {implementation} {filter_name}: {filter_time:.3}s ({speedup=:.2f}x)"
            )
            if implementation == "numba":
                print("\n")


if __name__ == "__main__":
    # run as `python -m instapy.timing`
    make_reports()
