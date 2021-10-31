from typing import Dict, List

from casting import tryboolean
from printing import ppt, pttyobj
from profileNode import Profiler, ResultStartEval, ResultEvaluated, ResultCustomEval, EvalAnnotation, RacketDefineError
from shortcuts import boolean, sexpr


class lam:
    def __init__(self, gc: Dict, context: List[Dict], ivar, code: sexpr):
        self.ibindings: List[str] = ivar
        self.execode: sexpr = code
        self.localcontext = context
        self.ppgc = gc

    def exec(self, gc: Dict, params: List, pf_node: Profiler):
        lc = {}
        paramdesc: str = ' '.join(list(map(pttyobj, params)))
        for var in self.ibindings:
            try:
                nextp = params.pop(0)
                lc[var] = nextp
            except:
                raise Exception("failed to resolve parameters for %s" % (self.__str__()))

        pf_updated: Profiler = pf_node.add_event(ResultCustomEval("started eval for: (lambda %s)" % paramdesc))
        return evalexpr(gc, self.localcontext + [lc], self.execode, pf_updated)

    def __str__(self):
        return "(%s (%s) %s)" % (
            chr(955), ' '.join(self.ibindings), softresolve([self.ppgc] + self.localcontext, self.execode))

    def detailed(self):
        return "[%s input function] (%s (%s) %s)" % (len(self.ibindings), chr(955), ' '.join(self.ibindings),
                                                     softresolve([self.ppgc] + self.localcontext, self.execode))


def softresolve(contexs: List[Dict], code: sexpr):
    if type(code) == list:
        # dont try to resolve functions on the offchance its a lambda -_-
        return ppt([code[0]] + list(map(lambda frag: softresolve(contexs, frag), code[1:])))
    elif type(code) == str:
        try:
            val = index(list(contexs), code)
            # print("mapped: %s to %s"%(code, val))
            return pttyobj(val)
        except:
            if code == "lambda":
                return chr(955)
            return code


def index(contexts, identifier):
    while len(contexts) > 0:
        top = contexts.pop()
        if identifier in top:
            return top[identifier]
    raise Exception("couldnt find identifier: " + str(identifier) + " in contexts.")


def constrlam(gc: Dict, lc: List[Dict], code: sexpr, pf_node: Profiler) -> lam:
    # (lam (params) (code))
    params = code[1]
    lambody: sexpr = code[2]
    lambdares: lam = lam(gc, lc, params, lambody)
    pf_node.add_event(ResultEvaluated(code, lambdares))
    return lambdares


def evalexpr(gc: Dict, inner_ctxs: List[Dict], code: sexpr, pf_node: Profiler):
    if type(code) == str:
        try:
            return index([gc] + inner_ctxs, code)
        except:
            return code
    else:
        if code[0] == "if":
            return evalif(gc, inner_ctxs, code, pf_node)
        elif code[0] == "cond":
            return evalcond(gc, inner_ctxs, code, pf_node)
        elif code[0] == "and":
            return evaland(gc, inner_ctxs, code, pf_node)
        elif code[0] == "or":
            return evalor(gc, inner_ctxs, code, pf_node)
        elif code[0] == "lambda" or code[0] == chr(955):  # chr 955 is lambda car
            return constrlam(gc, inner_ctxs, code, pf_node)
        elif code[0] == "local":
            return evallocal(gc, inner_ctxs, code, pf_node)

        else:
            # indexable lambda
            pre_argeval = pf_node.add_event(ResultStartEval(code, "Any"))

            code_eval: List = list(map(lambda frag: evalexpr(gc, inner_ctxs, frag, pre_argeval), code))
            # invoke code_eval[0] as a lambda ... how do we do that :thinking:
            if type(code_eval[0]) == str:
                Profiler(list(pre_argeval.getSinks()),
                         RacketDefineError(code_eval[0],
                                           code_eval[0],
                                           "unable to resolve possibly method: %s" % pttyobj))
                raise Exception("unable to resolve possibly method: %s" % pttyobj(code_eval[0]))
            pre_exec = Profiler(list(pre_argeval.getSinks()), ResultCustomEval("ready to evaluate lambda with %s args" % len(code_eval[1:])))

            val = code_eval[0].exec(gc, code_eval[1:], pre_exec)
            Profiler(list(pre_exec.getSinks()), ResultEvaluated(code_eval, val))
            return val


