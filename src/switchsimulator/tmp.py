class parent:

    def __init__(self, a:int) -> None:
        self.a = a

    def add_kid(self, kid: 'child') -> None:
        self.kid = kid


class child(parent):

    def __init__(self, a:int) -> None:
        self.a = a
