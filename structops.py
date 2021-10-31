## struct ops
from profileNode import Profiler, RacketDefineSucess, ResultInitated, RacketCheckSuccess, ResultCustomEval
from casting import trycast, ensure, tryboolean
from evalexpr import evalexpr
from lamstructs import pythoniclam, export_to_lam
from printing import pttyobj
from shortcuts import boolean


def handle_chkxpect(gc, lc, code, prof: Profiler):
    # (chk-xp left right)
    left = code[1]
    right = code[2]

    leval = evalexpr(gc, lc, left, prof.add_event(ResultInitated(left)))
    reval = evalexpr(gc, lc, right, prof.add_event(ResultInitated(right)))

    reconcile: Profiler = Profiler(list(prof.getSinks()),
                                   ResultCustomEval("checking for equality between %s and %s" % (pttyobj(leval),
                                                                                                 pttyobj(reval))))
    if equal(leval, reval)["value"]:
        reconcile.add_event(RacketCheckSuccess("Both are %s" % (pttyobj(leval))))
        return [True, "[ OK ]", "Both are %s" % (pttyobj(leval))]
    else:
        reconcile.add_event(RacketCheckSuccess("left: %s right: %s" % (pttyobj(leval), pttyobj(reval))))
        return [False, "[FAIL]", "left: %s right: %s" % (pttyobj(leval), pttyobj(reval))]


def handle_chksts(gc, lc, code, prof: Profiler):
    val = code[1]
    tosatisfy = code[2]
    leval = evalexpr(gc, lc, val, prof.add_event(ResultInitated(val)))
    reval = evalexpr(gc, lc, tosatisfy, prof.add_event(ResultInitated(tosatisfy)))
    pre_satcheck = Profiler(list(prof.getSinks()), ResultCustomEval("checking against function to satisfy."))
    predres = tryboolean(reval.exec(gc, leval, pre_satcheck))
    reconcile: Profiler = Profiler(list(pre_satcheck.getSinks()),
                                   ResultCustomEval("satis-func evaled to %s" % (pttyobj(predres))))
    if predres["value"]:
        reconcile.add_event(RacketCheckSuccess("predicate satisfied."))
        return [True, "[ OK ]", "Predicate Satisfied."]
    else:
        reconcile.add_event(RacketCheckSuccess("predicate failed."))
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


def makemethod(gc, base, extensions, pf_node: Profiler):
    fregis = ["make-%s" % base] + ["%s-%s" % (base, i) for i in extensions]
    gc["make-%s" % base] = export_to_lam(lambda ls: {"type": base, "const": ls})
    for ext in range(0, len(extensions)):
        gc["%s-%s" % (base, extensions[ext])] = pythoniclam(lambda x, ix=ext: ensure(x, base)["const"][ix],
                                                            "%s-%s" % (base, extensions[ext]))
    pf_node.add_event(RacketDefineSucess("batch added functions: " + ', '.join(fregis)))
    return gc


def makestruct(gc, lc, code, pf_node: Profiler):
    # (define-struct base [ getters ] )
    base = code[1]
    extensions = code[2]
    gc = regexist(gc, base, pf_node)
    gc = makemethod(gc, base, extensions, pf_node)
    return gc


def tryexplode(optcheck, x):
    try:
        optcheck(x)
        return True
    except:
        return False


def regexist(context: dict, name: str, pf: Profiler, optcheck=None) -> dict:
    if optcheck is None:
        pf.add_event(RacketDefineSucess("registered %s via default standard" % (name + "?")))
        context[name + "?"] = pythoniclam(lambda x: boolean(type(x) == dict and x["type"] == name), name + "?")
    else:
        pf.add_event(RacketDefineSucess("registered %s via a casting standard" % (name + "?")))
        context[name + "?"] = pythoniclam(lambda x: boolean(tryexplode(optcheck, x)), name + "?")
    return context


equal_exported = pythoniclam(equal, "equal?")
