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
    forbid_arg  = 'forbid_url'
    timeout_arg = 'url_timeout'

    def __init__(self, base):
        self._base = base
    
    def open(self, uri, **kwargs):
        """ open file handle which is either url or local file path
        """
        try:
            if _is_absolute(uri):
                if not kwargs:  # by default
                    return contextlib.closing(urlopen(uri))

                if self.forbid_arg in kwargs and kwargs[self.forbid_arg] is True:
                    raise InvalidFileReferenceError("not allowed to retrieve external image '{0}'".format(uri))
                elif self.timeout_arg in kwargs and type(kwargs[self.timeout_arg]) is int and kwargs[self.timeout_arg] > 0:
                    url_timeout = kwargs[self.timeout_arg]
                    return contextlib.closing(urlopen(uri, timeout=url_timeout))
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
