"""Extracts microdata from the WikiTree public pages.

>>> from wikitree.public import Person
>>> p = Person('Sloan-518')
>>> p.name
'Clayton Sloan'
"""

import microdata
import urllib.request

from pprint import pformat


class MicrodataView(object):
    """Base class for all WikiTree types.

    Takes care of all generic functionality:
    - Lazy loading of data (only when data is accessed)
    - Unpacking of simple values (e.g. 'name' instead of ['name'])
    - Replacing references to types to callable objects (e.g. a Person object)

    This class is never used directly. Instead, use a type-specific class:
    >>> p = Person('Sloan-518')
    """
    __loaded__ = False
    __data__ = None

    def __init__(self):
        raise NotImplementedError('MicrodataView cannot be used directly. Please use a subclass like Person.')

    def load(self):
        """Retrieves the data for this object from the WikiTree server.
        This happens automatically when any of the properties are accessed.

        >>> p = Person('Sloan-518')
        >>> p.load()
        """
        items = microdata.get_items(urllib.request.urlopen(self.url))
        data = items[0].json_dict()['properties']

        self.__dict__ = self.__process_microdata__(None, data)
        self.__data__ = data
        self.__loaded__ = True

    def __process_microdata__(self, key, data):
        if type(data) == list:
            if len(data) == 1 and key not in __always_lists__:
                return self.__process_microdata__(key, data[0])
            else:
                return [self.__process_microdata__(key, d) for d in data]
        elif key is None or type(data) == dict:
            if 'type' in data:
                if data['type'][0] in __type__mapping__:
                    return __type__mapping__[data['type'][0]](data['properties']['url'][0])
                else:
                    return self.__process_microdata__(key, dict(data['properties']))
            else:
                for k, v in data.items():
                    data[k] = self.__process_microdata__(k, v)

                return data
        else:
            return data

    def __getattr__(self, item):
        if not self.__loaded__:
            self.load()

        return self.__getattribute__(item)

    def __repr__(self):
        if self.__loaded__:
            return pformat(self.__dict__)
        else:
            url = self.url.replace('http://www.wikitree.com/wiki/', '')
            return '<{} {}>'.format(self.__class__.__name__, url)

    def __dir__(self):
        if self.__loaded__:
            return self.__dict__.keys()
        else:
            return self.__keys__


class Person(MicrodataView):
    """Extract Person microdata from a public WikiTree profile.
    A Person object can be created by passing the identifier, or the URL of the person's profile page.

    >>> p = Person('Sloan-518')
    >>> p2 = Person('http://www.wikitree.com/wiki/Carvell-50')

    The data for this person is only retrieved when first accessing any of its properties.
    >>> p.name
    'Clayton Sloan'

    Any references to other persons are returned as Person objects, which makes it easy to retrieve additional details.
    >>> p.children[0].birthDate
    '1922-05-07'
    """
    __keys__ = ['additionalName', 'birth', 'birthDate', 'children', 'death', 'deathDate',
                'familyName', 'gender', 'givenName', 'image', 'marriage', 'name', 'parent',
                'sibling', 'spouse', 'startDate', 'url']

    def __init__(self, url):
        if "http://" in url:
            self.url = url
        elif '/wiki' in url:
            self.url = 'http://www.wikitree.com' + url
        else:
            self.url = 'http://www.wikitree.com/wiki/' + url

__always_lists__ = ['spouse', 'parent', 'marriage', 'children']
__type__mapping__ = {'http://schema.org/Person': Person}

