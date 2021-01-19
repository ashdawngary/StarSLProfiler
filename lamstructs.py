from typing import List

from evalexpr import evalexpr


def export_to_lam(execable):
    return pythonlistlam(execable)


def compose(f, g):
    return pythoniclam(lambda x: f.exec(None, [g.exec(None, [x])]))

class pythoniclam:
    def __init__(self, plam):
        self.method = plam

    def exec(self, gc, params):
        return self.method(*params)


class pythonlistlam:
    def __init__(self, llam):
        self.method = llam

    def exec(self, gc, params):
        return self.method(params)

class pythonlamwcontext:
    def __init__(self, llam):
        self.method = llam

    def exec(self, gc, params):
        return self.method(gc, params)