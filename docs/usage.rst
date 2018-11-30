=====
Usage
=====

To use Parameterize Jobs in a project::

    In [1]: import parameterize_jobs as pj




The Component class
-------------------

.. code:: ipython3

    In [2]: component = Component([0, 50, 100])
    In [3]: component
    Out[3]:
    <Component [0, 50, 100]>


components are essentially just a wrapper around whatever data you
provided, which should be an iterable.

.. code:: ipython3

    In [4]: component[0]
    Out[4]:
    0



.. code:: ipython3

    In [5]: len(component)
    Out[5]:
    3



.. code:: ipython3

    In [6]: list(component)
    Out[6]:
    [0, 50, 100]



| **Q:** sweet. but why would we want that?
| **A:** you don’t. components are just a helper class. you want to use
  a ``ComponentSet``!

The ComponentSet class
----------------------

.. code:: ipython3

    In [7]: cs = ComponentSet(a=range(5), b=['a', 'b', 'c', 'd'])
    In [8]: cs
    Out[8]:
    <ComponentSet {a: 5, b: 4}>



A ``ComponentSet`` is sort of like itertools.product with some
additional features:

-  ``ComponentSet`` objects have a length if the constituent
   ``Component`` objects have lengths:

   .. code:: python

      In [ 9]: cs = ComponentSet(a=range(5), b=['a', 'b', 'c', 'd'])
      In [10]: len(cs)
      Out[10]:
      20

-  ``ComponentSet`` objects can be positionally indexed:

   .. code:: python

      In [11]: cs[0]
      Out[11]:
      {'a': 0, 'b': 'a'}

      In [12]: cs[1]
      Out[12]:
      {'a': 0, 'b': 'b'}

      In [13]: cs[-1]
      Out[13]:
      {'a': 4, 'b': 'd'}

This is all done without computing the full set of combinations.
``ComponentSet`` objects can be iterated over to retrieve all
combinations:

.. code:: python

   In [14]: for c in cs:
       ...:      print(c)
       ...:
   Out[14]:     
   {'a': 0, 'b': 'a'}
   {'a': 0, 'b': 'b'}
   {'a': 0, 'b': 'c'}
   {'a': 0, 'b': 'd'}
   {'a': 1, 'b': 'a'}
   ...

You can see the performance implications of not producing the full
product by comparing ``len(cs)`` with ``len(list(cs))``:

.. code:: ipython3

    In [15]: %%timeit
        ...:
        ...: len(ComponentSet(a=range(100), b=range(100), c=range(100)))
    Out[15]:
    6.89 µs ± 265 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)


.. code:: ipython3

    In [16]: %%timeit
        ...:
        ...: len(list(ComponentSet(a=range(100), b=range(100), c=range(100))))
    Out[16]:
    1.35 s ± 41.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


| **Q:** that’s cool. can we do anything else with these?
| **A:** Yeah! You can do math!

.. code:: ipython3

    In [17]: a = ComponentSet(a=range(5), b=list('abcd'))
    In [18]: b = ComponentSet(c=range(0, 101, 50))
    In [19]: c = a * b

whoa. what is this?

.. code:: ipython3

    In [20]: c
    Out[20]: 
    <ComponentSet {a: 5, b: 4, c: 3}>



Multiplication: adding a new dimension
--------------------------------------

When you multiply two ``ComponentSet`` objects, the constituent
``Component`` objects are combined into a new ``ComponentSet`` with the
outer product of the constituent components.

.. code:: ipython3

    In [21]: a = ComponentSet(a=range(5), b=list('abcd'))
    In [22]: b = ComponentSet(c=range(0, 101, 50))
    In [23]: c = a * b

.. code:: ipython3

    In [24]: len(c)
    Out[24]:
    60

.. code:: ipython3

    In [25]: c[0]
    Out[25]:
    {'a': 0, 'b': 'a', 'c': 0}

.. code:: ipython3

    In [26]: c[-1]
    Out[26]:
    {'a': 4, 'b': 'd', 'c': 100}



