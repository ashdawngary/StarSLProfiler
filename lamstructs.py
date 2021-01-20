from typing import List

from evalexpr import evalexpr


def export_to_lam(execable, name="p-lam"):
    return pythonlistlam(execable, name)


def compose(f, g, name="pc-lam"):
    return pythoniclam(lambda x: f.exec(None, [g.exec(None, [x])]), name)


class pythoniclam:
    def __init__(self, plam, name="pc-lam"):
        self.method = plam
        self.name = name

    def __str__(self):
        return self.name

    def exec(self, gc, params):
        return self.method(*params)


class pythonlistlam:
    def __init__(self, llam, name="p-lam"):
        self.method = llam
        self.name = name

    def __str__(self):
        return self.name

    def exec(self, gc, params):
        return self.method(params)


class pythonlamwcontext:
    def __init__(self, llam, name="p-lam-wc"):
        self.method = llam
        self.name = name

    def __str__(self):
        return self.name

    def exec(self, gc, params):
        return self.method(gc, params)
