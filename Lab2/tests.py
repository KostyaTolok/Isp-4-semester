import pytest
from serializers.serializer_factory.serializer_factory import SerializerFactory
from student import *

factory = SerializerFactory()

name2 = "Slava"
arg2 = 4


def function(name):
    print(f"Hello, {name} and {name2}")


def do_test_obj(form: str):
    serializer = factory.get_serializer(form)
    student = Student()
    student.surname = "Tolok"
    obj = serializer.loads(serializer.dumps(student))
    assert obj.name == student.name
    assert obj.surname == student.surname
    assert obj.hello(obj) == student.hello()
    serializer.dump(student, "students." + form)
    obj_file = serializer.load("students." + form)
    assert obj_file.name == student.name
    assert obj_file.surname == student.surname
    assert obj_file.hello(obj) == student.hello()


def do_complex_test_obj(form: str):
    serializer = factory.get_serializer(form)
    student = Student()
    student.surname = "Tolok"
    student.grades = [10, 9, 5]
    student.tup = (3, 4, 6)
    student.set = {33, 5, 6}
    student.dictionary = {"Monday": 12, "Tuesday": 55}
    student.teacher = Student()
    student.teacher.name = "Vyacheslav"
    student.teacher.surname = "Zakharchuk"
    obj = serializer.loads(serializer.dumps(student))
    assert obj.name == student.name
    assert obj.surname == student.surname
    assert obj.grades == student.grades
    assert obj.dictionary == student.dictionary
    assert obj.teacher.name == student.teacher.name
    assert obj.teacher.surname == student.teacher.surname
    assert obj.hello(obj) == student.hello()
    serializer.dump(student, "students." + form)
    obj_file = serializer.load("students." + form)
    assert obj_file.name == student.name
    assert obj_file.surname == student.surname
    assert obj_file.grades == student.grades
    assert obj_file.dictionary == student.dictionary
    assert obj_file.teacher.name == student.teacher.name
    assert obj_file.teacher.surname == student.teacher.surname
    assert obj_file.hello(obj_file) == student.hello()


def do_test_list(form: str):
    serializer = factory.get_serializer(form)
    student = Student()
    student.surname = "Tolok"
    student.grades = [10, 9, 5]
    student.dictionary = {"Monday": 12, "Tuesday": 55}
    student.teacher = Student()
    student.teacher.name = "Vyacheslav"
    student.teacher.surname = "Zakharchuk"
    student2 = Student()
    student2.surname = "Trukhan"
    student2.grades = [float("inf"), 1, False]
    obj_list = serializer.loads(serializer.dumps([student, student2]))
    assert obj_list[0].name == student.name
    assert obj_list[0].surname == student.surname
    assert obj_list[0].grades == student.grades
    assert obj_list[0].dictionary == student.dictionary
    assert obj_list[0].teacher.name == student.teacher.name
    assert obj_list[0].teacher.surname == student.teacher.surname
    assert obj_list[0].hello(obj_list[0]) == student.hello()
    assert obj_list[1].name == student2.name
    assert obj_list[1].surname == student2.surname
    assert obj_list[1].grades == student2.grades
    assert obj_list[1].hello(obj_list[1]) == student2.hello()
    serializer.dump([student, student2], "students." + form)
    obj_list_file = serializer.load("students." + form)
    assert obj_list_file[0].name == student.name
    assert obj_list_file[0].surname == student.surname
    assert obj_list_file[0].grades == student.grades
    assert obj_list_file[0].dictionary == student.dictionary
    assert obj_list_file[0].teacher.name == student.teacher.name
    assert obj_list_file[0].teacher.surname == student.teacher.surname
    assert obj_list_file[0].hello(obj_list_file[0]) == student.hello()
    assert obj_list_file[1].name == student2.name
    assert obj_list_file[1].surname == student2.surname
    assert obj_list_file[1].grades == student2.grades
    assert obj_list_file[1].hello(obj_list_file[1]) == student2.hello()


def do_test_func(form: str):
    serializer = factory.get_serializer(form)
    obj = serializer.loads(serializer.dumps(function))
    assert function("Kostya") == obj("Kostya")
    serializer.dump(function, "students." + form)
    obj = serializer.load("students." + form)
    assert function("Kostya") == obj("Kostya")


def do_test_list_func(form: str):
    function2 = lambda arg1: arg1 ** arg2
    serializer = factory.get_serializer(form)
    obj = serializer.loads(serializer.dumps([function, function2]))
    assert obj[0]("Kostya") == function("Kostya")
    assert obj[1](3) == function2(3)


def do_test_class(form: str):
    cls = Student
    serializer = factory.get_serializer(form)
    obj = serializer.loads(serializer.dumps(cls))
    student = Student()
    student.surname = "Tolok"
    st = obj()
    st.surname = "Tolok"
    assert st.hello() == student.hello()
    assert st.name == student.name


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


@pytest.mark.json
def test_json_list_func():
    do_test_list_func("json")


@pytest.mark.json
def test_json_class():
    do_test_class("json")


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


@pytest.mark.yaml
def test_yaml_list_func():
    do_test_list_func("yml")


@pytest.mark.yaml
def test_yaml_class():
    do_test_class("yml")


@pytest.mark.toml
def test_toml_object():
    do_test_obj("toml")


@pytest.mark.toml
def test_toml_complex_object():
    do_complex_test_obj("toml")


@pytest.mark.toml
def test_toml_func():
    do_test_func("toml")


@pytest.mark.toml
def test_toml_class():
    do_test_class("toml")


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


@pytest.mark.pickle
def test_pickle_list_func():
    do_test_list_func("pickle")


@pytest.mark.pickle
def test_pickle_class():
    do_test_class("pickle")