.. code:: ipython3

    In [27]: list(c)
    Out[27]: 
    [{'a': 0, 'b': 'a', 'c': 0},
     {'a': 0, 'b': 'a', 'c': 50},
     {'a': 0, 'b': 'a', 'c': 100},
     {'a': 0, 'b': 'b', 'c': 0},
     {'a': 0, 'b': 'b', 'c': 50},
     {'a': 0, 'b': 'b', 'c': 100},
     {'a': 0, 'b': 'c', 'c': 0},
     {'a': 0, 'b': 'c', 'c': 50},
     {'a': 0, 'b': 'c', 'c': 100},
     {'a': 0, 'b': 'd', 'c': 0},
     {'a': 0, 'b': 'd', 'c': 50},
     {'a': 0, 'b': 'd', 'c': 100},
     {'a': 1, 'b': 'a', 'c': 0},
     {'a': 1, 'b': 'a', 'c': 50},
     {'a': 1, 'b': 'a', 'c': 100},
     {'a': 1, 'b': 'b', 'c': 0},
     {'a': 1, 'b': 'b', 'c': 50},
     {'a': 1, 'b': 'b', 'c': 100},
     {'a': 1, 'b': 'c', 'c': 0},
     {'a': 1, 'b': 'c', 'c': 50},
     {'a': 1, 'b': 'c', 'c': 100},
     {'a': 1, 'b': 'd', 'c': 0},
     {'a': 1, 'b': 'd', 'c': 50},
     {'a': 1, 'b': 'd', 'c': 100},
     {'a': 2, 'b': 'a', 'c': 0},
     {'a': 2, 'b': 'a', 'c': 50},
     {'a': 2, 'b': 'a', 'c': 100},
     {'a': 2, 'b': 'b', 'c': 0},
     {'a': 2, 'b': 'b', 'c': 50},
     {'a': 2, 'b': 'b', 'c': 100},
     {'a': 2, 'b': 'c', 'c': 0},
     {'a': 2, 'b': 'c', 'c': 50},
     {'a': 2, 'b': 'c', 'c': 100},
     {'a': 2, 'b': 'd', 'c': 0},
     {'a': 2, 'b': 'd', 'c': 50},
     {'a': 2, 'b': 'd', 'c': 100},
     {'a': 3, 'b': 'a', 'c': 0},
     {'a': 3, 'b': 'a', 'c': 50},
     {'a': 3, 'b': 'a', 'c': 100},
     {'a': 3, 'b': 'b', 'c': 0},
     {'a': 3, 'b': 'b', 'c': 50},
     {'a': 3, 'b': 'b', 'c': 100},
     {'a': 3, 'b': 'c', 'c': 0},
     {'a': 3, 'b': 'c', 'c': 50},
     {'a': 3, 'b': 'c', 'c': 100},
     {'a': 3, 'b': 'd', 'c': 0},
     {'a': 3, 'b': 'd', 'c': 50},
     {'a': 3, 'b': 'd', 'c': 100},
     {'a': 4, 'b': 'a', 'c': 0},
     {'a': 4, 'b': 'a', 'c': 50},
     {'a': 4, 'b': 'a', 'c': 100},
     {'a': 4, 'b': 'b', 'c': 0},
     {'a': 4, 'b': 'b', 'c': 50},
     {'a': 4, 'b': 'b', 'c': 100},
     {'a': 4, 'b': 'c', 'c': 0},
     {'a': 4, 'b': 'c', 'c': 50},
     {'a': 4, 'b': 'c', 'c': 100},
     {'a': 4, 'b': 'd', 'c': 0},
     {'a': 4, 'b': 'd', 'c': 50},
     {'a': 4, 'b': 'd', 'c': 100}]


Addition: creating a new MultiComponentSet
------------------------------------------

Adding two ``ComponentSet`` objects can be used when combining two
objects with similar dimensions but different labels within those
dimensions.

For example, the following ComponentSets are both indexed by ``a`` and
``b``, but there is no overlap *along* these dimensions:

.. code:: ipython3

    In [28]:  = ComponentSet(a=range(5), b=list('abcd'))
    In [29]: b = ComponentSet(a=range(10, 15), b=list('wxyz'))
    
    In [30]: ab = a + b

.. code:: ipython3

    In [31]: ab
    Out[31]:
    <MultiComponentSet [{a: 5, b: 4}, {a: 5, b: 4}]>



Instead of adding a new dimension or extending each dimension, addition
creates a new type of object, which is essentially a concatenated list
of ``ComponentSet`` objects

