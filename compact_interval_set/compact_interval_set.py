# Copyright (c) 2022 by Terry Greeniaus.
import math
import bisect


class Interval:
    '''
    Class representing the interval [start, end).  If either start or end is
    None then that boundary will be set to -math.inf or +math.inf, respectively.
    '''
    def __init__(self, start, end):
        self.start = -math.inf if start is None else start
        self.end   = math.inf if end is None else end
        assert self.start < self.end

    def __repr__(self):
        return 'Interval(%s, %s)' % (self.start, self.end)

    def __contains__(self, v):
        return self.start <= v < self.end

    def __lt__(self, other):
        if isinstance(other, Interval):
            if self.start == other.start:
                return self.end < other.end
            return self.start < other.start

        return self.start < other

    def __eq__(self, other):
        if isinstance(other, Interval):
            return self.start == other.start and self.end == other.end
        return NotImplemented


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
    def __init__(self, elems=None):
        if isinstance(elems, Set):
            elems = elems.elems
        if elems is None:
            self.elems = []
            return
        elems = sorted(elems)

        self.elems = [Interval(elems[0].start, elems[0].end)]
        for i in range(1, len(elems)):
            e = elems[i]
            if e.start <= self.elems[-1].end:
                self.elems[-1].end = max(e.end, self.elems[-1].end)
            else:
                self.elems.append(Interval(e.start, e.end))

        self._check_reduced()

    def __repr__(self):
        return 'Set(%s)' % self.elems

    def __len__(self):
        return len(self.elems)

    def __getitem__(self, key):
        return self.elems[key]

    def __iter__(self):
        return self.elems.__iter__()

    def __contains__(self, v):
        if not self.elems:
            return False
        if v == -math.inf:
            return self.elems[0].start == -math.inf
        if v == math.inf:
            return self.elems[-1].end == math.inf

        i = bisect.bisect_left(self.elems, v)
        if i > 0 and v in self.elems[i - 1]:
            return True
        return v == self.elems[i].start if i < len(self.elems) else False

    def __eq__(self, other):
        if not isinstance(other, Set):
            return False
        return self.elems == other.elems

    def __or__(self, B):
        if not isinstance(B, Set):
            return NotImplemented
        return Set(self.elems + B.elems)

    def __and__(self, B):
        if not isinstance(B, Set):
            return NotImplemented

        s  = Set()
        i  = 0
        j  = 0
        while i < len(self.elems) and j < len(B.elems):
            se        = self.elems[i]
            oe        = B.elems[j]
            max_start = max(se.start, oe.start)
            min_end   = min(se.end, oe.end)
            if max_start < min_end:
                s.elems.append(Interval(max_start, min_end))
            if se.end <= oe.end:
                i += 1
            if oe.end <= se.end:
                j += 1
        s._check_reduced()
        return s

    def __invert__(self):
        if not self.elems:
            return Set([Interval(-math.inf, math.inf)])

        s = Set()
        if self.elems[0].start != -math.inf:
            s.elems.append(Interval(-math.inf, self.elems[0].start))
        for i in range(len(self.elems) - 1):
            s.elems.append(Interval(self.elems[i].end, self.elems[i + 1].start))
        if self.elems[-1].end != math.inf:
            s.elems.append(Interval(self.elems[-1].end, math.inf))
        s._check_reduced()
        return s

    def __sub__(self, B):
        return self & ~B

    def _check_reduced(self):
        for i in range(len(self.elems) - 1):
            assert self.elems[i].end < self.elems[i + 1].start

    def insert(self, interval):
        assert isinstance(interval, Interval)
        i = bisect.bisect_left(self.elems, interval)
        if i > 0:
            if interval.start <= self.elems[i - 1].end:
                if interval.end <= self.elems[i - 1].end:
                    return

                interval.start = self.elems[i - 1].start
                del self.elems[i - 1]
                i -= 1
        while i < len(self.elems) and self.elems[i].end <= interval.end:
            del self.elems[i]
        if i < len(self.elems):
            if self.elems[i].start <= interval.end:
                interval.end = self.elems[i].end
                del self.elems[i]
        self.elems.insert(i, interval)
        self._check_reduced()
