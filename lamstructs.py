from typing import Dict, List

from printing import pttyobj
from profileNode import Profiler, ResultCustomEval, ResultEvaluated


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

    def exec(self, gc, params, prof: Profiler):
        pre_exec = prof.add_event(
            ResultCustomEval("executing (%s %s)" % (self.name, ' '.join(list(map(pttyobj, params))))))
        exres = self.method(*params)
        Profiler(list(pre_exec.getSinks()), ResultEvaluated([self.name] + params, exres))
        return exres


class pythonlistlam:
    def __init__(self, llam, name="p-lam"):
        self.method = llam
        self.name = name

    def __str__(self):
        return self.name

    def exec(self, gc, params, prof: Profiler):
        pre_exec = prof.add_event(
            ResultCustomEval("executing (%s %s)" % (self.name, ' '.join(list(map(pttyobj, params))))))
        exres = self.method(params)
        Profiler(list(pre_exec.getSinks()), ResultEvaluated([self.name] + params, exres))
        return exres


class pythonlamwcontext:
    def __init__(self, llam, name="p-lam-wc"):
        self.method = llam
        self.name = name

    def __str__(self):
        return self.name

    def exec(self, gc: Dict, params: List, prof: Profiler):
        pre_exec = prof.add_event(
            ResultCustomEval("executing (%s %s)" % (self.name, ' '.join(list(map(pttyobj, params))))))
        exres = self.method(gc, params)
        Profiler(list(pre_exec.getSinks()), ResultEvaluated([self.name] + params, exres))
        return exres
