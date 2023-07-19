
import collections


def merge_dicts(*dicts):
    res = collections.OrderedDict()

    for d in dicts:
        for k in d.keys():
            if k in res:
                raise TypeError(f'multiple instances of key {k}')
        res.update(d)
    return res
