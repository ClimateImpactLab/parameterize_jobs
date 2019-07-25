=================
Parameterize Jobs
=================

.. image:: https://img.shields.io/pypi/v/parameterize_jobs.svg
        :target: https://pypi.python.org/pypi/parameterize_jobs

.. image:: https://img.shields.io/travis/ClimateImpactLab/parameterize_jobs.svg
        :target: https://travis-ci.org/ClimateImpactLab/parameterize_jobs

.. image:: https://readthedocs.org/projects/parameterize-jobs/badge/?version=latest
        :target: https://parameterize-jobs.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/ClimateImpactLab/parameterize_jobs/shield.svg
     :target: https://pyup.io/repos/github/ClimateImpactLab/parameterize_jobs/
     :alt: Updates

``parameterize_jobs`` is a lightweight, pure-python toolkit for concisely and clearly creating large, parameterized, mapped job specifications.


* Free software: MIT license
* Documentation: https://parameterize-jobs.readthedocs.io

Features
--------

* Expand a job's dimensionality by multiplying ``ComponentSet``, ``Constant``, or ``ParallelComponentSet`` objects
* Extend the number of jobs by adding ``ComponentSet``, ``Constant``, or ``ParallelComponentSet`` objects
* Jobs are provided to functions as dictionaries of parameters
* The helper decorator ``@expand_kwargs`` turns these kwarg dictionaries into
  named argument calls
* Works seamlessly with many task running frameworks, including dask's `client.map` and profiling tools

TODOs
-----

View and submit issues on the `issues page <https://github.com/ClimateImpactLab/parameterize_jobs/issues>`_.

Quickstart
----------

``ComponentSet`` objects are the base objects, and can be defined with any number of named iterables:

.. code-block:: python

    >>> import parameterize_jobs as pjs

    >>> a = pjs.ComponentSet(a=range(5))
    >>> a
    <ComponentSet {'a': 5}>

These objects have defined lengths (if the provided iterable has a defined length), and can be indexed and iterated over:

.. code-block:: python

    >>> len(a)
    5

    >>> a[0]
    {'a': 0}

    >>> list(a)
    [{'a': 0},
     {'a': 1},
     {'a': 2},
     {'a': 3},
     {'a': 4}]

Adding two ``ComponentSet`` objects extends the total job length

.. code-block:: python

    >>> a2 = pjs.ComponentSet(a=range(3))

    >>> a+a2
    <MultiComponentSet [{'a': 5}, {'a': 3}]>

    >>> len(a+a2)
    8

    >>> list(a+a2)

    [{'a': 0},
     {'a': 1},
     {'a': 2},
     {'a': 3},
     {'a': 4},
     {'a': 0},
     {'a': 1},
     {'a': 2}]

Multiplying two ``ComponentSet`` objects expands their dimensionality:

.. code-block:: python

    >>> b = pjs.ComponentSet(b=range(3))

    >>> a*b
    <ComponentSet {'a': 5, 'b': 3}>

    >>> len(a*b)
    15

    >>> (a*b)[-1]
    {'a': 4, 'b': 2}

    >>> list(a*b)
    [{'a': 0, 'b': 0},
     {'a': 0, 'b': 1},
     {'a': 0, 'b': 2},
     {'a': 1, 'b': 0},
     {'a': 1, 'b': 1},
     {'a': 1, 'b': 2},
     {'a': 2, 'b': 0},
     {'a': 2, 'b': 1},
     {'a': 2, 'b': 2},
     {'a': 3, 'b': 0},
     {'a': 3, 'b': 1},
     {'a': 3, 'b': 2},
     {'a': 4, 'b': 0},
     {'a': 4, 'b': 1},
     {'a': 4, 'b': 2}]

These parameterized job specifications can be used in mappable jobs. The helper decorator ``expand_kwargs`` modifies a function to accept a dictionary and expands them into keyword arguments:

.. code-block:: python

    >>> @pjs.expand_kwargs
    ... def my_simple_func(a, b, c=1):
    ...     return a * b * c

    >>> list(map(my_simple_func, a*b))
    [0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 0, 2, 4, 6, 8, 0, 3, 6, 9, 12]

Jobs do not have to be the combinatorial product of all components:

.. code-block:: python

    >>> ab1 = pjs.ComponentSet(a=[0, 1], b=[0, 1])
    >>> ab2 = pjs.ComponentSet(a=[10, 11], b=[-1, 1])

    >>> list(map(my_simple_func, ab1 + ab2))
    [0, 0, 0, 1, -10, -11, 10, 11]

A ``Constant`` object is simply a ``ComponentSet`` object defined with single values passed as keyword arguments rather than iterables passed as keyword arguments:

.. code-block:: python

    >>> c = pjs.Constant(c=5)

    >>> list(map(my_simple_func, (ab1 + ab2) * c))
    [0, 0, 0, 5, -50, -55, 50, 55]

A ``ParallelComponentSet`` object is simply a ``MultiComponentSet`` object where each ``Component`` is a ``Constant`` object.

.. code-block:: python

    >>> pcs = pjs.ParallelComponentSet(a = [1, 2],
                               b = [10, 20])

    >>> list(map(my_simple_func, pcs))
    [10, 40]

Arbitrarily complex combinations of ComponentSets can be created:

.. code-block:: python

    >>> c1 = pjs.Constant(c=1)
    >>> c2 = pjs.Constant(c=2)

    >>> list(map(my_simple_func, (ab1 + ab2) * c1 + (ab1 + ab2) * c2))
    [0, 0, 0, 1, -10, -11, 10, 11, 0, 0, 0, 2, -20, -22, 20, 22]

Anything can be inside a ``ComponentSet`` iterable, including data, functions, or other objects:

.. code-block:: python

    >>> transforms = (
    ...     pjs.Constant(transform=lambda x: x, transform_name='linear')
    ...     + pjs.Constant(transform=lambda x: x**2, transform_name='quadratic'))
    ...

    >>> fps = pjs.Constant(
    ...     read_pattern='source/my-fun-data_{year}.csv',
    ...     write_pattern='transformed/my-fun-data_{transform_name}_{year}.csv')

    >>> years = pjs.ComponentSet(year=range(1980, 2018))

    >>> @pjs.expand_kwargs
    ... def process_data(read_pattern, write_pattern, transform, transform_name, year):
    ...
    ...     df = pd.read_csv(read_pattern.format(year=year))
    ...
    ...     transformed = transform(df)
    ...
    ...     transformed.to_csv(
    ...         write_pattern.format(
    ...             transform_name=transform_name,
    ...             year=year))
    ...

    >>> _ = list(map(process_data, transforms * fps * years))

This works seamlessly with dask's `client.map <http://distributed.dask.org/en/latest/api.html#distributed.Client.map>`_ to provide intuitive job parameterization:

.. code-block:: python

    >>> import dask.distributed as dd
    >>> client = dd.LocalClient()
    >>> futures = client.map(my_simple_func, (ab1 + ab2) * c1 + (ab1 + ab2) * c2)
    >>> dd.progress(futures)
