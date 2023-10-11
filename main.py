import collections.abc
from typing import TypeVar

_T = TypeVar("_T")  #: Any Type


class ArbitraryInsertList(collections.abc.MutableSequence):

    def __init__(self, initlist: collections.abc.Sequence = None):
        self.data: dict = {}        # TODO: Make this a TypedDict to avoid non-ints being used as keys.
        if initlist is not None:
            if isinstance(initlist, ArbitraryInsertList):
                self.data[:] = initlist.data[:]
            else:
                self.data = {idx: item for idx, item in enumerate(initlist) if item is not None}

    @property
    def baked(self):
        return [self.data.get(i, None) for i in range(len(self))]

    def __repr__(self):
        return f"{self.__class__.__name__}({repr(self.baked)})"

    def __lt__(self, other):
        if isinstance(other, ArbitraryInsertList):
            return self.data < other.data
        return self.baked < other

    def __le__(self, other):
        if isinstance(other, ArbitraryInsertList):
            return self.data <= other.data
        return self.baked <= other

    def __eq__(self, other):
        if isinstance(other, ArbitraryInsertList):
            return self.data == other.data
        return self.baked == other

    def __gt__(self, other):
        if isinstance(other, ArbitraryInsertList):
            return self.data > other.data
        return self.baked > other

    def __ge__(self, other):
        if isinstance(other, ArbitraryInsertList):
            return self.data >= other.data
        return self.baked >= other

    def __contains__(self, item):
        return item in self.data.values()

    def __len__(self):
        return self.filled_elements[-1]+1

    def __getitem__(self, i):
        if isinstance(i, slice):
            return self.__class__(self.data[i])     # TODO: this slices thing
        else:
            return self.data[i]

    def __setitem__(self, i, item):
        self.data[i] = item

    def __delitem__(self, i):
        del self.data[i]

    def __add__(self, other):
        if isinstance(other, ArbitraryInsertList):
            return self.__class__(self.data | other.data)
        elif isinstance(other, type(self.baked)):
            return self.__class__(self.baked + other)
        return self.__class__(self.baked + list(other))

    def __radd__(self, other):
        if isinstance(other, ArbitraryInsertList):
            return self.__class__(other.data | self.data)
        elif isinstance(other, type(self.baked)):
            return self.__class__(other + self.baked)
        return self.__class__(list(other) + self.baked)

    def __iadd__(self, other):
        if isinstance(other, ArbitraryInsertList):
            self.data |= other.data
        elif isinstance(other, type(self.baked)):
            self.data = {idx: item for idx, item in enumerate(self.baked + other) if item is not None}  # TODO: Optimise?
        else:
            self.data = {idx: item for idx, item in enumerate(self.baked + list(other)) if item is not None}  # TODO: Optimise?
        return self

    def __mul__(self, n):
        return self.__class__(self.baked * n)

    __rmul__ = __mul__

    def __imul__(self, n):
        self.data *= n  # TODO
        return self

    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["data"] = self.__dict__["data"][:]
        return inst

    @property
    def filled_elements(self):
        """Returns a list of the indices that are not filled with None."""
        all_keys = list(self.data.keys())
        all_keys.sort()
        return all_keys

    def append(self, item):
        self.data[len(self)] = item

    def insert(self, i, item):
        self.data[i] = item

    def pop(self, i=-1):
        if i < 0:
            i = self.filled_elements[i]
        return self.data.pop(i)

    def remove(self, item):
        for key, value in self.data.items():
            if value == item:
                del self.data[key]

    def clear(self):
        self.data.clear()

    def copy(self):
        return self.__class__(self)

    def count(self, item):
        return tuple(self.data.values()).count(item)

    def index(self, item, *args):
        return self.baked.index(item, *args)

    def reverse(self):
        baked_copy = self.baked.copy()
        baked_copy.reverse()
        self.data = {idx: item for idx, item in enumerate(baked_copy) if item is not None}  # TODO: Optimise.

    def sort(self, /, *args, **kwds):
        baked_copy = self.baked.copy()
        baked_copy.sort(*args, **kwds)
        self.data = {idx: item for idx, item in enumerate(baked_copy) if item is not None}  # TODO: Optimise.

    def extend(self, other):
        if isinstance(other, ArbitraryInsertList):
            other_data_copy = other.data.copy()
            other_keys = list(other_data_copy.keys())
            other_keys.sort()
            other_keys.reverse()
            orig_self_len = len(self)
            for key in other_keys:
                new_idx = key + orig_self_len
                self.data[new_idx] = other_data_copy[key]
        else:
            baked_copy = self.baked.copy()
            baked_copy.extend(other)
            self.data = {idx: item for idx, item in enumerate(baked_copy) if item is not None}  # TODO: Optimise.


if __name__ == '__main__':
    ail = ArbitraryInsertList([0, 1, 2, 3, 4])
    ail.insert(9, 9)
    ail.insert(8, 8)
    ail.insert(5, 5)
    print(ail)
