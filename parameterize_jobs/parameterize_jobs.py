# -*- coding: utf-8 -*-

from __future__ import absolute_import

import itertools
import functools
from collections import OrderedDict

import parameterize_jobs._compat as _compat
from parameterize_jobs._utils import _product, _cumprod


class Component(object):
    def __init__(self, values):
        if isinstance(values, Component):
            self._values = values._values
        else:
            self._values = values

    def __getitem__(self, index):
        return self._values[index]

    def __len__(self):
        return len(self._values)

    def __iter__(self):
        for v in self._values:
            yield v

    def __repr__(self):
        return '<{} [{}]>'.format(
            self.__class__.__name__,
            ', '.join(map(str, self._values[:3]))
            + (', ...' if len(self) > 3 else ''))


class ComponentSet(object):
    '''
    Indexable combinatorial product job specification
    '''

    def __init__(self, **kwargs):
        self._sets = OrderedDict([
            (k, Component(v)) for k, v in kwargs.items()])

    def __getitem__(self, idx):
        if isinstance(idx, dict):
            raise NotImplemented('dictionary indexing not yet supported')

        elif isinstance(idx, slice):
            raise NotImplemented('slice indexing not yet supported')

        elif isinstance(idx, int):

            if (idx >= len(self)) or (idx < -1 * len(self)):
                raise KeyError(
                    'index {} out of bounds for {} with length {}'
                    .format(idx, self.__class__.__name__, len(self)))

            lens = list(map(len, self._sets.values()))
            cplens = list(_cumprod(list(
                list(lens[1:]) + [1])))

            idxers = list(
                (idx // cplens[i]) % lens[i]
                for i in range(len(cplens)))

            return {
                k: self._sets[k][idxers[i]]
                for i, k in enumerate(self._sets.keys())}

        else:
            raise NotImplemented(
                '{} indexing not yet supported'.format(type(idx)))

    def __len__(self):
        return _product(map(len, self._sets.values()))

    def __iter__(self):
        for v in itertools.product(*self._sets.values()):
            yield dict(zip(self._sets.keys(), v))

    def __mul__(self, other):
        if isinstance(other, ComponentSet):
            return ComponentSet(
                **_compat.merge_dicts(self._sets, other._sets))

        elif isinstance(other, MultiComponentSet):
            return MultiComponentSet([self * c for c in other._components])
        else:
            raise TypeError(
                'Cannot multiply {} by {}'.format(type(self), type(other)))

    def __add__(self, other):
        return MultiComponentSet([self, other])

    def _stringify(self):
        try:
            return (
                '{'
                + ', '.join(map(
                    lambda k: str(k[0]) + ': ' + str(len(k[1])),
                    list(self._sets.items())[:5]))
                + (', ...' if len(self._sets.keys()) > 5 else '')
                + '}')
        except TypeError:
            return (
                '{'
                + ', '.join(map(
                    lambda k: str(k[0]) + ': (...)',
                    list(self._sets.items())[:5]))
                + (', ...' if len(self._sets.keys()) > 5 else '')
                + '}')

    def __repr__(self):
        return (
            '<{} {}>'.format(
                self.__class__.__name__,
                self._stringify()))


class MultiComponentSet(object):
    '''
    A list of multiple ComponentSet objects
    '''

    def __init__(self, components):
        self._components = components

    def __add__(self, other):
        return self.__class__([self, other])

    def __mul__(self, other):
        return self.__class__([c * other for c in self._components])

    def __iter__(self):
        for c in self._components:
            for s in c:
                yield s

    def __len__(self):
        return sum([len(c) for c in self._components])

    def __getitem__(self, idx):
        if (idx >= len(self)) or (idx < -1 * len(self)):
            raise KeyError(
                'index {} out of bounds for {} with length {}'
                .format(idx, self.__class__.__name__, len(self)))

        idx = idx % len(self)

        lens = list(map(len, self._components))
        cslens = ([0] + [
            sum((list(lens))[:i + 1])
            for i in range(len(self._components))])

        pos = [
            i
            for i in range(len(self._components))
            if (idx >= cslens[i] and idx < cslens[i + 1])][0]

        return self._components[pos][idx - cslens[pos]]

    def _stringify(self):
        return (
            '['
            + ', '.join([c._stringify() for c in self._components])
            + ']')

    def __repr__(self):
        return (
            '<{} {}>'.format(
                self.__class__.__name__,
                self._stringify()))


class Constant(ComponentSet):
    '''
    A ComponentSet where each iterable has only one element
    '''

    def __init__(self, **kwargs):
        self._sets = OrderedDict([
            (k, Component([v])) for k, v in kwargs.items()])


def expand_kwargs(func):
    '''
    Decorator to expand an kwargs in function calls

    Parameters
    ----------
    func : function
        Function to have arguments expanded. Func can have any
        number of keyword arguments.
    Returns
    -------
    wrapped : function
        Wrapped version of ``func`` which accepts a single
        ``kwargs`` dict.
    Examples
    --------
    .. code-block:: python

        >>> @expand_kwargs
        ... def my_func(a, b, exp=1):
        ...     return (a * b)**exp
        ...
        >>> my_func({'a': 2, 'b': 3})
        6
        >>> my_func({'a': 2, 'b': 3, 'exp': 2})
        36

    '''

    @functools.wraps(func)
    def inner(k, *args, **kwargs):
        kw = _compat.merge_dicts(k, kwargs)
        return func(*args, **kw)
    return inner
