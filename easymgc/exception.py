import sys
from easymgc import _encodings, _unicode_encode, _unicode_decode

class EasyException(Exception):
    """General superclass for portage exceptions"""
    def __init__(self,value):
        self.value = value[:]
        if isinstance(self.value, basestring):
            self.value = _unicode_decode(self.value,
                encoding=_encodings['content'], errors='replace')

    def __str__(self):
        if isinstance(self.value, basestring):
            return self.value
        else:
            return _unicode_decode(repr(self.value),
                encoding=_encodings['content'], errors='replace')

    if sys.hexversion < 0x3000000:

        __unicode__ = __str__

        def __str__(self):
            return _unicode_encode(self.__unicode__(),
                encoding=_encodings['content'], errors='backslashreplace')

class CommandNotFound(EasyException):
    """A required binary was not available or executable"""

class SignatureException(EasyException):
    """Signature was not present in the checked file"""

class DigestException(SignatureException):
    """A problem exists in the digest"""
