README
------

Erklärung der Laufzeitprotokolle (Logs):

Jeder Durchlauf der Simulation wird automatisch mit Timestamp im Namen als txt-Datei abgespeichert.

Für jeden Zyklus der Ameisenweltsimulation wird der Zustand der Welt in dieser Form dargestellt:

Koordinaten werden von links oben aus gelesen.

Cycle N : Nest = (X_K, Y_K) , {(X_1, Y_2): (F, V, [A1, A2, ...]), ...}
          [((X_1, Y_1), (X_2, Y_2), F_P, N_P), ...]

Cycle N:                                            N-ter Zyklus der Simulation
Nest = (X_, Y_K):                                      Die Koordinaten des Nestknotens im Kotengitter.
{(X_1, Y_1): (F, V, [A1, A2, ...]), ...}:               Dictionary aller Knoten im Gitter
    (X_1, Y_1):                                             Koordinate des jeweiligen Knoten
    F:                                                  Anzahl der dort vorhandenen Essenseinheiten
	V:                                                  Markierung der Erkunderameisen
	[A1, A2, ...]:                                      Liste mit den sich in diesem Knoten aufhaltenden Ameisen. Folgende Zustände sind möglich:
	    O:                                                  Universalameise ohne Nahrung
	    1:                                                  Universalameise mit Nahrung
	    2:                                                  Erkunderameise auf Nahrungssuche
	    3:                                                  Erkunderameise auf dem Rückweg zum Nest
	    4:                                                  Trägerameise ohne Nahrung
	    5:                                                  Trägerameise mit Nahrung
[((X_1, Y_1), (X_2, Y_2), F_P, N_P), ...]:          Liste aller Kanten im Gitter
    (X_1, Y_1), (X_2, Y_2):                             Knoten, die von dieser Kante verbunden werden
    F:                                                  Stärke des Nahrungspheromons auf dieser Kante
    N:                                                  Stärke des Nestpheromons auf dieser Kante