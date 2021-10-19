from basic_components import Switch
from logicgates import AND, OR, XOR, NOR

asd = 2

def ho(a=asd, b="None", c="None", d=None):
    print(a)
    print(id(b))
    print(id(c))
    print(id(d))
    c = None
    print(id(c))

asd = 3

ho()

qwe = [2,3]
id(qwe)
qwe.append(4)
id(qwe)


a = ("hi", "du:8", "vogel:1")
b = [x.split(":") for x in a]

"hi".split(":")[0]


def deco(fun):
    def newfun(self):
        print("deco")
        return fun(self)
    return newfun

class mom():
    @deco
    def __init__(self):
        print("mom")

class child(mom):
    def __init__(self):
        print("child")
        super().__init__()

print("start")
child()
print("middle")
mom()
print("stop")


class A():
    @staticmethod
    def asd():
        print("hi")

    def __init__(self) -> None:
        pass

class B(A):
    b = A.asd()

    def __init__(self) -> None:
        super().__init__()



yx = A()

yx.qwe


asd = [2,3,4,5]
setattr(self, input_name, input_circuit)
self.setup()

        old_input = getattr(self, input_name)
        
        input_is_list = isinstance(input_circuit, list)
        if input_is_list:
            for i in range(len(input_circuit)):
                input_circuit[i].forward_connections = old_input[i].forward_connections
        else:
     
{'in_a': {'N': '8'}, 'in_b': {'N': '8'}, 'in_carry': {'N': 1}}



class B:

    def __init__(self) -> None:
        imalist = 3


def fun():
    if True:
        return B()


class A:

    def __init__(self, a=B(), b=B()) -> None:
        self.a=a 
        self.b = b

asd = A()
qwe = A()
asd.a
asd.b
qwe.a
qwe.b


class A:

    def __init__(self, a=fun(), b=fun()) -> None:
        self.a=a 
        self.b = b


asd = A()
qwe = A()
asd.a
asd.b
qwe.a
qwe.b

from singlestatecomp import LooseWire


class D:

    def __init__(self, a=LooseWire(), b=LooseWire()) -> None:
        self.a=a 
        self.b = b

asd = D()
qwe = D()
asd.a
asd.b
qwe.a
qwe.b