The ``MultiComponentSet`` has a length equal to the sum of the lengths
of the constituent ``Componentset`` objects, and on iteration, the
result simply proceeds thorugh each of the constituent ComponentSets.

.. code:: ipython3

    In [32]: len(a), len(b)
    Out[32]:
    (20, 20)



.. code:: ipython3

    In [33]: len(ab)
    Out[33]:
    40



.. code:: ipython3

    In [34]: list(ab)
    Out[34]:
    [{'a': 0, 'b': 'a'},
     {'a': 0, 'b': 'b'},
     {'a': 0, 'b': 'c'},
     {'a': 0, 'b': 'd'},
     {'a': 1, 'b': 'a'},
     {'a': 1, 'b': 'b'},
     {'a': 1, 'b': 'c'},
     {'a': 1, 'b': 'd'},
     {'a': 2, 'b': 'a'},
     {'a': 2, 'b': 'b'},
     {'a': 2, 'b': 'c'},
     {'a': 2, 'b': 'd'},
     {'a': 3, 'b': 'a'},
     {'a': 3, 'b': 'b'},
     {'a': 3, 'b': 'c'},
     {'a': 3, 'b': 'd'},
     {'a': 4, 'b': 'a'},
     {'a': 4, 'b': 'b'},
     {'a': 4, 'b': 'c'},
     {'a': 4, 'b': 'd'},
     {'a': 10, 'b': 'w'},
     {'a': 10, 'b': 'x'},
     {'a': 10, 'b': 'y'},
     {'a': 10, 'b': 'z'},
     {'a': 11, 'b': 'w'},
     {'a': 11, 'b': 'x'},
     {'a': 11, 'b': 'y'},
     {'a': 11, 'b': 'z'},
     {'a': 12, 'b': 'w'},
     {'a': 12, 'b': 'x'},
     {'a': 12, 'b': 'y'},
     {'a': 12, 'b': 'z'},
     {'a': 13, 'b': 'w'},
     {'a': 13, 'b': 'x'},
     {'a': 13, 'b': 'y'},
     {'a': 13, 'b': 'z'},
     {'a': 14, 'b': 'w'},
     {'a': 14, 'b': 'x'},
     {'a': 14, 'b': 'y'},
     {'a': 14, 'b': 'z'}]



Math with MultiComponentSets
----------------------------

Works just like you’d expect! Multiplication applies to each consitutent
ComponentSet, Addition nests MultiComponentSets.

.. code:: ipython3

    In [35]: d1 = ComponentSet(d=['first', 'second'])

.. code:: ipython3

    In [36]: ab
    Out[36]:
    <MultiComponentSet [{a: 5, b: 4}, {a: 5, b: 4}]>



.. code:: ipython3

    In [37]: ab*d1
    Out[37]:
    <MultiComponentSet [{a: 5, b: 4, d: 2}, {a: 5, b: 4, d: 2}]>



.. code:: ipython3

    In [38]: d2 = ComponentSet(d=['third', 'fourth'])

.. code:: ipython3

    In [39]: e = ComponentSet(e=['another'])

.. code:: ipython3

    In [40]: abdde = ((ab * d1) + (ab * d2)) * e
    In [41]: abdde
    Out[41]:
    <MultiComponentSet [[{a: 5, b: 4, d: 2, e: 1}, {a: 5, b: 4, d: 2, e: 1}], [{a: 5, b: 4, d: 2, e: 1}, {a: 5, b: 4, d: 2, e: 1}]]>



.. code:: ipython3

    In [42]: len(abdde)
    Out[42]:
    160



.. code:: ipython3

    In [43]: abdde[0]
    Out[43]:
    {'a': 0, 'b': 'a', 'd': 'first', 'e': 'another'}



.. code:: ipython3

    In [44]: abdde[-1]
    Out[44]:
    {'a': 14, 'b': 'z', 'd': 'fourth', 'e': 'another'}



ComponentSets with exhaustible generators
-----------------------------------------

ComponentSet objects can be used with generators, but the length and
indexing features will not work:

.. code:: ipython3

    In [45]: with_generator = ComponentSet(gen=(i for i in [1, 2, 3, 4]))

