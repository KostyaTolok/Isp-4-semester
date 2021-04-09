from abc import abstractmethod


class Serializer(object):
    @abstractmethod
    def dumps(self, obj: object):
        ...

    @abstractmethod
    def dump(self, obj: object, fp: str):
        ...

    @abstractmethod
    def loads(self, data: str):
        ...

    @abstractmethod
    def load(self, fp: str):
        ...
