from typing import Dict, List

from evalexpr import evalexpr, lam
from structops import makestruct


def handle_define(gc, code):
    maybename = code[1]
    if code[0] == "define-struct":
        return makestruct(gc, {}, code)
    if type(maybename) == str:
        return parsevariable(gc, code)
    else:
        return parsefunction(gc, code)


def parsevariable(context: Dict, code: List) -> Dict:  # return context updated (define f 2)
    name = code[1]
    value = code[2]
    if type(name) != str:
        raise Exception("racket doesnt allow dynamic naming of identifers: %s" % name)

    if name in context:
        raise Exception("tried to double define %s" % name)
    if type(value) == str:
        context[name] = value
        return context
    elif type(value) == list:
        # need to evaluate this :/
        refinedvalue = evalexpr(context, [], value)
        context[name] = refinedvalue
        return context
    else:
        raise Exception(f"tried to assign nonsense {value} to {name}")


def parsefunction(context: Dict, code: List) -> Dict:  # returns context updated (define (f _____) )
    params = code[1]
    body = code[2]
    name = params.pop(0)
    if len(params) == 0:
        raise Exception("need a non-zero number of parameters for function: %s" % name)
    if name in context:
        raise Exception("tried to double define function %s" % name)
    context[name] = lam(context,[], params, body)
    return context
