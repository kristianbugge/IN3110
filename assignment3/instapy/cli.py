"""Command-line (script) interface to instapy"""

import argparse
import sys
from skimage.transform import resize
import numpy as np
from PIL import Image

import instapy

from instapy.io import read_image, write_image, display
from instapy.python_filters import python_color2gray, python_color2sepia
from instapy.numpy_filters import numpy_color2gray, numpy_color2sepia
from instapy.numba_filters import numba_color2gray, numba_color2sepia

def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
) -> None:
    """Run the selected filter"""
    # load the image from a file
    image = read_image(file)
    shape = np.asarray(np.shape(image))
    #if shape != 1:
    #    Image.resize(image, (shape[0] * scale, shape[1] * scale))
    filters = {
        "python_color2gray": python_color2gray,
        "numpy_color2gray": numpy_color2gray,
        "numba_color2gray": numba_color2gray,
        "python_color2sepia": python_color2sepia,
        "numpy_color2sepia": numpy_color2sepia,
        "numba_color2sepia": numba_color2sepia
    }

    filter_function= implementation+"_"+filter
    filtered = filters[filter_function](image)

    if out_file:
        # save the file
        write_image(filtered, out_file)
    else:
        # not asked to save, display it instead
        display(filtered)


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments"""
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", help="The output filename")


    # Add required arguments
    parser.add_argument("-i", "--implementation", help="python, numpy or numba")
    parser.add_argument("-f", "--filter", help="color2gray or color2sepia")
    parser.add_argument("-sc", "--scale", help="Scale to resize your picture with")

    # parse arguments and call run_filter
    args = parser.parse_args()
    run_filter(args.file, args.out, args.implementation, args.filter, args.scale)
