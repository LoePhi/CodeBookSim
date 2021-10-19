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

# Alternative: setup benutzen -> allerdings müsste ElectricComponent dafür LooseWire kennen


# TODO?: by default für alle outputs connectors erzeugen?
# + weniger getipsel
# - unnötige connectoren für singlestatecomponents
# - schlechter ersichtlich was genau beim bau des circuits passiert,
#       auch weil die ssc-connectoren erstmal nicht benutzt werden
# + einheitliches interface für 

# TODO: __repr__ mit pretty printing

# TODO: Implement __str__ für alle Komponenten

# TODO: ?Macht es Sinn __eq__ basierend auf __str__ zu bauen?
# -> Nachlesen was für __eq__ erwartet wird

# TODO: Use queue for updates
# -> bsp. 8bitadder: bisher löst jede änderung eines bits eine Kaskade für sich aus
# durch queue könnten alle gemeinsam erfolgen
# !Auf Reihenfolge der bits achten! lsb zuerst

# TODO: out-connectors können aus der output-liste erzeugt werden, egal ob benutzt oder nicht

# TODO: forward_connections zu _output, out_carry, etc. mit anderem Namen kennzeichnen (z.B. <class>_carry)
# -> auch damit es einen Fhler gibt wenn versucht wird dem einen neuen Input zuzuweisen

# TODO: bessere namen für in-, outputs; v.a. _output ersetzen