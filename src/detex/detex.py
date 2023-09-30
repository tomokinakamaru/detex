from argparse import ArgumentParser
from pathlib import Path
from re import sub
from sys import stdout

from TexSoup import TexSoup
from TexSoup.data import TexExpr, TexGroup, TexText
from TexSoup.utils import Token


class Detex(object):
    def __init__(self):
        self._actions = {}

    def __call__(self, *args):
        if len(args) == 1 and callable(args[0]):
            return self._register(args[0])
        return lambda f: self._register(f, *args)

    def _register(self, func, *names):
        for name in names or [func.__name__]:
            self._actions[name] = func
        return func

    def _read_rcfiles(self, paths):
        for path in paths:
            self._read_rcfile(path)

    def _read_rcfile(self, path):
        with open(path) as f:
            exec(f.read(), globals(), locals())

    def _detex_files(self, paths):
        return "\n\n".join(self._detex_file(p) for p in paths)

    def _detex_file(self, path):
        with open(path) as f:
            return self._detex_str(f.read())

    def _detex_str(self, src):
        node = TexSoup(src)
        return self._detex_elem(node.expr)

    def _detex_elem(self, elem):
        if isinstance(elem, Token):
            return "" if elem.startswith("%") else str(elem)
        if isinstance(elem, (TexGroup, TexText)):
            return self._detex_elems(elem._contents)
        if isinstance(elem, TexExpr):
            func = self._actions.get(elem.name, lambda _, c: c)
            args = self._detex_elems(elem.args)
            cons = self._detex_elems(elem._contents)
            return func(args, cons)
        raise Exception(type(elem))

    def _detex_elems(self, elems):
        return "".join(self._detex_elem(e) for e in elems)


def cli(args=None, out=stdout):
    parser = ArgumentParser("detex")

    parser.add_argument(
        "-r",
        "--rcfile",
        dest="rcfiles",
        action="append",
        metavar="rcfile",
        help="read custom rcfile",
    )

    parser.add_argument(
        "files",
        nargs="+",
        metavar="file",
        help="path to tex file",
    )

    parsed = parser.parse_args(args)

    if parsed.rcfiles:
        detex._read_rcfiles(parsed.rcfiles)
    else:
        for rcfile in ["detexrc", "detexrc.py"]:
            if Path(rcfile).exists():
                detex._read_rcfile(rcfile)

    print(detex._detex_files(parsed.files), file=out)


detex = Detex()


@detex("[tex]")
def tex(_, cons):
    cons = cons.replace("~", " ")
    cons = cons.replace("--", "—")
    cons = cons.replace("``", '"')
    cons = cons.replace("''", '"')
    cons = cons.replace(r"\\", "\n")
    cons = cons.replace("\\", "")
    cons = sub("\n\n+", "\n\n", cons)
    cons = sub("([^\n])\n([^\n])", r"\1 \2", cons)
    cons = sub(r" +", r" ", cons)
    cons = "\n".join(s.strip() for s in cons.splitlines())
    return cons.strip()
