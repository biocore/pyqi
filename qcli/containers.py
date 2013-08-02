#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__author__ = "Daniel McDonald"
__copyright__ = "Copyright 2013, The QIIME Project"
__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]
__license__ = "BSD"
__version__ = "0.1.0-dev"
__maintainer__ = "Daniel McDonald"
__email__ = "mcdonadt@colorado.edu"

class ContainerError(Exception):
    pass
 
class CannotReadError(ContainerError):
    pass
 
class CannotWriteError(ContainerError):
    pass
 
class Passthrough(object):
    """Basic pass through container class"""
    _reserved = set(['_reserved','TypeName', 'Info'])
    TypeName = "Passthrough"
    Info = None
 
    def __init__(self, *args, **kwargs):
        if 'Info' in kwargs:
            super(Passthrough, self).__setattr__('Info',  kwargs['Info'])
 
    def _load_if_needed(self):
        raise NotImplementedError("Passthrough cannot issue IO")
 
    def __getattr__(self, attr):
        """Pass through to contained class if the attribute is not recognized"""
        if attr in super(Passthrough, self).__getattribute__('_reserved'):
            return super(Passthrough, self).__getattribute__(attr)
        
        self._load_if_needed()
        
        return getattr(self._object, attr)
 
    def __setattr__(self, attr, val):
        """Pass through to contained class if the attribute is not recognized"""
        if attr in super(Passthrough, self).__getattribute__('_reserved'):
            return super(Passthrough, self).__setattr__(attr, val)
       
        self._load_if_needed()
 
        setattr(self._object, attr, val)
 
    def __hasattr__(self, attr):
        """Pass through to contained class if the attribute is not recognized"""
        if attr in super(Passthrough, self).__getattribute__('_reserved'):
            return True
 
        self._load_if_needed()
        
        return hasattr(self._object, attr)
 
class DelayIO(Passthrough):
    """Contain an object and issue IO when an object attribute is requested"""
    _reserved = set(['_reserved', 'TypeName', '_reader', '_writer',
                     '_object', 'InPath', 'OutPath','read', 'write',
                     '_load_if_needed', 'Info'])
    TypeName = "DelayIO"
    _object = None
    InPath = None
    OutPath = None
    Info = None
 
    def __init__(self, *args, **kwargs):
        super(DelayIO, self).__init__(*args, **kwargs)
        
        if 'Object' in kwargs:
            super(DelayIO, self).__setattr__('_object',  kwargs['Object'])
        if 'InPath' in kwargs:
            super(DelayIO, self).__setattr__('InPath',  kwargs['InPath'])
        if 'OutPath' in kwargs:
            super(DelayIO, self).__setattr__('OutPath',  kwargs['OutPath'])
 
    def _load_if_needed(self):
        """Load if the object has not already been loaded"""
        if self._object is None:
            if self.InPath is not None:
                self._object = self._reader(self.InPath)
            else:
                raise CannotReadError("No object and InPath is None!")
    
    def write(self):
        """Attempted to write"""
        if self._object is not None:
            if self.OutPath is None:
                raise CannotWriteError("OutPath is None!")
            self._writer(self.OutPath)
 
    def read(self):
        """Attempt to read"""
        if self._object is None:
            if self.InPath is None:
                raise CannotReadError("InPath is None!")
            self._object = self._reader(self.InPath)

class ImmediateRead(Passthrough):
    """Issue an immediate read on construction"""
    _reserved = set(['_reserved', 'TypeName', '_reader', '_writer',
                     '_object', 'InPath', 'OutPath','read', 'write',
                     '_load_if_needed', 'Info'])
    TypeName = "ImmediateRead"
    _object = None
    InPath = None
    OutPath = None
    Info = None
 
    def __init__(self, *args, **kwargs):
        super(ImmediateRead, self).__init__(*args, **kwargs)
        
        if 'Object' in kwargs:
            super(ImmediateRead, self).__setattr__('_object',  kwargs['Object'])
        if 'InPath' in kwargs:
            super(ImmediateRead, self).__setattr__('InPath',  kwargs['InPath'])
        if 'OutPath' in kwargs:
            super(ImmediateRead, self).__setattr__('OutPath',  kwargs['OutPath'])
        
        self.read()

    def read(self):
        """Attempt to read"""
        if self._object is None:
            if self.InPath is None:
                raise CannotReadError("InPath is None!")
            self._object = self._reader(self.InPath)

class ImmediateWrite(Passthrough):
    _reserved = set(['_reserved', 'TypeName', '_reader', '_writer',
                     '_object', 'InPath', 'OutPath','read', 'write',
                     '_load_if_needed', 'Info'])
    TypeName = "ImmediateWrite"
    _object = None
    InPath = None
    OutPath = None
    Info = None
 
    def __init__(self, *args, **kwargs):
        super(ImmediateWrite, self).__init__(*args, **kwargs)
        
        if 'Object' in kwargs:
            super(ImmediateWrite, self).__setattr__('_object',  kwargs['Object'])
        if 'InPath' in kwargs:
            super(ImmediateWrite, self).__setattr__('InPath',  kwargs['InPath'])
        if 'OutPath' in kwargs:
            super(ImmediateWrite, self).__setattr__('OutPath',  kwargs['OutPath'])
        
        self.write()

    def write(self):
        """Attempt to write"""
        if self._object is not None:
            if self.OutPath is None:
                raise CannotWriteError("OutPath is None!")
            self._writer(self.OutPath)
