from casting import ensure, trynum, trysymbol
from lamstructs import pythoniclam, compose, export_to_lam
from printing import pttyobj, topylist
from shortcuts import symbol, string, foldr, num, boolean
from structops import equal


def intify(x):
    if x != int(x):
        raise Exception("the value %s is not an integer." % x)
    else:
        return int(x)


def cons(f, r):  # a cons is a 2-tuple (first, rest) with accesors first lambda x y x and rest lambda x y y
    return {"type": "cons", "const": [f, r], "pure_list?": isPureList(r)}


def isCons(x):
    return type(x) == dict and x["type"] == "cons"


def isPureCons(x):
    return isCons(x) and x["pure_list?"]


def isPureList(x):
    global list_empty
    return equal(x, list_empty)["value"] or isPureCons(x)


def isList(x):
    global list_empty
    return equal(x, list_empty) or isCons(x)


def getListLen(lst):
    if equal(lst, list_empty):
        return 0
    elif isCons(lst):
        return 1 + lst["const"][1]
    else:
        raise Exception("found non list object in list: %s" % pttyobj(lst))


def quicklist(listeles: list):
    return foldr(listeles, cons, list_empty)


def make_list(inp):
    tms = trynum(inp[0])["value"]
    if tms == 0:
        return list_empty
    else:
        return cons(inp[1], make_list([num(tms - 1), inp[1]]))


sym_eq = pythoniclam(lambda symx, symy: boolean(trysymbol(symx)["value"] == trysymbol(symy)["value"]))
sym_tostr = pythoniclam(lambda symx: string(trysymbol(symx)["value"][1:]))
list_empty = symbol("'()")
list_fst = pythoniclam(lambda x: ensure(x, "cons")["const"][0])
list_rst = pythoniclam(lambda x: ensure(x, "cons")["const"][1])
list_snd = compose(list_fst, list_rst)
list_trd = compose(list_fst, compose(list_rst, list_rst))
list_len = pythoniclam(lambda x: num(getListLen))
list_cons = pythoniclam(cons)
list_isempty = pythoniclam(lambda x: equal(x, list_empty))
list_iscons = pythoniclam(lambda x: boolean(isCons(x)))
list_rev = pythoniclam(lambda x: quicklist(topylist(x)[::-1]))
list_range = pythoniclam(lambda s, e, st: quicklist(
    list(map(num, range(intify(trynum(s)["value"]), intify(trynum(e)["value"]), intify(trynum(st)["value"]))))))
list_qlist = export_to_lam(quicklist)
list_mklist = export_to_lam(make_list)
