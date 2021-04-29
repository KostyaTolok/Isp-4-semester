import pytomlpp
from serializers.abstract_serializer.abstract_serializer import Serializer
from converter.converter import to_dict, from_dict


class TomlSerializer(Serializer):

    def dumps(self, obj: object) -> str:
        return pytomlpp.dumps(to_dict(obj))

    def dump(self, obj: object, fp: str):
        with open(fp, "w") as file:
            file.write(self.dumps(obj))

    def loads(self, data: str) -> dict or list:

        return from_dict(pytomlpp.loads(data))

    def load(self, fp) -> dict or list:
        with open(fp, "r") as file:
            return self.loads(file.read())
