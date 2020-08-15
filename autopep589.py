from collections import OrderedDict
from typing import List, Union

def gen(d: dict, name: str="classname", tabsize: int=4):
    s = f"class {name}(TypedDict):\n"
    space = " "
    for k, v in d.items():
        s += f"{space * tabsize}{k}: {type(v).__name__}\n"
    return s


def get_typestr_jsonlike(v: Union[dict, list, int, str, float, bool, None], name: str="classname", tabsize: int=4, classes: list = []) -> str:
    typeslist: List[str]
    typename: str = type(v).__name__
    if isinstance(v, dict):
        if len(v) == 0:
            typestr = "dict"
        else:
            typestr=f"{name}_Dict_t"
            classes.append(gen_rec_jsonlike(v, name=typestr))
    elif isinstance(v, list):
        if len(v) == 0:
            typestr = "list"
        else:
            typeslist = list(set((get_typestr_jsonlike(e, f"{name}_elem_t") for i, e in enumerate(v)))) # FIXME assumes lists have all the same type
            s = ", ".join(typeslist)
            typestr = f"List[{s}]"
    else:
        # FIXME this should raise a custom error
        assert(typename in set(("int", "str", "float", "bool", "NoneType")))
        typestr = "None" if typename == "NoneType" else typename
    return typestr

import_str = "from typing import List, TypedDict\n\n"
# items can be dict, list, str, int, float, none, bool
# recurse on dict and list
def gen_rec_jsonlike(d: dict, name: str="classname", tabsize: int=4, classes: List[str] = []) -> str:
    s: str = f"class {name}(TypedDict):\n"
    space: str = " "
    for k, v in d.items():
        s += f"{space * tabsize}{k}: {get_typestr_jsonlike(v, name=k)}\n\n"
    classes.append(s)
    s = "\n\n".join(list(OrderedDict.fromkeys(classes)))
    return f"{import_str}{s}\n"
