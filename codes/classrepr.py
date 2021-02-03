#coding:utf-8
class Serializable(object):
    """
    This base class for an object than can be serialized. More specifically,
    such objects can be read from and written into a Python dictionary.
    """

    @classmethod
    def new(cls, dct):
        """Creates a new instance of the object."""
        obj = cls.__new__(cls)
        object.__init__(obj)
        obj.parse(dct)
        return obj

    def build(self, dct):
        """Writes the object into the dictionary."""
        pass

    def parse(self, dct):
        """Reads the object from the dictionary."""
        pass


class Default(Serializable):
    """This object will be serialized using its attributes dictionary."""

    @staticmethod
    def attrs(dct):
        """
        Get a filtered version of an attributes dictionary. This method
        currently simply removes the private attributes of the object.
        """
        return {
            key: val for key, val in dct.items()  # if not key.startswith("_")
        }

    def build_default(self, dct):
        """Write the object to the dictionary."""
        dct.update(Default.attrs(self.__dict__))

    def parse_default(self, dct):
        """Read the object from the dictionary."""
        self.__dict__.update(Default.attrs(dct))


class classlayout(Default):
    def __init__(self):
        # self.ckx = [1, 3, 4, 5]
        # self.ppk = {"a": 1, "b": 2.3, "c": "aaaa"}
        # self.offsetdict = {}
        pass
        # self.baseoffsetdict = {}

    def build(self, dct):
        self.build_default(dct)
        return dct

    def parse(self, dct):
        self.parse_default(dct)
        return self

    def __repr__(self):
        """
        Return a textual representation of the object. It will mainly be used
        for pretty-printing into the console.
        """
        attrs = u", ".join(
            [
                u"{}={}".format(key, val)
                for key, val in Default.attrs(self.__dict__).items()
            ]
        )
        return u"{}({})".format(self.__class__.__name__, attrs)


class classcollections(dict, Default):
    pass
    # def __getattr__(self, key):
    #     return self[key]


class overridevf(Default):
    def __init__(self, methodename, parentname, itselfname):
        self.methodname = methodename
        self.parent = parentname
        self.itself = itselfname
        self.accesslist = []

    def __repr__(self):
        """
        Return a textual representation of the object. It will mainly be used
        for pretty-printing into the console.
        """
        attrs = u", ".join(
            [
                u"{}={}".format(key, val)
                for key, val in Default.attrs(self.__dict__).items()
            ]
        )
        return u"{}({})".format(self.__class__.__name__, attrs)

    def set_accessname(self):
        for accessfield in self.accesslist:
            accessfield.set_variablename()

    def build(self, dct):
        self.build_default(dct)
        return dct

    def parse(self, dct):
        self.parse_default(dct)
        return self


# class overridevfcollection
class overridevfcollection():
    def __init__(self):
        self.overridevfdict = {}
