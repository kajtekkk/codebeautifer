def oblicz_srednia(lista_liczb):
    suma = 0
    for i in range(1, len(lista_liczb)):  # błąd logiczny: zaczyna od 1, pomija pierwszy element
        suma += lista_liczb[i]
    srednia = suma / len(lista_liczb     # błąd składniowy: nawias niezamknięty
    return srednia

liczby = [4, 8, 15, 16, 23, 42]

print("Średnia wynosi: " + oblicz_srednia(liczby))  # błąd: próba konkatenacji stringa i float

if oblicz_srednia(liczby) > 10
    prnt("Średnia jest większa od 10") # literówka
else:
    print("Średnia jest mniejsza lub równa 10")