.. code:: ipython3

    In [46]: with_generator
    Out[46]:
    <ComponentSet {gen: (...)}>



The following would return an error:

.. code:: ipython3

   In [47]: len(with_generator)
   ---------------------------------------------------------------------------
   TypeError                                 Traceback (most recent call last)
   <ipython-input-32-028f83238a52> in <module>
   ----> 1 len(with_generator)

   <ipython-input-1-2d6ab0f3cd2e> in __len__(self)
        69 
        70     def __len__(self):
   ---> 71         return product(map(len, self._sets.values()))
        72 
        73     def __iter__(self):

   <ipython-input-1-2d6ab0f3cd2e> in product(arr)
         4 
         5 def product(arr):
   ----> 6     return reduce(lambda x, y: x * y, arr, 1)
         7 
         8 def cumprod(arr):

   <ipython-input-1-2d6ab0f3cd2e> in __len__(self)
        20 
        21     def __len__(self):
   ---> 22         return len(self._values)
        23 
        24     def __iter__(self):

   TypeError: object of type 'generator' has no len()

but this can still be iterated over:

.. code:: ipython3

    In [48]: list(with_generator)
    Out[48]:
    [{'gen': 1}, {'gen': 2}, {'gen': 3}, {'gen': 4}]



as it’s a generator, the list is exhausted on use:

.. code:: ipython3

    In [49]: list(with_generator)
    Out[49]:
    []



Use with dask
-------------

ComponentSet and MultiComponentSet objects can be used with many
queueing libraries, including dask

.. code:: ipython3

    In [50]: import dask.distributed as dd

.. code:: ipython3

    In [51]: client = dd.Client()
    In [52]: client

.. raw:: html

    <table style="border: 2px solid white;">
    <tr>
    <td style="vertical-align: top; border: 0px solid white">
    <h3>Client</h3>
    <ul>
      <li><b>Scheduler: </b>tcp://127.0.0.1:50567
      <li><b>Dashboard: </b><a href='http://127.0.0.1:8787/status' target='_blank'>http://127.0.0.1:8787/status</a>
    </ul>
    </td>
    <td style="vertical-align: top; border: 0px solid white">
    <h3>Cluster</h3>
    <ul>
      <li><b>Workers: </b>4</li>
      <li><b>Cores: </b>4</li>
      <li><b>Memory: </b>8.59 GB</li>
    </ul>
    </td>
    </tr>
    </table>



.. code:: ipython3

    In [53]: def do_something(kwargs):
        ...:     import time
        ...:     import random
        ...:     time.sleep(random.random())
        ...:     return str(kwargs)

.. code:: ipython3

    In [54]: futures = client.map(do_something, abdde)
    In [55]: dd.progress(futures)
    Out[55]:
    VBox()


A real-world example
--------------------

parameterizing operations over multiple incompatible climate model,
year, and scenario combinations

Global climate model outputs from CMIP5 simulations typically have an
incompatible set of historical and projection years, ensemble members,
and even models, as some models are run with some scenario and ensemble
combinations, and others do not. At the same time, you may wish to do
the same operation across all the existing model years, and would like
to manage the runs with a single job generator.

This can be easily handled by building a MultiComponentset:

.. code:: ipython3

    In [56]: hist = Constant(rcp='historical', model='obs')
    In [57]: hist_years = ComponentSet(year=list(range(1950, 2006)))

.. code:: ipython3

    In [58]: rcp45 = ComponentSet(
        ...:     rcp=['rcp45'],
        ...:     model=(
        ...:         ['ACCESS1-0', 'CCSM4']
        ...:         + ['pattern{}'.format(i) for i in [1, 2, 3, 5, 6, 27, 28, 29, 30, 31, 32]]))
    
    In [59]: rcp85 = ComponentSet(
        ...:     rcp=['rcp85'],
        ...:     model=(
        ...:         ['ACCESS1-0', 'CCSM4']
        ...:         + ['pattern{}'.format(i) for i in [1, 2, 3, 4, 5, 6, 28, 29, 30, 31, 32, 33]]))
    
    In [60]: proj_years = ComponentSet(year=list(range(2006, 2100)))

Jobs can also be added into the parameterization

