from detex import Detex

detex = Detex()

detex.walk_contents(
    'document',
    'abstract',
    'enumsentence'
)


@detex.replace('section*', 'subsection*')
def head(node):
    return f'\n1. {node.args[0].value}\n'


@detex.replace('emph', 'ex')
def text(node):
    return f'{node.args[0].value}'


def test_string():
    assert detex.strings(r'''
    \begin{document}
        \begin{abstract}
            test
        \end{abstract}
    \end{document}
    ''') == 'test'


def test_file():
    with open('sample.txt') as txt:
        assert txt.read().strip() == detex.files('sample.tex')
