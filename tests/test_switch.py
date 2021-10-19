from switchsimulator.singlestatecomp import Switch


def test_a():
    assert(Switch(True).is_on is True)
    assert(Switch(False).is_on is False)
    tmp = Switch(False)
    tmp.flip()
    assert(tmp.is_on is True)
    tmp.open()
    assert(tmp.is_on is False)
    tmp.close()
    assert(tmp.is_on is True)
