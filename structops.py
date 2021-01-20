## struct ops
from casting import trycast, ensure, tryboolean
from evalexpr import evalexpr
from lamstructs import pythoniclam, export_to_lam
from printing import pttyobj
from shortcuts import boolean


def handle_chkxpect(gc, lc, code):
    # (chk-xp left right)
    left = code[1]
    right = code[2]
    leval = evalexpr(gc, lc, left)
    reval = evalexpr(gc, lc, right)
    if equal(leval, reval)["value"]:
        return [True, "[ OK ]", "Both are %s" % (pttyobj(leval))]
    else:
        return [False, "[FAIL]", "left: %s right: %s" % (pttyobj(leval), pttyobj(reval))]


def handle_chksts(gc, lc, code):
    val = code[1]
    tosatisfy = code[2]
    leval = evalexpr(gc, lc, val)
    reval = evalexpr(gc, lc, tosatisfy)
    predres = tryboolean(reval.exec(gc, leval))
    if predres["value"]:
        return [True, "[ OK ]", "Predicate Satisfied."]
    else:
        return [False, "[FAIL]", "Predicate Failed."]


def equal(a, b):
    if type(a) == str and type(b) == str:
        return boolean(a == b)
    elif type(a) == str and type(b) == dict:
        return equal(trycast(a, b["type"]), b)
    elif type(a) == dict and type(b) == str:
        return equal(b, a)
    elif type(a) == dict and type(b) == dict:
        if a["type"] != b["type"] or sorted(list(a.keys())) != sorted(list(b.keys())):
            return boolean(False)
        for key in list(a.keys()):
            v = equal(a[key], b[key])
            if not v["value"]:
                return boolean(False)
        return boolean(True)
    elif type(a) == list and type(b) == list:
        if len(a) != len(b):
            return boolean(False)
        else:
            for eix in range(0, len(a)):
                v = equal(a[eix], b[eix])
                if not v["value"]:
                    return boolean(False)
            return boolean(True)
    else:
        return boolean(a == b)


def makemethod(gc, base, extensions):
    gc["make-%s" % base] = export_to_lam(lambda ls: {"type": base, "const": ls})
    for ext in range(0, len(extensions)):
        gc["%s-%s" % (base, extensions[ext])] = pythoniclam(lambda x, ix=ext: ensure(x, base)["const"][ix],
                                                            "%s-%s" % (base, extensions[ext]))
    return gc


def makestruct(gc, lc, code):
    # (define-struct base [ getters ] )
    base = code[1]
    extensions = code[2]
    gc = regexist(gc, base)
    gc = makemethod(gc, base, extensions)
    return gc


def tryexplode(optcheck, x):
    try:
        optcheck(x)
        return True
    except:
        return False


def regexist(context: dict, name: str, optcheck=None) -> dict:
    if optcheck is None:
        context[name + "?"] = pythoniclam(lambda x: boolean(type(x) == dict and x["type"] == name), name + "?")
    else:
        context[name + "?"] = pythoniclam(lambda x: boolean(tryexplode(optcheck, x)), name + "?")
    return context


equal_exported = pythoniclam(equal, "equal?")
