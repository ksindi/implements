"""implements library.

:copyright: (c) 2017 by Kamil Sindi.
:license: MIT, see LICENSE for more details.
"""
import inspect

from pkg_resources import get_distribution, DistributionNotFound

__title__ = 'implements'
__author__ = 'Kamil Sindi'
__license__ = 'MIT'
__email__ = 'ksindi@ksindi.com'
try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass

__all__ = ['Interface', 'implements']


class Interface:
    pass


def implements(interface_cls):
    def _decorator(cls):
        verify_methods(interface_cls, cls)
        verify_properties(interface_cls, cls)
        verify_attributes(interface_cls, cls)
        return cls

    return _decorator


def verify_methods(interface_cls, cls):
    methods_predicate = lambda m: inspect.isfunction(m) or inspect.ismethod(m)
    for name, method in inspect.getmembers(interface_cls, methods_predicate):
        signature = inspect.signature(method)
        cls_method = getattr(cls, name, None)
        cls_signature = inspect.signature(cls_method) if cls_method else None
        if cls_signature != signature:
            raise NotImplementedError(
                "'{}' must implement method '{}({})' defined in interface '{}'"
                .format(cls.__name__, name, signature, interface_cls.__name__)
            )


def verify_properties(interface_cls, cls):
    prop_attrs = dict(fget='getter', fset='setter', fdel='deleter')
    for name, prop in inspect.getmembers(interface_cls, inspect.isdatadescriptor):
        cls_prop = getattr(cls, name, None)
        for attr in prop_attrs:
            # instanceof doesn't work for class function comparison
            if type(getattr(prop, attr, None)) != type(getattr(cls_prop, attr, None)):
                raise NotImplementedError(
                    "'{}' must implement a {} for property '{}' defined in interface '{}'"  # flake8: noqa
                    .format(cls.__name__, prop_attrs[attr], name, interface_cls.__name__)
                )


def verify_attributes(interface_cls, cls):
    interface_attributes = get_attributes(interface_cls)
    cls_attributes = get_attributes(cls)
    for missing_attr in (interface_attributes - cls_attributes):
        raise NotImplementedError(
            "'{}' must have class attribute '{}' defined in interface '{}'"
            .format(cls.__name__, missing_attr, interface_cls.__name__)
        )


def get_attributes(cls):
    boring = dir(type('dummy', (object,), {}))
    return set(item[0] for item in inspect.getmembers(cls)
               if item[0] not in boring and not callable(item[1]))
