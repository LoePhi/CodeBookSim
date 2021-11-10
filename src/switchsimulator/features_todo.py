# flake8: noqa

# TODO: __str__: implement für alle

# TODO: sollten Tests wirklich aud __str__ basieren?

# TODO: helpers -> überlegen wie weit ich hier abstrahieren möchte (zb selebr zwischen systemen kovertieren)
# -> dann gute namen finden, richtig funktionen auswählen und tests schreiben

# TODO: tuples statt list?

# TODO: read, understand https://codereview.stackexchange.com/questions/269579/decorating-init-for-automatic-attribute-assignment-safe-and-good-practice

# TODO: ?nicht alle Zwischenelemente der Instanz zuweisen -> können auch über connections gefunden werden
# Andererseits kostet das auch nicht wirklich was und macht das inspizieren leichter
# -> dann aber auch alle zuweisen (nicht self.out_main = AND(...))

# TODO: main_out für alle multibit-Secondary Components die nur einen Output haben
# -> in eigene Klasse packen
# -> darin über __getitem__, __iter__ an main_out verweisen
# -> AddingMachine2, RippleCounter, LevelTrig8BitLatch, EdgeTrig8BitLatchPreCl, OnesComplement, Decoder_3_8, RAM...

# autoparse fix: https://github.com/microsoft/pyright/issues/774

# List of not implemented circuits
# And3, p. 115 
# Buffer, p. 128
# oscillator, p. 157
# Adding machines, p.168
# Level-Triggered-8-Bit-Latch with clear, p. 170
# Level-Triggered D-type flip-flop, p. 191 -> its the same as the other ltdtff, just with different labels and no qb
# Level-Triggered-8-Bit-Latch, p. 192 -> same as the other one with differnt labels

# List of modified circuits
# Adding machine p. 170 - EdgeTriggered FF instead of Level-Triggered
# 8-Bit Ripple Counter - Generalized to any numer of bits

# new components
# Any-Bit-Adder