import yaml
from converter.converter import to_dict, from_dict

from serializers.abstract_serializer.abstract_serializer import Serializer


class YamlSerializer(Serializer):

    def dumps(self, obj: object, dumper=yaml.Dumper) -> str:
        return yaml.dump(to_dict(obj), Dumper=dumper)

    def dump(self, obj: object, fp: str, dumper=yaml.Dumper):

        with open(fp, "w") as file:
            file.write(self.dumps(obj, dumper=dumper))

    def loads(self, data: str, loader=yaml.FullLoader) -> dict or list:

        return from_dict(yaml.load(data, Loader=loader))

    def load(self, fp: str, loader=yaml.FullLoader) -> dict or list:
        with open(fp, "r") as file:
            return self.loads(file.read(), loader=loader)
