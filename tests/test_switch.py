from switchsimulator.singlestatecomp import Switch


def test_a():
    assert(Switch(True).is_on is True)
    assert(Switch(False).is_on is False)
    s1 = Switch(False)
    s1.flip()
    assert(s1.is_on is True)
    s1.open()
    assert(s1.is_on is False)
    s1.close()
    assert(s1.is_on is True)
