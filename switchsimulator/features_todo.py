# flake8: noqa

# TODO: Input-Handling
# Im Moment erzeugen die
# LooseWire()-Defaults nur deshalb eigene Instanzen weil __slots__ in
# LooseWire gesetzt ist. Das ist von außen aber nicht ersichtlich

# Ich denke die Inits könnten in dieser Weise decoriert werden
# um die Inputs automatisch umzuwandeln
# es muss aber arauf geachtet werden, dass es immer noch möglich ist
# weitere Argumente zu übergeben (wie zb in connector) bzw. muss sichergestellt werden,
# dass es sich nur um tatsächliche inputs handelt -> input-tuple


def my_dec(func):
    def inner(*args, **kwargs):
        print('w')
        rea = [str(x) for x in args]
        for e in kwargs:
            kwargs[e] = e + str(kwargs[e])
        return func(*rea, **kwargs)
    return inner


@my_dec
def hihi(a=None, b=None):
    print(a)
    print(b)


hihi(2, b=3)


# TODO: __repr__ mit pretty printing

# TODO: Implement __str__ für alle Komponenten

# TODO: ?Macht es Sinn __eq__ basierend auf __str__ zu bauen?
# -> Nachlesen was für __eq__ erwartet wird

# TODO: Use queue for updates
# -> bsp. 8bitadder: bisher löst jede änderung eines bits eine Kaskade für sich aus
# durch queue könnten alle gemeinsam erfolgen
# !Auf Reihenfolge der bits achten! lsb zuerst
# Achtung, könnte dazu führen dass iene Änderung die anderen überholt
# -> neue Queue für jeden Clock-Tick

# TODO: helpers -> überlegen wie weit ich hier abstrahieren möchte (zb selebr zwischen systemen kovertieren)
# -> dann gute namen finden, richtig funktionen auswählen und tests schreiben


# List of not implemented circuits
# Buffer, p. 128
# oscillator, p. 157
# Adding machines, p.168, p. 170
# And3, p. 115 