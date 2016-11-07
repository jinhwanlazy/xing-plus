import os
from xing.logger import Logger
import pandas as pd

log = Logger(__name__)


def _parse_res(fname):
    with open(fname, 'r', encoding='CP949') as f:
        assert f.readline().strip() == "BEGIN_FUNCTION_MAP"

        type_, tr_name, tr_code, *rest = f.readline().strip()[:-1].split(',')
        tr_info = {
            "type": {".Func": "Query", ".Feed": "Real"}[type_],
            "name": _strip_suffix_brace(tr_name),
            "code": tr_code,
            "Attribute": "attr" in rest,
            "Block Mode": "block" in rest,
            "blocks": {}
        }

        for w in rest:
            if w.startswith('headtype='):
                tr_info["Header"] = w[-1]
            if w.startswith('key='):
                tr_info["key"] = int(w.split('=')[-1])
            if w.startswith('group='):
                tr_info["group"] = int(w.split('=')[-1])

        assert f.readline().strip() == "BEGIN_DATA_MAP"

        line = f.readline().strip()
        while line != "END_DATA_MAP":
            bl_code, bl_name, bl_type, *rest = line[:-1].split(',')
            bl_info = {
                "name": bl_name,
                "type": bl_type,
                "occurs": "occurs" in rest
            }
            bl_info["member"] = _read_block_member(f)
            tr_info["blocks"][bl_code] = bl_info
            line = f.readline().strip()

        assert f.readline().strip() == "END_FUNCTION_MAP"
    return tr_info


def _read_block_member(f):
    assert f.readline().strip() == "begin"
    line = f.readline().strip()
    ret = []
    while line != "end":
        if line == "":
            line = f.readline().strip()
            continue
        exp, name1, name2, ty, size = line[:-1].split(',')
        content = {
            "name": name1,
            "type": ty,
            "size": size,
            "explanation": exp
        }
        ret.append(content)
        line = f.readline().strip()
    return ret


def _strip_suffix_brace(s):
    if '(' in s and s[-1] == ')':
        return s[:s.rfind('(')]
    else:
        return s

_tr_raw = {}
res_path = os.path.join(os.path.dirname(__file__), 'res')
for fname in os.listdir(res_path):
    if (fname == "__init__.py" or
            fname.endswith('_1.res') or
            fname.endswith('_2.res')):
        continue
    try:
        raw = _parse_res(os.path.join(res_path, fname))
        _tr_raw[raw['code']] = raw
    except:
        log.debug("failed to parse", fname)


trname2code = {raw['name']: code for code, raw in _tr_raw.items()}
trcode2name = {code: raw['name'] for code, raw in _tr_raw.items()}

queries = {k: v for k, v in _tr_raw.items() if v['type'] == "Query"}
reals = {k: v for k, v in _tr_raw.items() if v['type'] == "Real"}


def list_queries():
    for n, key in enumerate(queries.keys()):
        print(n, key, trcode2name[key])


def list_reals():
    for n, key in enumerate(reals.keys()):
        print(n, key, trcode2name[key])


def _blank(type_):
    if type_ == 'long':
        return int()
    if type_ == 'float':
        return 0.0
    if type_ == 'string':
        return ""


def _keep_tr_unique(cls):
    instances = {}

    def getinstance(tr):
        if tr not in _tr_raw:
            log.critical("undefined TR", tr)
            raise
        if tr not in instances:
            instances[tr] = cls(tr)
        return instances[tr]
    return getinstance


@_keep_tr_unique
class TR:
    def __init__(self, trcode):
        self.raw = _tr_raw[trcode]
        self.code = trcode
        self.attribute = raw['Attribute']
        self.block_mode = raw['Block Mode']
        self.type = raw['type']

    def in_blocks(self, **args):
        fields = _tr_raw[self.code]['blocks'][self._find_in_block()]['member']
        return {'InBlock': {f['name']: args[f['name']] if f['name'] in args
                            else _blank(f['type']) for f in fields}}

    def out_blocks(self):
        ret = {}
        for block_name, block in self._find_out_blocks().items():
            _n = block_name[len(self.code):]
            if block['occurs']:
                ret[_n] = pd.DataFrame(
                    columns=(f['name'] for f in block['member']))
            else:
                ret[_n] = tuple(f['name'] for f in block['member'])
        return ret

    def _find_in_block(self):
        for k, v in _tr_raw[self.code]['blocks'].items():
            if v['type'] == 'input':
                return k

    def _find_out_blocks(self):
        return {k: v for k, v in _tr_raw[self.code]['blocks'].items()
                if v['type'] == 'output'}

    def input_dataframe(self):
        return pd.DataFrame(
            _tr_raw[self.code]['blocks'][self._find_in_block()]['member'])
