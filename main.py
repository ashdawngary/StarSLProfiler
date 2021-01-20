from boolops import not_bool, eq_bool, bool_tostr
from casting import trynum, tryboolean, trystring, trysymbol
from defines import handle_define
from evalexpr import evalexpr
from isllistcomp import export_listcomp
from listops import sym_eq, sym_tostr, list_len, list_trd, list_snd, list_fst, list_empty, list_iscons, list_isempty, \
    list_cons, list_rst, list_mklist, list_qlist, list_rev, list_range
from numberops import eq_num, min_num, max_num, sqr_num, div_num, mul_num, sub_num, add_num, add1_num, geq_num, ge_num, \
    leq_num, le_num, sqrt_num, num_tostr, modu_num, num_neghuh, num_poshuh, num_zerohuh, num_odd, num_even, sub1_num
from printing import ppt, pttydesc, pttyobj
from synparser import treeifysrc
from strops import lenstr, appstr, substr, strne, strsuff, strpref, strcont, strup, strlo, strgeq, strge, strleq, strle, \
    streq
from structops import regexist, handle_chkxpect, equal, handle_chksts, equal_exported

univ_ctx = {
    "=": eq_num,
    "+": add_num,
    "-": sub_num,
    "*": mul_num,
    "/": div_num,
    "sqr": sqr_num,
    "sqrt": sqrt_num,
    "max": max_num,
    "min": min_num,
    "add1": add1_num,
    "sub1": sub1_num,
    "<": le_num,
    "<=": leq_num,
    ">": ge_num,
    ">=": geq_num,
    "boolean=?": eq_bool,
    "not": not_bool,
    "string-length": lenstr,
    "string-append": appstr,
    "string=?": streq,
    "string<?": strle,
    "string<=?": strleq,
    "string>?": strge,
    "string>=?": strgeq,
    "string-downcase": strlo,
    "string-upcase": strup,
    "string-contains?": strcont,
    "string-prefix?": strpref,
    "string-suffix?": strsuff,
    "non-empty-string?": strne,
    "substring": substr,
    "equal?": equal_exported,
    "number->string": num_tostr,
    "symbol->string": sym_tostr,
    "boolean->string": bool_tostr,
    "symbol=?": sym_eq,
    "range": list_range,
    "empty": list_empty,
    "first": list_fst,
    "rest": list_rst,
    "second": list_snd,
    "third": list_trd,
    "length": list_len,
    "cons": list_cons,
    "empty?": list_isempty,
    "cons?": list_iscons,
    "list": list_qlist,
    "make-list": list_mklist,
    "reverse": list_rev,
    "even?": num_even,
    "odd?": num_odd,
    "zero?: ": num_zerohuh,
    "positive?": num_poshuh,
    "negative?": num_neghuh,
    "remainder": modu_num,
    "modulo": modu_num,
}

regexist(univ_ctx, "number", trynum)
regexist(univ_ctx, "boolean", tryboolean)
regexist(univ_ctx, "string", trystring)
regexist(univ_ctx, "symbol", trysymbol)
univ_ctx = handle_define(univ_ctx, ["define-struct", "posn", ["x", "y"]])
univ_ctx = export_listcomp(univ_ctx)


ftorun = "testing/symboltest.txt"
with open(ftorun, "r") as vkh:
    data = str(vkh.read())
    vkh.close()

sourceparse = treeifysrc(data)
print(sourceparse)
print("starting exec...\n\n\n")

while len(sourceparse) > 0:
    nxc = sourceparse.pop(0)
    print("%s" % (ppt(nxc)), end="")
    if nxc[0] in ["define", "define-struct"]:
        univ_ctx = handle_define(univ_ctx, nxc)
        if type(nxc[1]) == str and nxc[0] == "define":
            print("\t\t-- %s holds %s" % (nxc[1], pttydesc(evalexpr(univ_ctx, [], nxc[1]))))
        else:
            print("")
    elif nxc[0] == "check-expect":
        result = handle_chkxpect(univ_ctx, [], nxc)
        if result[0]:
            print(f"\t\t-- {result[1]} {result[2]}")
        else:
            print(f"\n\t-- {result[1]} {result[2]}")
    elif nxc[0] == "check-satisfied":
        result = handle_chksts(univ_ctx, [], nxc)
        if result[0]:
            print(f"\t\t-- {result[1]} {result[2]}")
        else:
            print(f"\n\t-- {result[1]} {result[2]}")
    else:
        print("\n --> %s" % (pttyobj(evalexpr(univ_ctx, [], nxc))))

