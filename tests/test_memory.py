# import pytest
# from switchsimulator.singlestatecomp import Switch
# from switchsimulator.memory import RSFlipFlop


# def test_rs_flipflop():
#     r = Switch(False)
#     s = Switch(True)
#     ff = RSFlipFlop(r, s)
#     assert(ff.__str__() == '10')  # 10
#     s.open()
#     assert(ff.__str__() == '10')  # 10
#     r.close()
#     assert(ff.__str__() == '01')  # 01
#     r.open()
#     assert(ff.__str__() == '01')  # 01
#     with pytest.raises(ValueError):
#         s.close()
#         r.close()
