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


lenstr = pythoniclam(lambda x: num(len(trystring(x)["value"])), "string-length")
appstr = export_to_lam(appendstrings, "string-append")
streq = pythoniclam(lambda x, y: boolean(trystring(x)["value"] == trystring(y)["value"]), "string=?")
strle = pythoniclam(lambda x, y: boolean(trystring(x)["value"] < trystring(y)["value"]), "string<?")
strleq = pythoniclam(lambda x, y: boolean(trystring(x)["value"] <= trystring(y)["value"]), "string<=?")
strge = pythoniclam(lambda x, y: boolean(trystring(x)["value"] > trystring(y)["value"]), "string>?")
strgeq = pythoniclam(lambda x, y: boolean(trystring(x)["value"] >= trystring(y)["value"]), "string>=?")
strlo = pythoniclam(lambda x: string(trystring(x)["value"].lower()), "string-downcase")
strup = pythoniclam(lambda x: string(trystring(x)["value"].upper()), "string-upcase")
strcont = pythoniclam(lambda s, n: boolean(trystring(n)["value"] in trystring(s)["value"]), "string-contains?")
strpref = pythoniclam(lambda s, p: boolean(areprefixes(trystring(s)["value"], trystring(p)["value"])), "string-prefix?")
strsuff = pythoniclam(lambda sr, su: boolean(areprefixes(trystring(sr)["value"][::-1], trystring(su)["value"][::-1])), "string-suffix?")
strne = pythoniclam(lambda x: boolean(len(trystring(x)["value"]) > 0), "non-empty-string?")
substr = export_to_lam(substringrack, "substring")
