from typing import Dict, List

from casting import tryboolean
from printing import ppt, pttyobj
from shortcuts import boolean


class lam:
    def __init__(self, gc, context, ivar, code):
        self.ibindings: List[str] = ivar
        self.execode = code
        self.localcontext = context
        self.ppgc = gc

    def exec(self, gc, params):
        lc = {}
        for var in self.ibindings:
            nextp = params.pop(0)
            lc[var] = nextp
        return evalexpr(gc, self.localcontext + [lc], self.execode)

    def __str__(self):
        return "[%s input function] (lambda (%s) %s)" % (
            len(self.ibindings), ' '.join(self.ibindings), softresolve([self.ppgc] + self.localcontext, self.execode))


def softresolve(contexs, code):
    if type(code) == list:
        return ppt(list(map(lambda frag: softresolve(contexs, frag), code)))
    elif type(code) == str:
        try:
            val = index(list(contexs), code)
            return ppt(val)
        except:
            return code


def index(contexts, identifier):
    while len(contexts) > 0:
        top = contexts.pop()
        if identifier in top:
            return top[identifier]
    raise Exception("couldnt find identifier: " + str(identifier) + " in contexts.")


def constrlam(gc: Dict, lc: List[Dict], code) -> lam:
    # (lam (params) (code))
    params = code[1]
    lambody = code[2]
    return lam(gc, lc, params, lambody)


def evalexpr(gc: Dict, inner_ctxs: List[Dict], code):
    if type(code) == str:
        try:
            return index([gc] + inner_ctxs, code)
        except:
            return code
    else:
        if code[0] == "if":
            return evalif(gc, inner_ctxs, code)
        elif code[0] == "cond":
            return evalcond(gc, inner_ctxs, code)
        elif code[0] == "and":
            return evaland(gc, inner_ctxs, code)
        elif code[0] == "or":
            return evalor(gc, inner_ctxs, code)
        elif code[0] == "lambda":
            return constrlam(gc, inner_ctxs, code)
        elif code[0] == "local":
            return evallocal(gc, inner_ctxs, code)

        else:
            # indexable lambda
            code_eval = list(map(lambda frag: evalexpr(gc, inner_ctxs, frag), code))
            # invoke code_eval[0] as a lambda ... how do we do that :thinking:
            if type(code_eval[0]) == str:
                raise Exception("unable to resolve possibly method: %s" % pttyobj(code_eval[0]))
            return code_eval[0].exec(gc, code_eval[1:])


def evaland(gc, lc, andparts):
    for part in andparts[1:]:  # skip the first part
        val = tryboolean(evalexpr(gc, lc, part))
        if not val["value"]:
            return val
    return boolean(True)


def evalor(gc, lc, andparts):
    for part in andparts[1:]:  # skip the first part
        val = tryboolean(evalexpr(gc, lc, part))
        if val["value"]:
            return val
    return boolean(False)


def evalcond(gc, lc, condparts):
    # (cond [case1] [case2] ... [casen])
    cases = condparts[1:]
    for case in cases:
        test = case[0]
        ansiftrue = case[1]
        testres = boolean(True)
        if test != "else":
            testres = tryboolean(evalexpr(gc, lc, test))
        if testres["value"]:
            return evalexpr(gc, lc, ansiftrue)
    raise Exception("ran through all cases of cond.  all fail.")


def evalif(gc, lc, ifparts):
    # ifparts [if, test, iftrue, iffalse]
    test = ifparts[1]
    iftrue = ifparts[2]
    iffalse = ifparts[3]
    boolres = tryboolean(evalexpr(gc, lc, test))
    if boolres["value"]:
        return evalexpr(gc, lc, iftrue)
    else:
        return evalexpr(gc, lc, iffalse)


def pvarlocal(gc: Dict, localcontext: List[Dict], code: List):
    name = code[1]
    value = code[2]

    if type(value) == str:
        return [name, value]
    else:
        res = evalexpr(gc, localcontext, value)
        return [name, res]


def evallocal(gc, lc, localparts):
    deflist = localparts[1]
    evxp = localparts[2]
    new_context = {}
    # (local [deflist] evalexpr)
    for defs in deflist:
        toadd = pvarlocal(gc, lc + [new_context], defs)
        new_context[toadd[0]] = toadd[1]
    return evalexpr(gc, lc + [new_context], evxp)