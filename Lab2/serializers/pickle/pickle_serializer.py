import pickle
from serializers.abstract_serializer.abstract_serializer import Serializer
from converter.converter import from_dict, to_dict


class PickleSerializer(Serializer):

    def dumps(self, obj: object) -> bytes:

        return pickle.dumps(to_dict(obj))

    def dump(self, obj: object, fp: str):
        with open(fp, 'wb') as file:
            pickle.dump(to_dict(obj), file)

    def loads(self, data: bytes):
        return from_dict(pickle.loads(data))

    def load(self, fp):
        with open(fp, 'rb') as file:
            return from_dict(pickle.load(file))
