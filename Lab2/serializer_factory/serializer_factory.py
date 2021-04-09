from _json_.json_serializer import JsonSerializer
from _yaml_.yaml_serializer import YamlSerializer
from _toml_.toml_serializer import TomlSerializer
from _pickle_.pickle_serializer import PickleSerializer
from abstract_serializer.abstract_serializer import Serializer


class SerializerFactory:

    def __init__(self):
        self.serializers = {}
        self.register_format("json", JsonSerializer)
        self.register_format("yml", YamlSerializer)
        self.register_format("toml", TomlSerializer)
        self.register_format("pickle", PickleSerializer)

    def register_format(self, form: str, serializer: Serializer.__subclasses__()):
        if form in self.serializers.keys():
            raise ValueError(f"Key {form} is already contained in serializers")
        elif serializer not in Serializer.__subclasses__():
            raise ValueError(f"Serializer is incorrect")
        self.serializers[form] = serializer

    def get_serializer(self, form: str):
        serializer = self.serializers.get(form)
        if not serializer:
            raise ValueError(f"Key {form} isn't contained in serializers")
        return serializer()
