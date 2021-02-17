class GrandParent:
    x = 10

    def __init__(self):
        self.name = "GrandPa"


def grandparent_func():
    print("in grandparent function")


class Person(GrandParent):
    age = 23
    name = "Adam"

    def __init__(self):
        super(Person, self).__init__()
        self.me = "Anak"

    def parent_func(self):
        pass


person = Person()
print("The age is:", getattr(person, "age"))
print("The age is:", person.age)
print()
