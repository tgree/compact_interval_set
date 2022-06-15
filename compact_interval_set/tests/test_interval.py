import unittest

from .. import Interval


class TestInterval(unittest.TestCase):
    def test_lt(self):
        i0 = Interval(12,   17)
        i1 = Interval(12,   14)
        i2 = Interval( 3,    7)
        i3 = Interval(13,   20)
        i4 = Interval( 5,  105)

        self.assertFalse(i0 < i0)   # pylint: disable=R0124
        self.assertFalse(i0 < i1)
        self.assertFalse(i0 < i2)
        self.assertTrue(i0 < i3)
        self.assertFalse(i0 < i4)

        self.assertTrue(i1 < i0)
        self.assertFalse(i1 < i1)   # pylint: disable=R0124
        self.assertFalse(i1 < i2)
        self.assertTrue(i1 < i3)
        self.assertFalse(i1 < i4)

        self.assertTrue(i2 < i0)
        self.assertTrue(i2 < i1)
        self.assertFalse(i2 < i2)   # pylint: disable=R0124
        self.assertTrue(i2 < i3)
        self.assertTrue(i2 < i4)

        self.assertFalse(i3 < i0)
        self.assertFalse(i3 < i1)
        self.assertFalse(i3 < i2)
        self.assertFalse(i3 < i3)   # pylint: disable=R0124
        self.assertFalse(i3 < i4)

        self.assertTrue(i4 < i0)
        self.assertTrue(i4 < i1)
        self.assertFalse(i4 < i2)
        self.assertTrue(i4 < i3)
        self.assertFalse(i4 < i4)   # pylint: disable=R0124

    def test_eq(self):
        self.assertTrue(Interval(123, 456) == Interval(123, 456))
        self.assertFalse(Interval(123, 456) == Interval(123, 789))
        self.assertFalse(Interval(123, 124) == Interval(123, 125))
        self.assertFalse(Interval(123, 124) == Interval(456, 457))


if __name__ == '__main__':
    unittest.main()