def evaland(gc: Dict, lc: List[Dict], andparts: List, and_source: Profiler):
    for part in andparts[1:]:  # skip the first part
        val = tryboolean(evalexpr(gc, lc, part, and_source))
        if not val["value"]:
            Profiler(list(and_source.getSinks()),
                     ResultCustomEval("and shortcircuted to false by expr: %s" % (ppt(part))))
            return val
    Profiler(list(and_source.getSinks()), ResultEvaluated(andparts, boolean(True)))
    return boolean(True)


def evalor(gc: Dict, lc: List[Dict], orparts: List, or_source: Profiler):
    for part in orparts[1:]:  # skip the first part
        val = tryboolean(evalexpr(gc, lc, part, or_source))
        if val["value"]:
            Profiler(list(or_source.getSinks()), ResultCustomEval("or shortcircuted to true by expr: %s" % (ppt(part))))
            return val
    Profiler(list(or_source.getSinks()), ResultEvaluated(orparts, boolean(False)))
    return boolean(False)


def evalcond(gc, lc, condparts: List, cond_source: Profiler):
    # (cond [case1] [case2] ... [casen])
    cases = condparts[1:]
    bn = 0
    for case in cases:
        bn += 1
        test = case[0]
        ansiftrue = case[1]
        testres = boolean(True)
        if test != "else":
            testres = tryboolean(evalexpr(gc, lc, test, cond_source))
        if testres["value"]:
            ev_pfnode = Profiler(list(cond_source.getSinks()), ResultCustomEval(
                "evaluating the %sth branch, %s" % (bn, ppt(ansiftrue))))
            condres = evalexpr(gc, lc, ansiftrue, ev_pfnode)
            Profiler(list(ev_pfnode.getSinks()), ResultEvaluated(condparts, condres))
            return condres
    raise Exception("ran through all cases of cond.  all fail.")


def evalif(gc, lc, ifparts, pf_node: Profiler):
    # ifparts [if, test, iftrue, iffalse]
    test = ifparts[1]
    iftrue = ifparts[2]
    iffalse = ifparts[3]
    boolres = tryboolean(evalexpr(gc, lc, test, pf_node.add_event(ResultStartEval(test, "boolean"))))
    post_check_node = list(pf_node.getSinks())[0]

    if boolres["value"]:
        ifres = evalexpr(gc, lc, iftrue, post_check_node)
    else:
        ifres = evalexpr(gc, lc, iffalse, post_check_node)

    final = Profiler(list(post_check_node.getSinks()) + [pf_node],
                     ResultEvaluated(iftrue if boolres["true"] else iffalse,
                                     ifres))  # final sink for if statement, coalesced.
    return ifres


def pvarlocal(gc: Dict, localcontext: List[Dict], code: List, pf_local: Profiler):
    name = code[1]
    value = code[2]
    if type(name) == str:  # shadowing a variable
        if type(value) == str:
            pf_local.add_event(ResultCustomEval("stored value: %s to identifier: %s" % (name, value)))
            return [name, value]
        else:
            pre_local_eval = pf_local.add_event(ResultCustomEval("local complex expr: %s" % (ppt(value))))
            res = evalexpr(gc, localcontext, value, pre_local_eval)
            pre_local_eval.add_event("stored value: %s to identifier %s" % (pttyobj(res), name))
            return [name, res]
    elif type(name) == list:
        body = value
        lamres: lam = lam(gc, localcontext, name[1:], body)
        pf_local.add_event(ResultEvaluated(code, lamres))
        return [name[0], lamres]


def evallocal(gc: Dict, lc: List[Dict], localparts: sexpr, pf_node: Profiler):
    deflist = localparts[1]
    evxp = localparts[2]
    new_context = {}
    pf_local_src: Profiler = pf_node.add_event(ResultStartEval(localparts, "Any"))
    # (local [deflist] evalexpr)
    for defs in deflist:
        toadd = pvarlocal(gc, lc + [new_context], defs, pf_local_src)
        new_context[toadd[0]] = toadd[1]

    pf_local_postdef: Profiler = Profiler(list(pf_local_src.getSinks()),
                                          ResultCustomEval("Got local defintions, ready to eval local."))

    return evalexpr(gc, lc + [new_context], evxp, pf_local_postdef)
