from distutils.core import setup

setup(
    name="Serializers",
    version='1.0',
    author="Kostya Tolok",
    packages=['_json_.json_serializer', '_yaml_.yaml_serializer', '_toml_.toml_serializer',
              '_pickle_.pickle_serializer', 'abstract_serializer.abstract_serializer',
              'serializer_factory.serializer_factory', 'converter'],
    url="https://github.com/KostyaTolok/Isp-4-semester/tree/main/Lab2"
)
