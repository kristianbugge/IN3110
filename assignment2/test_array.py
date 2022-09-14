"""
Tests for our array class
"""

from array_class import Array

# 1D tests (Task 4)


def test_str_1d():
    array1 = Array((4,), 1, 2, 3, 4)

    assert str(array1) == "[1, 2, 3, 4]"


def test_add_1d():
    array1 = Array((4,), 2, 2, 3, 3)
    arraySum1 = array1 + 1
    array2 = Array((4,), 2, 0, 4, 1)
    arraySum2 = array1 + array2

    assert str(arraySum1) == "[3, 3, 4, 4]"
    assert str(arraySum2) == "[4, 2, 7, 4]"


def test_sub_1d():
    array1 = Array((4,), 2, 2, 3, 3)
    arraySum1 = array1 - 1
    array2 = Array((4,), 4, 2, 1, 5)
    arraySum2 = array1 - array2

    assert str(arraySum1) == "[1, 1, 2, 2]"
    assert str(arraySum2) == "[-2, 0, 2, -2]"

def test_mul_1d():
    array1 = Array((4,), 1, 2, 3, 4)
    arraySum1 = array1 * 3
    array2 = Array((4,), 10, 2, 30, 100)
    arraySum2 = array1 * array2

    assert str(arraySum1) == "[3, 6, 9, 12]"
    assert str(arraySum2) == "[10, 4, 90, 400]"

def test_eq_1d():
    array1 = Array((4,), 1, 2, 3, 4)
    array2 = Array((4,), 1, 2, 3, 4)
    array3 = Array((4,), 1, 2, 3, 3)

    assert array1 == array2
    assert array1 != array3
    assert array3 != "hei"


def test_same_1d():
    array1 = Array((4,), 1, 2, 3, 4)
    array2 = Array((4,), 1, 2, 3, 4)
    array3 = Array((4,), 1, 2, 3, 3)

    boolArray1 = array1.is_equal(array2)
    boolArray2 = array1.is_equal(array3)
    boolArray3 = array1.is_equal(4)

    assert boolArray1 == Array((4,), True, True, True, True)
    assert boolArray2 == Array((4,), True, True, True, False)
    assert boolArray3 == Array((4,), False, False, False, True)

def test_smallest_1d():
    array1 = Array((4,), -1, 5, -10, 0)
    array2 = Array((4,), -2.5, 0.3, 1.0, -1.0)

    assert array1.min_element() == -10
    assert array2.min_element() == -2.5


def test_mean_1d():
    array1 = Array((4,), 4, 2, 7, 3)
    array2 = Array((4,), 1, 2, 3, 4)
    array3 = Array((3,), 2.5, 3.5, 3.0)

    assert array1.mean_element() == 4
    assert array2.mean_element() != 8
    assert array3.mean_element() == 3.0


# 2D tests (Task 6)


def test_add_2d():
    array1 = Array((3, 2), 1, 2, 3, 0, 1, 2)
    array2 = Array((3, 2), 1, 0, 1, 0, 1, 2)
    arraySum1 = array1 + array2

    assert arraySum1 == Array((3, 2), 2, 2, 4, 0, 2, 4)

def test_mult_2d():
    array1 = Array((3, 2), 1, 2, 3, 0, 1, 2)
    array2 = Array((3, 2), 1, 0, 1000, 0, 1, 2)
    arraySum1 = array1 * array2

    assert arraySum1 == Array((3, 2), 1, 0, 3000, 0, 1, 4)


def test_same_2d():
    array1 = Array((3, 2), 1, 2, 3, 0, 1, 2)
    array2 = Array((3, 2), 1, 0, 1000, 0, 1, 2)

    boolArray1 = array1.is_equal(array2)
    boolArray2 = array1.is_equal(3)

    assert boolArray1 == Array((3, 2), True, False, False, True, True, True)
    assert boolArray2 == Array((3, 2), False, False, True, False, False, False)




def test_mean_2d():
    array1 = Array((3, 2), 1, 2, 3, 9, 1, 2)

    assert array1.mean_element() == 3
    assert array1.mean_element() != 4



if __name__ == "__main__":
    """
    Note: Write "pytest" in terminal in the same folder as this file is in to run all tests
    (or run them manually by running this file).
    Make sure to have pytest installed (pip install pytest, or install anaconda).
    """

    # Task 4: 1d tests
    test_str_1d()
    test_add_1d()
    test_sub_1d()
    test_mul_1d()
    test_eq_1d()
    test_mean_1d()
    test_same_1d()
    test_smallest_1d()

    # Task 6: 2d tests
    test_add_2d()
    test_mult_2d()
    test_same_2d()
    test_mean_2d()
