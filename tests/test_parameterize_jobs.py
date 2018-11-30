#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `parameterize_jobs` package."""

import pytest

import parameterize_jobs as pj
from parameterize_jobs._utils import _product
from parameterize_jobs._compat import merge_dicts

try:
    import numpy as np
    numpy_installed = True
except ImportError:
    numpy_installed = False

requires_numpy = pytest.mark.skipif(
    not numpy_installed,
    reason="numpy required")


@pytest.fixture
def sample_py_constant():
    '''
    get a (Constant, shape) tuple for a Constant with builtin values
    '''
    return pj.Constant(cons=3.14), (1, )


@pytest.fixture
def another_py_constant():
    '''
    get a (Constant, shape) tuple for a Constant with builtin values
    '''
    return pj.Constant(cons=6.022e23), (1, )


@pytest.fixture
def sample_py_componentset():
    '''
    get a (ComponentSet, shape) tuple for a ComponentSet with builtin values
    '''
    return pj.ComponentSet(fib10=[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]), (10, )


@pytest.fixture
def another_py_componentset():
    '''
    get a (ComponentSet, shape) tuple for a ComponentSet with builtin values
    '''
    return pj.ComponentSet(range10=range(10)), (10, )


@pytest.fixture
def sample_py_nd_componentset():
    '''
    get a (ComponentSet, shape) tuple for a ComponentSet with multiple builtins
    '''
    return (
        pj.ComponentSet(
            fib10=[0, 1, 1, 2, 3, 5, 8, 13, 21, 34],
            range10=range(10)),
        (10, 10))


@pytest.fixture
def sample_numpy_componentset():
    '''
    get a (ComponentSet, shape) tuple for a ComponentSet with numpy values
    '''
    return (
        pj.ComponentSet(fib10=np.array([0, 1, 1, 2, 3, 5, 8, 13, 21, 34])),
        (10, ))


@pytest.fixture
def another_numpy_componentset():
    '''
    get a (ComponentSet, shape) tuple for a ComponentSet with numpy values
    '''
    return (
        pj.ComponentSet(sin=np.sin(np.linspace(0, 2*np.pi, 100))),
        (100, ))


@pytest.fixture
def sample_numpy_nd_componentset():
    '''
    get a (ComponentSet, shape) tuple for a ComponentSet with numpy values
    '''
    return (
        pj.ComponentSet(
            range10=np.arange(10),
            fib10=np.array([0, 1, 1, 2, 3, 5, 8, 13, 21, 34]),
            sin=np.sin(np.linspace(0, 2*np.pi, 100))),
        (10, 10, 100))


def test_constant(sample_py_constant):
    cs, shape = sample_py_constant

    assert len(cs) == 1
    assert len(cs[0]) == len(shape)
    assert cs[0] == cs[-1]

    assert len(cs + cs) == 2

    with pytest.raises(TypeError):
        cs * cs  # cannot multiply ComponentSets by themselves


def test_componentset(sample_py_componentset):
    cs, shape = sample_py_componentset

    assert len(cs) == shape[0]
    assert len(cs[0]) == 1
    assert cs[0] == cs[-len(cs)]

    # requires sample_py_componentset to have unique first and last elements
    assert cs[0] != cs[-1]

    with pytest.raises(KeyError):
        cs[shape[0]]

    with pytest.raises(KeyError):
        cs[-shape[0] - 1]

    assert len(cs + cs) == shape[0] * 2

    with pytest.raises(TypeError):
        cs * cs  # cannot multiply ComponentSets by themselves


def test_ndcomponentset(sample_py_nd_componentset):
    cs, shape = sample_py_nd_componentset

    assert len(cs) == _product(shape)
    assert len(cs[0]) == len(shape)
    assert cs[0] == cs[-len(cs)]

    # requires sample_py_componentset to have unique first and last elements
    assert cs[0] != cs[-1]

    with pytest.raises(KeyError):
        cs[_product(shape)]

    with pytest.raises(KeyError):
        cs[-_product(shape) - 1]

    assert len(cs + cs) == _product(shape) * 2

    with pytest.raises(TypeError):
        cs * cs  # cannot multiply ComponentSets by themselves


def test_py_multiple_componentsets(
        sample_py_componentset, another_py_componentset):

    cs1, shape1 = sample_py_componentset
    cs2, shape2 = another_py_componentset

    assert len(cs1 + cs2) == len(cs1) + len(cs2)
    assert len(cs1 + cs2) == _product(shape1) + _product(shape2)

    assert len(cs1 * cs2) == len(cs1) * len(cs2)
    assert len(list(cs1 * cs2)) == len(cs1 * cs2)

    assert (cs1 + cs2)[0] == cs1[0]
    assert (cs1 + cs2)[1] == cs1[1]
    assert (cs1 + cs2)[-2] == cs2[-2]
    assert (cs1 + cs2)[-1] == cs2[-1]

    assert (cs1 * cs2)[0] == merge_dicts(cs1[0], cs2[0])
    assert (cs1 * cs2)[-1] == merge_dicts(cs1[-1], cs2[-1])

    full_product = list(cs1 * cs2)
    assert full_product[0] == (cs1 * cs2)[0]
    assert full_product[-1] == (cs1 * cs2)[-1]


