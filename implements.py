# Copyright 2017-2020 Kamil Sindi
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect
import types
import sys

from pkg_resources import get_distribution, DistributionNotFound

__title__ = 'implements'
__author__ = 'Kamil Sindi'
__license__ = 'Apache License, Version 2.0'
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


def getobj_via_dict(cls, name):
    for c in cls.__mro__:
        if name in c.__dict__:
            return c.__dict__[name]
    return None


def is_classmethod(obj):
    if sys.version_info < (3, 7):
        clsmethod_ident = classmethod
    else:
        clsmethod_ident = (classmethod, types.ClassMethodDescriptorType)
    return isinstance(obj, clsmethod_ident)


def is_staticmethod(obj):
    return isinstance(obj, (staticmethod, types.BuiltinMethodType))


def verify_methods(interface_cls, cls):
    methods_predicate = lambda m: inspect.isfunction(m) or inspect.ismethod(m)
    for name, method in inspect.getmembers(interface_cls, methods_predicate):
        signature = inspect.signature(method)
        cls_method = getattr(cls, name, None)
        cls_signature = None
        ifc_name = interface_cls.__name__
        cls_name = cls.__name__
        if cls_method and callable(cls_method):
            cls_signature = inspect.signature(cls_method)
        ifc_obj = getobj_via_dict(interface_cls, name)
        cls_obj = getobj_via_dict(cls, name)

        if is_classmethod(ifc_obj):
            if not is_classmethod(cls_obj):
                raise NotImplementedError(
                    "'{}' must implement '{}' as a classmethod as defined in "
                    "interface '{}'".format(cls_name, name, ifc_name)
                )
        elif is_staticmethod(ifc_obj):
            if not is_staticmethod(cls_obj):
                raise NotImplementedError(
                    "'{}' must implement '{}' as a staticmethod as defined in "
                    "interface '{}'".format(cls_name, name, ifc_name)
                )

        if cls_signature != signature:
            raise NotImplementedError(
                "'{}' must implement method '{}{}' defined in interface '{}'"
                .format(cls_name, name, signature, ifc_name)
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

