from collections import deque
from dataclasses import FrozenInstanceError, dataclass

# === module names ===
a = 1
b = 2
del a, b
a = 3
assert a == 3

try:
    del missing
    assert False, 'expected NameError'
except NameError as exc:
    assert str(exc) == "name 'missing' is not defined"

x = 1
del x
try:
    del x
    assert False, 'expected NameError'
except NameError as exc:
    assert str(exc) == "name 'x' is not defined"


# === locals ===
def del_then_rebind():
    y = 1
    del y
    y = 2
    return y


assert del_then_rebind() == 2

g = 1


def del_global_without_declaration():
    del g


try:
    del_global_without_declaration()
    assert False, 'expected UnboundLocalError'
except UnboundLocalError as exc:
    assert str(exc) == "cannot access local variable 'g' where it is not associated with a value"


def del_twice():
    y = 1
    del y
    del y


try:
    del_twice()
    assert False, 'expected UnboundLocalError'
except UnboundLocalError as exc:
    assert str(exc) == "cannot access local variable 'y' where it is not associated with a value"


# === cells and nonlocal ===
def del_cell_then_rebind():
    y = 1

    def inner():
        return y

    del y
    y = 2
    return inner()


assert del_cell_then_rebind() == 2


def del_nonlocal():
    y = 1

    def inner():
        nonlocal y
        del y

    inner()
    return y


try:
    del_nonlocal()
    assert False, 'expected UnboundLocalError'
except UnboundLocalError as exc:
    assert str(exc) == "cannot access local variable 'y' where it is not associated with a value"

# === declared globals ===
h = 1


def del_declared_global():
    global h
    del h


del_declared_global()
try:
    h
    assert False, 'expected NameError'
except NameError as exc:
    assert str(exc) == "name 'h' is not defined"


def del_declared_missing_global():
    global never_defined
    del never_defined


try:
    del_declared_missing_global()
    assert False, 'expected NameError'
except NameError as exc:
    assert str(exc) == "name 'never_defined' is not defined"


# === except alias ===
def del_except_alias():
    try:
        raise ValueError('boom')
    except ValueError as e:
        del e
    return 'ok'


assert del_except_alias() == 'ok'

# === dict items ===
d = {'a': 1, 'b': 2}
del d['a']
assert d == {'b': 2}
try:
    del d['missing']
    assert False, 'expected KeyError'
except KeyError as exc:
    assert str(exc) == "'missing'"

# === list items and slices ===
items = [1, 2, 3]
del items[-2]
assert items == [1, 3]
try:
    del items[5]
    assert False, 'expected IndexError'
except IndexError as exc:
    assert str(exc) == 'list assignment index out of range'
try:
    del items['x']
    assert False, 'expected TypeError'
except TypeError as exc:
    assert str(exc) == 'list indices must be integers or slices, not str'

nums = list(range(10))
del nums[::2]
assert nums == [1, 3, 5, 7, 9]
nums = list(range(10))
del nums[::-3]
assert nums == [1, 2, 4, 5, 7, 8]
nums = list(range(10))
del nums[8:1:-2]
assert nums == [0, 1, 3, 5, 7, 9]
nums = list(range(10))
del nums[5:2]
assert nums == list(range(10))
del nums[:]
assert nums == []

shared = [1]
holder = [shared, shared, 'a']
del holder[0:2]
assert holder == ['a']
assert shared == [1]

# === deque items ===
dq = deque([1, 2, 3])
del dq[1]
assert list(dq) == [1, 3]


# === attributes ===
class C:
    x = 1


c = C()
c.y = 2
del c.y
del C.x
assert not hasattr(c, 'y')
assert not hasattr(C, 'x')
try:
    del c.missing
    assert False, 'expected AttributeError'
except AttributeError as exc:
    assert str(exc) == "'C' object has no attribute 'missing'"
try:
    del C.missing
    assert False, 'expected AttributeError'
except AttributeError as exc:
    assert str(exc) == "type object 'C' has no attribute 'missing'"


@dataclass(frozen=True)
class Frozen:
    x: int = 1


try:
    del Frozen().x
    assert False, 'expected FrozenInstanceError'
except FrozenInstanceError as exc:
    assert str(exc) == "cannot delete field 'x'"


# === class bodies ===
class Rebound:
    x = 1
    del x
    x = 2


assert Rebound.x == 2


class Removed:
    x = 1
    x = 2
    del x


assert not hasattr(Removed, 'x')


class RemovedTwice:
    x = 1
    del x
    x = 2
    del x
    y = 3


assert not hasattr(RemovedTwice, 'x')
assert RemovedTwice.y == 3


class ItemInBody:
    data = {'x': 1}
    del data['x']


assert ItemInBody.data == {}

try:

    class Missing:
        del missing_name

    assert False, 'expected NameError'
except NameError as exc:
    assert str(exc) == "name 'missing_name' is not defined"

# === target groups run left to right ===
gd = {'x': 1}
gl = [1, 2]
gx = 3
del (gd['x'], [gl[0], gx])
assert gd == {}
assert gl == [2]

# === inside exec ===
ex = 1
exec('del ex')
try:
    ex
    assert False, 'expected NameError'
except NameError as exc:
    assert str(exc) == "name 'ex' is not defined"
ns = {'z': 1}
exec('del z', ns)
assert 'z' not in ns
