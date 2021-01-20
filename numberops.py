from math import sqrt
from typing import List

from casting import trynum
from lamstructs import pythoniclam, export_to_lam
from shortcuts import valuesof, foldr, num, boolean, string

type_num = "number"

def consisestr(v):
    if int(v) == v:
        return str(int(v))
    else:
        return str(v)
def num_add(nums: List):
    q = list(map(trynum, nums))
    return {"type": "number", "value": sum(valuesof(q))}


def num_mul(nums: List):
    q = list(valuesof(map(trynum, nums)))
    val = foldr(q, lambda x, y: x * y, 1)
    return {"type": "number", "value": val}


def num_sub(nums: List):
    q = list(valuesof(map(trynum, nums)))
    val = q.pop(0)
    return {"type": "number", "value": val - sum(q)}


def num_div(nums: List):
    q = list(valuesof(map(trynum, nums)))
    base = q.pop(0)
    val = foldr(q, lambda x, y: x * y, 1)
    return {"type": "number", "value": base / val}


def num_max(nums: List):
    q = list(map(trynum, nums))
    return {"type": "number", "value": max(valuesof(q))}


def num_min(nums: List):
    q = list(map(trynum, nums))
    return {"type": "number", "value": min(valuesof(q))}


add_num = export_to_lam(num_add, "+")
mul_num = export_to_lam(num_mul, "*")
sub_num = export_to_lam(num_sub, "-")
div_num = export_to_lam(num_div, "/")
max_num = export_to_lam(num_max, "max")
min_num = export_to_lam(num_min, "min")
add1_num = pythoniclam(lambda x: num(trynum(x)["value"] + 1), "add1")
sub1_num = pythoniclam(lambda x: num(trynum(x)["value"] - 1), "sub1")
abs_num = pythoniclam(lambda x: num(abs(trynum(x)["value"])), "abs")
eq_num = pythoniclam(lambda x, y: boolean(trynum(x)["value"] == trynum(y)["value"]), "=")
ge_num = pythoniclam(lambda x, y: boolean(trynum(x)["value"] > trynum(y)["value"]), ">")
geq_num = pythoniclam(lambda x, y: boolean(trynum(x)["value"] >= trynum(y)["value"]), ">=")
le_num = pythoniclam(lambda x, y: boolean(trynum(x)["value"] < trynum(y)["value"]), "<")
leq_num = pythoniclam(lambda x, y: boolean(trynum(x)["value"] <= trynum(y)["value"]), "<=")
modu_num = pythoniclam(lambda x, y: num(trynum(x)["value"] % trynum(y)["value"]), "modulo")
sqr_num = pythoniclam(lambda x: num(trynum(x)["value"] ** 2), "sqr")
sqrt_num = pythoniclam(lambda x: num(sqrt(trynum(x)["value"])), "sqrt")
num_tostr = pythoniclam(lambda x: string(consisestr(trynum(x)["value"])), "number->string")
num_even = pythoniclam(lambda x: boolean(trynum(x)["value"] % 2 == 0), "even?")
num_odd = pythoniclam(lambda x: boolean(trynum(x)["value"] % 2 == 1), "odd?")
num_zerohuh = pythoniclam(lambda x: boolean(trynum(x)["value"] == 0), "zero?")
num_neghuh = pythoniclam(lambda x: boolean(trynum(x)["value"] < 0), "negative?")
num_poshuh = pythoniclam(lambda x: boolean(trynum(x)["value"] > 0), "positive?")