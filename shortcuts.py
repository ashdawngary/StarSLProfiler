from typing import Iterator, List


def num(inp):
    return {"type": "number", "value": inp}


def boolean(inp):
    return {"type": "boolean", "value": inp}


def string(inp):
    return {"type": "string", "value": inp}


def symbol(inp):
    return {"type": "symbol", "value": inp}


def valuesof(lst: Iterator):
    return map(lambda x: x["value"], lst)


def foldr(lst: List, f, base):
    q = base
    for ele in lst[::-1]:
        q = f(ele, q)
    return q