.. code:: ipython3

    In [61]: days_under = Constant(func = lambda x, thresh: x <= thresh, threshold=32)
    In [62]: days_over = ComponentSet(func = [lambda x, thresh: x >= thresh], threshold=[90, 95])

The entire job set is the sum of valid (model \* model years), the
entire set of which is run for each job specification:

.. code:: ipython3

    In [63]: runs = ((hist * hist_years) + ((rcp45 + rcp85) * proj_years)) * (days_under + days_over)

.. code:: ipython3

    In [64]: runs
    Out[64]:
    <MultiComponentSet [[{rcp: 1, model: 1, year: 56, func: 1, threshold: 1}, {rcp: 1, model: 1, year: 56, func: 1, threshold: 2}], [[{rcp: 1, model: 13, year: 94, func: 1, threshold: 1}, {rcp: 1, model: 13, year: 94, func: 1, threshold: 2}], [{rcp: 1, model: 14, year: 94, func: 1, threshold: 1}, {rcp: 1, model: 14, year: 94, func: 1, threshold: 2}]]]>



.. code:: ipython3

    In [65]: len(runs)
    Out[65]:
    7782



The different job specifications can be examined to make sure the job
was built the way you expect:

.. code:: ipython3

    In [66]: runs[0]
    Out[66]:
    {'rcp': 'historical',
     'model': 'obs',
     'year': 1950,
     'func': <function __main__.<lambda>(x, thresh)>,
     'threshold': 32}



.. code:: ipython3

    In [67]: runs[55]
    Out[67]:
    {'rcp': 'historical',
     'model': 'obs',
     'year': 2005,
     'func': <function __main__.<lambda>(x, thresh)>,
     'threshold': 32}



.. code:: ipython3

    In [68]: runs[56]
    Out[68]:
    {'rcp': 'historical',
     'model': 'obs',
     'year': 1950,
     'func': <function __main__.<lambda>(x, thresh)>,
     'threshold': 90}



.. code:: ipython3

    In [69]: runs[167]
    Out[69]:
    {'rcp': 'historical',
     'model': 'obs',
     'year': 2005,
     'func': <function __main__.<lambda>(x, thresh)>,
     'threshold': 95}



.. code:: ipython3

    In [70]: runs[168]
    Out[70]:
    {'rcp': 'rcp45',
     'model': 'ACCESS1-0',
     'year': 2006,
     'func': <function __main__.<lambda>(x, thresh)>,
     'threshold': 32}



.. code:: ipython3

    In [71]: runs[261]
    Out[71]:
    {'rcp': 'rcp45',
     'model': 'ACCESS1-0',
     'year': 2099,
     'func': <function __main__.<lambda>(x, thresh)>,
     'threshold': 32}



.. code:: ipython3

    In [72]: runs[262]
    Out[72]:
    {'rcp': 'rcp45',
     'model': 'CCSM4',
     'year': 2006,
     'func': <function __main__.<lambda>(x, thresh)>,
     'threshold': 32}



.. code:: ipython3

    In [73]: runs[3833]
    Out[73]:
    {'rcp': 'rcp45',
     'model': 'pattern32',
     'year': 2099,
     'func': <function __main__.<lambda>(x, thresh)>,
     'threshold': 95}



.. code:: ipython3

    In [74]: runs[3834]
    Out[74]:
    {'rcp': 'rcp85',
     'model': 'ACCESS1-0',
     'year': 2006,
     'func': <function __main__.<lambda>(x, thresh)>,
     'threshold': 32}



.. code:: ipython3

    In [75]: runs[-1]
    Out[75]:
    {'rcp': 'rcp85',
     'model': 'pattern33',
     'year': 2099,
     'func': <function __main__.<lambda>(x, thresh)>,
     'threshold': 95}



This entire set can be run using a single call

.. code:: ipython3

    In [76]: def do_something_fast(kwargs):
        ...:     return str(kwargs)

.. code:: ipython3

    In [77]: futures = client.map(do_something_fast, runs)
    In [78]: dd.progress(futures)
    Out[78]:
    VBox()


.. code:: ipython3

    In [79]: client.gather(futures[-1])
    Out[79]:
    "{'rcp': 'rcp85', 'model': 'pattern33', 'year': 2099, 'func': <function <lambda> at 0x10f4c9400>, 'threshold': 95}"

