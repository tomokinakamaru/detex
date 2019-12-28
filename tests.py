import os
import io
import detex


def test_cli1():
    out = io.StringIO()
    detex.cli(['-r', 'sample/detexrc', 'sample/sample.tex'], out)
    with open('sample/sample.txt') as txt:
        assert txt.read() == out.getvalue()


def test_cli2():
    os.chdir('sample')
    out = io.StringIO()
    detex.cli(['sample.tex'], out)
    with open('sample.txt') as txt:
        assert txt.read() == out.getvalue()
