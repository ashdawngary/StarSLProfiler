from casting import tryboolean
from lamstructs import pythoniclam
from shortcuts import boolean, string

eq_bool = pythoniclam(lambda x, y: boolean(tryboolean(x)["value"] == tryboolean(y)["value"]))
not_bool = pythoniclam(lambda x: boolean(not tryboolean(x)["value"]))
bool_tostr = pythoniclam(lambda x: string(str(tryboolean(x)["value"])))