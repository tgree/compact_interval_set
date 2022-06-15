import math
import unittest

from .. import Set, Interval


def is_sorted(elems):
    if len(elems) < 2:
        return True
    for i in range(len(elems) - 1):
        if elems[i + 1] < elems[i]:
            return False
    return True


class TestSet(unittest.TestCase):
    def test_is_sorted(self):
        self.assertTrue(is_sorted([1, 2, 3, 4]))
        self.assertTrue(is_sorted([1, 2, 2, 3, 4]))
        self.assertTrue(is_sorted([]))
        self.assertTrue(is_sorted([1]))
        self.assertTrue(is_sorted([1, 1]))
        self.assertFalse(is_sorted([2, 1]))
        self.assertFalse(is_sorted([1, 2, 3, 4, 3]))

    def test_set_elems_sorted_and_reduced(self):
        s = Set()
        self.assertTrue(is_sorted(s.elems))

        s = Set([Interval(1, 11)])
        self.assertTrue(is_sorted(s.elems))

        s = Set([Interval(1, 11),
                 Interval(1, 6)])
        self.assertTrue(is_sorted(s.elems))
        self.assertEqual(s.elems, [Interval(1, 11),
                                   ])

        s = Set([Interval(10, 20),
                 Interval( 2,  4),
                 Interval( 5, 22),
                 Interval( 6,  9),
                 Interval( 6,  8),
                 Interval(12, 13),
                 Interval( 1,  2),
                 ])
        self.assertTrue(is_sorted(s.elems))
        self.assertEqual(s.elems, [Interval(1,  4),
                                   Interval(5, 22),
                                   ])

    def test_complement(self):
        s0 = Set()
        s1 = Set([Interval(-math.inf, math.inf)])
        self.assertEqual(~s0, s1)
        self.assertEqual(s0, ~s1)
        self.assertEqual( s0 | ~s0, s1)
        self.assertEqual(~s0 |  s0, s1)
        self.assertEqual( s1 | ~s1, s1)
        self.assertEqual(~s1 |  s1, s1)
        self.assertEqual( s0 |  s1, s1)

        s2 = Set([Interval( 0, 10),
                  Interval(20, 30),
                  Interval(40, 50),
                  ])
        s3 = Set([Interval(-math.inf,        0),
                  Interval(       10,       20),
                  Interval(       30,       40),
                  Interval(       50, math.inf),
                  ])
        self.assertEqual(~s2, s3)
        self.assertEqual(s2, ~s3)
        self.assertEqual( s2 | ~s2, s1)
        self.assertEqual(~s2 |  s2, s1)
        self.assertEqual( s3 | ~s3, s1)
        self.assertEqual(~s3 |  s3, s1)
        self.assertEqual( s2 |  s3, s1)

        s4 = Set([Interval(20, 30)])
        s5 = Set([Interval(-math.inf, 20),
                  Interval(30, math.inf),
                  ])
        self.assertEqual(~s4, s5)
        self.assertEqual(s4, ~s5)

        s6 = Set([Interval(-math.inf, 20)])
        s7 = Set([Interval(20, math.inf)])
        self.assertEqual(~s6, s7)
        self.assertEqual(s6, ~s7)

    def test_difference(self):
        s0 = Set()
        s1 = Set([Interval(  0,  10),
                  Interval( 20,  30),
                  Interval( 40,  50),
                  Interval( 60,  70),
                  Interval( 80,  90),
                  Interval(100, 110),
                  Interval(200, 210),
                  ])
        s2 = Set([Interval(10, 15),     # No overlap.
                  Interval(19, 31),     # Full overlap.
                  Interval(45, 48),     # Split.
                  Interval(65, 70),     # Back overlap.
                  Interval(75, 85),     # Front overlap.
                  ])
        s3 = Set([Interval(  0,  10),
                  Interval( 40,  45),
                  Interval( 48,  50),
                  Interval( 60,  65),
                  Interval( 85,  90),
                  Interval(100, 110),
                  Interval(200, 210),
                  ])
        self.assertEqual(s1 - s1, s0)
        self.assertEqual(s1 - s2, s3)

    def test_intersection(self):
        s1 = Set([Interval(  0,  10),
                  Interval( 20,  30),
                  Interval( 40,  50),
                  Interval( 60,  70),
                  Interval( 80,  90),
                  Interval(100, 110),
                  Interval(200, 210),
                  ])
        s2 = Set([Interval(10, 15),     # No overlap.
                  Interval(19, 31),     # Full overlap.
                  Interval(45, 48),     # Split.
                  Interval(65, 75),     # Back overlap.
                  Interval(75, 85),     # Front overlap.
                  ])
        s3 = Set([Interval(20, 30),
                  Interval(45, 48),
                  Interval(65, 70),
                  Interval(80, 85),
                  ])
        self.assertEqual(s1 & s2, s3)

    def test_gaps(self):
        s1 = Set([Interval(  0,  10),
                  Interval( 20,  30),
                  Interval( 40,  50),
                  Interval( 60,  70),
                  Interval( 80,  90),
                  Interval(100, 110),
                  Interval(200, 210),
                  ])
        s2 = Set([Interval(-1000, 1000)])
        s3 = Set([Interval(-1000,    0),
                  Interval(   10,   20),
                  Interval(   30,   40),
                  Interval(   50,   60),
                  Interval(   70,   80),
                  Interval(   90,  100),
                  Interval(  110,  200),
                  Interval(  210, 1000),
                  ])
        self.assertEqual(s2 - s1, s3)

    def test_insert(self):
        s1 = Set([Interval(  0,  10),
                  Interval( 20,  30),
                  Interval( 40,  50),
                  ])
        s2 = s1 | Set([Interval(60, 70)])
        s1.insert(Interval(60, 70))
        self.assertEqual(s1, s2)

        s2 |= Set([Interval(10, 20)])
        s1.insert(Interval(10, 20))
        self.assertEqual(s1, s2)

        s2 |= Set([Interval(-20, -10)])
        s1.insert(Interval(-20, -10))
        self.assertEqual(s1, s2)

        s2 |= Set([Interval(35, 37)])
        s1.insert(Interval(35, 37))
        self.assertEqual(s1, s2)

        s2 |= Set([Interval(-1000, 40)])
        s1.insert(Interval(-1000, 40))
        self.assertEqual(s1, s2)

        s2 |= Set([Interval(60, math.inf)])
        s1.insert(Interval(60, math.inf))
        self.assertEqual(s1, s2)

        s2 |= Set([Interval(-math.inf, 60)])
        s1.insert(Interval(-math.inf, 60))
        self.assertEqual(s1, s2)

        self.assertEqual(s1, Set([Interval(-math.inf, math.inf)]))

    def test_contains(self):
        s1 = Set([Interval(-math.inf,      -10),
                  Interval(        0,       10),
                  Interval(       20,       30),
                  Interval(       40,       50),
                  Interval(       60, math.inf),
                  ])
        self.assertIn(-math.inf, s1)
        self.assertIn(-1000000, s1)
        self.assertIn(-11, s1)
        self.assertNotIn(-10, s1)
        self.assertNotIn(-5, s1)
        self.assertNotIn(-1, s1)
        self.assertIn(0, s1)
        self.assertIn(5.5, s1)
        self.assertIn(9, s1)
        self.assertNotIn(10, s1)
        self.assertNotIn(15, s1)
        self.assertNotIn(19, s1)
        self.assertIn(20, s1)
        self.assertIn(25, s1)
        self.assertIn(29, s1)
        self.assertNotIn(30, s1)
        self.assertNotIn(35, s1)
        self.assertNotIn(39, s1)
        self.assertIn(40, s1)
        self.assertIn(45, s1)
        self.assertIn(49, s1)
        self.assertNotIn(50, s1)
        self.assertNotIn(55, s1)
        self.assertNotIn(59, s1)
        self.assertIn(60, s1)
        self.assertIn(1000000, s1)
        self.assertIn(math.inf, s1)

        s2 = Set()
        self.assertNotIn(-math.inf, s2)
        self.assertNotIn(      -10, s2)
        self.assertNotIn(        0, s2)
        self.assertNotIn(       10, s2)
        self.assertNotIn( math.inf, s2)

        s3 = Set([Interval(        0,       10),
                  Interval(       20,       30),
                  Interval(       40,       50),
                  ])
        self.assertNotIn(-1, s3)
        self.assertIn(0, s3)
        self.assertIn(5.5, s3)
        self.assertIn(9, s3)
        self.assertNotIn(10, s3)
        self.assertNotIn(15, s3)
        self.assertNotIn(19, s3)
        self.assertIn(20, s3)
        self.assertIn(25, s3)
        self.assertIn(29, s3)
        self.assertNotIn(30, s3)
        self.assertNotIn(35, s3)
        self.assertNotIn(39, s3)
        self.assertIn(40, s3)
        self.assertIn(45, s3)
        self.assertIn(49, s3)
        self.assertNotIn(50, s3)

    def test_iter(self):
        s1 = Set([Interval(-math.inf,      -10),
                  Interval(        0,       10),
                  Interval(       20,       30),
                  Interval(       40,       50),
                  Interval(       60, math.inf),
                  ])
        for e1, e2 in zip(s1, s1.elems):
            self.assertIs(e1, e2)

    def test_subscript(self):
        s1 = Set([Interval(-math.inf,      -10),
                  Interval(        0,       10),
                  Interval(       20,       30),
                  Interval(       40,       50),
                  Interval(       60, math.inf),
                  ])
        self.assertIs(s1[0], s1.elems[0])
        self.assertIs(s1[1], s1.elems[1])
        self.assertIs(s1[2], s1.elems[2])
        self.assertIs(s1[3], s1.elems[3])
        self.assertIs(s1[4], s1.elems[4])

    def test_len(self):
        s1 = Set([Interval(-math.inf,      -10),
                  Interval(        0,       10),
                  Interval(       20,       30),
                  Interval(       40,       50),
                  Interval(       60, math.inf),
                  ])
        self.assertEqual(len(s1), 5)

        self.assertEqual(len(Set()), 0)


if __name__ == '__main__':
    unittest.main()
