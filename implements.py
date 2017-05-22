"""implements library.

:copyright: (c) 2017 by Kamil Sindi.
:license: MIT, see LICENSE for more details.
"""
import inspect
from pkg_resources import get_distribution, DistributionNotFound

__all__ = ['Interface', 'implements']

__title__ = 'implements'
__author__ = 'Kamil Sindi'
__license__ = 'MIT'
__email__ = 'ksindi@ksindi.com'
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


class Interface:
    pass


def implements(interface_cls):
    def _decorator(cls):
        verify_methods(interface_cls, cls)
        verify_properties(interface_cls, cls)
        return cls

    return _decorator


def verify_methods(src_cls, tgt_cls):
    for name, method in inspect.getmembers(src_cls, inspect.isfunction):
        tgt_signature = inspect.signature(method)
        src_method = getattr(tgt_cls, name, None)
        src_signature = inspect.signature(src_method) if src_method else None
        if src_signature != tgt_signature:
            raise NotImplementedError(
                "Class '{}' must implement method '{}({})' defined in Interface '{}'.".format(
                    tgt_cls.__name__, name, tgt_signature, src_cls.__name__
                ))


def verify_properties(src_cls, tgt_cls):
    prop_attrs = dict(fget='getter', fset='setter', fdel='deleter')
    for name, prop in inspect.getmembers(src_cls, lambda v: hasattr(v, 'fget')):
        impl = getattr(tgt_cls, name, None)
        for attr in prop_attrs:
            # for some reason instanceof doesn't work
            if type(getattr(prop, attr, None)) != type(getattr(impl, attr, None)):
                raise NotImplementedError(
                    "Class '{}' must implement a {} for property '{}' defined in interface '{}'.".format(
                        tgt_cls.__name__, prop_attrs[attr], name, src_cls.__name__))