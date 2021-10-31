from typing import List, Set

from networkx import DiGraph

from printing import pttyobj, ppt

profID = 0


class ProfEvent:
    def __init__(self):
        global profID
        self.eveid = profID
        profID += 1


def genesis():
    return Profiler([], ResultInitated(["no-racket-expression"]))


class RacketCheckSuccess(ProfEvent):
    def __init__(self, message: str):
        super().__init__()
        self.msg = message

    def __str__(self):
        return self.msg


class EvalAnnotation(ProfEvent):
    def __init__(self, message: str):
        super().__init__()
        self.msg = message

    def __str__(self):
        return self.msg


class RacketDefineError(ProfEvent):
    def __init__(self, defcode: list, maybe_name, info: str):
        super().__init__()
        self.defintion = defcode
        self.name = maybe_name
        self.problem = info

    def __str__(self):
        return self.problem + " for " + ppt(self.defintion)


class RacketDefineSucess(ProfEvent):
    def __init__(self, message: str):
        super().__init__()
        self.msg = message

    def __str__(self):
        return self.msg


class ResultInitated(ProfEvent):
    def __init__(self, orexpr):
        super().__init__()
        self.orexpr = orexpr

    def __str__(self):
        return "evaluating expr: %s" % (ppt(self.orexpr))


class ResultStartEval(ProfEvent):
    def __init__(self, orexpr, ttype: str):
        super().__init__()
        self.orexpr = orexpr
        self.targetType = ttype

    def __str__(self):
        return "evaluating the expr: %s for target type: %s" % (ppt(self.orexpr), self.targetType)


class ResultCustomEval(ProfEvent):
    def __init__(self, message: str):
        super().__init__()
        self.msg = message

    def __str__(self):
        return self.msg


class ResultEvaluated(ProfEvent):
    def __init__(self, orexpr, res):
        super().__init__()
        self.orexpr = orexpr
        self.result = res

    def __str__(self):
        return "evaluated result of: %s to %s" % (ppt(self.orexpr), pttyobj(self.result))


class Profiler:
    def __init__(self, src: List['Profiler'], event: ProfEvent):
        self.source: List[Profiler] = src
        for source in self.source:
            source.registerChild(self)
        self.children: List[Profiler] = []
        self.sinks: Set[Profiler] = set([])
        self.status = "ok"
        self.event = event
        self.profid = self.event.eveid

    def populate(self, nxgraph: DiGraph, tooltip_info: dict):
        tooltip_info[str(self.event.eveid)] = str(self.event)
        for child in self.children:
            childvisited = child.profid in nxgraph.nodes
            nxgraph.add_edges_from([(str(self.event.eveid), str(child.profid))])
            if not childvisited:
                child.populate(nxgraph, tooltip_info)

    def __str__(self):
        return "(number branches: %s) w/ event of %s" % (len(self.children), str(self.event)) + "\n" + '\n'.join(
            map(str, self.children))

    def add_event(self, event: ProfEvent):
        np = Profiler([self], event)
        return np

    def registerChild(self, pf_nn: 'Profiler'):
        self.children.append(pf_nn)
        self.sinks = self.sinks.union(pf_nn.getSinks())

    def getSinks(self) -> Set['Profiler']:
        if not self.children:
            return {self}
        else:
            allsinks = set([])
            if len(self.sinks) == 0:  # shouldnt happen but end all be all
                for child in self.children:
                    allsinks = allsinks.union(child.getSinks())
            else:
                for oldsink in self.sinks:
                    allsinks = allsinks.union(oldsink.getSinks())
            self.sinks = allsinks
            return allsinks

    def getAllTerminals(self) -> Set:
        if len(self.children) == 0:
            return {self}
        else:
            bigset = set([])
            for child in self.children:
                terms = child.getAllTerminals()
                bigset = bigset.union(terms)
            return bigset
