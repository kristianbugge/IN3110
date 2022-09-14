"""
Array class for assignment 2
"""

class Array:

    def __init__(self, shape, *values):
        """Initialize an array of 1-dimensionality. Elements can only be of type:

        - int
        - float
        - bool

        Make sure the values and shape are of the correct type.

        Make sure that you check that your array actually is an array, which means it is homogeneous (one data type).

        Args:
            shape (tuple): shape of the array as a tuple. A 1D array with n elements will have shape = (n,).
            *values: The values in the array. These should all be the same data type. Either int, float or boolean.

        Raises:
            TypeError: If "shape" or "values" are of the wrong type.
            ValueError: If the values are not all of the same type.
            ValueError: If the number of values does not fit with the shape.
        """

        # Check if the values are of valid types
        if isinstance(values[0], (int, float, bool)):
            datatype = type(values[0])
        else:
            raise TypeError("values parameters must be int, float or boolean")
        for value in values:
            if type(value) != datatype:
                raise ValueError("Values must be of same type")

        if isinstance(shape, tuple) and all(isinstance(n, int) for n in shape):
            self.shape = shape
        else:
            raise TypeError("Shape must be a tuple of ints")

        # Check that the amount of values corresponds to the shape
        self.dim = len(shape)

        if self.dim == 1:
            elementCap = shape[0]
        else:
            elementCap = shape[0] * shape[1]
        if elementCap != len(values):
            raise ValueError("Number of values do not fit with shape")


        # Set instance attributes
        self.values = values

    #Return element in array at index of argument key (int)
    def __getitem__(self, key):
        if self.dim == 1:
            return self.values[key]
        else:
            return self.values[self.shape[1] * key]



    def __str__(self):
        """Returns a nicely printable string representation of the array.

        Returns:
            stringOut: A string representation of the array.

        """
        stringOut = "["
        if self.dim == 1: #1d
            for i in range(len(self.values)):
                stringOut += str(self.values[i])
                if (i != len(self.values) - 1):
                    stringOut += ", "
                else:
                    stringOut += "]"
        else: #2d
            rows = self.shape[0]
            columns = self.shape[1]
            index = 0 #to iterate on correct index in 2d array
            for i in range(rows):
                stringOut += "["
                for j in range(columns):
                    stringOut += str(self.values[j + index])
                    if (j != columns - 1):
                        stringOut += ", "
                index += columns
                stringOut += "]"

                if(i != rows -1):
                    #stringOut += ", "
                    stringOut += "\n"
                else:
                    stringOut += "]"
        return stringOut


    def __add__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """

        # check that the method supports the given arguments (check for data type and shape of array)
        # if the array is a boolean you should return NotImplemented
        if isinstance(other, Array):
            if self.shape != other.shape:
                return ValueError("Shapes of arrays do not match")
            if type(self.values[0]) != type(other.values[0]): #we know if the first elements have matching datatypes, all else also match
                raise TypeError("Datatypes of arrays do not match")
            else:
                outTuple = ()
                for i in range(len((self.values))):
                    sum = self.values[i] + other.values[i]
                    outTuple += (sum,)

                return Array(self.shape, *outTuple)

        elif isinstance(other, (int, float)):
            outTuple = () #tuple to fill new list
            for i in range(len(self.values)):
                sum = self.values[i] + other
                outTuple += (sum,)

            return Array(self.shape, *outTuple)

        else:
            return NotImplemented


    def __radd__(self, other):
        """Element-wise adds Array with another Array or number.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to add element-wise to this array.

        Returns:
            Array: the sum as a new array.

        """
        return self.__add__(other)

    def __sub__(self, other):
        """Element-wise subtracts an Array or number from this Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to subtract element-wise from this array.

        Returns:
            Array: the difference as a new array.

        """
        if isinstance(other, Array):
            if self.shape != other.shape:
                return ValueError("Shapes of arrays do not match")
            if type(self.values[0]) != type(other.values[0]): #we know if the first elements have matching datatypes, all else also match
                raise TypeError("Datatypes of arrays do not match")
            else:
                outTuple = ()
                for i in range(len((self.values))):
                    diff = self.values[i] - other.values[i]
                    outTuple += (diff,)

                return Array(self.shape, *outTuple)

        elif isinstance(other, (int, float)):
            outTuple = () #tuple to fill new list
            for i in range(len(self.values)):
                diff = self.values[i] - other
                outTuple += (diff,)

            return Array(self.shape, *outTuple)

        else:
            return NotImplemented

    def __rsub__(self, other):
        """Element-wise subtracts this Array from a number or Array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number being subtracted from.

        Returns:
            Array: the difference as a new array.

        """
        return self.__sub__(other)

    def __mul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        if isinstance(other, Array):
            if self.shape != other.shape:
                return ValueError("Shapes of arrays do not match")
            if type(self.values[0]) != type(other.values[0]): #we know if the first elements have matching datatypes, all else also match
                raise TypeError("Datatypes of arrays do not match")
            else:
                outTuple = ()
                for i in range(len(self.values)):
                    product = self.values[i] * other.values[i]
                    outTuple += (product,)

                return Array(self.shape, *outTuple)

        elif isinstance(other, (int, float)):
            outTuple = () #tuple to fill new list
            for i in range(len(self.values)):
                product = self.values[i] * other
                outTuple += (product,)

            return Array(self.shape, *outTuple)

        else:
            return NotImplemented

    def __rmul__(self, other):
        """Element-wise multiplies this Array with a number or array.

        If the method does not support the operation with the supplied arguments
        (specific data type or shape), it should return NotImplemented.

        Args:
            other (Array, float, int): The array or number to multiply element-wise to this array.

        Returns:
            Array: a new array with every element multiplied with `other`.

        """
        return self.__mul__(other)

    def __eq__(self, other):
        """Compares an Array with another Array.

        If the two array shapes do not match, it should return False.
        If `other` is an unexpected type, return False.

        Args:
            other (Array): The array to compare with this array.

        Returns:
            bool: True if the two arrays are equal (identical). False otherwise.

        """
        if isinstance(other, Array):
            if self.shape != other.shape:
                return False

            for i in range(len(self.values)):
                if(self.values[i] != other.values[i]):
                    return False

            return True
        else:
            return False


    def is_equal(self, other):
        """Compares an Array element-wise with another Array or number.

        If `other` is an array and the two array shapes do not match, this method should raise ValueError.
        If `other` is not an array or a number, it should return TypeError.

        Args:
            other (Array, float, int): The array or number to compare with this array.

        Returns:
            Array: An array of booleans with True where the two arrays match and False where they do not.
                   Or if `other` is a number, it returns True where the array is equal to the number and False
                   where it is not.

        Raises:
            ValueError: if the shape of self and other are not equal.

        """
        outTuple = ()
        if isinstance(other, Array):
            if self.shape != other.shape:
                raise ValueError("Parameter is array with non matching shape")
            else:
                for i in range(len(self.values)):
                    outBool = self.values[i] == other.values[i]
                    outTuple += (outBool,)
        elif isinstance(other, (int, float)):
            for i in range(len(self.values)):
                outBool = self.values[i] == other
                outTuple += (outBool,)
        else:
            raise TypeError("parameter must be an array or number")

        return Array(self.shape, *outTuple)

    def min_element(self):
        """Returns the smallest value of the array.

        Only needs to work for type int and float (not boolean).

        Returns:
            float: The value of the smallest element in the array.

        """

        if isinstance(self.values[0], (int, float)):
            min = self.values[0]
            for i in self.values:
                if (i < min):
                    min = i
            return float(min)
        else:
            raise TypeError("Array must contain numeric elements")

    def mean_element(self):
        """Returns the mean value of an array

        Only needs to work for type int and float (not boolean).

        Returns:
            float: the mean value
        """

        if isinstance(self.values[0], (int, float)):
            sum = 0
            for i in self.values:
                sum += i

            return float(sum / len(self.values))
        else:
            raise TypeError("Array must contain numeric elements")
