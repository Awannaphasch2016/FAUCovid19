import pytest


def pytest_addoption(parser):
    parser.addoption("--input1", action="store", default="default input1")
    parser.addoption("--input2", action="store", default="default input2")


@pytest.fixture
def input1(request):
    return request.config.getoption("--input1")


@pytest.fixture
def input2(request):
    return request.config.getoption("--input2")
