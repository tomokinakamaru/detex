import re
from TexSoup import TexSoup
from TexSoup.data import Arg, TexCmd, TexEnv, TexNode
from TexSoup.utils import TokenWithPosition


class Detex(object):

    _WALK_CONTENTS = object()

    def __init__(self):
        self._actions = {'[tex]': self._WALK_CONTENTS}

    def files(self, *paths):
        return '\n\n'.join(self.file(p) for p in paths)

    def strings(self, *strings):
        return '\n\n'.join(self.string(s) for s in strings)

    def file(self, path):
        with open(path) as f:
            return self.string(f.read())

    def string(self, string):
        walker, blocks = Walker(TexSoup(string)), []
        while walker:
            node = walker.next()
            if isinstance(node, (TexNode, TexCmd, TexEnv)):
                if node.name in self._actions:
                    action = self._actions[node.name]
                    if action is self._WALK_CONTENTS:
                        walker.traverse_current_contents()
                    else:
                        blocks.append(str(action(node)))

            elif isinstance(node, TokenWithPosition):
                if not node.text.startswith('%'):
                    blocks.append(node.text)

            elif isinstance(node, Arg):
                walker.traverse_current_contents()

        return self.post_process(''.join(blocks))

    def walk_contents(self, *names):
        for name in names:
            self._actions[name] = self._WALK_CONTENTS

    def replace(self, *names):
        def _(f):
            for name in names:
                self._actions[name] = f
            return f
        return _

    @staticmethod
    def post_process(text):
        text = text.replace('~', ' ')
        text = text.replace(r'\\', '\n')
        text = text.replace('\\', '')
        text = re.sub('\n\n+', '\n\n', text)
        text = re.sub('([^\n])\n([^\n])', r'\1 \2', text)
        text = re.sub(r' +', r' ', text)
        return text.strip()


class Walker(object):
    def __init__(self, node):
        self._stack = [node]
        self._current = None

    def __bool__(self):
        return bool(self._stack)

    def next(self):
        self._current = self._stack.pop()
        return self._current

    def traverse_current_contents(self):
        self._stack.extend(reversed(list(self._current.contents)))
