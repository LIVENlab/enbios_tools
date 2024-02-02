import pytest

def bw_project_name() -> str:
    return ""


@pytest.fixture(scope="module")
def set_bw_project(bw_project_name: str):
    pass