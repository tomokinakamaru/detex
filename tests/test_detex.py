from io import StringIO
from os import chdir

from detex.detex import cli


def test_detex_custom_rfcile_path():
    sio = StringIO()
    cli(["-r", "tests/resources/detexrc.py", "tests/resources/sample.tex"], sio)
    with open("tests/resources/sample.txt") as txt:
        assert txt.read() == sio.getvalue()


def test_detex_default_rcfile_path():
    sio = StringIO()
    chdir("tests/resources")
    cli(["sample.tex"], sio)
    with open("sample.txt") as txt:
        assert txt.read() == sio.getvalue()
