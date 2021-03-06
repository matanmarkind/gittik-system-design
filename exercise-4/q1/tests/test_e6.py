import pytest

from e6 import ContextManager


@pytest.fixture
def cm():
    @ContextManager
    def cm():
        cm.flow.append('started')
        try:
            yield 'value'
        except Exception:
            cm.flow.append('error')
            raise
        finally:
            cm.flow.append('ended')
    cm.flow = []
    return cm


def test_flow(cm):
    assert cm.flow == []
    with cm as value:
        assert cm.flow == ['started']
        assert value == 'value'
    assert cm.flow == ['started', 'ended']


def test_error(cm):
    assert cm.flow == []
    with pytest.raises(ValueError):
        with cm as value:
            raise ValueError()
    assert cm.flow == ['started', 'error', 'ended']
