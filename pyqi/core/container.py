#!/usr/bin/env python

#-----------------------------------------------------------------------------
# Copyright (c) 2013, The BiPy Development Team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
#-----------------------------------------------------------------------------

__credits__ = ["Greg Caporaso", "Daniel McDonald", "Doug Wendel",
               "Jai Ram Rideout"]

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
        raise NotImplementedError("Passthrough cannot issue I/O.")
 
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

class PassthroughIO(Passthrough):
    _reserved = set(['_reserved', 'TypeName', '_reader', '_writer',
                     '_object', 'InPath', 'OutPath','read', 'write',
                     '_load_if_needed', 'Info'])
    TypeName = "PassthroughIO"
     
    def __init__(self, *args, **kwargs):
        super(PassthroughIO, self).__init__(*args, **kwargs)
        
        if 'Object' in kwargs:
            super(PassthroughIO, self).__setattr__('_object',  kwargs['Object'])
        else:
            self._object = None

        if 'InPath' in kwargs:
            super(PassthroughIO, self).__setattr__('InPath',  kwargs['InPath'])
        else:
            self.InPath = None

        if 'OutPath' in kwargs:
            super(PassthroughIO, self).__setattr__('OutPath',  kwargs['OutPath'])
        else:
            self.OutPath = None

    def _load_if_needed(self):
        """Load if the object has not already been loaded"""
        if self._object is None:
            if self.InPath is not None:
                self._object = self._reader(self, self.InPath)
            else:
                raise CannotReadError("No object and InPath is None.")
    
    def read(self):
        """Attempt to read"""
        if self._object is None:
            if self.InPath is None:
                raise CannotReadError("InPath is None.")
            self._object = self._reader(self, self.InPath)

    def write(self):
        """Attempt to write"""
        if self._object is None:
            self._read()
        if self._object is not None:
            if self.OutPath is None:
                raise CannotWriteError("OutPath is None.")
            self._writer(self, self.OutPath)
            self._object = None

class PassthroughRead(PassthroughIO):
    def __init__(self, *args, **kwargs):
        if 'reader' in kwargs:
            super(PassthroughRead, self).__setattr__('_reader', kwargs['reader'])
        else:
            raise ContainerError("A reader is required.")
        super(PassthroughRead, self).__init__(*args, **kwargs)

class PassthroughWrite(PassthroughIO):
    def __init__(self, *args, **kwargs):
        if 'writer' in kwargs:
            super(PassthroughWrite, self).__setattr__('_reader', kwargs['writer'])
        else:
            raise ContainerError("A writer is required.")
        super(PassthroughWrite, self).__init__(*args, **kwargs)

class DelayRead(PassthroughRead):
    """Contain an object and issue IO when an object attribute is requested"""
    TypeName = "DelayRead"
 
class DelayWrite(PassthroughWrite):
    """Contain an object and issue IO with the container is no more"""
    TypeName = "DelayWrite"

    def __del__(self):
        self.write()

class ImmediateRead(PassthroughRead):
    """Issue an immediate read on construction"""
    TypeName = "ImmediateRead"
 
    def __init__(self, *args, **kwargs):
        super(ImmediateRead, self).__init__(*args, **kwargs)
        self.read() 

class ImmediateWrite(PassthroughWrite):
    TypeName = "ImmediateWrite"
 
    def __init__(self, *args, **kwargs):
        super(ImmediateWrite, self).__init__(*args, **kwargs)
        self.write()    

def default_write_str(obj, path):
    f = open(path,'w')
    f.write(str(obj._object))
    f.close()

def default_read_str(obj, path):
    f = open(path)
    return f.read()

def default_write_object(obj, path):
    f = open(path, 'w')
    f.write(repr(obj._object))
    f.close()

def default_read_object(obj, path):
    f = open(path)
    return f.read() # eval isn't safe...

IOType = {'ImmediateRead':ImmediateRead,
            'ImmediateWrite':ImmediateWrite,
            'DelayRead':DelayRead,
            'DelayWrite':DelayWrite}

IOLookup = {str:(default_read_str, default_write_str)}

def WithIO(obj, IO_type=None, IO_lookup=None, **kwargs):
    if IO_type is None:
        raise ContainerError("IO_type is required.")
    
    if IO_type not in IOType:
        raise ContainerError("Unknown IO_type: %s" % IO_type)
    
    if kwargs is None:
        kwargs = {}

    if IO_lookup is None:
        IO_lookup = IOLookup

    obj_type = obj.__class__
    kwargs['Object'] = obj

    if obj_type in IO_lookup:
        reader, writer = IO_lookup[obj_type]
    else:
        reader, writer = default_read_object, default_write_object
    
    kwargs['reader'] = reader
    kwargs['writer'] = writer

    return IOType[IO_type](**kwargs)

def WithoutIO(obj, **kwargs):
    return obj
