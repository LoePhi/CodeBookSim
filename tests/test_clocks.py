from codebooksim.corecomponents import Switch
from codebooksim.clocks import clock, book_oscillator, RippleCounter
import threading
from time import sleep


def test_oscillator():
    try:
        _ = book_oscillator()
        assert False
    except RecursionError:
        assert True


def test_clock_counter():
    sw = Switch(False)
    cl = clock(sw)
    rc = RippleCounter(cl, 16)
    sw.flip()
    x = threading.Thread(target=cl.start)
    x.start()
    sleep(.1)
    sw.flip()
    outp = [b.is_on for b in rc[:14]]
    assert sum(outp) > 1
