from __future__ import with_statement
from copy import deepcopy
import simplejson


def load_file(filename):
    with open(filename) as fp:
        return DotDict(simplejson.load(fp))


def load(fp):
    return DotDict(simplejson.load(fp))


def dump(obj, fp):
    return simplejson.dump(obj, fp, indent=2, sort_keys=True)


#--------------------------------------
class DotDict(dict):
#--------------------------------------

    __getattr__= dict.__getitem__

    def __init__(self, d):
        self.update(**dict((k, self.parse(v))
                           for k, v in d.iteritems()))  # in py3 use .items

    def _asdict(self):
        return self
       
    @classmethod
    def parse(cls, v):
        if isinstance(v, dict):
            return cls(v)
        elif isinstance(v, list):
            return [cls.parse(i) for i in v]
        else:
            return v