from detex import Detex

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
    with open('sample.txt') as txt:
        assert txt.read().strip() == detex.files('sample.tex')
