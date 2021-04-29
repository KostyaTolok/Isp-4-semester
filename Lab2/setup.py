from setuptools import setup

setup(
    name="Serializers",
    version='1.0.4',
    author="Kostya Tolok",
    packages=['serializers.json', 'serializers.yaml', 'serializers.toml',
              'serializers.pickle', 'serializers.abstract_serializer',
              'serializers.serializer_factory', 'converter', 'log'],
    install_requires=['pytomlpp==0.3.5', 'PyYAML==5.3.1'],
    scripts=['serialize'],
    url="https://github.com/KostyaTolok/Serializers",
    tests_require=['pytest']
)
