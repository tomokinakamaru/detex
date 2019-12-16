from detex import Detex
from io import StringIO

detex = Detex()


@detex
def document(text):
    return text


@detex('abstract', 'enumsentence', 'emph', 'ex')
def identity(text):
    return text


@detex('section*', 'subsection*')
def head(text):
    return f'\n1. {text}\n'


def test_string():
    assert detex.str(r'''
    \begin{document}
        \begin{abstract}
            test
        \end{abstract}
    \end{document}
    ''') == 'test'


def test_file():
    out = StringIO()
    detex.cli(['sample.tex'], out)
    with open('sample.txt') as txt:
        assert txt.read() == out.getvalue()
