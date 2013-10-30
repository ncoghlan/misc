#!/usr/bin/env python3

# The standard slice object has annoying behaviour in a number of cases
#  - a stop index of 0 is interpreted as the start (problem when calculating
#    and an end relative index programmatically)
#  - a stop index of -len(seq) is also interpreted as the start
#  - changing the direction of the slice also requires adjusting the end
#    points, and that can go wrong due to the above two issues

class _FromEnd(int):
    # Bare minimum to make this work
    # Real thing would need much better error handling
    def __add__(self, other):
        return _FromEnd(int(self) + other)
    def __sub__(self, other):
        return _FromEnd(int(self) - other)
    def to_index(self):
        return int(self) if self else None

End = _FromEnd()

def _to_index(idx):
    if idx is None:
        return idx
    try:
        to_index = idx.to_index
    except AttributeError:
        # clamp normal integers at zero
        return max(idx, 0)
    return to_index()

def _parse_slice_args(args):
    num_args = len(args)
    if num_args == 1:
        return (None, _to_index(args[0]), 1)
    elif num_args == 2:
        return (_to_index(args[0]), _to_index(args[1]), 1)
    return  (_to_index(args[0]), _to_index(args[1]), args[2])

def betterslice(*slice_args):
    """Like slice, but indexing from the end uses 'End - idx'

    Negative indices are clamped to zero instead.
    """
    start, stop, step = _parse_slice_args(slice_args)
    return slice(start, stop, step)


class rslice:
    """For args (i, j, k) computes a slice equivalent to [i:j][::-k]

    Negative indices are clamped to zero, use 'End - idx' for end indexing
    Use as_slice() to create a normal slice object given a length
    """

    def __init__(self, *slice_args):
        self.left, self.right, step = _parse_slice_args(slice_args)
        if step < 0:
            raise ValueError("Negative step {} not supported".format(step))
        self.step = -step

    def as_slice(self, length):
        step = self.step
        left = self.left
        right = self.right
        # Given slice args are closed on the left, open on the right,
        # simply negating the step and swapping left and right will introduce
        # an off-by-one error, so we need to adjust the endpoints to account
        # for the open/closed change
        stop = left
        if stop is not None:
            # Closed on the left -> open stop value in the reversed slice
            if step < 0:
                if not stop:
                    # Converting a stop of 0 to -1 does the wrong thing
                    stop -= length
                stop -= 1
            else:
                stop += 1
        start = right
        if start is not None:
            # Open on the right -> closed start value in the reversed slice
            if step < 0:
                if not start:
                    # Converting a start of 0 to -1 does the wrong thing
                    start -= length
                start -= 1
            else:
                start += 1
        return slice(start, stop, self.step)


if __name__ == "__main__":
    # Python 3.4 only - needs subTest support
    import unittest

    class SlicingTestCase(unittest.TestCase):
        min_step = None

        def setUp(self):
            self.data = data = range(10)
            end = len(data) + 1
            begin = -end
            self.left_indices = range(begin, end)
            self.right_indices = range(begin, end)
            if self.min_step is not None:
                min_step = self.min_step
            else:
                min_step = begin
            self.steps = range(min_step, end)

        def _iter_cases(self):
            for i in self.left_indices:
                for j in self.right_indices:
                    for k in self.steps:
                        if not k: continue
                        yield i, j, k


    class TestForwardSlice(SlicingTestCase):

        def test_end_conversion(self):
            for i, j, k in self._iter_cases():
                with self.subTest(i=i, j=j, k=k):
                    start = (End + i) if i < 0 else i
                    stop = (End + j) if j < 0 else j
                    the_slice = betterslice(start, stop, k)
                    self.assertEqual(the_slice.start, i)
                    self.assertEqual(the_slice.stop, j)
                    self.assertEqual(the_slice.step, k)
                    expected = self.data[i:j:k]
                    actual = self.data[the_slice]
                    self.assertEqual(actual, expected, the_slice)

        def test_integer_clamping(self):
            for i, j, k in self._iter_cases():
                with self.subTest(i=i, j=j, k=k):
                    start = 0 if i < 0 else i
                    stop = 0 if j < 0 else j
                    the_slice = betterslice(i, j, k)
                    self.assertEqual(the_slice.start, start)
                    self.assertEqual(the_slice.stop, stop)
                    self.assertEqual(the_slice.step, k)
                    expected = self.data[start:stop:k]
                    actual = self.data[the_slice]
                    self.assertEqual(actual, expected, the_slice)

    class TestReverseSlice(SlicingTestCase):
        min_step = 1

        def test_no_negative_step(self):
            with self.assertRaises(ValueError):
                rslice(0, 1, -1)

        def test_end_conversion(self):
            data_len = len(self.data)
            for i, j, k in self._iter_cases():
                with self.subTest(i=i, j=j, k=k):
                    start = (End + i) if i < 0 else i
                    stop = (End + j) if j < 0 else j
                    expected = self.data[i:j][::-k]
                    the_slice = rslice(start, stop, k).as_slice(data_len)
                    actual = self.data[the_slice]
                    self.assertEqual(actual, expected, the_slice)

        def test_integer_clamping(self):
            data_len = len(self.data)
            for i, j, k in self._iter_cases():
                with self.subTest(i=i, j=j, k=k):
                    start = 0 if i < 0 else i
                    stop = 0 if j < 0 else j
                    expected = self.data[start:stop][::-k]
                    the_slice = rslice(i, j, k).as_slice(data_len)
                    actual = self.data[the_slice]
                    self.assertEqual(actual, expected, the_slice)

    unittest.main()
