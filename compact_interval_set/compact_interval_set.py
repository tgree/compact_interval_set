# Copyright (c) 2022 by Terry Greeniaus.
import math
import bisect


class Set:
    '''
    Class containing points defined by [start, end) intervals.  Like any set, a
    point in the Set is present only once; this implies that intervals are
    coalesced as they are added to the Set.  Standard set operations are
    supported; it is assumed that points are all from the range [-inf, inf] and
    that infinities are valid interval endpoints.

    The following operators are defined for Set objects:

        A | B   - the union of A and B; all elements in at least one of A or B
        A & B   - the intersection of A and B; all elements in both A and B
        A - B   - the difference of A and B; all elements in A but not B
        ~A      - the complement of A; all elements not in A
    '''
    def __init__(self, points=()):
        self.points = []

        if isinstance(points, Set):
            points = points.points

        assert len(points) % 2 == 0
        for i in range(0, len(points), 2):
            self.insert(points[i], points[i + 1])

    def __repr__(self):
        return 'Set(%s)' % self.points

    def __len__(self):
        return len(self.points) // 2

    def __getitem__(self, key):
        return (self.points[2 * key], self.points[2 * key + 1])

    def __iter__(self):
        for i in range(0, len(self.points), 2):
            yield (self.points[i], self.points[i + 1])

    def __contains__(self, v):
        if not self.points:
            return False
        if v == math.inf:
            return self.points[-1] == math.inf
        return bisect.bisect_right(self.points, v) % 2 == 1

    def __eq__(self, B):
        return isinstance(B, Set) and self.points == B.points

    def __or__(self, B):
        if not isinstance(B, Set):
            return NotImplemented
        return Set(self.points + B.points)

    def __and__(self, B):
        if not isinstance(B, Set):
            return NotImplemented

        s = Set()
        i = 0
        j = 0
        while i < len(self.points) and j < len(B.points):
            s0, e0    = self.points[i], self.points[i + 1]
            s1, e1    = B.points[j], B.points[j + 1]
            max_start = max(s0, s1)
            min_end   = min(e0, e1)
            if max_start < min_end:
                s.points += [max_start, min_end]
            if e0 <= e1:
                i += 2
            if e1 <= e0:
                j += 2

        return s

    def __invert__(self):
        if not self.points:
            return Set([-math.inf, math.inf])

        s = Set()
        L = [] if self.points[0] == -math.inf else [-math.inf, self.points[0]]
        R = [] if self.points[-1] == math.inf else [self.points[-1], math.inf]
        s.points = L + self.points[1:-1] + R
        return s

    def __sub__(self, B):
        return self & ~B

    def insert(self, p0, p1):
        i0 = bisect.bisect_left(self.points, p0)
        i1 = bisect.bisect_right(self.points, p1)
        self.points[i0:i1] = (p0, p1)[i0 % 2:2 - (i1 % 2)]
