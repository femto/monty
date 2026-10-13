# === dict.clear() ===
d = {'a': 1, 'b': 2}
d.clear()
assert d == {}

d = {}
d.clear()
assert d == {}

# === dict.copy() ===
d = {'a': 1, 'b': 2}
copy = d.copy()
assert copy == {'a': 1, 'b': 2}
assert copy is not d
d['c'] = 3
assert 'c' not in copy

d = {}
copy = d.copy()
assert copy == {}

# === dict.update() ===
d = {'a': 1}
d.update({'b': 2})
assert d == {'a': 1, 'b': 2}

d = {'a': 1}
d.update({'a': 10})
assert d == {'a': 10}

d = {'a': 1}
d.update()
assert d == {'a': 1}

d = {}
d.update([('a', 1), ('b', 2)])
assert d == {'a': 1, 'b': 2}

# === dict.setdefault() ===
d = {'a': 1}
result = d.setdefault('a', 10)
assert result == 1
assert d == {'a': 1}

d = {'a': 1}
result = d.setdefault('b', 2)
assert result == 2
assert d == {'a': 1, 'b': 2}

d = {'a': 1}
result = d.setdefault('b')
assert result is None
assert d == {'a': 1, 'b': None}

# === dict.popitem() ===
d = {'a': 1, 'b': 2}
item = d.popitem()
assert item == ('b', 2)
assert d == {'a': 1}

d = {'x': 10}
item = d.popitem()
assert item == ('x', 10)
assert d == {}

# === deletion keeps insertion order and lookups ===
# Deletions leave tombstones that are trimmed from the end or compacted once
# they outnumber live entries; order and every remaining key survive both.
d = {i: i * 10 for i in range(10)}
assert d.pop(0) == 0
assert d.pop(5) == 50
assert d.pop(9) == 90
assert list(d) == [1, 2, 3, 4, 6, 7, 8]
assert d[4] == 40
assert 5 not in d
d[5] = 55
assert list(d) == [1, 2, 3, 4, 6, 7, 8, 5]
assert d.popitem() == (5, 55)
assert d.popitem() == (8, 80)
assert len(d) == 6

# draining from the front crosses several compactions
d = {i: i for i in range(100)}
for i in range(95):
    assert d.pop(i) == i
assert list(d.items()) == [(95, 95), (96, 96), (97, 97), (98, 98), (99, 99)]
assert d == {95: 95, 96: 96, 97: 97, 98: 98, 99: 99}
for i in range(95):
    assert i not in d
for i in range(95, 100):
    assert d[i] == i

# draining with popitem is LIFO, including after middle deletions
d = dict.fromkeys('abcdefgh', 0)
d.pop('c')
d.pop('f')
assert [d.popitem()[0] for _ in range(6)] == ['h', 'g', 'e', 'd', 'b', 'a']
assert d == {}

# a re-inserted key moves to the end; an emptied dict is reusable
d = {'a': 1, 'b': 2, 'c': 3}
d.pop('a')
d['a'] = 4
assert list(d) == ['b', 'c', 'a']
d.pop('a')
d.pop('b')
d.pop('c')
assert d == {}
d['z'] = 1
assert list(d.items()) == [('z', 1)]

# copies, views, repr and unpacking skip the tombstones
d = {i: str(i) for i in range(6)}
d.pop(1)
d.pop(3)
assert repr(d) == "{0: '0', 2: '2', 4: '4', 5: '5'}"
assert d.copy() == {0: '0', 2: '2', 4: '4', 5: '5'}
assert list(d.copy()) == [0, 2, 4, 5]
assert dict(d) == d
assert {**d} == d
assert list(d.keys()) == [0, 2, 4, 5]
assert list(d.values()) == ['0', '2', '4', '5']
assert list(d.items()) == [(0, '0'), (2, '2'), (4, '4'), (5, '5')]
assert len(d.keys()) == 4
assert sorted(d, reverse=True) == [5, 4, 2, 0]

# === dict.fromkeys() ===
d = dict.fromkeys(['a', 'b', 'c'])
assert d == {'a': None, 'b': None, 'c': None}

d = dict.fromkeys(['a', 'b'], 0)
assert d == {'a': 0, 'b': 0}

d = dict.fromkeys([])
assert d == {}

d = dict.fromkeys('abc')
assert d == {'a': None, 'b': None, 'c': None}

d = dict.fromkeys(range(3), 'x')
assert d == {0: 'x', 1: 'x', 2: 'x'}

d = dict.fromkeys((1, 2, 3), [])
assert d[1] is d[2] and d[2] is d[3], 'fromkeys shares same value object for all keys'

# Duplicate keys - later occurrence wins
d = dict.fromkeys(['a', 'b', 'a'], 1)
assert d == {'a': 1, 'b': 1}
assert list(d.keys()) == ['a', 'b']

# === dict.fromkeys() instance access ===
# fromkeys is a classmethod but should also work on instances
d = {}.fromkeys(['a', 'b'])
assert d == {'a': None, 'b': None}

d = {'x': 1}.fromkeys(['a', 'b'], 0)
assert d == {'a': 0, 'b': 0}

# === dict.update() with keyword arguments ===
d = {'a': 1}
d.update(b=2)
assert d == {'a': 1, 'b': 2}

d = {'a': 1}
d.update(b=2, c=3)
assert d == {'a': 1, 'b': 2, 'c': 3}

d = {'a': 1}
d.update(a=10)
assert d == {'a': 10}

d = {}
d.update(a=1, b=2)
assert d == {'a': 1, 'b': 2}

# update with both positional dict and kwargs
d = {'a': 1}
d.update({'b': 2}, c=3)
assert d == {'a': 1, 'b': 2, 'c': 3}

# kwargs overwrite positional dict values
d = {'a': 1}
d.update({'b': 2}, b=20)
assert d == {'a': 1, 'b': 20}

# update with iterable and kwargs
d = {}
d.update([('a', 1)], b=2)
assert d == {'a': 1, 'b': 2}

# `**` unpacking with a runtime-built (non-interned) string key must still
# reach **kwargs — only genuinely non-string keys are rejected.
runtime_key = 'zzz' + 'qqq'
d = dict(**{runtime_key: 1})
assert d == {'zzzqqq': 1}
d.update(**{runtime_key: 2})
assert d == {'zzzqqq': 2}

# === Error message for unknown classmethod ===
# Error message should say 'dict' not 'type'
try:
    dict.nonexistent()
    assert False, 'should raise AttributeError'
except AttributeError as e:
    msg = str(e)
    assert 'dict' in msg, f'error should mention dict, got: {e}'
    assert 'nonexistent' in msg, f'error should mention method name, got: {e}'

# === dict.update() sequence element error ===
# an element of the wrong length names its index and length
for source, message in [
    ([('a', 1), 'x', ('c', 3)], 'dictionary update sequence element #1 has length 1; 2 is required'),
    ([[]], 'dictionary update sequence element #0 has length 0; 2 is required'),
    ([(1, 2, 3)], 'dictionary update sequence element #0 has length 3; 2 is required'),
    ([('a', 1), range(5)], 'dictionary update sequence element #1 has length 5; 2 is required'),
    ([iter([1, 2, 3])], 'dictionary update sequence element #0 has length 3; 2 is required'),
]:
    d = {}
    try:
        d.update(source)
        assert False, 'expected ValueError'
    except ValueError as exc:
        assert str(exc) == message
    assert d == {} or d == {'a': 1}
