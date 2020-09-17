import os
import contextlib
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class Files(object):

    def __init__(self, base):
        self._base = base
    
    def open(self, uri, forbid_url=False, timeout=0):
        """ open file handle which is either url or local file path
        """
        try:
            if _is_absolute(uri):

                if forbid_url is True:
                    raise NotAllowedAccessError("not allowed to retrieve external image '{0}'".format(uri))
                elif timeout > 0:
                    return contextlib.closing(urlopen(uri, timeout=timeout))
                else:
                    return contextlib.closing(urlopen(uri))
            elif self._base is not None:
                return open(os.path.join(self._base, uri), "rb")
            else:
                raise InvalidFileReferenceError("could not find external image '{0}', fileobj has no name".format(uri))
        except IOError as error:
            message = "could not open external image: '{0}' (document directory: '{1}')\n{2}".format(
                uri, self._base, str(error))
            raise InvalidFileReferenceError(message)


def _is_absolute(url):
    return urlparse(url).scheme != ""


class InvalidFileReferenceError(ValueError):
    pass

class NotAllowedAccessError(ValueError):
    pass