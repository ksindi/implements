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


def implements(interface_cls, *, cache=True):
    if cache:
        pass  # TODO

    def _decorator(cls):
        verify_methods(interface_cls, cls)
        verify_properties(interface_cls, cls)
        return cls

    return _decorator


def verify_methods(interface_cls, cls):
    method_predicate = lambda m: inspect.isfunction(m) or inspect.ismethod(m)
    for name, method in inspect.getmembers(interface_cls, method_predicate):
        interface_signature = inspect.signature(method)
        cls_method = getattr(cls, name, None)
        cls_signature = inspect.signature(cls_method) if cls_method else None
        if cls_signature != interface_signature:
            raise NotImplementedError(
                "Class '{}' must implement method '{}({})' defined in Interface '{}'."
                .format(cls.__name__, name, interface_signature, interface_cls.__name__)
            )


def verify_properties(interface_cls, cls):
    prop_attrs = dict(fget='getter', fset='setter', fdel='deleter')
    for name, prop in inspect.getmembers(interface_cls, inspect.isdatadescriptor):
        cls_prop = getattr(cls, name, None)
        for attr in prop_attrs:
            # for some reason instanceof doesn't class function type comparison
            interface_prop_type = type(getattr(prop, attr, None))
            cls_prop_type = type(getattr(cls_prop, attr, None))
            if interface_prop_type != cls_prop_type:
                raise NotImplementedError(
                    "Class '{}' must implement a {} for property '{}' defined in interface '{}'."
                    .format(cls.__name__, prop_attrs[attr], name, interface_cls.__name__)
                )
