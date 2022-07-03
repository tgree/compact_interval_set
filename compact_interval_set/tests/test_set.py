import math
import unittest

from .. import Set


class TestSet(unittest.TestCase):
    def test_insert(self):
        s = Set()
        self.assertEqual(s.points, [])

        s = Set([10, 20])
        self.assertTrue(s.points, [10, 20])

        s = Set([10, 20,
                 0,  1])
        self.assertEqual(s.points, [0, 1, 10, 20])

        s = Set([10, 20,
                 0,  10])
        self.assertEqual(s.points, [0, 20])

        s = Set([10, 20,
                 0,  15])
        self.assertEqual(s.points, [0, 20])

        s = Set([10, 20,
                 10, 15])
        self.assertEqual(s.points, [10, 20])

        s = Set([10, 20,
                 10, 20])
        self.assertEqual(s.points, [10, 20])

        s = Set([10, 20,
                 10, 25])
        self.assertEqual(s.points, [10, 25])

        s = Set([10, 20,
                 15, 25])
        self.assertEqual(s.points, [10, 25])

        s = Set([10, 20,
                 20, 25])
        self.assertEqual(s.points, [10, 25])

        s = Set([10, 20,
                 21, 25])
        self.assertEqual(s.points, [10, 20, 21, 25])

        s = Set([10, 20,
                 5,  25])
        self.assertEqual(s.points, [5, 25])

        s = Set([10,        20,
                 -math.inf, 30])
        self.assertEqual(s.points, [-math.inf, 30])

        s = Set([10, 20,
                 0,  math.inf])
        self.assertEqual(s.points, [0, math.inf])

        s = Set([10, 20,
                 -math.inf,  math.inf])
        self.assertEqual(s.points, [-math.inf, math.inf])

        s = Set([0,   math.inf,
                 -10, -5,
                 25,  math.inf])
        self.assertEqual(s.points, [-10, -5, 0, math.inf])

        s = Set([-math.inf, 0,
                 5,         10,
                 -math.inf, -15])
        self.assertEqual(s.points, [-math.inf, 0, 5, 10])

        s = Set([-math.inf, math.inf,
                 5,         10])
        self.assertEqual(s.points, [-math.inf, math.inf])

    def test_complement(self):
        s0 = Set()
        s1 = Set([-math.inf, math.inf])
        self.assertEqual(~s0, s1)
        self.assertEqual(s0, ~s1)
        self.assertEqual( s0 | ~s0, s1)
        self.assertEqual(~s0 |  s0, s1)
        self.assertEqual( s1 | ~s1, s1)
        self.assertEqual(~s1 |  s1, s1)
        self.assertEqual( s0 |  s1, s1)

        s2 = Set([0,  10,
                  20, 30,
                  40, 50,
                  ])
        s3 = Set([-math.inf, 0,
                  10,        20,
                  30,        40,
                  50,        math.inf,
                  ])
        self.assertEqual(~s2, s3)
        self.assertEqual(s2, ~s3)
        self.assertEqual( s2 | ~s2, s1)
        self.assertEqual(~s2 |  s2, s1)
        self.assertEqual( s3 | ~s3, s1)
        self.assertEqual(~s3 |  s3, s1)
        self.assertEqual( s2 |  s3, s1)

        s4 = Set([20, 30])
        s5 = Set([-math.inf, 20,
                  30,        math.inf,
                  ])
        self.assertEqual(~s4, s5)
        self.assertEqual(s4, ~s5)

        s6 = Set([-math.inf, 20])
        s7 = Set([20,        math.inf])
        self.assertEqual(~s6, s7)
        self.assertEqual(s6, ~s7)

    def test_difference(self):
        s0 = Set()
        s1 = Set([0,   10,
                  20,  30,
                  40,  50,
                  60,  70,
                  80,  90,
                  100, 110,
                  200, 210,
                  ])
        s2 = Set([10, 15,     # No overlap.
                  19, 31,     # Full overlap.
                  45, 48,     # Split.
                  65, 70,     # Back overlap.
                  75, 85,     # Front overlap.
                  ])
        s3 = Set([0,   10,
                  40,  45,
                  48,  50,
                  60,  65,
                  85,  90,
                  100, 110,
                  200, 210,
                  ])
        self.assertEqual(s1 - s1, s0)
        self.assertEqual(s1 - s2, s3)

    def test_intersection(self):
        s1 = Set([0,   10,
                  20,  30,
                  40,  50,
                  60,  70,
                  80,  90,
                  100, 110,
                  200, 210,
                  ])
        s2 = Set([10, 15,     # No overlap.
                  19, 31,     # Full overlap.
                  45, 48,     # Split.
                  65, 75,     # Back overlap.
                  75, 85,     # Front overlap.
                  ])
        s3 = Set([20, 30,
                  45, 48,
                  65, 70,
                  80, 85,
                  ])
        self.assertEqual(s1 & s2, s3)

    def test_gaps(self):
        s1 = Set([0,   10,
                  20,  30,
                  40,  50,
                  60,  70,
                  80,  90,
                  100, 110,
                  200, 210,
                  ])
        s2 = Set([-1000, 1000])
        s3 = Set([-1000, 0,
                  10,    20,
                  30,    40,
                  50,    60,
                  70,    80,
                  90,    100,
                  110,   200,
                  210,   1000,
                  ])
        self.assertEqual(s2 - s1, s3)

    def test_contains(self):
        s1 = Set([-math.inf, -10,
                  0,         10,
                  20,        30,
                  40,        50,
                  60,        math.inf,
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

        s3 = Set([0,  10,
                  20, 30,
                  40, 50,
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
        s1 = Set([-math.inf, -10,
                  0,         10,
                  20,        30,
                  40,        50,
                  60,        math.inf,
                  ])
        i1 = [(-math.inf, -10),
              (0,         10),
              (20,        30),
              (40,        50),
              (60,        math.inf),
              ]
        for e1, e2 in zip(s1, i1):
            self.assertEqual(e1, e2)

    def test_subscript(self):
        s1 = Set([-math.inf, -10,
                  0,         10,
                  20,        30,
                  40,        50,
                  60,        math.inf,
                  ])
        i1 = [(-math.inf, -10),
              (0,         10),
              (20,        30),
              (40,        50),
              (60,        math.inf),
              ]
        self.assertEqual(s1[0], i1[0])
        self.assertEqual(s1[1], i1[1])
        self.assertEqual(s1[2], i1[2])
        self.assertEqual(s1[3], i1[3])
        self.assertEqual(s1[4], i1[4])

    def test_len(self):
        s1 = Set([-math.inf, -10,
                  0,         10,
                  20,        30,
                  40,        50,
                  60,        math.inf,
                  ])
        self.assertEqual(len(s1), 5)

        self.assertEqual(len(Set()), 0)
