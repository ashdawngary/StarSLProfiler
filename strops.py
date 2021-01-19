from casting import trystring, trynum
from lamstructs import pythoniclam, export_to_lam
from shortcuts import boolean, string, num, foldr, valuesof


def substringrack(params):
    ostr = params[0]["value"]
    start = trynum(params[1])["value"]
    if len(params) == 2:
        return string(ostr[start:])
    elif len(params) == 3:
        end = trynum(params[2])["value"]
        return string(ostr[start: end])


def appendstrings(params):
    return string(foldr(list(valuesof(map(trystring, params))), lambda x, y: x + y, ""))


def areprefixes(a, b):
    if len(b) <= len(a):
        return b == a[:len(b)]


lenstr = pythoniclam(lambda x: num(len(trystring(x)["value"])))
appstr = export_to_lam(appendstrings)
streq = pythoniclam(lambda x, y: boolean(trystring(x)["value"] == trystring(y)["value"]))
strle = pythoniclam(lambda x, y: boolean(trystring(x)["value"] < trystring(y)["value"]))
strleq = pythoniclam(lambda x, y: boolean(trystring(x)["value"] <= trystring(y)["value"]))
strge = pythoniclam(lambda x, y: boolean(trystring(x)["value"] > trystring(y)["value"]))
strgeq = pythoniclam(lambda x, y: boolean(trystring(x)["value"] >= trystring(y)["value"]))
strlo = pythoniclam(lambda x: string(trystring(x)["value"].lower()))
strup = pythoniclam(lambda x: string(trystring(x)["value"].upper()))
strcont = pythoniclam(lambda s, n: boolean(trystring(n)["value"] in trystring(s)["value"]))
strpref = pythoniclam(lambda s, p: boolean(areprefixes(trystring(s)["value"], trystring(p)["value"])))
strsuff = pythoniclam(lambda sr, su: boolean(areprefixes(trystring(sr)["value"][::-1], trystring(su)["value"][::-1])))
strne = pythoniclam(lambda x: boolean(len(trystring(x)["value"]) > 0))
substr = export_to_lam(substringrack)
