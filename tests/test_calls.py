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