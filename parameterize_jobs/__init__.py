# -*- coding: utf-8 -*-

"""Top-level package for Parameterize Jobs."""

from __future__ import absolute_import

from parameterize_jobs.parameterize_jobs import (
    Component,
    ComponentSet,
    MultiComponentSet,
    Constant,
    expand_kwargs)

__author__ = """Michael Delgado"""
__email__ = 'delgado.michaelt@gmail.com'
__version__ = '0.1.0'

_module_imports = (
    Component,
    ComponentSet,
    MultiComponentSet,
    Constant,
    expand_kwargs
)

__all__ = list(map(lambda x: x.__name__, _module_imports))
