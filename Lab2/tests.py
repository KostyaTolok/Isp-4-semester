import pytest
from serializer_factory.serializer_factory import SerializerFactory
from student import *


factory = SerializerFactory()

name2 = "Slava"


def function(name):
    print(f"Hello, {name} and {name2}")


def do_test_obj(form: str):
    serializer = factory.get_serializer(form)
    student = Student("Kostya", "Tolok")
    obj = serializer.loads(serializer.dumps(student))
    assert obj.name == student.name
    assert obj.surname == student.surname
    serializer.dump(student, "students." + form)
    obj_file = serializer.load("students." + form)
    assert obj_file.name == student.name
    assert obj_file.surname == student.surname


def do_complex_test_obj(form: str):
    serializer = factory.get_serializer(form)
    student = Student("Kostya", "Tolok")
    student.grades = [10, 9, 5]
    student.tup = (3, 4, 6)
    student.set = {33, 5, 6}
    student.dictionary = {"Monday": 12, "Tuesday": 55}
    student.teacher = Student("Vyacheslav", "Zakharchuk")
    obj = serializer.loads(serializer.dumps(student))
    assert obj.name == student.name
    assert obj.surname == student.surname
    assert obj.grades == student.grades
    assert obj.dictionary == student.dictionary
    assert obj.teacher.name == student.teacher.name
    assert obj.teacher.surname == student.teacher.surname
    serializer.dump(student, "students." + form)
    obj_file = serializer.load("students." + form)
    assert obj_file.name == student.name
    assert obj_file.surname == student.surname
    assert obj_file.grades == student.grades
    assert obj_file.dictionary == student.dictionary
    assert obj_file.teacher.name == student.teacher.name
    assert obj_file.teacher.surname == student.teacher.surname


def do_test_list(form: str):
    serializer = factory.get_serializer(form)
    student = Student("Kostya", "Tolok")
    student.grades = [10, 9, 5]
    student.dictionary = {"Monday": 12, "Tuesday": 55}
    student.teacher = Student("Vyacheslav", "Zakharchuk")
    student2 = Student("Daniil", "Trukhan")
    student2.grades = [6, 6, 6]
    obj_list = serializer.loads(serializer.dumps([student, student2]))
    assert obj_list[0].name == student.name
    assert obj_list[0].surname == student.surname
    assert obj_list[0].grades == student.grades
    assert obj_list[0].dictionary == student.dictionary
    assert obj_list[0].teacher.name == student.teacher.name
    assert obj_list[0].teacher.surname == student.teacher.surname
    assert obj_list[1].name == student2.name
    assert obj_list[1].surname == student2.surname
    assert obj_list[1].grades == student2.grades
    serializer.dump([student, student2], "students." + form)
    obj_list_file = serializer.load("students." + form)
    assert obj_list_file[0].name == student.name
    assert obj_list_file[0].surname == student.surname
    assert obj_list_file[0].grades == student.grades
    assert obj_list_file[0].dictionary == student.dictionary
    assert obj_list_file[0].teacher.name == student.teacher.name
    assert obj_list_file[0].teacher.surname == student.teacher.surname
    assert obj_list_file[1].name == student2.name
    assert obj_list_file[1].surname == student2.surname
    assert obj_list_file[1].grades == student2.grades


def do_test_func(form: str):
    serializer = factory.get_serializer(form)
    obj = serializer.loads(serializer.dumps(function))
    assert function("Kostya") == obj("Kostya")


@pytest.mark.json
def test_json_object():
    do_test_obj("json")


@pytest.mark.json
def test_complex_json_object():
    do_complex_test_obj("json")


@pytest.mark.json
def test_json_list():
    do_test_list("json")


@pytest.mark.json
def test_json_func():
    do_test_func("json")


@pytest.mark.yaml
def test_yaml_object():
    do_test_obj("yml")


@pytest.mark.yaml
def test_yaml_complex_object():
    do_complex_test_obj("yml")


@pytest.mark.yaml
def test_yaml_list():
    do_complex_test_obj("yml")


@pytest.mark.yaml
def test_yaml_func():
    do_test_func("yml")


@pytest.mark.toml
def test_toml_object():
    do_test_obj("toml")


@pytest.mark.toml
def test_toml_complex_object():
    do_complex_test_obj("toml")


@pytest.mark.toml
def test_toml_list():
    do_complex_test_obj("toml")


@pytest.mark.toml
def test_toml_func():
    do_test_func("toml")


@pytest.mark.pickle
def test_pickle_object():
    do_test_obj("pickle")


@pytest.mark.pickle
def test_pickle_complex_object():
    do_complex_test_obj("pickle")


@pytest.mark.pickle
def test_pickle_list():
    do_complex_test_obj("pickle")


@pytest.mark.pickle
def test_pickle_func():
    do_test_func("pickle")
