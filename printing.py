LIST_ABREV = True

def ppt(sexpr):
    if type(sexpr) == str:
        return sexpr
    else:
        return "(" + ' '.join(map(ppt, sexpr)) + ")"


def topylist(rack_list):
    if not rack_list["type"] == "cons":
        return []
    else:
        return [rack_list["const"][0]] + topylist(rack_list["const"][1])


def pttyobj(val):
    if type(val) != dict:
        return str(val)
    elif val["type"] == "number":
        if int(val["value"]) == val["value"]:
            return str(int(val["value"]))
        return str(val["value"])
    elif val["type"] == "boolean":
        return str(val["value"])
    elif val["type"] == "string":
        return "\"%s\"" % (val["value"])
    elif val["type"] == "symbol":
        return str(val["value"])
    elif val["type"] == "cons":
        global LIST_ABREV
        if val["pure_list?"] and LIST_ABREV:
            # render this as (list )
            pythonized = topylist(val)
            return "(list %s)" % (" ".join(list(map(pttyobj, pythonized))))
        else:
            return "(cons %s)" % (" ".join(list(map(pttyobj, val["const"]))))
    else:
        return "(make-%s %s)" % (val["type"], " ".join(list(map(pttyobj, val["const"]))))


def pttydesc(val):
    if type(val) != dict:
        return str(val)
    else:
        return "%s of %s" % (val["type"], pttyobj(val))
