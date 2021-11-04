# flake8: noqa

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

# TODO: tuples statt list?

# TODO: read, understand https://codereview.stackexchange.com/questions/269579/decorating-init-for-automatic-attribute-assignment-safe-and-good-practice

# TODO: remove main_out from multibit components

# TODO: ?nicht alle Zwischenelemente der Instanz zuweisen -> können auch über connections gefunden werden
# Andererseits kostet das auch nicht wirklich was und macht das inspizieren leichter
# -> dann aber auch alle zuweisen (nicht self.out_main = AND(...))

# TODO: durchgehen und überall type hints setzen (mypy --strict)

# TODO: variable sized version von adder, latch, OnesComplement, ..?

# List of not implemented circuits
# And3, p. 115 
# Buffer, p. 128
# oscillator, p. 157
# Adding machines, p.168
# Level-Triggered-8-Bit-Latch with clear, p. 170

# List of modified circuits
# Adding machine p. 170 - EdgeTriggered FF instead of Level-Triggered
# 8-Bit Ripple Counter - Generalized to any numer of bits