def test_complex_componentsets(
        sample_py_constant,
        another_py_constant,
        sample_py_componentset,
        another_py_componentset):

    cons1, _ = sample_py_constant
    cons2, _ = another_py_constant
    cs1, shape1 = sample_py_componentset
    cs2, shape2 = another_py_componentset

    cplx = (cs1 + cs2) * cons1 + cons2 * (cs1 + cs2)

    assert len(cplx) == 2 * (_product(shape1) + _product(shape2))

    assert cplx[1] == merge_dicts(cs1[1], cons1[0])
    assert cplx[len(cs1) + 1] == merge_dicts(cs2[1], cons1[0])
    assert cplx[-1] == merge_dicts(cs2[-1], cons2[0])

    full_cplx = list(cplx)
    assert len(full_cplx) == len(cplx)


@requires_numpy
def test_numpy_componentset(sample_numpy_componentset):
    cs, shape = sample_numpy_componentset

    assert len(cs) == shape[0]
    assert len(cs[0]) == 1
    assert len(cs) == len(list(cs))
    assert cs[0] == cs[-len(cs)]

    # requires sample_py_componentset to have unique first and last elements
    assert cs[0] != cs[-1]

    with pytest.raises(KeyError):
        cs[shape[0]]

    with pytest.raises(KeyError):
        cs[-shape[0] - 1]

    assert len(cs + cs) == shape[0] * 2

    with pytest.raises(TypeError):
        cs * cs  # cannot multiply ComponentSets by themselves


@requires_numpy
def test_numpy_ndcomponentset(sample_numpy_nd_componentset):
    cs, shape = sample_numpy_nd_componentset

    assert len(cs) == _product(shape)
    assert len(cs[0]) == len(shape)
    assert cs[0] == cs[-len(cs)]

    # requires sample_py_componentset to have unique first and last elements
    assert cs[0] != cs[-1]

    with pytest.raises(KeyError):
        cs[_product(shape)]

    with pytest.raises(KeyError):
        cs[-_product(shape) - 1]

    assert len(cs + cs) == _product(shape) * 2

    with pytest.raises(TypeError):
        cs * cs  # cannot multiply ComponentSets by themselves


@requires_numpy
def test_numpy_multiple_componentsets(
        sample_numpy_componentset, another_numpy_componentset):

    cs1, shape1 = sample_numpy_componentset
    cs2, shape2 = another_numpy_componentset

    assert len(cs1 + cs2) == len(cs1) + len(cs2)
    assert len(cs1 + cs2) == _product(shape1) + _product(shape2)

    assert len(cs1 * cs2) == len(cs1) * len(cs2)
    assert len(list(cs1 * cs2)) == len(cs1 * cs2)

    assert (cs1 + cs2)[0] == cs1[0]
    assert (cs1 + cs2)[1] == cs1[1]
    assert (cs1 + cs2)[-2] == cs2[-2]
    assert (cs1 + cs2)[-1] == cs2[-1]

    assert (cs1 * cs2)[0] == merge_dicts(cs1[0], cs2[0])
    assert (cs1 * cs2)[-1] == merge_dicts(cs1[-1], cs2[-1])

    full_product = list(cs1 * cs2)
    assert full_product[0] == (cs1 * cs2)[0]
    assert full_product[-1] == (cs1 * cs2)[-1]


@requires_numpy
def test_numpy_complex_componentsets(
        sample_py_constant,
        another_py_constant,
        sample_numpy_componentset,
        another_numpy_componentset):

    cons1, _ = sample_py_constant
    cons2, _ = another_py_constant
    cs1, shape1 = sample_numpy_componentset
    cs2, shape2 = another_numpy_componentset

    cplx = (cs1 + cs2) * cons1 + cons2 * (cs1 + cs2)

    assert len(cplx) == 2 * (_product(shape1) + _product(shape2))

    assert cplx[1] == merge_dicts(cs1[1], cons1[0])
    assert cplx[len(cs1) + 1] == merge_dicts(cs2[1], cons1[0])
    assert cplx[-1] == merge_dicts(cs2[-1], cons2[0])

    full_cplx = list(cplx)
    assert len(full_cplx) == len(cplx)


def test_reprs(
        sample_py_constant,
        sample_py_componentset,
        another_py_componentset,
        sample_py_nd_componentset):

    cs0 = sample_py_constant[0]
    cs1 = sample_py_componentset[0]
    cs2 = another_py_componentset[0]
    cs3 = sample_py_nd_componentset[0]

    assert '<Component' in str(list(cs0._sets.values())[0])

    assert '<Constant' in str(cs0)
    assert '<ComponentSet' in str(cs1)
    assert '<MultiComponentSet' in str(cs1 + cs2)
    assert '<ComponentSet' in str(cs3)
