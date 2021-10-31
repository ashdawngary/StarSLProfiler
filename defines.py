from typing import Dict, List

from profileNode import Profiler, RacketDefineError, RacketDefineSucess, genesis
from evalexpr import evalexpr, lam
from printing import pttyobj
from structops import makestruct


def handle_define(gc, code, pf_node: Profiler = genesis()):
    maybename = code[1]
    if code[0] == "define-struct":
        return makestruct(gc, {}, code, pf_node)
    if type(maybename) == str:
        return parsevariable(gc, code, pf_node)
    else:
        return parsefunction(gc, code, pf_node)


def parsevariable(context: Dict, code: List, profiler: Profiler) -> Dict:  # return context updated (define f 2)
    name = code[1]
    value = code[2]
    if type(name) != str:
        profiler.add_event(RacketDefineError(code, name, "racket doesnt allow dynamic naming of identifers:"))
        raise Exception("racket doesnt allow dynamic naming of identifers: %s" % name)

    if name in context:
        raise Exception("tried to double define %s" % name)
    if type(value) == str:
        context[name] = value
        profiler.add_event(RacketDefineSucess("added the name: %s w/ value %s to context." % name, value))
        return context
    elif type(value) == list:
        # need to evaluate this :/
        refinedvalue = evalexpr(context, [], value, profiler)
        profiler.add_event(RacketDefineSucess("Successfully evaled for %s to val %s" % (name, pttyobj(refinedvalue))))
        context[name] = refinedvalue
        return context
    else:
        profiler.add_event(RacketDefineError(code, name, f"tried to assign nonsense {value} to {name}"))
        raise Exception(f"tried to assign nonsense {value} to {name}")


def parsefunction(context: Dict, code: List, profiler: Profiler) -> Dict:  # returns context updated (define (f _____) )
    params = code[1]
    body = code[2]
    name = params.pop(0)
    if len(params) == 0:
        profiler.add_event(RacketDefineError(code, name, "need a non-zero number of parameters for the function."))
        raise Exception("need a non-zero number of parameters for function: %s" % name)
    if name in context:
        profiler.add_event(RacketDefineError(code, name, "tried to double define function %s " % name))
        raise Exception("tried to double define function %s" % name)
    context[name] = lam(context, [], params, body)
    profiler.add_event(RacketDefineSucess("succesfully inst. %s" % name))
    return context
