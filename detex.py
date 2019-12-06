import re
from argparse import ArgumentParser
from types import MethodType
from TexSoup import TexSoup
from TexSoup.data import Arg, TexExpr, TexNode
from TexSoup.utils import TokenWithPosition


class Detex(object):
    def __init__(self):
        self._actions = {'[tex]': self._default_root_action}

    def cli(self):
        parser = ArgumentParser('detex')
        parser.add_argument('files', metavar='file', nargs='+')
        args = parser.parse_args()
        print(self.files(*args.files))

    def files(self, *paths):
        return '\n\n'.join(self.file(p) for p in paths)

    def file(self, path):
        with open(path) as f:
            return self.str(f.read())

    def str(self, src):
        node = TexSoup(src)
        for n in self._walk(node):
            n._eval = self._create_eval(n)
        return node.expr._eval()

    def __call__(self, *args):
        if len(args) == 1 and callable(args[0]):
            f = args[0]
            self._actions[f.__name__] = f
            return f
        else:
            def _(f):
                for name in args:
                    self._actions[name] = f
                return f
            return _

    def _create_eval(self, node):
        if isinstance(node, TexExpr):
            def _(n):
                g = (self._peel(c)._eval() for c in n.contents)
                a = self._actions.get(n.name, lambda x: None)
                return a(''.join(t for t in g if t))
            return MethodType(_, node)

        elif isinstance(node, Arg):
            def _(n):
                g = (self._peel(c)._eval() for c in n.contents)
                return ''.join(t for t in g if t)
            return MethodType(_, node)

        elif isinstance(node, TokenWithPosition):
            def _(n):
                return None if n.text.startswith('%') else n.text
            return MethodType(_, node)

    def _walk(self, node):
        stack = [node]
        while stack:
            n = self._peel(stack.pop())
            yield n
            if isinstance(n, (TexExpr, Arg)):
                stack.extend(reversed(list(n.contents)))

    def _peel(self, node):
        return node.expr if isinstance(node, TexNode) else node

    @staticmethod
    def _default_root_action(text):
        text = text.replace('~', ' ')
        text = text.replace(r'\\', '\n')
        text = text.replace('\\', '')
        text = re.sub('\n\n+', '\n\n', text)
        text = re.sub('([^\n])\n([^\n])', r'\1 \2', text)
        text = re.sub(r' +', r' ', text)
        return text.strip()
