import pytest
import py_compile


def test_main_compiles():
    try:
        py_compile.compile("main.py", doraise=True)
    except py_compile.PyCompileError:
        pytest.fail("main.py failed to compile")
