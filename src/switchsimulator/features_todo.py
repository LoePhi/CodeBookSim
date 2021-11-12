# flake8: noqa

# TODO: helpers -> überlegen wie weit ich hier abstrahieren möchte (zb selebr zwischen systemen kovertieren)
# -> dann gute namen finden, richtig funktionen auswählen und tests schreiben

# TODO: read, understand https://codereview.stackexchange.com/questions/269579/decorating-init-for-automatic-attribute-assignment-safe-and-good-practice

# TODO: ?nicht alle Zwischenelemente der Instanz zuweisen -> können auch über connections gefunden werden
# Andererseits kostet das auch nicht wirklich was und macht das inspizieren leichter
# -> dann aber auch alle zuweisen (nicht self.out_main = AND(...))

# TODO: gerade wird bei multibit immer Sequence[InputComponent] benutzt.
# Müsste aber eigentlich Iterable+"Indexable" sein

# List of not implemented circuits
# And3, p. 115
# Buffer, p. 128
# Adding machine Nr1, p.168
# Level-Triggered-8-Bit-Latch with clear, p. 170
# Level-Triggered D-type flip-flop, p. 191 -> its the same as the other ltdtff, just with different labels and no qb
# Level-Triggered-8-Bit-Latch, p. 192 -> same as the other one with differnt labels

# List of modified circuits
# oscillator, p. 157
# Adding machine p. 170 - EdgeTriggered FF instead of Level-Triggered
# 8-Bit Ripple Counter - Generalized to any numer of bits
# 16x1 RAM, p.200 (Circuit in book is defect)

# new components
# Any-Bit-Adder
