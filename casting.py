from typing import Any, Dict

from printing import pttyobj
from shortcuts import string, num, boolean, symbol


def ensure(x: Any, t: str) -> Any:
    if type(x) == dict and x["type"] == t:
        return x
    else:
        raise Exception("failed to ensure %s was of type %s" % (pttyobj(x), t))


def trysymbol(maybesym):
    if type(maybesym) == dict:
        if maybesym['type'] == "symbol":
            return maybesym
        else:
            raise Exception("tried to cast %s to str" % maybesym)
    elif type(maybesym) == str:
        if maybesym[0] == "\'":
            return symbol(maybesym)
        else:
            raise Exception("try to cast %s to symbol, but it doesnt start with a quote" % maybesym)
    else:
        raise Exception("got nonsense %s for symbol" % maybesym)


def trystring(maybestr):
    if type(maybestr) == dict:
        if maybestr['type'] == "string":
            return maybestr
        else:
            raise Exception("tried to cast %s to str" % maybestr)
    elif type(maybestr) == str:
        if len(maybestr) < 2 or maybestr[0] != "\"" or maybestr[-1] != "\"":
            raise Exception("tried to cast %s to a str, but its malformed." % maybestr)
        else:
            return string(maybestr[1:-1])
    else:
        raise Exception("got nonsense %s for string" % maybestr)


def trynum(maybenum):
    if type(maybenum) == dict:
        if maybenum["type"] == "number":
            return maybenum
        else:
            raise Exception("tried to cast %s to num" % maybenum)
    elif type(maybenum) == str:
        try:
            return num(float(maybenum))
        except:
            raise Exception("failed to cast %s to num" % maybenum)
    else:
        raise Exception("got nonsense in trynum eval: " % maybenum)


def tryboolean(maybebool) -> Dict:
    if type(maybebool) == dict:
        if maybebool["type"] == "boolean":
            return maybebool
        else:
            raise Exception("tried to cast %s to boolean" % maybebool)
    elif type(maybebool) == str:
        if maybebool in ["#t", "#true"]:
            return boolean(True)
        elif maybebool in ["#f", "#false"]:
            return boolean(False)
        else:
            raise Exception("tried to cast %s to boolean" % maybebool)
    else:
        raise Exception("got nonsense in tryboolean eval: %s " % maybebool)


def trycast(interpretive, targettype: str):
    if targettype == "string":
        return trystring(interpretive)
    elif targettype == "number":
        return trynum(interpretive)
    elif targettype == "boolean":
        return tryboolean(interpretive)
    elif targettype == "symbol":
        return trysymbol(interpretive)
    else:
        raise Exception("cant cast %s to type %s" % (interpretive, targettype))
