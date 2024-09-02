import pytest


def test_exit_works_for_empty_test(client, server):
    pass

def test_closeShutter(client, server):
    client.closeShutter()

def test_setFilterThickness(client, server):
    #Default value of server is 0
    assert client.getFilterThickness() == 0

    client.setFilterThickness(14)
    assert client.getFilterThickness() == 14

def test_filter_thickness_property(client, server):
    assert client.filter_thickness == 0

    client.filter_thickness = 14
    assert client.filter_thickness == 14

def test_read_a_list(client, server):
    assert client.getSomeList() == [1, 'two', 3]

def test_read_a_dict(client, server):
    assert client.getSomeDict() == {'one': 1, 'two': 2, 'three': 3}

def test_raise_exception(client, server):
    """If an exception is raised on the server side it should be raised on the client side"""
    with pytest.raises(ValueError):
        client.raiseException()