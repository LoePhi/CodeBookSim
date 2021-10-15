# TODO: Input-Handling
# Inputs automatisch umwandeln (eg '1',1,'1010' -> Switch(T), S(T), [S(T), S(F), ..])
# Dabei evtl. auch den default-Input verändern. Im Moment erzeugen die 
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


# TODO?: alle outputs als connectors ausgeben 
# -> compute_state entfällt außer für die grund-bausteine (INV, AND, OR)
# -> dann geht das hier aber nicht mehr ohne weiteres:
#     self.INV1 = INV(self.XOR1)
# -> INV added fc zu XOR1; nicht zu dem connector der aus XOR1 heruas führt
# stattdessen müsste dann
#     self.INV1 = INV(self.XOR1.con_out)
# das erzeugt aber viel getipsel und geht auf Kosten der Lesbarkeit
# es lässt sich sicher so lösen, aber wie hoch sind die KOsten an die Lesbarkeit und der Wartungsaufwand?
# Beifang:
# - jede Menge neue Instanzen
# - zusammengestzte Elemente haben erstmal keinen eigenen state mehr
# !ACHTUNG: so lange der circuit neu gebaut wird, wenn ein innput hinzu kommt dann
#   führt diese Vorgehensweise dazu, dass die forward connections verloren gehen


# TODO: Implement __str__ für alle Komponenten

# TODO: ?Macht es Sinn __eq__ basierend auf __str__ zu bauen?
# -> Nachlesen was für __eq__ erwartet wird