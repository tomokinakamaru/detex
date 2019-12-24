import detex
from io import StringIO


def test_cli():
    out = StringIO()
    detex.cli(['-r', 'sample/detexrc', 'sample/sample.tex'], out)
    with open('sample/sample.txt') as txt:
        assert txt.read() == out.getvalue()
